import os
from pathlib import Path

secret_path = Path(__file__).resolve().parent.parent / "config" / "secret.json"

vpn_cli_file_path_win = Path("C:\\") / \
                        "Program Files (x86)\\" / "Cisco\\" / \
                        "Cisco AnyConnect Secure Mobility Client\\vpncli.exe"

vpn_cli_file_path_osx = Path("/opt/cisco/anyconnect/bin/vpn")
