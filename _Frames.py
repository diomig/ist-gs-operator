import tkinter as tk

import customtkinter as ctk

from defaults import Default as df
from MQTT import Topics, mqttC
from utils import colors, fonts

telemetry = "abcd"


def to_float(val):
    try:
        return float(val)
    except ValueError:
        #         print("Not a float")
        return -1


def to_int(val):
    return int(val) if val.isdigit() else -1


def dash(self):
    """Dashboard widget"""
    self.clear_frame()
    # ctk.CTkLabel...
    telemetryBox = ctk.CTkLabel(
        self.frame,
        text=telemetry,
    )
    telemetryBox.place(x=100, y=100)
    #     print(telemetry)
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
        self.frame,
        placeholder_text=(
            "Host" if not self.values.host else self.values.host),
        font=fonts.entry,
        width=300,
    )
    hostEntry.place(x=20, y=80)

    ctk.CTkLabel(self.frame, text="Port", font=fonts.label).place(x=420, y=50)
    portEntry = ctk.CTkEntry(
        self.frame,
        placeholder_text=(
            "Port" if not self.values.port else self.values.port),
        font=fonts.entry,
        width=200,
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
        self.connectionIndicator.configure(
            text='MQTT\nConnected\n✔️',
            text_color=colors.connected
        )
        self.values.host = hostEntry.get()
        self.values.port = portEntry.get()
        self.values.usr = unameEntry.get()
        self.values.pw = pwEntry.get()
        if success:
            self.connected = True
            connectButton.pack_forget()
            #             disconnectButton.place(relx=0.7, rely=0.9)
            disconnectButton.pack(side=tk.BOTTOM, padx=50, pady=20)

    connectButton = ctk.CTkButton(
        self.frame, text="Connect", font=fonts.button, command=connect_event
    )

    def disconnect_event():
        print("time to go...")
        mqttC.loop_stop()
        mqttC.disconnect()
        self.connected = False
        hostEntry.configure(border_color=colors.border)
        portEntry.configure(border_color=colors.border)
        self.connectionIndicator.configure(
            text='MQTT\nNOT Connected\n❌',
            text_color=colors.failed
        )
        disconnectButton.pack_forget()
        #         connectButton.place(relx=0.32, rely=0.9)
        connectButton.pack(side=tk.BOTTOM, padx=10, pady=20)

    disconnectButton = ctk.CTkButton(
        self.frame,
        text="Disconnect",
        font=fonts.button,
        command=disconnect_event,
        fg_color=colors.disconnect,
        hover_color=colors.disconnect_hover,
    )
    if not self.connected:
        connectButton.pack(side=tk.BOTTOM, padx=10, pady=20)
    else:
        disconnectButton.pack(side=tk.BOTTOM, padx=10, pady=20)


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
    self.clear_frame()

    # Frame Title
    ctk.CTkLabel(self.frame, text="Radio Config", font=fonts.header).pack()

    # FREQUENCY ===================================
    freqLabel = ctk.CTkLabel(self.frame, text="Frequency", font=fonts.label)
    freqLabel.place(x=10, y=50)

    def set_freq(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        freqEntry.configure(border_color=color)
        self.values.freq = val
        print(f"Frequency {self.values.freq} Hz")
        unit = 1e6 if self.values.freq_unit == "MHz" else 1
        f = self.values.freq * unit
        if f >= 240e6 and f <= 960e6:
            mqttC.publish(Topics.freq, f)
            color = colors.units
        else:
            color = colors.failed
        freqRange.configure(text_color=color)

    freqSV = tk.StringVar()
    freqSV.trace("w", lambda name, index, mode, sv=freqSV: set_freq(freqSV))
    freqEntry = ctk.CTkEntry(self.frame, font=fonts.entry, textvariable=freqSV)
    freqEntry.place(x=150, y=50)
    freqEntry.insert(0, self.values.freq)
    freqEntry.bind(command=set_freq)

    def set_freq_unit(option):
        self.values.freq_unit = option
        unit = 1e6 if self.values.freq_unit == "MHz" else 1
        f = self.values.freq * unit
        if f >= 240e6 and f <= 960e6:
            mqttC.publish(Topics.freq, f)
            color = colors.units
        else:
            color = colors.failed
        freqRange.configure(text_color=color)

    freqCombo = ctk.CTkComboBox(
        self.frame, values=["Hz", "MHz"], width=70, command=set_freq_unit
    )
    freqCombo.set(self.values.freq_unit)
    freqCombo.place(x=300, y=50)
    freqRange = ctk.CTkLabel(
        self.frame,
        text="[240.0 - 960.0] MHz",
        font=fonts.units,
        text_color=colors.units,
    )
    freqRange.place(x=380, y=50)

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

    def set_bw(option):
        self.values.bw = bwopts[option]
        mqttC.publish(Topics.bw, self.values.bw)

    bwOption = ctk.CTkOptionMenu(
        self.frame, values=list(bwopts.keys()), command=set_bw)
    bwOption.set(list(bwopts)[list(bwopts.values()).index(self.values.bw)])
    bwOption.place(x=150, y=100)

    # CODE RATE =========================================
    ctk.CTkLabel(self.frame, text="CR", font=fonts.label).place(x=400, y=100)
    cropts = {"4/5": 5, "4/6": 6, "4/7": 7, "4/8": 8}

    def set_cr(option):
        self.values.cr = cropts[option]
        mqttC.publish(Topics.cr, self.values.cr)

    crOption = ctk.CTkOptionMenu(
        self.frame, values=list(cropts.keys()), command=set_cr)
    crOption.set(list(cropts)[list(cropts.values()).index(self.values.cr)])
    crOption.place(x=450, y=100)

    # PREAMBLE LENGTH ===================================
    ctk.CTkLabel(self.frame, text="Preamble Length", font=fonts.label).place(
        x=10, y=150
    )

    def set_plen(sv):
        val = to_int(sv.get())
        color = colors.failed if val < 0 else colors.border
        plenEntry.configure(border_color=color)
        if val > 0:
            self.values.plen = val
        print(f"Preamble length {self.values.plen}")
        if self.values.plen >= 3 and self.values.plen <= 65536:
            mqttC.publish(Topics.plen, self.values.plen)
            color = colors.units
        else:
            color = colors.failed
        plenRange.configure(text_color=color)

    plenSV = tk.StringVar()
    plenSV.trace("w", lambda name, index, mode, sv=plenSV: set_plen(plenSV))
    plenEntry = ctk.CTkEntry(
        self.frame, font=fonts.entry, width=80, textvariable=plenSV
    )
    plenEntry.insert(0, self.values.plen)
    plenEntry.place(x=180, y=150)
    plenRange = ctk.CTkLabel(
        self.frame, text="(3 - 65536)", font=fonts.units, text_color=colors.units
    )
    plenRange.place(x=290, y=150)

    # Spreading Factor ==================================

    def sfCallback(value):
        self.values.sf = value
        mqttC.publish(Topics.sf, self.values.sf)

    ctk.CTkLabel(self.frame, text="Spreading Factor", font=fonts.label).place(
        x=10, y=200
    )
    sfSegmented = ctk.CTkSegmentedButton(
        self.frame, values=range(7, 12 + 1), command=sfCallback
    )
    sfSegmented.set(self.values.sf)
    sfSegmented.place(x=200, y=200)

    # TX POWER ========================================
    ctk.CTkLabel(self.frame, text="Tx Power",
                 font=fonts.label).place(x=10, y=250)

    def slider_event(value):
        txpwrValue.configure(text=f"{int(value)} dBm")
        if value != self.values.tx_power:
            self.values.tx_power = value
            mqttC.publish(Topics.txpwr, self.values.tx_power)

    txpwrSlider = ctk.CTkSlider(
        self.frame, from_=5, to=23, number_of_steps=18, command=slider_event
    )
    txpwrSlider.place(x=200, y=250)
    txpwrValue = ctk.CTkLabel(
        self.frame,
        text=f"{self.values.tx_power} dBm",
        font=fonts.units,
        text_color=colors.units,
    )
    txpwrSlider.set(self.values.tx_power)
    txpwrValue.place(x=410, y=250)

    # LNA GAIN ========================================
    ctk.CTkLabel(self.frame, text="LNA Gain",
                 font=fonts.label).place(x=10, y=300)

    def lna_slider_event(value):
        lnaValue.configure(text=f"Lvl {int(value)}")
        if value != self.values.lna_gain:
            self.values.lna_gain = value
            mqttC.publish(Topics.lnag, self.values.lna_gain)

    lnaSlider = ctk.CTkSlider(
        self.frame, from_=1, to=6, number_of_steps=5, command=lna_slider_event
    )
    lnaSlider.place(x=200, y=300)
    lnaValue = ctk.CTkLabel(
        self.frame,
        text=f"Lvl {self.values.lna_gain}",
        font=fonts.units,
        text_color=colors.units,
    )
    lnaSlider.set(self.values.lna_gain)
    lnaValue.place(x=410, y=300)

    # ACKNOWLEDGE =====================================
    ctk.CTkLabel(self.frame, text="ACK Delay",
                 font=fonts.label).place(x=20, y=350)

    def set_ackdelay(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        ackdelayEntry.configure(border_color=color)
        self.values.ack_delay = val
        # TODO: verify boundaries
        print(f"ACK delay {self.values.ack_delay}")
        mqttC.publish(Topics.ackdelay, self.values.ack_delay)

    ackdSV = tk.StringVar()
    ackdSV.trace("w", lambda name, index, mode,
                 sv=ackdSV: set_ackdelay(ackdSV))
    ackdelayEntry = ctk.CTkEntry(
        self.frame, font=fonts.entry, width=100, textvariable=ackdSV
    )
    ackdelayEntry.insert(0, self.values.ack_delay)
    ackdelayEntry.place(x=20, y=380)
    ctk.CTkLabel(self.frame, text="s", font=fonts.units, text_color=colors.units).place(
        x=125, y=380
    )

    ctk.CTkLabel(self.frame, text="ACK Wait",
                 font=fonts.label).place(x=220, y=350)

    def set_ackwait(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        ackwaitEntry.configure(border_color=color)
        self.values.ack_wait = val
        # TODO: verify boundaries
        print(f"ACK wait {self.values.ack_wait}")
        mqttC.publish(Topics.ackwait, self.values.ack_wait)

    ackwSV = tk.StringVar()
    ackwSV.trace("w", lambda name, index, mode, sv=ackwSV: set_ackwait(ackwSV))
    ackwaitEntry = ctk.CTkEntry(
        self.frame, font=fonts.entry, width=100, textvariable=ackwSV
    )
    ackwaitEntry.insert(0, self.values.ack_wait)
    ackwaitEntry.place(x=220, y=380)
    ctk.CTkLabel(self.frame, text="s", font=fonts.units, text_color=colors.units).place(
        x=325, y=380
    )
    # RX TIMEOUT ======================================
    ctk.CTkLabel(self.frame, text="Rx Timeout",
                 font=fonts.label).place(x=420, y=350)

    def set_rxtimeout(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        rxtoEntry.configure(border_color=color)
        if val > 0:
            self.values.rx_timeout = val
        # TODO: verify boundaries
        print(f"Rx timeout {self.values.rx_timeout}")
        mqttC.publish(Topics.rxto, self.values.rx_timeout)

    rxtoSV = tk.StringVar()
    rxtoSV.trace("w", lambda name, index, mode,
                 sv=rxtoSV: set_rxtimeout(rxtoSV))
    rxtoEntry = ctk.CTkEntry(
        self.frame, font=fonts.entry, width=100, textvariable=rxtoSV
    )
    rxtoEntry.insert(0, self.values.rx_timeout)
    rxtoEntry.place(x=420, y=380)
    ctk.CTkLabel(self.frame, text="s", font=fonts.units, text_color=colors.units).place(
        x=525, y=380
    )

    # CHECKSUM ========================================

    def chksumEvent():
        self.values.chksum = has_chksum.get()
        mqttC.publish(Topics.chksum, self.values.chksum)

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
    chksumSwitch.select() if self.values.chksum else chksumSwitch.deselect()
    chksumSwitch.place(x=150, y=600)

    # SUBMIT
    def button_event():
        value, unit = (float(freqEntry.get()), freqCombo.get())
        freqval = int(value * 1e6 if unit == "MHz" else value)
        #         print(value, unit, " -> ", freqval)
        mqttC.publish("radio/freq", str(freqval))

        value = bwopts[bwOption.get()]
        #         print(value)
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
