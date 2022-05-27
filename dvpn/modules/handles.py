import json
import tkinter.messagebox
from json import JSONDecodeError
from tkinter import StringVar, BooleanVar

from dvpn.config.constants import PublicVars
from dvpn.config.paths import secret_path


def add_credentials(cli_path: str, name: str, host: str, user: str, pwd: str,
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
        "cli_path": cli_path,
        "host": host,
        "username": user,
        "password": pwd,
        "banner": banner,
    }

    try:
        PublicVars().credentials = credentials
    except PermissionError:
        failed_text = f"Failed to save due to permission error {str(secret_path)}"
        print(failed_text)
        tkinter.messagebox.showinfo("Fail", failed_text)
        return False

    success_text = "Saved Successfully"
    print(success_text)
    tkinter.messagebox.showinfo("Success", success_text)
    return True


def load_credentials(name: str, cli_path: StringVar, host: StringVar, user: StringVar,
                     pwd: StringVar,
                     banner: BooleanVar):
    if not name:
        tkinter.messagebox.showwarning("Missing params", "Please enter Name of the VPN to load")
        return False

    exists = secret_path.exists()
    credentials = None

    if exists:
        try:
            credentials = PublicVars().credentials.get(name, None)
        except JSONDecodeError:
            invalid_text = "Invalid JSON!"
            print(invalid_text)
            tkinter.messagebox.showwarning("Invalid save", invalid_text)
            return False
        except PermissionError:
            permission_error_text = f"Failed to load due to permission error {str(secret_path)}"
            print(permission_error_text)
            tkinter.messagebox.showwarning("Permission error", permission_error_text)
            return False

    if credentials is None:
        tkinter.messagebox.showinfo("No Data", "No saved data found")
        return False

    cli_path.set(credentials.get("cli_path", ""))
    host.set(credentials.get("host", ""))
    user.set(credentials.get("username", ""))
    pwd.set(credentials.get("password", ""))
    banner.set(credentials.get("banner", False))
    print("Loaded Successfully")
    tkinter.messagebox.showinfo("Loaded", "Loaded Data Successfully")
    return True
