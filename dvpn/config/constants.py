import json
from builtins import dict

from dvpn.config.paths import secret_path
from dvpn.vpns.anyconnect import AnyConnectCLI

CONNECTED_CLI = None

DEFAULT_TITLE = "Die VPN Control"

CLI_RESOLVE = {
    "AnyConnect": AnyConnectCLI
}

class PublicVars:
    _credentials = {}
    instance = None

    def __init__(self):
        self._credentials = {}
        self.load_vars()

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            cls.instance = object.__new__(cls)
            return cls.instance
        else:
            return cls.instance

    @property
    def credentials(self) -> dict:
        if not secret_path.exists():
            self.save_vars({})
        else:
            self.load_vars()
        return self._credentials

    def save_vars(self, vars: dict):
        with open(str(secret_path), "w") as fp:
            json.dump(vars, fp, indent=4)

    def load_vars(self):
        with open(str(secret_path), "r") as fp:
            self._credentials = json.load(fp)

    @credentials.setter
    def credentials(self, updated: dict):
        self.save_vars(updated)

    def __getitem__(self, item):
        return self._credentials[item]

    def __setitem__(self, key, value):
        self._credentials[key] = value
        self.save_vars(self._credentials)
