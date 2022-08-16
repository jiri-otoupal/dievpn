import sys
from threading import Thread
from time import sleep
from typing import Iterable

from PySide6.QtCore import (
    QObject,
    QCoreApplication,
    QUrl,
    qInstallMessageHandler,
    Slot,
    Signal,
)
from PySide6.QtGui import Qt, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

import dvpn.res  # noqa
from dvpn.config.constants import PublicVars, CLI_RESOLVE
from dvpn.logger import qt_message_handler
from dvpn.modules.tools import connect


class Bridge(QObject):
    periodic_thread = None
    connectedVPNs: Iterable[str] = set()
    changingVPNs = set()

    connectStatusChange = Signal(str, bool, bool, name="connectStatusChange")
    disconnectChange = Signal(str, bool, bool, name="disconnectChange")

    def periodic_check(self):
        if self.periodic_thread is not None:
            return False
        t = Thread(target=self._periodic_check, name="Periodic status Check", daemon=True)
        self.periodic_thread = t
        t.start()
        return True

    def _periodic_check(self):
        while True:
            for conn_vpn in set(self.connectedVPNs):
                creds = PublicVars().credentials[conn_vpn]
                cli_type = CLI_RESOLVE[creds["selectedVpn"]]
                cli_instance = cli_type(creds["cliPath"])
                if "disconnected" in cli_instance.get_state(conn_vpn).lower():
                    self.disconnect_notify(conn_vpn, cli_instance, False)
            sleep(0.5)

    @Slot(str)
    def log(self, text):
        print(text)

    @Slot(result="QVariantMap")
    def list_vpn(self) -> dict:
        return PublicVars().credentials

    @Slot(str, result="QVariantMap")
    def get_vpn_details(self, vpn_name: str) -> dict:
        if vpn_name not in PublicVars().credentials.keys():
            return {}
        details = PublicVars().credentials[vpn_name]
        # details["cliPath"] = QUrl.fromLocalFile(details["cliPath"]).toString()
        return details

    @Slot("QVariantMap", result=bool)
    def add_vpn(self, obj: dict) -> bool:
        vpn_name = obj["VPN Name"]
        if vpn_name not in PublicVars().credentials.keys():
            PublicVars()[vpn_name] = obj
            return True
        return False

    @Slot(str, result=list)
    def get_vpn_fields(self, vpn_name):
        cli = CLI_RESOLVE[vpn_name]
        return cli.fields

    @Slot(str)
    def connect(self, vpn_name: str):
        # noinspection PyUnresolvedReferences
        self.connectStatusChange.emit(vpn_name, False, True)
        self.changingVPNs.add(vpn_name)

        vpn_conf = PublicVars()[vpn_name]
        cli = CLI_RESOLVE[vpn_conf["selectedVpn"]](vpn_conf["cliPath"])
        t = Thread(
            target=lambda: connect(cli, vpn_conf["VPN Name"], self),
            name=f"Connecting {vpn_conf['VPN Name']}",
            daemon=True,
        )
        t.start()

    @Slot(str, "QVariantMap")
    def edit(self, vpn_name: str, contents: dict):
        tmp = PublicVars().credentials
        tmp[vpn_name] = contents
        PublicVars().credentials = tmp

    @Slot(str)
    def delete(self, vpn_name: str):
        tmp = PublicVars().credentials
        tmp.pop(vpn_name, None)
        PublicVars().credentials = tmp

    @Slot(str)
    def connected_notify(self, vpn_name: str):
        self.connectedVPNs.add(vpn_name)

    @Slot(str)
    def disconnect(self, vpn_name: str):
        # noinspection PyUnresolvedReferences
        self.disconnectChange.emit(vpn_name, True, True)
        vpn_conf = PublicVars()[vpn_name]
        cli = CLI_RESOLVE[vpn_conf["selectedVpn"]](vpn_conf["cliPath"])
        t = Thread(
            target=lambda: self.disconnect_notify(vpn_name, cli),
            name=f"Disconnecting {vpn_name}",
            daemon=True,
        )
        t.start()

    @Slot()
    def reset(self):
        for host in set(self.connectedVPNs):
            creds = PublicVars().credentials[host]
            cli_type = CLI_RESOLVE[creds["selectedVpn"]]
            cli = cli_type(str(creds["cliPath"]))
            t = Thread(
                target=lambda: self.disconnect_notify(host, cli),
                name=f"Disconnecting {host}",
                daemon=True,
            )
            t.start()

    def disconnect_notify(self, vpn_name, cli, reset=True):
        self.disconnectChange.emit(vpn_name, False, True)
        if reset:
            cli.reset(host=vpn_name)
        # noinspection PyUnresolvedReferences
        self.disconnectChange.emit(vpn_name, False, False)
        self.connectedVPNs.remove(vpn_name)


def main():
    qInstallMessageHandler(qt_message_handler)
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    app.setOrganizationName("Jiri Otoupal")
    app.setOrganizationDomain("https://github.com/jiri-otoupal/dievpn")
    app.setWindowIcon(QIcon(":/icons/dievpn.ico"))
    app.setApplicationName("DieVpn")
    engine = QQmlApplicationEngine()
    bridge = Bridge()
    bridge.periodic_check()
    context = engine.rootContext()
    context.setContextProperty("con", bridge)
    engine.load(QUrl("qrc:/qml/main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
