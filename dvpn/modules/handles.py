from json import JSONDecodeError

from dvpn.config.constants import PublicVars
from dvpn.config.paths import secret_path


def add_credentials(name: str, host: str, user: str, pwd: str, banner: bool):
    if not name:
        return False

    exists = secret_path.exists()

    credentials = dict()

    if exists:
        try:
            credentials = PublicVars().credentials
        except JSONDecodeError:
            print("Invalid JSON!")

    credentials[name] = {
        "host": host,
        "username": user,
        "password": pwd,
        "banner": banner,
    }

    PublicVars().credentials = credentials

    return True
