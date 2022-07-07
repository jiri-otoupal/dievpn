import QtQuick 2.15
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.1

RowLayout {
    width: parent.width

    TextFieldRegular {

        placeholderText: qsTr("Enter name")
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.right: parent.right
    }
}