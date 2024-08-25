import tkinter as tk

import customtkinter as ctk
from utils import colors, fonts


def rot_config_create(app):

    def update(data):
        # Clear the listbox
        app.my_list.delete(0, "end")

        # Add modelopts to listbox
        for item in data:
            app.my_list.insert("end", item)

    # Update entry box with listbox clicked
    def fillout(e):
        # Delete whatever is in the entry box
        app.my_entry.delete(0, "end")

        # Add clicked list item to entry box
        selected = app.my_list.get("anchor")
        app.my_entry.insert(0, "  ".join(selected.split()))
        app.modelselectLabel.grid(row=3, column=1, padx=30, sticky="E")
        print("Selected: ", selected)
        if selected:
            app.values.rotmodel = selected.split()[0]
            print("Rotator model: ", app.values.rotmodel)

    # Create function to check entry vs listbox
    def check(e):
        # grab what was typed
        typed = app.my_entry.get()
        app.modelselectLabel.grid_forget()
        if typed == "":
            data = modelopts
        else:
            data = []
            for item in modelopts:
                if typed.lower() in item.lower():
                    data.append(item)

        # update our listbox with selected items
        update(data)

    # Frame Title
    app.rotTitle = ctk.CTkLabel(
        app.frame,
        text="Rotator Config",
        font=fonts.header,
    )

    # Create a label
    app.rotmodelLabel = ctk.CTkLabel(
        app.frame,
        text="Rotator Model",
        font=fonts.label,
    )

    # Create an entry box
    app.my_entry = ctk.CTkEntry(
        app.frame,
        font=fonts.entry,
        width=500,
    )

    app.modelselectLabel = ctk.CTkLabel(
        app.frame,
        text="✔️",
        text_color="green",
        font=fonts.label,
    )

    # Create a listbox
    app.my_list = tk.Listbox(
        app.frame,
        width=70,
        bg=colors.bg,
        fg="#ffffff",
        highlightcolor="#666666",
        font=fonts.listbox,
        # selectbackground="#aaaaaa",
    )

    modelopts = open("hamlib-rotators.txt", "r").read().splitlines()
    # Add the modelopts to our list
    update(modelopts)

    # Create a binding on the listbox onclick
    app.my_list.bind("<<ListboxSelect>>", fillout)

    # Create a binding on the entry box
    app.my_entry.bind("<KeyRelease>", check)

    app.rothostLabel = ctk.CTkLabel(
        app.frame,
        text="Host",
        font=fonts.label,
    )
    app.rothostEntry = ctk.CTkEntry(
        app.frame,
        width=300,
    )
    app.rothostEntry.insert(0, app.values.rothost)
    app.colon = ctk.CTkLabel(
        app.frame,
        text=":",
        font=fonts.label,
    )
    app.rotportLabel = ctk.CTkLabel(
        app.frame,
        text="Port",
        font=fonts.label,
    )
    app.rotportEntry = ctk.CTkEntry(
        app.frame,
        width=100,
    )
    app.rotportEntry.insert(0, app.values.rotport)

    app.rotdevLabel = ctk.CTkLabel(
        app.frame,
        text="Device",
        font=fonts.label,
    )
    app.rotdevEntry = ctk.CTkEntry(
        app.frame,
        width=200,
    )
    app.rotdevEntry.insert(0, app.values.rotdevice)

    app.rotbaudLabel = ctk.CTkLabel(
        app.frame,
        text="Serial speed/baudrate",
        font=fonts.label,
    )
    app.rotbaudEntry = ctk.CTkEntry(
        app.frame,
        width=100,
    )
    app.rotbaudEntry.insert(0, app.values.sspeed)

    def model_index(rots, num):
        for i, rot in enumerate(rots):
            if rot.split()[0] == num:
                return i
        return 0

    index = model_index(modelopts, app.values.rotmodel)
    app.my_list.selection_set(index)
    app.my_list.yview_scroll(index - 3, "units")


def rot_config(app):
    app.clear_frame()
    app.rotTitle.grid(row=0, column=0, columnspan=5, pady=(20, 40))
    app.rotmodelLabel.grid(row=2, column=0, padx=80, pady=(50, 5), sticky='w')
    app.my_entry.grid(row=3, column=0, padx=40, columnspan=3)
    app.my_list.grid(row=4, column=0, padx=40, pady=5, columnspan=3)
    app.rothostLabel.grid(row=6, column=0, padx=50, pady=(40, 5), sticky="W")
    app.rothostEntry.grid(row=7, column=0, padx=(50, 40), sticky="W")
    app.colon.grid(row=7, column=0, padx=10, sticky="E")
    app.rotportLabel.grid(row=6, column=1, padx=10, pady=(40, 5), sticky="W")
    app.rotportEntry.grid(row=7, column=1, padx=10, sticky="W")
    app.rotdevLabel.grid(row=8, column=0, padx=50, pady=(40, 5), sticky="W")
    app.rotdevEntry.grid(row=9, column=0, padx=50, sticky="W")
    app.rotbaudLabel.grid(row=8, column=1, padx=10, pady=(40, 5), sticky="W")
    app.rotbaudEntry.grid(row=9, column=1, padx=10, sticky="W")
