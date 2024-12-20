import tkinter
import yaml
import json
from datetime import datetime

import customtkinter as ctk
from PIL import Image, ImageTk

from defaults import Default
from Frames import (Dashboard, DecoderConfig, MQTTSetup, Preferences,
                    RadioConfig, RotConfig)
from MQTT import mqttC
from utils import colors, fonts

DARK_MODE = "dark"
ctk.set_appearance_mode(DARK_MODE)
ctk.set_default_color_theme("dark-blue")


class App(ctk.CTk):

    def __init__(self):

        pages = {
            "Dashboard": self.dash,
            "MQTT Setup": self.mqtt_setup,
            #             "Data Request": self.categories,
            "Radio Config": self.radio_config,
            "Rotator Config": self.rot_config,
            "Decoders": self.decoders,
            "Preferences": self.preferences,
        }
        super().__init__()

        # values -------------------------------------
        self.values = Default
        self.connected = False

        # --------------------------------------------

        self.title("IST Ground Station")
        self.geometry("1000x1000")

        self.telemetry = "..."
        # root!
        self.main_container = ctk.CTkFrame(self, corner_radius=10)
        self.main_container.pack(
            fill=tkinter.BOTH,
            expand=True,
            padx=10,
            pady=10,
        )

        # left side panel -> for frame selection
        self.left_side_panel = ctk.CTkFrame(
            self.main_container,
            width=150,
            corner_radius=10,
        )
        self.left_side_panel.pack(
            side=tkinter.LEFT,
            fill=tkinter.Y,
            expand=False,
            padx=5,
            pady=5,
        )

        self.left_side_panel.grid_columnconfigure(0, weight=1)
        self.left_side_panel.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=0)
        self.left_side_panel.grid_rowconfigure((7, 8), weight=1)

        # self.left_side_panel WIDGET
        self.logo_label = ctk.CTkLabel(
            self.left_side_panel,
            text="IST \nGround Station \n",
            font=ctk.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.bt_Quit = ctk.CTkButton(
            self.left_side_panel,
            text="Quit",
            fg_color=colors.red,
            hover_color=colors.red_hover,
            command=self.close_window,
        )
        self.bt_Quit.grid(row=9, column=0, padx=20, pady=10)
        # ----------------------------------------------------

        # button to select correct frame IN self.left_side_panel WIDGET

        for i, page in enumerate(pages):
            ctk.CTkButton(
                self.left_side_panel,
                text=page,
                command=pages[page],
                width=200,
                height=30,  # fg_color='#1140e5',
            ).grid(row=i + 1, column=0, padx=20, pady=10)

        self.connectionIndicator = ctk.CTkLabel(
            self.left_side_panel,
            text="MQTT\nNOT Connected\n❌",
            text_color=colors.failed,
            font=fonts.indicator,
        )
        self.connectionIndicator.grid(row=8, column=0, padx=20, pady=10)
        # ----------------------------------------------------

        # right side panel -> have self.frame inside it
        self.right_side_panel = ctk.CTkFrame(
            self.main_container,
            corner_radius=10,
        )
        self.right_side_panel.pack(
            side=tkinter.LEFT,
            fill=tkinter.BOTH,
            expand=True,
            padx=5,
            pady=5,
        )

        self.frame = ctk.CTkFrame(
            self.main_container,
            corner_radius=10,
            #             fg_color=colors.bg,
        )
        self.frame.pack(
            in_=self.right_side_panel,
            side=tkinter.TOP,
            fill=tkinter.BOTH,
            expand=True,
            padx=0,
            pady=0,
        )

        Dashboard.dash_create(self)
        MQTTSetup.mqtt_setup_create(self)
        RadioConfig.radio_config_create(self)
        RotConfig.rot_config_create(self)

        Preferences.preferences_create(self)

        # MQTT setup is the first thing that appears
        MQTTSetup.mqtt_setup(self)

    #     def update_telemetryBox(telemetry, msg):
    #         new = f"\n{msg.topic}: {msg.payload.decode()}"
    #         telemetry += new

    def dash(self):
        Dashboard.dash(self)

    def mqtt_setup(self):
        MQTTSetup.mqtt_setup(self)

    #     def categories(self):
    #         _Frames.categories(self)

    def radio_config(self):
        RadioConfig.radio_config(self)

    def rot_config(self):
        RotConfig.rot_config(self)

    def decoders(self):
        DecoderConfig.decoders(self)

    def preferences(self):
        Preferences.preferences(self)

    # close the entire window

    def close_window(self):
        App.destroy(self)

    # CLEAR ALL THE WIDGET BEFORE loading the widget of the concerned page
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.grid_forget()


a = App()

# a.after(201, lambda: a.iconbitmap('logo.jpeg'))
ico = Image.open("logo.png")
photo = ImageTk.PhotoImage(ico)
a.wm_iconphoto(False, photo)


def just_quit(e):
    a.close_window()


a.bind("<Control-w>", just_quit)


def parse_msg(pkt, indent=4):

    from Decoders import prometheus as decoder

    try:
        msg = decoder.Prometheus.from_bytes(pkt)

        def to_dict(item):

            match item:
                case dict():
                    data = {}
                    for k, v in item.items():
                        data[k] = to_dict(v)
                    return data
                case list() | tuple():
                    return [to_dict(x) for x in item]
                case object(__dict__=_):
                    data = {}
                    for k, v in item.__dict__.items():
                        if not k.startswith("_"):
                            data[k] = to_dict(v)
                    return data
                case _:
                    if isinstance(item, bytes):
                        return item.hex()
                    return item

        msg_dict = to_dict(msg)
        out = json.dumps(msg_dict, indent=indent)
        return out
    except Exception:
        print(Exception)
        return 'Failed to Decode: Wrong Packet Format'


def update_telemetryBox(app, msg):
    packet = msg.payload
    format = '%Y-%m-%d %H:%M:%S'
    timestamp = f"\n\t\t\t==={datetime.now().strftime(format)}===\n"
    new = f"{timestamp}{msg.topic}:\n{packet}\n\n\n"
    app.telemetry += new
    app.msg_panel.raw_box.insert("end", new)
    app.msg_panel.decoded_box.insert("end", f"{timestamp}{parse_msg(packet)}\n\n\n")
    print(parse_msg(packet))
    print(packet[4])
    print(len(packet))


def on_message(client, userdata, msg):
    if msg.topic.endswith('rssi'):
        rssi = round(float(msg.payload.decode()), 2)
        print(f'RSSI: {rssi}')
        a.rssiLabel.configure(text=f'Packet RSSI: {rssi} dBm')
    else:
        message = msg.payload
        print(f"Received message on {msg.topic}: {message}")
        update_telemetryBox(a, msg)


mqttC.on_message = on_message

try:
    a.mainloop()
except Exception:
    pass
