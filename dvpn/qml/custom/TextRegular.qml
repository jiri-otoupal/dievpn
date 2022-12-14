import QtQuick 2.15

Rectangle {
        id: control
        property string text;
        implicitHeight: 30
        width:  70
        color: "#777777"
        radius: 4
        anchors.top: parent.top

        Text {
            id: a_text
            anchors.centerIn: parent
            text: parent.text
            color: "#f8f8f8"
            font.family: "Roboto"
            font.pixelSize: 12
        }

        TextMetrics {
            id:     t_metrics
            font:   a_text.font
            text:   a_text.text
        }
}
