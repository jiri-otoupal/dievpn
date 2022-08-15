import QtQuick 2.15
import QtQuick.Layouts 1.1
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2



ModalAdd {
    id: editModal


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