pyinstaller --name "DieVpn" --icon "dvpn/icons/dievpn.ico" --windowed --add-data="./dvpn/res.py:." dvpn/main.py
create-dmg --volname "DieVpn" --volicon "dvpn/icons/dievpn.ico" --window-size 600 300 --icon-size 100 --icon "DieVpn.app" 150 120 --app-drop-link 425 120 --hide-extension "DieVpn.app"  "dist/DieVpn.dmg" "dist/DieVpn.app"