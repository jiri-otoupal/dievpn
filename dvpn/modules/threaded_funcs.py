import tkinter.messagebox
from threading import Thread
from tkinter import Tk, Button

from dvpn.config.constants import default_title
from dvpn.modules.tools import state_buttons, clear_buttons, connect
from dvpn.modules.vpncli import VpnCli


def connect_threaded(window, host, instigator):
    _connect_threaded(window, host, instigator)
    # Thread(target=_connect_threaded, args=[window, host, instigator], daemon=True).start()


def disconnect_threaded(window: Tk):
    _disconnect_threaded(window)
    # Thread(target=_disconnect_threaded, args=[window], daemon=True).start()


def _connect_threaded(window: Tk, host, instigator: Button):
    window.title(f"DieVPN Connecting to {host}")
    # state_buttons("disabled")
    clear_buttons()
    stat = connect(host)
    if stat[0]:
        instigator.config(bg="darkgreen")
        window.title(f"DieVPN Connected to {host}")
    else:
        instigator.config(bg="darkred")
        window.title("Die VPN Control")
        if stat[1].get("reason", False) == "invalid credentials":
            tkinter.messagebox.showerror("Invalid Credentials",
                                         f"Invalid Login Credentials for VPN {host}")
    # state_buttons("normal")


def _disconnect_threaded(window: Tk):
    window.title("Disconnecting")
    VpnCli.reset()
    window.title(default_title)
    clear_buttons()
