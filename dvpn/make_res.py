import subprocess

subprocess.call(["pyside6-rcc", "main.qrc", "-o", "res.py"])
