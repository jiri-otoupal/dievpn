import QtQuick 2.15
import QtQuick.Layouts 1.1
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2


ApplicationWindow {
    id: window
    visible: true
    width: 600
    height: 450
    title: "DieVPN"
    color: "#292D3E"

    maximumHeight: this.height
    minimumHeight: this.height
    maximumWidth: this.width
    minimumWidth: 250


    GroupBox {
        width: parent.width
        Layout.fillWidth: true
        anchors.fill: parent

        Rectangle {
            radius: 6
            width: parent.width - vpn_list.width -12
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            color :"#222436"

            ColumnLayout {
                anchors.fill: parent
                Text {
                    text: "Edit VPN"
                    color: "#F7F7F7"
                    font.pixelSize: 18
                    anchors.top: parent.top
                    anchors.left: parent.left
                    anchors.right: parent.right
                    topPadding: 6

                    horizontalAlignment: Text.AlignHCenter
                }
                ScrollView {
                    width: parent.width
                    height: parent.height
                    anchors.fill: parent
                    leftPadding: 16
                    rightPadding: 16
                    topPadding : 60
                    bottomPadding : 80
                    ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                    ListView {
                        model: 20
                        spacing: 6
                        delegate: RowLayout {
                            width: parent.width
                            Layout.fillWidth: true
                            TextField {
                                color: "white"
                                placeholderText: qsTr("Enter name")
                                anchors.top: parent.top
                                anchors.left: parent.left
                                anchors.right: parent.right
                            }
                        }
                    }
                }

                BlueButton {
                    Layout.fillWidth: true
                    text: "Apply"

                    anchors.bottom: parent.bottom
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.leftMargin: 12
                    anchors.rightMargin: 12
                }
            }
        }

        ColumnLayout {
            id: vpn_list
            width: 250
            anchors.bottom: parent.bottom
            anchors.top: parent.top
            anchors.left: parent.left

            ScrollView {
                width: parent.width
                height: parent.height
                anchors.fill: parent
                leftPadding: 16
                rightPadding: 16
                topPadding : 60
                bottomPadding : 80
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                ListView {
                    model: 20
                    spacing: 6
                    delegate: VPNRow {
                        Layout.fillWidth: true

                    }
                }
            }


            BlueButton {
                anchors.top: parent.top
                Layout.fillWidth: true
                text: "Add"

            }

            DisconnectButton {
                anchors.bottom: parent.bottom
                Layout.fillWidth: true

            }
        }
    }

}