import QtQuick 2.15
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2


Button {
    id: control
    Material.background: "#717CB4"
    Material.foreground: "#F8F8F8"
    property bool connected: false


    Image {
        id: conn_status
        antialiasing: true
        source: parent.connected ? "qrc:/images/connected.png": "qrc:/images/disconnected.png"
        transform: [Scale {
            yScale: 0.6
            xScale: 0.6
        }]
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.topMargin: 10
        anchors.leftMargin: 6
    }
}