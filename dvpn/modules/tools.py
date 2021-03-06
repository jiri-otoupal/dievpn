from tkinter import Tk

from dvpn.config.constants import PublicVars
from dvpn.modules.vpncli import VpnCli

buttons = dict()


def state_buttons(state_out):
    for btn in buttons.values():
        btn.config(state=state_out)


def clear_buttons():
    tmp = dict(buttons)
    tmp.pop("Disconnect")
    for btn in tmp.items():
        try:
            btn[1].config(bg="lightgray", fg="black", text=btn[0])
        except Exception:
            # Just tkinter and its sometime problem with config
            pass


def reopen(last_window: Tk):
    last_window.destroy()
    from dvpn.modules.windows import open_gui
    open_gui()


def connect(host) -> (bool, dict):
    creds = PublicVars().credentials[host]
    vpncli = VpnCli(str(creds["cli_path"]))
    try:
        return vpncli.connect(creds)
    except Exception as ex:
        print("DieVpn encountered problem with anyconnect, can be cause by stucked "
              "ovpn agent from previous instance or already running cli try to check"
              " for other cli or anyconnect processes or reboot computer")
        return False, {"exception": str(ex)}
