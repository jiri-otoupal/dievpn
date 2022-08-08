from tkinter import Tk

from dvpn.config.constants import PublicVars
from dvpn.vpns.base import VpnCli

buttons = []


def state_buttons(state_out):
    for btn in buttons:
        btn.config(state=state_out)


def clear_buttons():
    for btn in buttons[:-1]:
        try:
            btn.config(bg="lightgray", fg="black")
        except Exception:
            # Just tkinter and its sometime problem with config
            pass


def reopen(last_window: Tk):
    last_window.destroy()
    from dvpn.modules.windows import open_gui
    open_gui()


def connect(cli: VpnCli, host: str) -> (bool, dict):
    creds = PublicVars().credentials[host]
    vpncli = type(cli)(str(creds["cliPath"]))
    try:
        return vpncli.connect(creds)
    except Exception as ex:
        print("DieVpn encountered problem with anyconnect, can be cause by stuck "
              "ovpn agent from previous instance or already running cli try to check"
              " for other cli or anyconnect processes or reboot computer")
        return False, {"exception": str(ex)}
