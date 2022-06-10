import json
from json import JSONDecodeError
from tkinter import StringVar, BooleanVar

from dvpn.config.constants import PublicVars
from dvpn.config.paths import secret_path


def add_credentials(vpn_type: str, cli_path: str, name: str, host: str, user: str,
                    pwd: str,
                    banner: bool):
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
        "vpn_type": vpn_type,
        "cli_path": cli_path,
        "host": host,
        "username": user,
        "password": pwd,
        "banner": banner,
    }

    try:
        PublicVars().credentials = credentials
    except PermissionError:
        print(f"Failed to save due to permission error {str(secret_path)}")
        return False

    print("Saved Successfully")
    return True


def load_credentials(name: str, vpn_type: StringVar, cli_path: StringVar, host: StringVar,
                     user: StringVar,
                     pwd: StringVar,
                     banner: BooleanVar):
    if not name:
        return False

    exists = secret_path.exists()
    credentials = None

    if exists:
        try:
            credentials = PublicVars().credentials.get(name, None)
        except JSONDecodeError:
            print("Invalid JSON!")
            return False
        except PermissionError:
            print(f"Failed to load due to permission error {str(secret_path)}")
            return False

    if credentials is None:
        return False

    vpn_type.set(credentials.get("vpn_type", ""))
    cli_path.set(credentials.get("cli_path", ""))
    host.set(credentials.get("host", ""))
    user.set(credentials.get("username", ""))
    pwd.set(credentials.get("password", ""))
    banner.set(credentials.get("banner", False))
    print("Saved Successfully")
    return True
