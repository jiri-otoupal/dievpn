import click as click

from config.secret import credentials
from modules.vpncli import VpnCli, vpn_cli_file_path


@click.group()
def cli():
    pass


@cli.command(name="connect")
@click.argument("host", nargs=1)
def _connect(host):
    vpncli = VpnCli(str(vpn_cli_file_path))
    vpncli.connect(credentials[host])


@cli.command(name="disconnect")
def _disconnect():
    VpnCli.reset()


if __name__ == '__main__':
    cli()
