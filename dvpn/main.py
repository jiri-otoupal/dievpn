import json
from pathlib import Path
from threading import Thread
from tkinter import Tk, Button, Menu

import click as click

from dvpn.config.constants import default_title, PublicVars
from dvpn.config.paths import secret_path
from dvpn.modules.windows import new_vpn_window

from dvpn.modules.tools import buttons, state_btns, clear_btns
from dvpn.modules.vpncli import VpnCli, vpn_cli_file_path


@click.group()
def cli():
    pass


@cli.command(name="connect")
@click.argument("host", nargs=1)
def _connect(host):
    connect(host)


def connect(host) -> bool:
    vpncli = VpnCli(str(vpn_cli_file_path))
    return vpncli.connect(PublicVars().credentials[host])


@cli.command(name="disconnect")
def _disconnect():
    VpnCli.reset()


@cli.command(name="autoresolve")
def _auto():
    print("This is not implemented yet")
    VpnCli.check_accessed()


@cli.command()
def gui():
    # TODO: Refresh
    print("Make sure to kill all VPN clients before usage, as cli would collide with it")
    window = Tk()
    # add widgets here
    main_menu = Menu(window, tearoff=0)
    main_menu.add_command(label="Add VPN", command=lambda: new_vpn_window(window))
    main_menu.add_command(label="Select CLI", command=None)
    window.config(menu=main_menu)

    window.title(default_title)

    keys = PublicVars().credentials.keys()
    window.geometry(f"300x{(len(keys) + 1) * 35}+10+20")
    for vpn_connection in keys:
        btn = Button(text=vpn_connection.capitalize(), bg="darkgray", fg="white")
        btn.bind('<Button-1>',
                 lambda event, con=vpn_connection, tbtn=btn: connect_threaded(window, con,
                                                                              tbtn))
        buttons.append(btn)
        btn.pack(expand=True, fill="x")
    btn = Button(text="Disconnect", bg="black", fg="white",
                 command=lambda: disconnect_threaded(window))
    btn.pack(expand=True, fill="x", pady=5)
    buttons.append(btn)
    window.mainloop()


def _connect_threaded(window: Tk, host, instigator: Button):
    window.title(f"DieVPN Connecting to {host}")
    state_btns("disabled")
    clear_btns()
    if connect(host):
        instigator.config(bg="darkgreen")
        window.title(f"DieVPN Connected to {host}")
    else:
        instigator.config(bg="darkred")
        window.title("Die VPN Control")
    state_btns("normal")


def connect_threaded(window, host, instigator):
    Thread(target=_connect_threaded, args=[window, host, instigator]).start()


def disconnect_threaded(window: Tk):
    Thread(target=_disconnect_threaded, args=[window]).start()


def _disconnect_threaded(window: Tk):
    window.title("Disconnecting")
    VpnCli.reset()
    window.title(default_title)
    clear_btns()


if __name__ == '__main__':

    if not secret_path.exists():
        print(
            f"Please first Create secret.json according to README at"
            f" {str(Path(__file__).resolve().parent / 'config')} or use dvpn gui")
        exit(1)
    else:
        PublicVars()

    if len(PublicVars().credentials.keys()) == 0:
        print("No Credentials Found please make sure to add your VPNs before continuing "
              "with dvpn gui")
    cli()
