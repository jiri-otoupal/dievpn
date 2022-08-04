import sys

from PySide6.QtCore import QObject, QCoreApplication, QUrl, qInstallMessageHandler, Slot
from PySide6.QtGui import Qt, QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

import res  # noqa
from dvpn.windows.logger import qt_message_handler


class Bridge(QObject):
    @Slot("QVariantMap", result=None)
    def add_vpn(self, obj):
        pass


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
