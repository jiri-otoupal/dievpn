import QtQuick 2.15
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.1
import QtQuick.Dialogs
import ":/../../../js/Basic.js" as Basic

RowLayout {
    id: control
    property string vpn_name;
    anchors.left: parent.left
    anchors.right: parent.right

    width: parent.width

    ColumnLayout {

        width: parent.width
        Layout.fillWidth: true
        Button {
            Material.background: "#c8d3f5"
            icon.color: "#333333"
            icon.source: "qrc:images/edit.png"
            width: parent.width
            Layout.fillWidth: true

            onClicked: con.edit(parent.parent.vpn_name);
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
            onClicked: {
                askConfirmDelete.open();
            }
        }
    }

    MessageDialog {
        id: askConfirmDelete
        title: "Deleting VPN " +control.vpn_name
        text: "Do you really want to delete "+control.vpn_name+" VPN?"

        buttons: MessageDialog.Yes | MessageDialog.No

        onAccepted: {
            Basic.removeVpn(control.vpn_name);
             con.delete(control.vpn_name);
        }

    }
}