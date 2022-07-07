import QtQuick 2.15
import QtQuick.Controls 2.15

TextField {
    id: control

    font.family: "Roboto"
    font.pixelSize: 12
    implicitHeight: 30

    background: Rectangle {
        color: control.enabled ? Style.colors.white : Style.colors.grey
        border.color: control.activeFocus ? Style.colors.turquoise : Style.colors.greyDarker
        radius: 4
    }

    selectionColor: "#70b0ff"
    selectByMouse: true
}