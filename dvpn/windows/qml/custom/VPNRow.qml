import QtQuick 2.15
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.1

RowLayout {
    width: parent.width


    Rectangle {
        radius:6
        Layout.fillWidth: true
        width: parent.width
        color :"#191a2a"
        height: 96

        ColumnLayout {
            spacing: 0
            width: parent.width -12
            anchors.centerIn: parent
            Layout.fillWidth: true


            VPNButton {
                Layout.fillWidth: true
                text: "VPN " + (index + 1)
            }

            EditRow {
                Layout.fillWidth: true

            }

        }
    }
}