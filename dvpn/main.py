import sys
from threading import Thread
from time import sleep
from typing import Iterable

import click
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
from dvpn.config.paths import secret_path
from dvpn.logger import qt_message_handler
from dvpn.modules.tools import connect
from dvpn.vpns.base import VpnCli


class Bridge(QObject):
    periodic_thread = None
    connectedVPNs: Iterable[str] = set()
    changingVPNs = set()

    disconnectBtnChangeEnabled = Signal(bool, str, name="disconnectBtnChangeEnabled")
    connectStatusChange = Signal(str, bool, bool, name="connectStatusChange")
    disconnectChange = Signal(str, bool, bool, name="disconnectChange")

    @Slot(result=list)
    def get_available_cli(self) -> list:
        return list(CLI_RESOLVE.keys())

    def periodic_check(self):
        if self.periodic_thread is not None:
            return False
        t = Thread(
            target=self._periodic_check, name="Periodic status Check", daemon=True
        )
        self.periodic_thread = t
        t.start()
        return True

    def _periodic_check(self):
        while True:
            for vpn_name in list(PublicVars().credentials.keys()):

                # Wait for previous operation to finish
                while vpn_name in self.changingVPNs:
                    sleep(0.1)

                creds = PublicVars().credentials[vpn_name]
                cli_type = CLI_RESOLVE[creds["selectedVpn"]]
                cli_instance = cli_type(creds["cliPath"])
                state = cli_instance.get_state(vpn_name).lower()

                if "disconnected" in state:
                    self.disconnect_notify(vpn_name, cli_instance, False)
                    break

                elif "connected" in state and vpn_name not in self.connectedVPNs:
                    self.disconnectBtnChangeEnabled.emit(True, vpn_name)
                    break

                # Limit CPU usage
                sleep(0.1)

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

    @Slot(str, result=str)
    def get_vpn_default_cli(self, vpn_name):
        cli: VpnCli = CLI_RESOLVE[vpn_name]
        return cli.get_default_cli_path()

    @Slot(str, result=list)
    def get_vpn_fields(self, vpn_name):
        cli = CLI_RESOLVE[vpn_name]
        return cli.fields

    @Slot(str)
    def connect(self, vpn_name: str):
        # noinspection PyUnresolvedReferences
        self.changingVPNs.add(vpn_name)
        self.connectStatusChange.emit(vpn_name, False, True)

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
        Thread(
            target=self.disconnect_joined, name="Disconnect All", daemon=True
        ).start()

    def disconnect_joined(self):
        for host in set(self.connectedVPNs):
            self.changingVPNs.add(host)
            creds = PublicVars().credentials[host]
            cli_type = CLI_RESOLVE[creds["selectedVpn"]]
            cli = cli_type(str(creds["cliPath"]))
            self.disconnect_notify(host, cli),

    def disconnect_notify(self, vpn_name, cli, reset=True):
        self.disconnectChange.emit(vpn_name, False, True)
        if reset:
            cli.reset(host=vpn_name)
        # noinspection PyUnresolvedReferences
        self.disconnectChange.emit(vpn_name, False, False)
        self.connectedVPNs.discard(vpn_name)
        self.changingVPNs.discard(vpn_name)


@click.group()
def cli():
    pass


@cli.command(name="connect")
@click.argument("host", nargs=1)
def _connect(host):
    bridge = Bridge()
    vpn_conf = PublicVars()[host]
    cli = CLI_RESOLVE[vpn_conf["selectedVpn"]](vpn_conf["cliPath"])
    connect(cli, vpn_conf["VPN Name"], bridge)


@cli.command(name="disconnect")
@click.argument("host", nargs=1)
def _disconnect(host):
    vpn_conf = PublicVars()[host]
    cli = CLI_RESOLVE[vpn_conf["selectedVpn"]](vpn_conf["cliPath"])
    cli.reset()


@cli.command()
def gui():
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
    # bridge.periodic_check()
    context = engine.rootContext()
    context.setContextProperty("con", bridge)
    engine.load(QUrl("qrc:/qml/main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())


def main():
    secret_path.parent.mkdir(exist_ok=True)
    if len(sys.argv) < 2:
        gui()
    cli()


if __name__ == "__main__":
    main()
