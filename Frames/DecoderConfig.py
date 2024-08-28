import json
import subprocess
import tkinter as tk
from os.path import basename, expanduser

import customtkinter as ctk
import yaml

from utils import colors, fonts


def decoders(app):
    app.clear_frame()

    def update(d):
        # Clear the listbox
        data = list(d)
        app.decList.delete(0, "end")

        # Add modelopts to listbox
        for item in data:
            compiled = decoderopts[item]["compiled"]
            compdec = f"({compiled})✔️" if compiled else "---"
            spacing = 20 - len(item)
            line = item + spacing * " " + compdec
            app.decList.insert("end", line)

    # Update entry box with listbox clicked
    def fillout(e):
        # Delete whatever is in the entry box
        app.decEntry.delete(0, "end")

        # Add clicked list item to entry box
        selected = app.decList.get("anchor").split()[0]
        app.decEntry.insert(0, "  ".join(selected.split()))
        app.decoderselectLabel.grid(row=3, column=1, padx=30, sticky="E")
        print("Selected: ", selected, decoderopts[selected])
        if selected:
            app.decoder = selected
        if decoderopts[selected]["compiled"]:
            app.compileButton.configure(state="disabled")
            app.setdecButton.configure(state="normal")
        else:
            app.compileButton.configure(state="normal")
            app.setdecButton.configure(state="disabled")

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

    app.decTitle = ctk.CTkLabel(
        app.frame,
        text="Set Decoder",
        font=fonts.header,
    )
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
        width=40,
        bg=colors.bg,
        fg=colors.listbox_bg,
        highlightcolor=colors.listbox_hl,
        selectbackground=colors.listbox_sel,
        font=fonts.listbox,
    )

    try:
        with open("decoders.json", "r") as df:
            decoderopts = json.load(df)
    except Exception:
        decoderopts = dict()

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
        files = tk.filedialog.askopenfiles(
            mode="r",
            initialdir=expanduser("~"),
            title="Select a file",
            filetypes=[("Decoder Files", "*.ksy"), ("all files", "*.*")],
        )
        for file in files:
            if file is not None:
                # decoderopts.insert(0, basename(file.name))
                decoderopts[basename(file.name)] = {
                    "source": file.name,
                    "compiled": None,
                }
                update(decoderopts)
                #             with open("decoder-list.dat", "a") as dl:
                #                 dl.write(file.name + "\n")
                with open("decoders.json", "w") as df:
                    json.dump(decoderopts, df, indent=4)

    app.addfileButton = ctk.CTkButton(
        app.frame,
        text="+",
        font=fonts.button,
        width=40,
        command=open_file,
    )

    def compile_decoder():
        selected = app.decList.get("anchor").split()[0]
        if not decoderopts[selected]["compiled"]:
            print(f"Compiling {selected}... {decoderopts[selected]['source']}")
            sel_ks = yaml.safe_load(open(decoderopts[selected]["source"], "r"))
            name = sel_ks.get("meta").get("id") + ".py"
            subprocess.run(
                [
                    "kaitai-struct-compiler",
                    "-t",
                    "python",
                    "--outdir",
                    "Decoders",
                    decoderopts[selected]["source"],
                ]
            )
            decoderopts[selected]["compiled"] = name
            update(decoderopts)
            with open("decoders.json", "w") as df:
                json.dump(decoderopts, df, indent=4)

    app.compileButton = ctk.CTkButton(
        app.frame,
        text="Compile",
        font=fonts.button,
        command=compile_decoder,
    )

    def set_decoder():
        print("This is the one!")

    app.setdecButton = ctk.CTkButton(
        app.frame,
        text="Use Decoder",
        font=fonts.button,
        state="disabled",
        command=set_decoder,
    )

    app.decTitle.grid(row=0, column=0, columnspan=4, padx=30, pady=(20, 40))
    app.decLabel.grid(row=2, column=0)
    app.decoderselectLabel.grid(row=2, column=1)
    app.decEntry.grid(row=3, column=0, padx=10)
    app.addfileButton.grid(row=3, column=1, padx=10, sticky="W")
    app.decList.grid(row=4, column=0, padx=(30, 0), sticky="W")
    app.compileButton.grid(row=4, column=1, padx=20, pady=30, sticky="W")
    app.setdecButton.grid(row=5)
