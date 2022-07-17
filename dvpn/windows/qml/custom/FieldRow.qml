import QtQuick 2.15
import QtQuick.Controls.Material 2.2
import QtQuick.Controls 2.2
import QtQuick.Layouts 1.1

RowLayout {
    anchors.leftMargin: 16
    anchors.rightMargin: 16
    anchors.left: parent.left
    anchors.right: parent.right
    width: parent.width

    property var echoMode
    property string fieldName: ""
    property string placeholderText: ""

    TextRegular{
        id: textLabel
        text: parent.fieldName
    }

    TextFieldRegular {
        echoMode: parent.echoMode
        placeholderText: parent.placeholderText
        anchors.leftMargin: 2
        anchors.top: parent.top
        anchors.left: textLabel.right
        anchors.right: parent.right
    }
}