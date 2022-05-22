from tkinter import Tk, StringVar, BooleanVar, Label, Entry, Checkbutton, Button, Toplevel

from dvpn.modules.handles import add_credentials


def new_vpn_window(root):
    window = Toplevel(root)
    window.title("Modify or add VPNs")

    name = StringVar()
    host = StringVar()
    user = StringVar()
    pwd = StringVar()
    banner_var = BooleanVar()

    window.geometry(f"300x300+10+20")

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
            name.get(), host.get(), user.get(), pwd.get(), banner_var.get()
        ),
    )

    window.mainloop()


if __name__ == "__main__":
    new_vpn_window()
