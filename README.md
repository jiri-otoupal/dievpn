# DieVPN

### This tool Allows you to switch between VPNs in ease and speed

### Supported

* `AnyConnectVPN` - Cisco

## How to setup

* Install requirements with pip install -r requirements.txt
* Edit `config/template_secret.json` with your credentials, passwords are plaintext
* Rename `config/template_secret.json` to secret.py

## Usage
All commands need to be launched in os terminal not in Pycharm terminal

Connect to VPN specified in `config/secret.json`

```
dvpn connect name_in_credentials
```

Disconnect from any currently connected VPN
```
dvpn disconnect
```
