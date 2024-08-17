import customtkinter as ctk

from MQTT import mqttC
from utils import colors, fonts

telemetry = "abcd"


def dash(self):
    """Dashboard widget"""
    self.clear_frame()
    # ctk.CTkLabel...
    telemetryBox = ctk.CTkLabel(
        self.frame,
        text=telemetry,
    )
    telemetryBox.place(x=100, y=100)
    print(telemetry)
    return telemetryBox


#  self.frame   ----> statement widget


# def update_telemetryBox(telemetry, msg):
#     new = f"\n{msg.topic}: {msg.payload.decode()}"
#     telemetry += new
#
#
# def on_message(client, userdata, msg):
#     print(f"Received message on {msg.topic}: {msg.payload.decode()}")
#     # previous = self.telemetryBox.get()
#     # new = f"{msg.topic}: {msg.payload.decode()}"
#     # self.telemetryBox.configure(text=f"{previous}\n{new}")
#     update_telemetryBox(telemetry, msg)
#
#
# mqttC.on_message = on_message


def mqtt_setup(self):
    """MQTT Setup Widget"""
    self.clear_frame()
    ctk.CTkLabel(self.frame, text="Host", font=fonts.label).place(x=20, y=50)
    hostEntry = ctk.CTkEntry(
        self.frame, placeholder_text="Host", font=fonts.entry, width=300
    )
    hostEntry.place(x=20, y=80)

    ctk.CTkLabel(self.frame, text="Port", font=fonts.label).place(x=420, y=50)
    portEntry = ctk.CTkEntry(
        self.frame, placeholder_text="Port", font=fonts.entry, width=200
    )
    portEntry.place(x=420, y=80)

    ctk.CTkLabel(self.frame, text="Username",
                 font=fonts.label).place(x=40, y=250)
    unameEntry = ctk.CTkEntry(
        self.frame, placeholder_text="Username", font=fonts.entry, width=300
    )
    unameEntry.place(x=40, y=280)

    ctk.CTkLabel(self.frame, text="Password",
                 font=fonts.label).place(x=40, y=350)
    pwEntry = ctk.CTkEntry(
        self.frame, placeholder_text="Password", font=fonts.entry, width=300
    )
    pwEntry.place(x=40, y=380)

    # Connect
    def connect_event():
        print(f"Connecting to {hostEntry.get()}:{portEntry.get()}...")
        try:
            result = mqttC.connect(hostEntry.get(), int(portEntry.get()))
            mqttC.loop_start()
            print("Connected")
            success = True
        except Exception:
            print("CONNECTION FAILED!")
            success = False
        color = colors.connected if success else colors.failed
        hostEntry.configure(border_color=color, placeholder_text_color=color)
        portEntry.configure(border_color=color, placeholder_text_color=color)

    ctk.CTkButton(
        self.frame, text="Connect", font=fonts.button, command=connect_event
    ).place(relx=0.32, rely=0.90)


#  self.frame   ----> categories widget


def categories(self):
    """Categories Management Widget"""
    self.clear_frame()
    self.bt_from_frame4 = ctk.CTkButton(
        self.frame, text="categories", command=lambda: print("test cats")
    )
    self.bt_from_frame4.grid(row=0, column=0, padx=20, pady=(10, 0))


#   self.frame ----> GS config
def radio_config(self):
    """Ground Station Configuration Widget"""
    print("GS Config")
    self.clear_frame()

    # Frame Title
    ctk.CTkLabel(self.frame, text="Radio Config", font=fonts.header).pack()

    # FREQUENCY
    freqLabel = ctk.CTkLabel(self.frame, text="Frequency", font=fonts.label)
    freqLabel.place(x=10, y=50)

    freqEntry = ctk.CTkEntry(
        self.frame, placeholder_text="Enter frequency", font=fonts.entry
    )
    freqEntry.place(x=150, y=50)

    freqCombo = ctk.CTkComboBox(self.frame, values=["Hz", "MHz"], width=70)
    freqCombo.place(x=300, y=50)

    # BANDWIDTH ==========================================
    bwLabel = ctk.CTkLabel(self.frame, text="Bandwidth", font=fonts.label)
    bwLabel.place(x=10, y=100)
    bwopts = {
        "7.8 kHz": 7800,
        "10.4 kHz": 10400,
        "15.6 kHz": 15600,
        "20.8 kHz": 20800,
        "31.2 kHz": 31250,
        "41.7 kHz": 41700,
        "62.5 kHz": 62500,
        "125 kHz": 125000,
        "250 kHz": 250000,
    }

    bwOption = ctk.CTkOptionMenu(
        self.frame,
        values=list(bwopts.keys()),
    )
    bwOption.place(x=150, y=100)

    # CODE RATE =========================================
    ctk.CTkLabel(self.frame, text="CR", font=fonts.label).place(x=400, y=100)
    cropts = {"4/5": 5, "4/6": 6, "4/7": 7, "4/8": 8}
    crOption = ctk.CTkOptionMenu(self.frame, values=list(cropts.keys()))
    crOption.place(x=450, y=100)

    # PREAMBLE LENGTH ===================================
    ctk.CTkLabel(self.frame, text="Preamble Length", font=fonts.label).place(
        x=10, y=150
    )
    plenEntry = ctk.CTkEntry(
        self.frame, placeholder_text="--", font=fonts.entry, width=80
    )
    plenEntry.place(x=180, y=150)
    ctk.CTkLabel(
        self.frame, text="(3 - 65536)", font=fonts.units, text_color=colors.units
    ).place(x=290, y=150)

    # Spreading Factor ==================================

    def sfCallback(value):
        print("segmented button clicked:", value)

    ctk.CTkLabel(self.frame, text="Spreading Factor", font=fonts.label).place(
        x=10, y=200
    )
    sfSegmented = ctk.CTkSegmentedButton(
        self.frame, values=range(7, 12 + 1), command=sfCallback
    )
    sfSegmented.set(10)
    sfSegmented.place(x=200, y=200)

    # TX POWER ========================================
    ctk.CTkLabel(self.frame, text="Tx Power",
                 font=fonts.label).place(x=10, y=250)

    def slider_event(value):
        txpwrValue.configure(text=f"{int(value)} dBm")
        print(value)

    txpwrSlider = ctk.CTkSlider(
        self.frame, from_=5, to=23, number_of_steps=18, command=slider_event
    )
    txpwrSlider.place(x=200, y=250)
    txpwrValue = ctk.CTkLabel(
        self.frame, text="-- dBm", font=fonts.units, text_color=colors.units
    )
    txpwrValue.place(x=410, y=250)

    # LNA GAIN ========================================
    ctk.CTkLabel(self.frame, text="LNA Gain",
                 font=fonts.label).place(x=10, y=300)

    def lna_slider_event(value):
        lnaValue.configure(text=f"Lvl {int(value)}")
        print(value)

    lnaSlider = ctk.CTkSlider(
        self.frame, from_=1, to=6, number_of_steps=5, command=lna_slider_event
    )
    lnaSlider.place(x=200, y=300)
    lnaValue = ctk.CTkLabel(
        self.frame, text="Lvl --", font=fonts.units, text_color=colors.units
    )
    lnaValue.place(x=410, y=300)

    # ACKNOWLEDGE =====================================
    ctk.CTkLabel(self.frame, text="ACK Delay",
                 font=fonts.label).place(x=20, y=350)
    ackdelayEntry = ctk.CTkEntry(
        self.frame, placeholder_text="ACK Delay", font=fonts.entry, width=100
    )
    ackdelayEntry.place(x=20, y=380)
    ctk.CTkLabel(self.frame, text="s", font=fonts.units, text_color=colors.units).place(
        x=125, y=380
    )

    ctk.CTkLabel(self.frame, text="ACK Wait",
                 font=fonts.label).place(x=220, y=350)
    ackwaitEntry = ctk.CTkEntry(
        self.frame, placeholder_text="ACK Wait", font=fonts.entry, width=100
    )
    ackwaitEntry.place(x=220, y=380)
    ctk.CTkLabel(self.frame, text="s", font=fonts.units, text_color=colors.units).place(
        x=325, y=380
    )

    ctk.CTkLabel(self.frame, text="Rx Timeout",
                 font=fonts.label).place(x=420, y=350)
    rxtoEntry = ctk.CTkEntry(
        self.frame, placeholder_text="Rx Timeout", font=fonts.entry, width=100
    )
    rxtoEntry.place(x=420, y=380)
    ctk.CTkLabel(self.frame, text="s", font=fonts.units, text_color=colors.units).place(
        x=525, y=380
    )

    # CHECKSUM ========================================

    def chksumEvent():
        print("CHEKSUM: ", has_chksum.get())

    ctk.CTkLabel(self.frame, text="Checksum",
                 font=fonts.label).place(x=10, y=600)
    has_chksum = ctk.StringVar(value=True)
    chksumSwitch = ctk.CTkSwitch(
        self.frame,
        text="",
        command=chksumEvent,
        variable=has_chksum,
        onvalue=True,
        offvalue=False,
    )
    chksumSwitch.place(x=150, y=600)

    # SUBMIT
    def button_event():
        value, unit = (float(freqEntry.get()), freqCombo.get())
        freqval = int(value * 1e6 if unit == "MHz" else value)
        print(value, unit, " -> ", freqval)
        mqttC.publish("radio/freq", str(freqval))

        value = bwopts[bwOption.get()]
        print(value)
        mqttC.publish("radio/bw", str(value))

    button = ctk.CTkButton(
        self.frame, text="Submit", font=fonts.button, command=button_event
    )
    button.place(relx=0.32, rely=0.90)


# ===================================================
# Change scaling of all widget 80% to 120%
def change_scaling_event(new_scaling):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    ctk.set_widget_scaling(new_scaling_float)


def view(self):
    """edit UI"""
    self.clear_frame()
    self.scaling_label = ctk.CTkLabel(
        self.frame, text="UI Scaling:", anchor="w")
    self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

    self.scaling_optionemenu = ctk.CTkOptionMenu(
        self.frame,
        values=["80%", "90%", "100%", "110%", "120%"],
        command=change_scaling_event,
    )
    self.scaling_optionemenu.grid(
        row=8, column=0, padx=20, pady=(10, 20), sticky="s")
    # TODO: Change theme
