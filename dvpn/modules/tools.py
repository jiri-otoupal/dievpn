buttons = []


def state_btns(state_out):
    for btn in buttons:
        btn.config(state=state_out)


def clear_btns():
    for btn in buttons[:-1]:
        btn.config(bg="darkgray", fg="white")



