import abc

from dvpn.modules.vpn_cli_singleton import SingletonMeta


class VpnCli(metaclass=SingletonMeta):

    def __init__(self, cli_path):
        print("\nWelcome to DieVPN\n")
        print(
            "Make sure to kill all VPN clients before usage, as cli would collide with it"
        )
        self.excluded_fields = []
        self.process_pipe = None
        self.cli_path = cli_path

    @abc.abstractmethod
    def get_connected_vpn(self):
        pass

    @classmethod
    @abc.abstractmethod
    def reset(cls, cli_path=None):
        pass

    @abc.abstractmethod
    def __connect(self, host, username, password, **kwargs) -> dict:
        pass

    @abc.abstractmethod
    def connect(self, creds: dict) -> (bool, dict):
        pass
