import QtQuick 2.15
import QtQuick.Controls 2.15

TextField {
    id: control

    font.family: "Roboto"
    font.pixelSize: 12
    leftPadding: 8

    background: Rectangle {
        height: 30
        color: control.enabled ? "white" : "#333333"
        border.color: control.activeFocus ? "purple" : "#333333"
        radius: 4
    }

    selectionColor: "#70b0ff"
    selectByMouse: true
}