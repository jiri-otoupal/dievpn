import os
from pathlib import Path
from tkinter import (
    Tk,
    StringVar,
    BooleanVar,
    Label,
    Entry,
    Checkbutton,
    Button,
    Toplevel,
    Frame,
    RIGHT,
    LEFT, Menu, TOP,
)

from dvpn.config.constants import default_title, PublicVars
from dvpn.config.paths import vpn_cli_file_path_osx, vpn_cli_file_path_win
from dvpn.modules.commands import select_file
from dvpn.modules.handles import add_credentials
from dvpn.modules.threaded_funcs import connect_threaded, disconnect_threaded
from dvpn.modules.tools import buttons, reopen


def new_vpn_window(root):
    window = Toplevel(root)
    window.title("Modify or add VPNs")

    file_name = StringVar()
    file_name.set(
        str(vpn_cli_file_path_win) if os.name == "nt" else str(vpn_cli_file_path_osx)
    )

    file_frame = Frame(window)
    name = StringVar()
    host = StringVar()
    user = StringVar()
    pwd = StringVar()
    banner_var = BooleanVar()

    window.geometry(f"300x300+10+20")

    file_path = Entry(file_frame, textvariable=file_name)
    fp_btn = Button(
        file_frame,
        text="Open",
        command=lambda file_tmp=str(Path(file_name.get()).parent): select_file(
            file_name,
            file_tmp,
        ),
    )
    lbl_clipath = Label(file_frame, text="VPN Cli Path")
    lbl_name = Label(window, text="Name")
    text_name = Entry(window, textvariable=name)
    lbl_host = Label(window, text="Host")
    text_host = Entry(window, textvariable=host)
    lbl_user = Label(window, text="Username")
    text_user = Entry(window, textvariable=user)
    lbl_pwd = Label(window, text="Password")
    text_pwd = Entry(window, textvariable=pwd)
    banner = Checkbutton(window, text="Has Banner", variable=banner_var)

    submit_btn = Button(window, text="Apply", foreground="white", bg="gray")

    lbl_clipath.pack(side=LEFT)
    file_path.pack(expand=True, fill="x", side=LEFT)
    fp_btn.pack(side=RIGHT)
    file_frame.pack(expand=True, fill="x")
    lbl_name.pack()
    text_name.pack(expand=True)
    lbl_host.pack()
    text_host.pack(expand=True)
    lbl_user.pack()
    text_user.pack(expand=True)
    lbl_pwd.pack()
    text_pwd.pack(expand=True)
    banner.pack(expand=True)
    submit_btn.pack(expand=True, fill="x")

    submit_btn.bind(
        "<Button-1>",
        lambda event: add_credentials(
            file_name.get(),
            name.get(),
            host.get(),
            user.get(),
            pwd.get(),
            banner_var.get(),
        ),
    )

    window.mainloop()


def open_gui():
    print("Make sure to kill all VPN clients before usage, as cli would collide with it")
    window = Tk()
    # add widgets here

    menu = Frame(window)
    menu.pack(fill="x", side=TOP)

    add_btn = Button(menu, text="Add VPN", command=lambda: new_vpn_window(window),
                     fg="black",
                     bg="lightgray", border=0)
    refresh_btn = Button(menu, text="Refresh", command=lambda: reopen(window),
                         fg="black", bg="lightgray", border=0)

    add_btn.pack(side=LEFT)
    refresh_btn.pack(side=LEFT)

    window.title(default_title)
    keys = PublicVars().credentials.keys()
    window.geometry(f"300x{(len(keys) + 2) * 30}+10+20")
    for vpn_connection in keys:
        btn = Button(text=vpn_connection.capitalize(), bg="gray", fg="black")
        btn.bind('<Button-1>',
                 lambda event, con=vpn_connection, tbtn=btn: connect_threaded(window, con,
                                                                              tbtn))
        buttons.append(btn)
        btn.pack(expand=True, fill="x")
    btn = Button(text="Disconnect", fg="black",
                 command=lambda: disconnect_threaded(window))
    btn.pack(expand=True, fill="x", pady=5)
    buttons.append(btn)
    window.mainloop()
