import tkinter.messagebox
from pathlib import Path
from sys import argv

import click as click
import psutil

from dvpn.config.constants import PublicVars
from dvpn.config.paths import secret_path
from dvpn.modules.tools import connect
from dvpn.modules.vpncli import VpnCli
from dvpn.modules.windows import open_gui


@click.group()
def cli():
    pass


@cli.command(name="connect")
@click.argument("host", nargs=1)
def _connect(host):
    connect(host)


@cli.command(name="disconnect")
def _disconnect():
    VpnCli.reset()


@cli.command(name="autoresolve")
def _auto():
    print("This is not implemented yet")
    VpnCli.check_accessed()


@cli.command()
def gui():
    open_gui()


def get_status(p):
    return (p.status() if hasattr(p.status, '__call__'
                                  ) else p.status)


def main():
    if "gui" not in argv:
        if not secret_path.exists():
            print(
                f"Please first Create secret.json according to README at"
                f" {str(Path(__file__).resolve().parent / 'config')} or use dvpn gui")
            exit(1)
        else:
            PublicVars()

        if len(PublicVars().credentials.keys()) == 0:
            print(
                "No Credentials Found please make sure to add your VPNs before "
                "continuing "
                "with dvpn gui")

    processes = [proc.name().lower() if get_status(proc) != psutil.STATUS_ZOMBIE else ""
                 for
                 proc in psutil.process_iter()]
    if "anyconnect" in "".join(processes):
        tkinter.messagebox.showwarning("AnyConnect is running",
                                       "End other Any connect instances before usage")
        exit(1)
    cli()


if __name__ == "__main__":
    main()
