import QtQuick 2.15

MouseArea {
    id: mouseArea

    anchors.fill: parent

    cursorShape: Qt.PointingHandCursor
    hoverEnabled: true

    onPressed: mouse.accepted = false;
    onReleased: mouse.accepted = false;
}
