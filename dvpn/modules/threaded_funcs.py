from threading import Thread
from tkinter import Tk, Button

from dvpn.config.constants import default_title
from dvpn.modules.tools import state_buttons, clear_buttons, connect
from dvpn.modules.vpncli import VpnCli


def connect_threaded(window, host, instigator):
    Thread(target=_connect_threaded, args=[window, host, instigator]).start()


def disconnect_threaded(window: Tk):
    Thread(target=_disconnect_threaded, args=[window]).start()


def _connect_threaded(window: Tk, host, instigator: Button):
    window.title(f"DieVPN Connecting to {host}")
    state_buttons("disabled")
    clear_buttons()
    if connect(host):
        instigator.config(bg="darkgreen")
        window.title(f"DieVPN Connected to {host}")
    else:
        instigator.config(bg="darkred")
        window.title("Die VPN Control")
    state_buttons("normal")


def _disconnect_threaded(window: Tk):
    window.title("Disconnecting")
    VpnCli.reset()
    window.title(default_title)
    clear_buttons()
