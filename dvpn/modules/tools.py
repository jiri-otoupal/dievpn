from typing import Optional

from dvpn.config.constants import PublicVars
from dvpn.vpns.base import VpnCli


def connect(cli: VpnCli, host: str, bridge: Optional["Bridge"]) -> (bool, dict):
    creds = PublicVars().credentials[host]
    vpncli = type(cli)(str(creds["cliPath"]))
    try:
        out = vpncli.connect(creds)
        if bridge:
            bridge.connectStatusChange.emit(host, out[0], False)
    except Exception as ex:
        print("DieVpn encountered problem with anyconnect, can be cause by stuck "
              "ovpn agent from previous instance or already running cli try to check"
              " for other cli or anyconnect processes or reboot computer")
        return False, {"exception": str(ex)}
