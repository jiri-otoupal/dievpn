import os
import subprocess

from secret import password

vpn_cli_dir_path = r"C:\\Program Files (x86)\\Cisco\\Cisco AnyConnect Secure Mobility Client\\"

vpn_cli_file_path = f"{vpn_cli_dir_path}\\vpncli{'.exe' if os.name == 'nt' else ''}"


# Press the green button in the gutter to run the script.

class VpnCli:

    def __init__(self, cli_path):
        self.process_pipe = None
        self.cli_path = cli_path

    def connect(self, host, username, password):
        self.process_pipe = subprocess.Popen([self.cli_path, "connect", f'{host}'], stdin=subprocess.PIPE,
                                             stdout=subprocess.PIPE, shell=True)
        while b"Use of" not in (read := self.process_pipe.stdout.readline()):
            if read:
                print(read)
        print(read)
        print("Inputting")
        print(self.process_pipe.communicate(str.encode(username + "\n")))
        print(self.process_pipe.communicate(str.encode(password + "\n")))

        #print(self.process_pipe.stdout.readlines())


if __name__ == '__main__':
    oracleVpn = VpnCli(vpn_cli_file_path)

    oracleVpn.connect("Oracle VPN", "jotoupal_cz", password)
