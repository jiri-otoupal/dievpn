import QtQuick 2.15
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.1

RowLayout {
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