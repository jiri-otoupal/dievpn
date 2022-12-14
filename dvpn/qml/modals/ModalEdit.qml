import QtQuick 2.15
import QtQuick.Layouts 1.1
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2
import ":/../../../js/Basic.js" as Basic


ModalBase {
    id: editModal
    property string vpn_name


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

        Component.onCompleted: {
            selectVpn.model = con.get_available_cli();
        }


        onCurrentTextChanged: {

            Basic.updateFieldsModalEdit();
            Basic.updateEdit();
        }
    }
    ColumnLayout {
        anchors.topMargin : 64
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: anchors.bottom

        FileField {
            id: cliPath

            placeholderText: "Cli Executable Path"
            anchors.rightMargin: 15
            anchors.leftMargin: 15
            anchors.left: parent.left
            anchors.right: parent.right
        }


        ScrollView {
            anchors.top: cliPath.top
            anchors.topMargin : 42
            anchors.fill: parent
            ScrollBar.horizontal.policy: ScrollBar.AlwaysOff

            ListView {
                anchors.fill: parent
                Component.onCompleted: {
                    vpnDetails.clear();


                }
                model: ListModel {
                    id: vpnDetails


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
    }
    Rectangle {
        color: "white"
        height: 45
        radius: 6
        anchors.bottom: submitEdit.top
        anchors.bottomMargin: 6
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.leftMargin: 16
        anchors.rightMargin: 16

        CheckBox {
            id: bannerCheckBox
            anchors.fill: parent
            text: "Has Banner"

        }
    }

    function capitalize(s) {
        return s[0].toUpperCase() + s.slice(1);
    }

    function load(vpn_name) {
        editModal.vpn_name=vpn_name;
        const details = con.get_vpn_details(vpn_name);

        const index = selectVpn.find(details.selectedVpn);
        selectVpn.currentIndex = index;
        Basic.updateEdit();


    }


    BlueButton {
        id: submitEdit
        text: "Save"

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

            for (var i=0; i < vpnDetails.count; i++) {
                const row = vpnDetails.get(i);
                obj[row.name] = row.textValue;
            }

            con.edit(editModal.vpn_name, obj);
        }



    }


}