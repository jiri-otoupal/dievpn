from pathlib import Path

RESOURCE_DIRS = [
    Path(d) for d in ["icons", "qml", "qml/custom", "images", "qml/modals", "js"]
]

with open("main.qrc", "w", encoding="utf-8") as f:

    def fprint(string=""):
        print(string, file=f)

    fprint('<!DOCTYPE RCC><RCC version="1.0">')
    fprint("  <qresource>")

    # main files
    fprint(f"    <!-- Main Interface files -->")
    for res_dir in RESOURCE_DIRS:
        fprint(f"    <!-- {res_dir}/ -->")
        for file in res_dir.iterdir():
            if not file.is_file():
                continue
            fprint(f"    <file>{file}</file>")
        fprint()

    fprint("  </qresource>")
    fprint("</RCC>")
