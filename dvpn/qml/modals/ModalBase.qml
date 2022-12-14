import QtQuick 2.15
import QtQuick.Window 2.15


PageBase {
    id: control
    property var parentContent: Window.window
    visible: opacity > 0
    opacity: 0
    anchors.centerIn: parent
    property int modalWidth: parent.width - 12
    property int modalMinimumHeight: parent.height - 32

    property string defaultTitle: ""

    property bool autohide: false
    property int autohideMs: 5000

    property Item contentHeightSource: null
    property Item contentTextTarget: null
    property int contentHeightAdjustment: 0

    property Item contentItem: contentItem


    Behavior on opacity {
        NumberAnimation {
            duration: 100
        }
    }

    function showMessage(message, title) {
        titleLabel.text = title ?? this.defaultTitle;
        if (this.contentTextTarget) {
            this.contentTextTarget.text = message;
        }

        this._show();

        if (this.autohide) autohideTimer.restart();
    }

    // Wrapper functions for compatibility
    function _open() {
        control.opacity=1;
    }

    function open() {
        control._open();
    }

    function close() {
        control.opacity=0;
    }

    Component.onCompleted: {

        this.anchors.fill = this.parentContent.contentItem;
    }

    Timer {
        id: autohideTimer

        interval: autohideMs

        onTriggered:         control.opacity=0;
    }

    Rectangle {
        color: "#770a0011"
        anchors.fill: parent

        MouseArea {
            anchors.fill: parent
            hoverEnabled: true
            cursorShape: Qt.PointingHandCursor

            onClicked:         control.opacity=0;
        }

        Rectangle {
            id: modalRect

            color: "#12141c"
            radius: 4

            width: control.modalWidth
            height: Math.max(Math.min((control.contentHeightSource ? control.contentHeightSource.height : 20) + 37 + control.contentHeightAdjustment, control.height - 20), control.modalMinimumHeight)

            anchors.centerIn: parent
            clip: true

            MouseArea { anchors.fill: parent }

            Image {
                id: closeButton

                source: "qrc:/images/error-icon.png"
                width: 16
                fillMode: Image.PreserveAspectFit
                mipmap: true

                anchors {
                    top: parent.top
                    right: parent.right
                    topMargin: 10
                    rightMargin: 10
                }

                MouseArea {
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor

                    onClicked:        control.opacity=0;
                }
            }



            Text {
                id: titleLabel
                color: "#f8f8f8"
                elide: Text.ElideRight
                font.family: "Roboto"
                font.pixelSize: 24

                anchors {
                    left: parent.left
                    top: parent.top
                    right: closeButton.left
                    leftMargin: 10
                    topMargin: 9
                    rightMargin: 10
                }
            }

            Rectangle {
                id: divider

                color: "#b3b3b3F5"
                height: 1

                anchors {
                    left: parent.left
                    top: parent.top
                    right: parent.right
                    topMargin: 36
                }
            }

            Item {
                id: contentItemParent

                anchors {
                    left: parent.left
                    top: divider.bottom
                    right: parent.right
                    bottom: parent.bottom
                }
            }
        }
    }
}
