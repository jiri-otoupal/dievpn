import tkinter.messagebox
from tkinter import Tk, Button

from dvpn.config.constants import DEFAULT_TITLE
from dvpn.modules.tools import clear_buttons, connect
from dvpn.modules.vpncli import VpnCli


def connect_threaded(window, host, instigator):
    _connect_threaded(window, host, instigator)
    # Thread(target=_connect_threaded, args=[window, host, instigator], daemon=True).start()
    # TODO: Fix this on OSX


def disconnect_threaded(window: Tk):
    _disconnect_threaded(window)
    # Thread(target=_disconnect_threaded, args=[window], daemon=True).start()


def _connect_threaded(window: Tk, host, instigator: Button):
    window.title(f"DieVPN Connecting to {host}")
    # state_buttons("disabled")
    clear_buttons()
    stat = connect(host)
    if stat[0]:
        instigator.config(bg="darkgreen", text=instigator.cget("text") + " (Connected)")
        window.title(f"DieVPN Connected to {host}")
    else:
        instigator.config(bg="darkred", text=instigator.cget("text") + " (Failed)")
        window.title(DEFAULT_TITLE)
        if stat[1].get("reason", False) == "invalid credentials":
            tkinter.messagebox.showerror("Invalid Credentials",
                                         f"Invalid Login Credentials for VPN {host}")
    # state_buttons("normal")


def _disconnect_threaded(window: Tk):
    window.title("Disconnecting")
    VpnCli.reset()
    window.title(DEFAULT_TITLE)
    clear_buttons()
