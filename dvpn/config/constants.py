import json
from builtins import dict

from dvpn.config.paths import secret_path

default_title = "Die VPN Control"


class PublicVars:
    _credentials = {}
    instance = None

    def __init__(self):
        self._credentials = {}

    def __new__(cls, *args, **kwargs):
        if cls.instance is None:
            return object.__new__(cls)
        else:
            return cls.instance

    @property
    def credentials(self) -> dict:
        if not secret_path.exists():
            with open(str(secret_path), "w") as fp:
                json.dump({}, fp, indent=1)
        with open(str(secret_path), "r") as fp:
            _credentials = json.load(fp)
        return _credentials

    @credentials.setter
    def credentials(self, updated: dict):
        with open(str(secret_path), "w") as fp:
            json.dump(updated, fp, indent=4)
