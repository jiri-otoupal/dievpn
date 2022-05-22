# DieVPN

### Tool that allows to switch between VPNs in ease and speed

[![image](https://img.shields.io/pypi/v/dvpn.svg)](https://pypi.org/project/dvpn/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dvpn)](https://pypi.org/project/dvpn/)
[![Downloads](https://pepy.tech/badge/dvpn)](https://pepy.tech/project/dvpn)
### Supported

#### VPNs

* `AnyConnectVPN` - Cisco

#### OS

* MacOS
* Linux (Debian, Ubuntu, ...)
* Windows

#### Python

* 3.7+

## Installing

Install and update using [pip](https://pip.pypa.io/en/stable/quickstart/):

```bash
pip install dvpn

or

pip3 install dvpn
```

## How to set up with GUI

* Use `dvpn gui` in terminal to add your VPNs, passwords and usernames are stored in plaintext so be sure to have disk
  encrypted.
* If it seems applications is freezing, it is just side effect of compatibility solution on OSX and not using threaded
  connection/disconnection currently **#TODO** just wait it will finish
* **Please be patient and don't click multiple times on buttons in same time**

## How to set up with CLI

* Copy `template_secret.json` to `package/config/secret.json`
* Edit secret accordingly to json format and your credentials
* **Now you can use cli commands**
* _Future Release will contain auto vpn resolve `dvpn autoresolve`_

## How to set up Manually

* Clone repository with `git clone https://github.com/jiri-otoupal/dievpn.git`
* Install requirements with `pip install -r requirements.txt` 
_(ignore / delete windows requirements pywin32 & wexpect if
  your pip is trying to install them)_
* Copy `template_secret.json` to `package/config/secret.json`
* **Edit secret accordingly to json format and your credentials**

## Usage

All commands need to be launched in os terminal not in Pycharm terminal

Access all functions through gui
```
dvpn gui
```

or CLI 

Connect to VPN specified in `config/secret.json`

```
dvpn connect {name_in_credentials}
```

Disconnect from any currently connected VPN

```
dvpn disconnect
```
