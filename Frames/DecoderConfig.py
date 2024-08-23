import tkinter as tk
from os.path import expanduser, basename

import customtkinter as ctk

from utils import colors, fonts


def decoders(app):
    app.clear_frame()

    def update(data):
        # Clear the listbox
        app.decList.delete(0, "end")

        # Add modelopts to listbox
        for item in data:
            app.decList.insert("end", item)

    # Update entry box with listbox clicked
    def fillout(e):
        # Delete whatever is in the entry box
        app.decEntry.delete(0, "end")

        # Add clicked list item to entry box
        selected = app.decList.get("anchor")
        app.decEntry.insert(0, "  ".join(selected.split()))
        app.decoderselectLabel.grid(row=3, column=1, padx=30, sticky="E")
        print("Selected: ", selected)
        if selected:
            app.decoder = selected
            print("Decoder: ", app.decoder)

    # Create function to check entry vs listbox
    def check(e):
        # grab what was typed
        typed = app.decEntry.get()
        app.decoderselectLabel.grid_forget()
        if typed == "":
            data = decoderopts
        else:
            data = []
            for item in decoderopts:
                if typed.lower() in item.lower():
                    data.append(item)

        # update our listbox with selected items
        update(data)

    # Create a label
    app.decLabel = ctk.CTkLabel(
        app.frame,
        text="Choose a decoder",
        font=fonts.label,
    )

    # Create an entry box
    app.decEntry = ctk.CTkEntry(
        app.frame,
        font=fonts.entry,
        width=500,
    )

    app.decoderselectLabel = ctk.CTkLabel(
        app.frame,
        text="✔️",
        text_color="green",
        font=fonts.label,
    )

    # Create a listbox
    app.decList = tk.Listbox(
        app.frame,
        width=30,
        bg=colors.bg,
        fg="#ffffff",
        highlightcolor="#666666",
        font=fonts.listbox,
        # selectbackground="#aaaaaa",
    )

    decoderopts = [
        "decoder1",
        "decoder2",
        "decoder3",
        "another one",
        "last entry",
        "SIKE, this one is the last tho",
    ]
    # Add the modelopts to our list
    update(decoderopts)

    # Create a binding on the listbox onclick
    app.decList.bind("<<ListboxSelect>>", fillout)

    # Create a binding on the entry box
    app.decEntry.bind("<KeyRelease>", check)

    # Hide hidden directy (the ones starting w/ a '.')
    try:
        try:
            app.tk.call("tk_getOpenFile", "-foobarbaz")
        except tk.TclError:
            pass
        # now set the magic variables accordingly
        app.tk.call("set", "::tk::dialog::file::showHiddenBtn", "1")
        app.tk.call("set", "::tk::dialog::file::showHiddenVar", "0")
    except Exception:
        pass

    def open_file():
        file = tk.filedialog.askopenfile(
            mode="r",
            initialdir=expanduser("~"),
            title="Select a file",
            filetypes=[("Decoder Files", "*.ksy"), ("all files", "*.*")],
        )
        if file is not None:
            decoderopts.insert(0, basename(file.name) + '\033[92m ~~ \033[00m')
            update(decoderopts)

    app.addfileButton = ctk.CTkButton(
        app.frame,
        text="+",
        font=fonts.button,
        width=40,
        command=open_file,
    )

    app.decLabel.grid(row=2, column=0)
    app.decoderselectLabel.grid(row=2, column=1)
    app.decEntry.grid(row=3, column=0)
    app.addfileButton.grid(row=3, column=1)
    app.decList.grid(row=4, column=0, padx=30, sticky='W')
