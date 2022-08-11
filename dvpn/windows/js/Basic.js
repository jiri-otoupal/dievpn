function addVpn(vpn_name) {
    vpn_model.append({"vpn_name": vpn_name, "running": false, "connected": false})
}

function removeVpn(vpn_name) {
    vpn_model.remove(vpn_name)
}

function changeVpn(vpn_name, connected, running) {
    for (let i = 0; vpn_model.count > i; i++) {
        const item = vpn_model.get(i);
        const name = item.vpn_name;

        if (name === vpn_name) {
            vpn_model.setProperty(i, "connected", connected);
            vpn_model.setProperty(i, "running", running);
            break;
        }

    }
}