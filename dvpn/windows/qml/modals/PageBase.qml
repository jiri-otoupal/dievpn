import QtQuick 2.15


Item {
    id: page

    visible: false
    anchors.fill: parent

    function show() {
        // To be able to add actions in derived components.
        _show();
    }

    function _show() {
        page.opacity = 0.0;
        page.visible = true;
        animateShow.start();
    }

    function hide() {
        // To be able to add actions in derived components.
        _hide();
    }

    function _hide() {
        page.visible = false;
    }

    PropertyAnimation {
        id: animateShow

        target: page
        duration: 100
        property: "opacity"
        to: 1.0
    }
}
