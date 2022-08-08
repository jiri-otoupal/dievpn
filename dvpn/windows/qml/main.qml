import QtQuick 2.15
import QtQuick.Layouts 1.1
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2
import QtQuick3D
import QtQuick3D.Effects
import QtQuick3D.AssetUtils
import QtQuick3D.Helpers
import QtQuick3D.Particles3D
import ":/../../js/Basic.js" as Basic


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

        Rectangle {
            visible: vpn_model.count == 0
            opacity: 0.5
            anchors.bottomMargin: 60
            anchors.topMargin: 60
            color: "#f8f8f8"
            radius: 6

            anchors.fill: parent
            Text{
                anchors.centerIn: parent
                font.family: "Roboto"
                font.pixelSize: 32

                text: "No VPNs added."
            }

        }

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

                Component.onCompleted: {
                         var vpns = con.list_vpn();

                         for (const [key, value] of Object.entries(vpns)) {
                                Basic.addVpn(key);
                         }
                    }

                ListView {
                    model: ListModel{
                        id: vpn_model

                    }
                    spacing: 6
                    delegate: VPNRow {
                        vpn_name: model.vpn_name
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

                onClicked: con.disconnect()
            }
        }
    }

    ModalAdd{
        id: addModal
    }

    ModalEdit {
        id: editModal

    }


}