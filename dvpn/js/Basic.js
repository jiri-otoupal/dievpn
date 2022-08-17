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
            vpnDetails.insert(0, arr);
        }
    }
}

function updateFieldsModalEdit(fill_cli_path = false) {
    const vpn_name = editModal.selectVpn.currentText;
    updateFieldsModal(fill_cli_path, vpn_name);
}

function updateFieldsModalAdd(fill_cli_path = false) {
    const vpn_name = selectVpn.currentText;
    updateFieldsModal(fill_cli_path, vpn_name);
}

function updateFieldsModal(fill_cli_path = false, vpn_name) {
    // Protect against crash
    if (vpn_name === "")
        return

    const fields = con.get_vpn_fields(vpn_name);

    for (let i = 0; i < fields.length; i++) {
        vpnDetails.append(fields[i]);
    }

    if (fill_cli_path)
        cliPath.value = con.get_vpn_default_cli(vpn_name)
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