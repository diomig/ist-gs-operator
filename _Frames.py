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
    telemetryBox.grid()
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


def mqtt_setup_create(self):
    """MQTT Setup Widget"""
    self.hostLabel = ctk.CTkLabel(self.frame, text="Host", font=fonts.label)

    self.hostEntry = ctk.CTkEntry(
        self.frame,
        placeholder_text=(
            "Host" if not self.values.host else self.values.host),
        font=fonts.entry,
        width=300,
    )

    self.portLabel = ctk.CTkLabel(self.frame, text="Port", font=fonts.label)
    self.portEntry = ctk.CTkEntry(
        self.frame,
        placeholder_text=(
            "Port" if not self.values.port else self.values.port),
        font=fonts.entry,
        width=200,
    )

    self.unameLabel = ctk.CTkLabel(
        self.frame, text="Username", font=fonts.label)
    self.unameEntry = ctk.CTkEntry(
        self.frame, placeholder_text="Username", font=fonts.entry, width=300
    )

    self.pwLabel = ctk.CTkLabel(self.frame, text="Password", font=fonts.label)
    self.pwEntry = ctk.CTkEntry(
        self.frame, placeholder_text="Password", font=fonts.entry, width=300
    )

    # Connect
    def connect_event():
        print(
            f"Connecting to {self.hostEntry.get()}:{self.portEntry.get()}...")
        try:
            result = mqttC.connect(self.hostEntry.get(),
                                   int(self.portEntry.get()))
            mqttC.loop_start()
            print("Connected")
            success = True
        except Exception:
            print("CONNECTION FAILED!")
            success = False
        color = colors.connected if success else colors.failed
        self.hostEntry.configure(
            border_color=color, placeholder_text_color=color)
        self.portEntry.configure(
            border_color=color, placeholder_text_color=color)
        if success:
            self.connectionIndicator.configure(
                text="MQTT\nConnected\n✔️", text_color=colors.connected
            )
        self.values.host = self.hostEntry.get()
        self.values.port = self.portEntry.get()
        self.values.usr = self.unameEntry.get()
        self.values.pw = self.pwEntry.get()
        if success:
            self.connected = True
            self.connectButton.grid_forget()
            self.disconnectButton.grid(row=8, column=0, columnspan=4, pady=100)

    self.connectButton = ctk.CTkButton(
        self.frame, text="Connect", font=fonts.button, command=connect_event
    )

    def disconnect_event():
        print("time to go...")
        mqttC.loop_stop()
        mqttC.disconnect()
        self.connected = False
        self.hostEntry.configure(border_color=colors.border)
        self.portEntry.configure(border_color=colors.border)
        self.connectionIndicator.configure(
            text="MQTT\nNOT Connected\n❌", text_color=colors.failed
        )
        self.disconnectButton.grid_forget()
        self.connectButton.grid(row=8, column=0, columnspan=4, pady=100)

    self.disconnectButton = ctk.CTkButton(
        self.frame,
        text="Disconnect",
        font=fonts.button,
        command=disconnect_event,
        fg_color=colors.disconnect,
        hover_color=colors.disconnect_hover,
    )
    self.mqttTitle = ctk.CTkLabel(self.frame, text='Connect to the MQTT broker', font=fonts.header)

def mqtt_setup(self):
    self.clear_frame()
    self.mqttTitle.grid(row=0, column=0, columnspan=4, pady=100)
    self.hostLabel.grid(row=1, column=0, padx=10, sticky=tk.W)
    self.hostEntry.grid(row=2, column=0, padx=10)
    self.portLabel.grid(row=1, column=1, padx=10, sticky=tk.W)
    self.portEntry.grid(row=2, column=1, padx=10)
    self.unameLabel.grid(row=3, column=0, padx=10, pady=(50, 2), sticky=tk.W)
    self.unameEntry.grid(row=4, column=0, padx=10)
    self.pwLabel.grid(row=5, column=0, padx=10, pady=(20, 2), sticky=tk.W)
    self.pwEntry.grid(row=6, column=0, padx=10)
    if not self.connected:
        self.connectButton.grid(row=8, column=0, columnspan=4, pady=100)
    else:
        self.disconnectButton.grid(row=8, column=0, columnspan=4, pady=100)
#  self.frame   ----> categories widget


def categories(self):
    """Categories Management Widget"""
    self.clear_frame()
    self.bt_from_frame4 = ctk.CTkButton(
        self.frame, text="categories", command=lambda: print("test cats")
    )
    self.bt_from_frame4.grid(row=0, column=0, padx=20, pady=(10, 0))


#   self.frame ----> GS config
def radio_config_create(self):
    """Ground Station Configuration Widget"""
    # self.clear_frame()

    # Frame Title
    self.radioTitle = ctk.CTkLabel(
        self.frame, text="Radio Config", font=fonts.header)

    # FREQUENCY ===================================
    self.freqLabel = ctk.CTkLabel(
        self.frame, text="Frequency", font=fonts.label)

    self.freqRange = ctk.CTkLabel(
        self.frame,
        text="[240.0 - 960.0] MHz",
        font=fonts.units,
        text_color=colors.units,
    )

    def set_freq(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        self.freqEntry.configure(border_color=color)
        self.values.freq = val
        print(f"Frequency {self.values.freq} Hz")
        unit = 1e6 if self.values.freq_unit == "MHz" else 1
        f = self.values.freq * unit
        if f >= 240e6 and f <= 960e6:
            mqttC.publish(Topics.freq, f)
            color = colors.units
        else:
            color = colors.failed
        self.freqRange.configure(text_color=color)

    freqSV = tk.StringVar()
    freqSV.trace("w", lambda name, index, mode, sv=freqSV: set_freq(freqSV))
    self.freqEntry = ctk.CTkEntry(
        self.frame, font=fonts.entry, textvariable=freqSV)
    self.freqEntry.insert(0, self.values.freq)
    self.freqEntry.bind(command=set_freq)

    def set_freq_unit(option):
        self.values.freq_unit = option
        unit = 1e6 if self.values.freq_unit == "MHz" else 1
        f = self.values.freq * unit
        if f >= 240e6 and f <= 960e6:
            mqttC.publish(Topics.freq, f)
            color = colors.units
        else:
            color = colors.failed
        self.freqRange.configure(text_color=color)

    self.freqCombo = ctk.CTkComboBox(
        self.frame, values=["Hz", "MHz"], width=70, command=set_freq_unit
    )
    self.freqCombo.set(self.values.freq_unit)

    # BANDWIDTH ==========================================
    self.bwLabel = ctk.CTkLabel(self.frame, text="Bandwidth", font=fonts.label)
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

    self.bwOption = ctk.CTkOptionMenu(
        self.frame, values=list(bwopts.keys()), command=set_bw
    )
    self.bwOption.set(
        list(bwopts)[list(bwopts.values()).index(self.values.bw)])

    # CODE RATE =========================================
    self.crLabel = ctk.CTkLabel(self.frame, text="Code Rate", font=fonts.label)
    cropts = {"4/5": 5, "4/6": 6, "4/7": 7, "4/8": 8}

    def set_cr(option):
        self.values.cr = cropts[option]
        mqttC.publish(Topics.cr, self.values.cr)

    self.crOption = ctk.CTkOptionMenu(
        self.frame, values=list(cropts.keys()), command=set_cr
    )
    self.crOption.set(
        list(cropts)[list(cropts.values()).index(self.values.cr)])

    # PREAMBLE LENGTH ===================================
    self.plenLabel = ctk.CTkLabel(
        self.frame, text="Preamble Length", font=fonts.label)

    self.plenRange = ctk.CTkLabel(
        self.frame, text="(3 - 65536)", font=fonts.units, text_color=colors.units
    )

    def set_plen(sv):
        val = to_int(sv.get())
        color = colors.failed if val < 0 else colors.border
        self.plenEntry.configure(border_color=color)
        if val > 0:
            self.values.plen = val
        print(f"Preamble length {self.values.plen}")
        if self.values.plen >= 3 and self.values.plen <= 65536:
            mqttC.publish(Topics.plen, self.values.plen)
            color = colors.units
        else:
            color = colors.failed
        self.plenRange.configure(text_color=color)

    plenSV = tk.StringVar()
    plenSV.trace("w", lambda name, index, mode, sv=plenSV: set_plen(plenSV))
    self.plenEntry = ctk.CTkEntry(
        self.frame, font=fonts.entry, width=80, textvariable=plenSV
    )
    self.plenEntry.insert(0, self.values.plen)

    # Spreading Factor ==================================

    def sfCallback(value):
        self.values.sf = value
        mqttC.publish(Topics.sf, self.values.sf)

    self.sfLabel = ctk.CTkLabel(
        self.frame, text="Spreading Factor", font=fonts.label)
    self.sfSegmented = ctk.CTkSegmentedButton(
        self.frame, values=range(7, 12 + 1), command=sfCallback
    )
    self.sfSegmented.set(self.values.sf)

    # TX POWER ========================================
    self.txpwrLabel = ctk.CTkLabel(
        self.frame, text="Tx Power", font=fonts.label)

    def slider_event(value):
        self.txpwrValue.configure(text=f"{int(value)} dBm")
        if value != self.values.tx_power:
            self.values.tx_power = value
            mqttC.publish(Topics.txpwr, self.values.tx_power)

    self.txpwrSlider = ctk.CTkSlider(
        self.frame, from_=5, to=23, number_of_steps=18, command=slider_event
    )
    self.txpwrValue = ctk.CTkLabel(
        self.frame,
        text=f"{self.values.tx_power} dBm",
        font=fonts.units,
        text_color=colors.units,
    )
    self.txpwrSlider.set(self.values.tx_power)

    # LNA GAIN ========================================
    self.lnaLabel = ctk.CTkLabel(self.frame, text="LNA Gain", font=fonts.label)

    def lna_slider_event(value):
        self.lnaValue.configure(text=f"Lvl {int(value)}")
        if value != self.values.lna_gain:
            self.values.lna_gain = value
            mqttC.publish(Topics.lnag, self.values.lna_gain)

    self.lnaSlider = ctk.CTkSlider(
        self.frame, from_=1, to=6, number_of_steps=5, command=lna_slider_event
    )
    self.lnaValue = ctk.CTkLabel(
        self.frame,
        text=f"Lvl {self.values.lna_gain}",
        font=fonts.units,
        text_color=colors.units,
    )
    self.lnaSlider.set(self.values.lna_gain)

    # ACKNOWLEDGE =====================================
    self.ackdLabel = ctk.CTkLabel(
        self.frame, text="ACK Delay", font=fonts.label)

    def set_ackdelay(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        self.ackdelayEntry.configure(border_color=color)
        self.values.ack_delay = val
        # TODO: verify boundaries
        print(f"ACK delay {self.values.ack_delay}")
        mqttC.publish(Topics.ackdelay, self.values.ack_delay)

    ackdSV = tk.StringVar()
    ackdSV.trace("w", lambda name, index, mode,
                 sv=ackdSV: set_ackdelay(ackdSV))
    self.ackdelayEntry = ctk.CTkEntry(
        self.frame, font=fonts.entry, width=100, textvariable=ackdSV
    )
    self.ackdelayEntry.insert(0, self.values.ack_delay)
    self.ackdUnit = ctk.CTkLabel(
        self.frame, text="s", font=fonts.units, text_color=colors.units
    )

    self.ackwLabel = ctk.CTkLabel(
        self.frame, text="ACK Wait", font=fonts.label)

    def set_ackwait(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        self.ackwaitEntry.configure(border_color=color)
        self.values.ack_wait = val
        # TODO: verify boundaries
        print(f"ACK wait {self.values.ack_wait}")
        mqttC.publish(Topics.ackwait, self.values.ack_wait)

    ackwSV = tk.StringVar()
    ackwSV.trace("w", lambda name, index, mode, sv=ackwSV: set_ackwait(ackwSV))
    self.ackwaitEntry = ctk.CTkEntry(
        self.frame, font=fonts.entry, width=100, textvariable=ackwSV
    )
    self.ackwaitEntry.insert(0, self.values.ack_wait)
    self.ackwUnit = ctk.CTkLabel(
        self.frame, text="s", font=fonts.units, text_color=colors.units
    )
    # RX TIMEOUT ======================================
    self.rxtoLabel = ctk.CTkLabel(
        self.frame, text="Rx Timeout", font=fonts.label)

    def set_rxtimeout(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        self.rxtoEntry.configure(border_color=color)
        if val > 0:
            self.values.rx_timeout = val
        # TODO: verify boundaries
        print(f"Rx timeout {self.values.rx_timeout}")
        mqttC.publish(Topics.rxto, self.values.rx_timeout)

    rxtoSV = tk.StringVar()
    rxtoSV.trace("w", lambda name, index, mode,
                 sv=rxtoSV: set_rxtimeout(rxtoSV))
    self.rxtoEntry = ctk.CTkEntry(
        self.frame, font=fonts.entry, width=100, textvariable=rxtoSV
    )
    self.rxtoEntry.insert(0, self.values.rx_timeout)
    self.rxtoUnit = ctk.CTkLabel(
        self.frame, text="s", font=fonts.units, text_color=colors.units
    )

    # CHECKSUM ========================================

    def chksumEvent():
        self.values.chksum = has_chksum.get()
        mqttC.publish(Topics.chksum, self.values.chksum)

    self.chksumLabel = ctk.CTkLabel(
        self.frame, text="Checksum", font=fonts.label)
    has_chksum = ctk.StringVar(value=True)
    self.chksumSwitch = ctk.CTkSwitch(
        self.frame,
        text="",
        command=chksumEvent,
        variable=has_chksum,
        onvalue=True,
        offvalue=False,
    )
    self.chksumSwitch.select() if self.values.chksum else self.chksumSwitch.deselect()

    # SUBMIT
    def button_event():
        value, unit = (float(self.freqEntry.get()), self.freqCombo.get())
        freqval = int(value * 1e6 if unit == "MHz" else value)
        #         print(value, unit, " -> ", freqval)
        mqttC.publish("radio/freq", str(freqval))

        value = bwopts[self.bwOption.get()]
        #         print(value)
        mqttC.publish("radio/bw", str(value))

    self.button = ctk.CTkButton(
        self.frame, text="Submit", font=fonts.button, command=button_event
    )


def radio_config(self):
    self.clear_frame()
    self.radioTitle.grid(row=0, column=0, columnspan=5)
    self.freqLabel.grid(row=1, column=0, padx=10, pady=20, sticky=tk.E)
    self.freqEntry.grid(row=1, column=1, padx=10, pady=20, sticky=tk.W)
    self.freqCombo.grid(row=1, column=1, padx=(160, 10), pady=20, sticky=tk.E)
    self.freqRange.grid(row=1, column=2, padx=10, pady=20, sticky=tk.W)
    self.bwLabel.grid(row=2, column=0, padx=10, pady=20, sticky=tk.E)
    self.bwOption.grid(row=2, column=1, padx=10, pady=20, sticky=tk.W)
    self.crLabel.grid(row=3, column=0, padx=10, pady=20, sticky=tk.E)
    self.crOption.grid(row=3, column=1, padx=10, pady=20, sticky=tk.W)
    self.plenLabel.grid(row=4, column=0, padx=10, pady=20, sticky=tk.E)
    self.plenEntry.grid(row=4, column=1, padx=10, pady=20, sticky=tk.W)
    self.plenRange.grid(row=4, column=1, padx=50, pady=20, sticky=tk.E)
    self.sfLabel.grid(row=5, column=0, padx=10, pady=20, sticky=tk.E)
    self.sfSegmented.grid(row=5, column=1, padx=10, pady=20, sticky=tk.W)
    self.txpwrLabel.grid(row=6, column=0, padx=10, pady=20, sticky=tk.E)
    self.txpwrSlider.grid(row=6, column=1, padx=10, pady=20)
    self.txpwrValue.grid(row=6, column=2, padx=10, pady=20, sticky=tk.W)
    self.lnaLabel.grid(row=7, column=0, padx=10, pady=20, sticky=tk.E)
    self.lnaSlider.grid(row=7, column=1, padx=10, pady=20)
    self.lnaValue.grid(row=7, column=2, padx=10, pady=20, sticky=tk.W)
    self.ackdLabel.grid(
        row=8, column=0, padx=10
    )
    self.ackdelayEntry.grid(
        row=9, column=0, padx=10
    )
    self.ackdUnit.grid(
        row=9, column=0, padx=(130, 10)
    )
    self.ackwLabel.grid(
        row=8, column=1, padx=10
    )
    self.ackwaitEntry.grid(
        row=9, column=1, padx=10
    )
    self.ackwUnit.grid(
        row=9, column=1, padx=(130, 10)
    )
    self.rxtoLabel.grid(
        row=8, column=2, padx=10
    )
    self.rxtoEntry.grid(
        row=9, column=2, padx=10
    )
    self.rxtoUnit.grid(
        row=9, column=2, padx=(130, 10)
    )
    self.chksumLabel.grid(
        row=10, column=0, padx=10, pady=20, sticky=tk.E
    )
    self.chksumSwitch.grid(
        row=10, column=1, padx=10, pady=20, sticky=tk.E
    )
    self.button.grid(row=11, column=1, padx=(10, 10), pady=20, columnspan=5)


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


#     self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20), sticky="s")    self.scaling_optionemenu.grid(
#         row=8, column=0, padx=20, pady=(10, 20), sticky="s")
# TODO: Change theme
# TODO: Change theme
# TODO: Change theme
# TODO: Change theme
# TODO: Change theme
# TODO: Change theme
# TODO: Change theme
# TODO: Change theme
# TODO: Change theme
