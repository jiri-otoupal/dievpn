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

            }

            DisconnectButton {
                anchors.bottom: parent.bottom
                Layout.fillWidth: true

            }
        }
    }

    ModalBase{
        visible: true

        ColumnLayout{
            anchors.topMargin : 45
            anchors.fill: parent

        FileField {

        }

        ScrollView {
                anchors.topMargin : 60
                anchors.fill: parent
                ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

                ListView {
                model: ListModel{
                    ListElement{
                        name: "VPN Name"; placeholderText: "My Zoo VPN"
                    }
                    ListElement{
                        name: "Host"; placeholderText: "favorite-zoo.com"
                    }
                    ListElement{
                        name: "Username"; placeholderText: "giraffe"
                    }
                    ListElement{
                        name: "Password"; placeholderText: "******"; password: true
                    }

                }
                    spacing: 6
                delegate:
                    FieldRow {
                        fieldName: model.name
                        placeholderText: model.placeholderText
                        echoMode: model.password ? TextInput.Password  : null
                    }
            }
        }

        }

    }

}