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
                Button {
                    Layout.fillWidth: true
                    Material.background: "#70b0ff"
                    Material.foreground: "#F8F8F8"
                    width: parent.width
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
                    delegate: RowLayout {
                        width: parent.width
                        Layout.fillWidth: true

                        Rectangle {
                            Layout.fillWidth: true
                            width: parent.width
                            color :"#2f334d"
                            height: 90

                            ColumnLayout {
                                spacing: 0
                                width: parent.width
                                Layout.fillWidth: true


                                Button {
                                    Material.background: "#717CB4"
                                    Material.foreground: "#F8F8F8"

                                    width: parent.width
                                    Layout.fillWidth: true
                                    text: "VPN " + (index + 1)

                                    Image {
                                        id: conn_status
                                        antialiasing: true
                                        source: "qrc:/images/disconnected.png"
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

                                RowLayout {
                                    anchors.left: parent.left
                                    anchors.right: parent.right

                                    width: parent.width
                                    Layout.fillWidth: true
                                    ColumnLayout {

                                        width: parent.width
                                        Layout.fillWidth: true
                                        Button {
                                            Material.background: "#c8d3f5"
                                            icon.color: "#333333"
                                            icon.source: "qrc:images/edit.png"
                                            width: parent.width
                                            Layout.fillWidth: true
                                        }
                                    }
                                    ColumnLayout {

                                        width: parent.width
                                        Layout.fillWidth: true
                                        Button {
                                            Material.background: "#ff757f"
                                            icon.color: "#333333"
                                            icon.source: "qrc:images/delete.png"
                                            width: parent.width
                                            Layout.fillWidth: true
                                        }
                                    }
                                }

                            }
                        }
                    }
                }
            }


            Button {
                anchors.top: parent.top
                Layout.fillWidth: true
                Material.background: "#70b0ff"
                Material.foreground: "#333333"
                width: parent.width
                text: "Add"
            }

            Button {
                Layout.fillWidth: true
                Material.background: "#ff757f"
                Material.foreground: "#F8F8F8"
                width: parent.width
                text: "Disconnect"
                enabled: false
                anchors.bottom: parent.bottom
            }
        }
    }

}