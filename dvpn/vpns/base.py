import abc
import os

from dvpn.modules.vpn_cli_singleton import SingletonMeta


class VpnCli(metaclass=SingletonMeta):
    def __init__(self, cli_path):
        print("\nWelcome to DieVPN\n")
        print(
            "Make sure to kill all VPN clients before usage, as cli would collide with it"
        )
        print(
            "If this is stuck, make sure you are NOT running it in virtual environment !"
        )
        self.excluded_fields = []
        self.process_pipe = None
        self.cli_path = cli_path

    @property
    @abc.abstractmethod
    def cli_path_win(self):
        raise NotImplementedError

    @property
    @abc.abstractmethod
    def cli_path_osx(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_state(self, name: str) -> str:
        """
        Gets state of VPN
        :param name:
        :return: Disconnected | Connected | ...
        """
        pass

    @classmethod
    def get_default_cli_path(cls):
        if os.name == "nt":
            return str(cls.cli_path_win)
        return str(cls.cli_path_osx)

    @abc.abstractmethod
    def get_connected_vpn(self):
        pass

    @classmethod
    @abc.abstractmethod
    def reset(cls, cli_path=None, host: str = None):
        pass

    @abc.abstractmethod
    def __connect(self, **kwargs) -> dict:
        pass

    @abc.abstractmethod
    def connect(self, creds: dict) -> (bool, dict):
        pass
