import QtQuick 2.15
import Qt.labs.platform
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.1


RowLayout {
    property string value
    property string placeholderText

    TextRegular {
        id: placeLabel
        text: "Cli Path"
    }

    TextFieldRegular {
        id: control
        text: parent.value

        placeholderText: parent.placeholderText
        anchors.left: placeLabel.right
        anchors.right: parent.right
        anchors.leftMargin: 2

        rightPadding: 36

        readOnly: false

        function onBrowseClicked() {
            cliFileDialog.visible=true;
        }
        FileDialog {
            id: cliFileDialog
            title: "Please choose a CLI executable"
            visible: false
            options: FileDialog.ReadOnly

            onAccepted: {
                control.text= cliFileDialog.file.toString()
            }
            onRejected: {}

        }



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
}