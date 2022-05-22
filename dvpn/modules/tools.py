from tkinter import Tk

from dvpn.config.constants import PublicVars
from dvpn.modules.vpncli import VpnCli

buttons = []


def state_buttons(state_out):
    for btn in buttons:
        btn.config(state=state_out)


def clear_buttons():
    for btn in buttons[:-1]:
        btn.config(bg="lightgray", fg="black")


def reopen(last_window: Tk):
    last_window.destroy()
    from dvpn.modules.windows import open_gui
    open_gui()


def connect(host) -> bool:
    creds = PublicVars().credentials[host]
    vpncli = VpnCli(str(creds["cli_path"]))
    return vpncli.connect(creds)
