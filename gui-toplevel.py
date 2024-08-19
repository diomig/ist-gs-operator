import tkinter

import customtkinter

import _Frames
from defaults import Default
from MQTT import mqttC
from utils import colors, fonts

DARK_MODE = "dark"
customtkinter.set_appearance_mode(DARK_MODE)
customtkinter.set_default_color_theme("dark-blue")


class App(customtkinter.CTk):

    def __init__(self):

        pages = {
            "Dashboard": self.dash,
            "MQTT Setup": self.mqtt_setup,
            "Data Request": self.categories,
            "Radio Config": self.radio_config,
            "Rotator Config": lambda: print("rot config"),
            "Decoders": lambda: print("Decoders"),
            "View": self.view,
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
        self.main_container = customtkinter.CTkFrame(self, corner_radius=10)
        self.main_container.pack(fill=tkinter.BOTH, expand=True, padx=10, pady=10)

        # left side panel -> for frame selection
        self.left_side_panel = customtkinter.CTkFrame(
            self.main_container, width=150, corner_radius=10
        )
        self.left_side_panel.pack(
            side=tkinter.LEFT, fill=tkinter.Y, expand=False, padx=5, pady=5
        )

        self.left_side_panel.grid_columnconfigure(0, weight=1)
        self.left_side_panel.grid_rowconfigure((0, 1, 2, 3, 4, 5, 6), weight=0)
        self.left_side_panel.grid_rowconfigure((7, 8), weight=1)

        # self.left_side_panel WIDGET
        self.logo_label = customtkinter.CTkLabel(
            self.left_side_panel,
            text="IST \nGround Station \n",
            font=customtkinter.CTkFont(size=20, weight="bold"),
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.bt_Quit = customtkinter.CTkButton(
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
            customtkinter.CTkButton(
                self.left_side_panel,
                text=page,
                command=pages[page],
                width=200,
                height=30,  # fg_color='#1140e5',
            ).grid(row=i + 1, column=0, padx=20, pady=10)

        self.connectionIndicator = customtkinter.CTkLabel(
            self.left_side_panel,
            text="MQTT\nNOT Connected\n❌",
            text_color=colors.failed,
            font=fonts.indicator,
        )
        self.connectionIndicator.grid(row=8, column=0, padx=20, pady=10)
        # ----------------------------------------------------

        # right side panel -> have self.frame inside it
        self.right_side_panel = customtkinter.CTkFrame(
            self.main_container,
            corner_radius=10,
        )
        self.right_side_panel.pack(
            side=tkinter.LEFT, fill=tkinter.BOTH, expand=True, padx=5, pady=5
        )

        self.frame = customtkinter.CTkFrame(
            self.main_container,
            corner_radius=10,  # fg_color=colors.bg
        )
        self.frame.pack(
            in_=self.right_side_panel,
            side=tkinter.TOP,
            fill=tkinter.BOTH,
            expand=True,
            padx=0,
            pady=0,
        )

        _Frames.mqtt_setup_create(self)
        _Frames.radio_config_create(self)

        # MQTT setup is the first thing that appears
        _Frames.mqtt_setup(self)

    def update_telemetryBox(telemetry, msg):
        new = f"\n{msg.topic}: {msg.payload.decode()}"
        telemetry += new

    #     def on_message(client, userdata, msg):
    #         print(f"Received message on {msg.topic}: {msg.payload.decode()}")
    #         # previous = self.telemetryBox.get()
    #         # new = f"{msg.topic}: {msg.payload.decode()}"
    #         # self.telemetryBox.configure(text=f"{previous}\n{new}")
    #         update_telemetryBox(telemetry, msg)

    def dash(self):
        # self.telemetryBox = _Frames.dash(self)
        """Dashboard widget"""
        self.clear_frame()
        # ctk.CTkLabel...
        telemetryBox = customtkinter.CTkLabel(
            self.frame,
            text=self.telemetry,
        )
        telemetryBox.grid()
        print(self.telemetry)

    def mqtt_setup(self):
        _Frames.mqtt_setup(self)

    def categories(self):
        _Frames.categories(self)

    def radio_config(self):
        _Frames.radio_config(self)

    def view(self):
        _Frames.view(self)

    # close the entire window

    def close_window(self):
        App.destroy(self)

    # CLEAR ALL THE WIDGET BEFORE loading the widget of the concerned page
    def clear_frame(self):
        for widget in self.frame.winfo_children():
            # widget.destroy()
            widget.grid_forget()


a = App()


def update_telemetryBox(app, msg):
    new = f"\n{msg.topic}: {msg.payload.decode()}"
    app.telemetry += new


def on_message(client, userdata, msg):
    print(f"Received message on {msg.topic}: {msg.payload.decode()}")
    # previous = self.telemetryBox.get()
    # new = f"{msg.topic}: {msg.payload.decode()}"
    # self.telemetryBox.configure(text=f"{previous}\n{new}")
    update_telemetryBox(a, msg)


mqttC.on_message = on_message

try:
    a.mainloop()
except Exception:
    pass
