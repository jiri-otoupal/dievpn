import QtQuick 2.15
import QtQuick.Layouts 1.1
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2
import ":/../../../js/Basic.js" as Basic
import QtQuick.Dialogs

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

        model: ["AnyConnect","Viscosity"]

        onCurrentTextChanged: {
            vpnAddDetails.clear();
            Basic.updateFieldsModalAdd();

        }
    }

    ColumnLayout {
        anchors.topMargin : 60
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
            anchors.topMargin : 50
            anchors.fill: parent
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

            ListView {
                Component.onCompleted: {
                    vpnAddDetails.clear();
                    Basic.updateFieldsModalAdd();


                }
                model: ListModel {
                    id: vpnAddDetails


                }
                spacing: 6
                delegate:
                FieldRow {
                    index: model.index
                    textValue: model.text
                    fieldName: model.name
                    placeholderText: model.placeholderText
                    echoMode: model.sensitive ? TextInput.Password : null
                }
            }
        }

        Rectangle{
        color: "white"
        height: 45
        radius: 6
            anchors.left: parent.left
            anchors.right: parent.right

            anchors.leftMargin: 16
            anchors.rightMargin: 16
        CheckBox{
            id: bannerCheckBox
            anchors.fill: parent
            text: "Has Banner"

            }
        }

        BlueButton {
            id: submitAdd
            text: "Add"

            anchors.bottomMargin: 16
            anchors.bottom: parent.bottom
            anchors.left: parent.left
            anchors.right: parent.right

            anchors.leftMargin: 16
            anchors.rightMargin: 16



            onClicked: {
                const obj = {};

                obj.banner = bannerCheckBox.checked;
                obj.selectedVpn = selectVpn.currentText;
                obj.cliPath = cliPath.value;

                for (var i=0; i < vpnAddDetails.count; i++) {
                    const row = vpnAddDetails.get(i);
                    obj[row.name] = row.textValue;
                }

                const res = con.add_vpn(obj);

                if(res)
                {
                    Basic.addVpn(obj["VPN Name"]);
                    addModal.close();
                    vpnAddDetails.clear();
                    Basic.updateFieldsModalAdd();
                }
                else {
                    warningDialog.visible = true;
                }
            }



        }

    }
    MessageDialog {
        id: warningDialog
        text: "VPN already exists"
        visible: false
        title: "Failed to Add VPN"

    }
}