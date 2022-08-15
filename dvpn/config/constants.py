import json
from builtins import dict
from typing import Optional

from dvpn.config.paths import secret_path
from dvpn.vpns.anyconnect import AnyConnectCLI
from dvpn.vpns.viscosity import ViscosityCLI

CONNECTED_CLI = None

DEFAULT_TITLE = "Die VPN Control"

CLI_RESOLVE = {
    "AnyConnect": AnyConnectCLI,
    "Viscosity": ViscosityCLI
}


class PublicVars:
    _credentials = {}
    instance = None

    def __init__(self):
        self._credentials = {}
        if secret_path.exists():
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

    def save_vars(self, variables: Optional[dict] = None):
        if variables is None:
            vars_save = PublicVars().credentials
        else:
            vars_save = variables

        with open(str(secret_path), "w") as fp:
            json.dump(vars_save, fp, indent=4)

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
