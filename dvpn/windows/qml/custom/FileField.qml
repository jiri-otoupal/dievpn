import QtQuick 2.15
import QtQuick.Controls 2.15

TextFieldRegular {
    id: control

    rightPadding: 36

    readOnly: true

    function onBrowseClicked() {}

    Image {
        id: browseIcon
        source: "qrc:/images/folder.png"
        width: 24
        fillMode: Image.PreserveAspectFit

        mipmap: true
        mirror: true

        anchors.right: parent.right
        anchors.rightMargin: 5
        anchors.verticalCenter: parent.verticalCenter

        opacity: browseMouseArea.containsMouse ? 1.0 : 0.3

        ClickMouseArea {
            id: browseMouseArea

            onPressed: mouse.accepted = true;
            onReleased: mouse.accepted = true;

            onClicked: control.onBrowseClicked();
        }
    }
}
