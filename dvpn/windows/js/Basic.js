function addVpn(vpn_name) {
    vpn_model.append({"vpn_name": vpn_name, "running": false, "connected": false})
}

function removeVpn(vpn_name) {
    for (let i = 0; vpn_model.count > i; i++) {
        const item = vpn_model.get(i);
        const name = item.vpn_name;

        if (name === vpn_name)
            vpn_model.remove(i)

    }
}

function updateEdit() {
    const details = con.get_vpn_details(editModal.vpn_name);
    cliPath.value = details.cliPath;
    bannerCheckBox.checked = details.banner;

    vpnDetails.clear();
    for (let key in details) {

        if (capitalize(key) === key) {
            const arr = {
                name: key,
                text: details[key]
            }
            vpnDetails.append(arr);
        }
    }
}

function updateFieldsModalAdd() {
    const fields = con.get_vpn_fields(selectVpn.currentText);
    for (var i = 0; i < fields.length; i++) {
        vpnDetails.append(fields[i]);
    }
}

function updateFieldsModalEdit() {
    const fields = con.get_vpn_fields(selectVpn.currentText);
    for (var i = 0; i < fields.length; i++) {
        vpnDetails.append(fields[i]);
    }
}

function changeVpn(vpn_name, connected, running) {
    for (let i = 0; vpn_model.count > i; i++) {
        const item = vpn_model.get(i);
        const name = item.vpn_name;

        if (name === vpn_name) {
            vpn_model.setProperty(i, "connected", connected);
            vpn_model.setProperty(i, "running", running);
            return;
        }

    }
}