import logging
import sys
from threading import Thread

from PySide6.QtCore import QObject, QCoreApplication, QUrl, qInstallMessageHandler, Slot, Signal
from PySide6.QtGui import Qt, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

import res  # noqa
from dvpn.config.constants import PublicVars, CLI_RESOLVE
from dvpn.modules.tools import connect
from dvpn.windows.logger import qt_message_handler


class Bridge(QObject):
    changingVPNs = []

    connectStatusChange = Signal(str, bool, bool, name="connectStatusChange")
    disconnectChange = Signal(str, bool, bool, name="disconnectChange")

    @Slot(str)
    def log(self, text):
        print(text)

    @Slot(result="QVariantMap")
    def list_vpn(self) -> dict:
        return PublicVars().credentials

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
        bridge.connectStatusChange.emit(vpn_name, False, True)
        self.changingVPNs.append(vpn_name)
        print(f"connecting {vpn_name}")
        vpn_conf = PublicVars()[vpn_name]
        cli = CLI_RESOLVE[vpn_conf["selectedVpn"]](vpn_conf["cliPath"])
        t = Thread(target=lambda: connect(cli, vpn_conf["VPN Name"], self),
                   name=f"Connecting {vpn_conf['VPN Name']}", daemon=True)
        t.start()

    @Slot(str)
    def edit(self, vpn_name: str):
        print(f"edit {vpn_name}")
        pass

    @Slot(str)
    def delete(self, vpn_name: str):
        tmp = PublicVars().credentials
        tmp.pop(vpn_name, None)
        PublicVars().credentials = tmp

    @Slot(str)
    def disconnect(self, vpn_name: str):
        self.disconnectChange.emit(vpn_name, True, True)
        vpn_conf = PublicVars()[vpn_name]
        cli = CLI_RESOLVE[vpn_conf["selectedVpn"]](vpn_conf["cliPath"])
        t = Thread(target=lambda: self.disconnect_notify(vpn_name, cli),
                   name=f"Disconnecting {vpn_name}", daemon=True)
        t.start()

    def disconnect_notify(self, vpn_name, cli):
        cli.reset()
        self.disconnectChange.emit(vpn_name, False, False)


if __name__ == "__main__":
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
    context = engine.rootContext()
    context.setContextProperty("con", bridge)
    engine.load(QUrl("qrc:/qml/main.qml"))
    if not engine.rootObjects():
        sys.exit(-1)
    sys.exit(app.exec())
