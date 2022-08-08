import QtQuick 2.15
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.1

RowLayout {
    width: parent.width
    property string vpn_name
    property bool running: false
    property bool connected: false

    Rectangle {
        radius:6
        Layout.fillWidth: true
        width: parent.width
        color :"#191a2a"
        height: 96

        ColumnLayout {
            spacing: 0
            width: parent.width - 12
            anchors.centerIn: parent
            Layout.fillWidth: true


            VPNButton {
                id: conn_button
                connected: parent.parent.parent.connected
                Layout.fillWidth: true
                text: parent.parent.parent.vpn_name
                onClicked: {
                    conn_status.running = true
                    con.connect(this.text);
                }

                BusyIndicator {
                    id: conn_status
                    visible: running
                    anchors.topMargin: 6
                    anchors.bottomMargin: 6
                    running: parent.parent.parent.parent.running
                    anchors.fill: parent
                }
            }

            EditRow {
                vpn_name: parent.parent.parent.vpn_name
                Layout.fillWidth: true

            }

        }
    }
}