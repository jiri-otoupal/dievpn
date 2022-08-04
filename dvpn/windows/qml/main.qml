import QtQuick 2.15
import QtQuick.Layouts 1.1
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2
import QtQuick3D
import QtQuick3D.Effects
import QtQuick3D.AssetUtils
import QtQuick3D.Helpers
import QtQuick3D.Particles3D

ApplicationWindow {
    id: window
    visible: true
    width: 300
    height: 450
    title: "DieVPN"
    color: "#292D3E"

    maximumHeight: this.height
    minimumHeight: this.height
    maximumWidth: this.width
    minimumWidth: this.width


    GroupBox {
        width: parent.width
        Layout.fillWidth: true
        anchors.fill: parent


        ColumnLayout {
            id: vpn_list
            width: parent.width
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

                onClicked: addModal.opacity=1
            }

            DisconnectButton {
                anchors.bottom: parent.bottom
                Layout.fillWidth: true

            }
        }
    }

    ModalBase {
        id: addModal
        visible: this.opacity > 0
        opacity: 0

        Behavior on opacity {
            NumberAnimation {
                duration: 100
                easing.type: Easing.Out
            }
        }

        ComboBox {
            id: selectVpn
            height: 36
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 48
            anchors.rightMargin: 48
            anchors.topMargin: 12
            font.family: "Roboto"
            font.pixelSize: 12

            model: ["AnyConnect","OpenVPN","TunnelBlick"]
        }

        ColumnLayout {
            anchors.topMargin : 45
            anchors.fill: parent

            FileField {
                id: cliPath

                placeholderText: "Cli Executable Path"
                anchors.rightMargin: 15
                anchors.leftMargin: 15
                anchors.topMargin : 20
                anchors.left: parent.left
                anchors.right: parent.right
            }


            ScrollView {
                anchors.topMargin : 60
                anchors.fill: parent
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                ListView {

                    model: ListModel {
                        id: vpnAddDetails
                        ListElement {
                            name: "VPN Name"; placeholderText: "My Zoo VPN"
                        }
                        ListElement {
                            name: "Host"; placeholderText: "favourite-zoo.com"
                        }
                        ListElement {
                            name: "Username"; placeholderText: "giraffe"
                        }
                        ListElement {
                            name: "Password"; placeholderText: "******"; password: true
                        }

                    }
                    spacing: 6
                    delegate:
                    FieldRow {
                        index: model.index
                        textValue: model.text
                        fieldName: model.name
                        placeholderText: model.placeholderText
                        echoMode: model.password ? TextInput.Password  : null
                    }
                }
            }

            BlueButton {
                id: "submitAdd"
                text: "Add"

                anchors.bottomMargin: 16
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.right: parent.right

                anchors.leftMargin: 16
                anchors.rightMargin: 16



                onClicked: {
                    const obj = {};

                    obj.selectedVpn = selectVpn.currentText;
                    obj.cliPath = cliPath.value;

                    for (var i=0; i < vpnAddDetails.count; i++) {
                        const row = vpnAddDetails.get(i);
                        obj[row.name] = row.textValue;
                    }

                    con.add_vpn(obj);
                }



            }

        }

    }

}