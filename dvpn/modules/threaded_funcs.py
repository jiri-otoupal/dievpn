import tkinter.messagebox
from tkinter import Tk, Button

import dvpn
from dvpn.config.constants import DEFAULT_TITLE, PublicVars
from dvpn.modules.tools import clear_buttons, connect
from dvpn.vpns.anyconnect import AnyConnectCLI


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
    record = PublicVars().credentials.get(host)
    cli = None
    if record.get("vpn_type") == "anyconnect":
        cli = AnyConnectCLI

    stat = connect(cli, host)
    dvpn.config.constants.CONNECTED_CLI = cli
    if stat[0]:
        instigator.config(bg="darkgreen")
        window.title(f"DieVPN Connected to {host}")
    else:
        instigator.config(bg="darkred")
        window.title(DEFAULT_TITLE)
        if stat[1].get("reason", False) == "invalid credentials":
            tkinter.messagebox.showerror("Invalid Credentials",
                                         f"Invalid Login Credentials for VPN {host}")
    # state_buttons("normal")


def _disconnect_threaded(window: Tk):
    window.title("Disconnecting")
    cli = dvpn.config.constants.CONNECTED_CLI
    if cli is not None:
        cli.reset()
    window.title(DEFAULT_TITLE)
    clear_buttons()
