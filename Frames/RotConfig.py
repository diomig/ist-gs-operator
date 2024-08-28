import json
import tkinter as tk

import customtkinter as ctk

from MQTT import Topics, mqttC
from utils import colors, fonts


def rot_config_create(app):

    def update(data):
        # Clear the listbox
        app.rotmodelList.delete(0, "end")

        # Add modelopts to listbox
        for item in data:
            app.rotmodelList.insert("end", item)

    # Update entry box with listbox clicked
    def fillout(e):
        # Delete whatever is in the entry box
        app.rotmodelEntry.delete(0, "end")

        # Add clicked list item to entry box
        selected = app.rotmodelList.get("anchor")
        app.rotmodelEntry.insert(0, "  ".join(selected.split()))
        if selected:
            print("Selected: ", selected)
            app.values.rotmodel = selected.split()[0]
            print("Rotator model: ", app.values.rotmodel)
            app.rotcheckIcon.grid(row=3, column=2, padx=40, sticky="E")

    # Create function to check entry vs listbox
    def check(e):
        # grab what was typed
        typed = app.rotmodelEntry.get()
        app.rotcheckIcon.grid_forget()
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
    app.rotmodelEntry = ctk.CTkEntry(
        app.frame,
        font=fonts.entry,
        width=500,
    )

    app.rotcheckIcon = ctk.CTkLabel(
        app.frame,
        text="✔️",
        text_color="green",
        font=fonts.label,
    )

    # Create a listbox
    app.rotmodelList = tk.Listbox(
        app.frame,
        width=70,
        bg=colors.bg,
        fg=colors.listbox_bg,
        highlightcolor=colors.listbox_hl,
        selectbackground=colors.listbox_sel,
        font=fonts.listbox,
    )

    modelopts = open("hamlib-rotators.txt", "r").read().splitlines()
    # Add the modelopts to our list
    update(modelopts)

    # Create a binding on the listbox onclick
    app.rotmodelList.bind("<<ListboxSelect>>", fillout)

    # Create a binding on the entry box
    app.rotmodelEntry.bind("<KeyRelease>", check)

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
        text="Serial speed",
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
    app.rotmodelList.selection_set(index)
    app.rotmodelList.yview_scroll(index - 3, "units")

    app.newpresetEntry = ctk.CTkEntry(
        app.frame,
        placeholder_text="Name new preset",
        font=fonts.entry,
    )

    def add_preset():
        name = app.newpresetEntry.get()
        success = False
        if name == "":
            print("Specify name of the preset")
        elif name in presetlist:
            print("Name already in use")
        else:
            success = True
            newpreset = {
                "host": app.values.rothost,
                "port": app.values.rotport,
                "model": app.values.rotmodel,
                "device": app.values.rotdevice,
                "sspeed": app.values.sspeed,
            }
            presetopts["presets"][name] = newpreset
            presetlist.append(name)
            json.dump(presetopts, open("rot_config.json", "w"), indent=4)
            app.presetOption.configure(values=presetlist)
            print(json.dumps({name: newpreset}))
            mqttC.publish(Topics.newpreset, json.dumps({name: newpreset}))
        color = colors.connected if success else colors.failed
        app.newpresetEntry.configure(border_color=color)

    app.newpresetButton = ctk.CTkButton(
        app.frame,
        text="Add\npreset",
        width=50,
        command=add_preset,
    )
    app.presetLabel = ctk.CTkLabel(
        app.frame,
        text="Select a preset",
        font=fonts.label,
    )
    presetopts = json.load(open("rot_config.json", "r"))
    presetlist = ["None"] + list(presetopts.get("presets"))

    def preset_selected(e):
        selected = app.presetOption.get()
        if selected == "None":
            app.deletepresetButton.configure(state="disabled")
            return
        else:
            app.deletepresetButton.configure(state="normal")
        this = presetopts['presets'][selected]
        app.rothostEntry.delete(0, 'end')
        app.rothostEntry.insert(0, this['host'])
        app.rotportEntry.delete(0, 'end')
        app.rotportEntry.insert(0, this['port'])
        app.rotdevEntry.delete(0, 'end')
        app.rotdevEntry.insert(0, this['device'])
        app.rotbaudEntry.delete(0, 'end')
        app.rotbaudEntry.insert(0, this['sspeed'])
        index = model_index(modelopts, this['model'])
#         print(index)
#         app.rotmodelList.selection_clear(0, 'end')
#         app.rotmodelList.selection_set(index)
#         app.rotmodelList.yview_scroll(index, "units")
        app.rotmodelEntry.delete(0, 'end')
        app.rotmodelEntry.insert(0, modelopts[index].split()[-1])
        check(None)
        print(modelopts[index].split()[-1])

    app.presetOption = ctk.CTkOptionMenu(
        app.frame,
        values=presetlist,
        command=preset_selected,
    )

    def delete_preset():
        obj = app.presetOption.get()
        print(f"Deleting {obj}")
        deleted = presetopts["presets"].pop(obj)
        print(deleted)
        print(presetopts)
        json.dump(presetopts, open("rot_config.json", "w"), indent=4)
        app.presetOption.configure(
            values=["None"] + list(presetopts.get("presets")))
        app.presetOption.set("None")

    app.deletepresetButton = ctk.CTkButton(
        app.frame,
        text="Delete",
        fg_color=colors.red,
        hover_color=colors.red_hover,
        command=delete_preset,
        state='disabled',
        width=20,
    )

    def start_rot():
        print(f"Model: {app.values.rotmodel}")
        print(f"Host: {app.values.rothost}")
        print(f"Port: {app.values.rotport}")
        print(f"Device: {app.values.rotdevice}")
        print(f"Serial Baud: {app.values.sspeed}")
        app.values.rotselect = ""
        mqttC.publish(Topics.rotmodel, app.values.rotmodel)
        mqttC.publish(Topics.rothost, app.values.rothost)
        mqttC.publish(Topics.rotport, app.values.rotport)
        mqttC.publish(Topics.rotdevice, app.values.rotdevice)
        mqttC.publish(Topics.rotsspeed, app.values.sspeed)
        mqttC.publish(Topics.rotselect, app.values.rotselect)

    app.rotstartButton = ctk.CTkButton(
        app.frame,
        text="Start Rotator",
        font=fonts.button,
        command=start_rot,
    )


def rot_config(app):
    app.clear_frame()
    app.rotTitle.grid(row=0, column=0, columnspan=5, pady=(20, 40))
    app.rotmodelLabel.grid(row=2, column=0, padx=80, pady=(50, 5), sticky="w")
    app.rotmodelEntry.grid(row=3, column=0, padx=40, columnspan=3)
    app.rotmodelList.grid(row=4, column=0, padx=40, pady=5, columnspan=3)
    app.rothostLabel.grid(row=6, column=0, padx=50, pady=(40, 5), sticky="W")
    app.rothostEntry.grid(row=7, column=0, padx=(50, 40), sticky="W")
    app.colon.grid(row=7, column=0, padx=10, sticky="E")
    app.rotportLabel.grid(row=6, column=1, padx=10, pady=(40, 5), sticky="W")
    app.rotportEntry.grid(row=7, column=1, padx=10, sticky="W")
    app.rotdevLabel.grid(row=8, column=0, padx=50, pady=(40, 5), sticky="W")
    app.rotdevEntry.grid(row=9, column=0, padx=50, sticky="W")
    app.rotbaudLabel.grid(row=8, column=1, padx=10, pady=(40, 5), sticky="W")
    app.rotbaudEntry.grid(row=9, column=1, padx=10, sticky="W")
    app.newpresetEntry.grid(row=10, column=1, pady=(40, 20), sticky="E")
    app.newpresetButton.grid(row=10, column=2, pady=(40, 20), sticky="W")
    app.presetLabel.grid(row=11, column=0, padx=50, pady=10, sticky="W")
    app.presetOption.grid(row=11, column=0, padx=50, sticky="E")
    app.deletepresetButton.grid(row=11, column=1)
    app.rotstartButton.grid(row=12, column=0, columnspan=4, pady=50)

    app.presetOption.set("None")
