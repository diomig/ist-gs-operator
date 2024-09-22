import tkinter as tk

import customtkinter as ctk

from MQTT import Topics, mqttC
from utils import colors, fonts


def to_float(val):
    try:
        return float(val)
    except ValueError:
        #         print("Not a float")
        return -1


def to_int(val):
    return int(val) if val.isdigit() else -1


def radio_config_create(app):
    """Ground Station Configuration Widget"""
    # Frame Title
    app.radioTitle = ctk.CTkLabel(
        app.frame,
        text="Radio Config",
        font=fonts.header,
    )

    # FREQUENCY ===================================
    app.freqLabel = ctk.CTkLabel(
        app.frame,
        text="Frequency",
        font=fonts.label,
    )

    app.freqRange = ctk.CTkLabel(
        app.frame,
        text="[240.0 - 960.0] MHz",
        font=fonts.units,
        text_color=colors.units,
    )

    def set_freq(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        app.freqEntry.configure(border_color=color)
        app.values.freq = val
        print(f"Frequency {app.values.freq} Hz")
        unit = 1e6 if app.values.freq_unit == "MHz" else 1
        f = app.values.freq * unit
        if f >= 240e6 and f <= 960e6:
            mqttC.publish(Topics.freq, f)
            color = colors.units
        else:
            color = colors.failed
        app.freqRange.configure(text_color=color)

    freqSV = tk.StringVar()
    freqSV.trace("w", lambda name, index, mode, sv=freqSV: set_freq(freqSV))
    app.freqEntry = ctk.CTkEntry(
        app.frame,
        font=fonts.entry,
        textvariable=freqSV,
    )
    app.freqEntry.insert(0, app.values.freq)
    app.freqEntry.bind(command=set_freq)

    def set_freq_unit(option):
        app.values.freq_unit = option
        unit = 1e6 if app.values.freq_unit == "MHz" else 1
        f = app.values.freq * unit
        if f >= 240e6 and f <= 960e6:
            mqttC.publish(Topics.freq, f)
            color = colors.units
        else:
            color = colors.failed
        app.freqRange.configure(text_color=color)

    app.freqCombo = ctk.CTkComboBox(
        app.frame, values=["Hz", "MHz"], width=70, command=set_freq_unit
    )
    app.freqCombo.set(app.values.freq_unit)

    # BANDWIDTH ==========================================
    app.bwLabel = ctk.CTkLabel(app.frame, text="Bandwidth", font=fonts.label)
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
        app.values.bw = bwopts[option]
        mqttC.publish(Topics.bw, app.values.bw)

    app.bwOption = ctk.CTkOptionMenu(
        app.frame,
        values=list(bwopts),
        command=set_bw,
    )

    def selected_option(options, sel):
        return list(options)[list(options.values()).index(sel)]

    app.bwOption.set(selected_option(bwopts, app.values.bw))

    # CODE RATE =========================================
    app.crLabel = ctk.CTkLabel(app.frame, text="Code Rate", font=fonts.label)
    cropts = {"4/5": 5, "4/6": 6, "4/7": 7, "4/8": 8}

    def set_cr(option):
        app.values.cr = cropts[option]
        mqttC.publish(Topics.cr, app.values.cr)

    app.crOption = ctk.CTkOptionMenu(
        app.frame,
        values=list(cropts),
        command=set_cr,
    )
    app.crOption.set(selected_option(cropts, app.values.cr))

    # PREAMBLE LENGTH ===================================
    app.plenLabel = ctk.CTkLabel(
        app.frame,
        text="Preamble\nLength",
        font=fonts.label,
    )

    app.plenRange = ctk.CTkLabel(
        app.frame,
        text="(3 - 65536)",
        font=fonts.units,
        text_color=colors.units,
    )

    def set_plen(sv):
        val = to_int(sv.get())
        color = colors.failed if val < 0 else colors.border
        app.plenEntry.configure(border_color=color)
        if val > 0:
            app.values.plen = val
        if app.values.plen >= 3 and app.values.plen <= 65536:
            mqttC.publish(Topics.plen, app.values.plen)
            color = colors.units
        else:
            color = colors.failed
        app.plenRange.configure(text_color=color)

    plenSV = tk.StringVar()
    plenSV.trace(
        "w",
        lambda name, index, mode, sv=plenSV: set_plen(plenSV),
    )
    app.plenEntry = ctk.CTkEntry(
        app.frame,
        font=fonts.entry,
        width=80,
        textvariable=plenSV,
    )
    app.plenEntry.insert(0, app.values.plen)

    # Spreading Factor ==================================

    def sfCallback(value):
        app.values.sf = value
        mqttC.publish(Topics.sf, app.values.sf)

    app.sfLabel = ctk.CTkLabel(
        app.frame,
        text="Spreading\nFactor",
        font=fonts.label,
    )
    app.sfSegmented = ctk.CTkSegmentedButton(
        app.frame,
        values=range(7, 12 + 1),
        command=sfCallback,
    )
    app.sfSegmented.set(app.values.sf)

    # TX POWER ========================================
    app.txpwrLabel = ctk.CTkLabel(
        app.frame,
        text="Tx Power",
        font=fonts.label,
    )

    def slider_event(value):
        app.txpwrValue.configure(text=f"{int(value)} dBm")
        if value != app.values.tx_power:
            app.values.tx_power = value
            mqttC.publish(Topics.txpwr, app.values.tx_power)

    app.txpwrSlider = ctk.CTkSlider(
        app.frame,
        from_=5,
        to=23,
        number_of_steps=18,
        command=slider_event,
    )
    app.txpwrValue = ctk.CTkLabel(
        app.frame,
        text=f"{app.values.tx_power} dBm",
        font=fonts.units,
        text_color=colors.units,
    )
    app.txpwrSlider.set(app.values.tx_power)

    # LNA GAIN ========================================
    app.lnaLabel = ctk.CTkLabel(
        app.frame,
        text="LNA Gain",
        font=fonts.label,
    )

    def lna_slider_event(value):
        app.lnaValue.configure(text=f"Lvl {int(value)}")
        if value != app.values.lna_gain:
            app.values.lna_gain = value
            mqttC.publish(Topics.lnag, app.values.lna_gain)

    app.lnaSlider = ctk.CTkSlider(
        app.frame,
        from_=1,
        to=6,
        number_of_steps=5,
        command=lna_slider_event,
    )
    app.lnaValue = ctk.CTkLabel(
        app.frame,
        text=f"Lvl {app.values.lna_gain}",
        font=fonts.units,
        text_color=colors.units,
    )
    app.lnaSlider.set(app.values.lna_gain)

    # ACKNOWLEDGE =====================================
    app.ackdLabel = ctk.CTkLabel(
        app.frame,
        text="ACK Delay",
        font=fonts.label,
    )

    def set_ackdelay(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        app.ackdelayEntry.configure(border_color=color)
        app.values.ack_delay = val
        print(f"ACK delay {app.values.ack_delay}")
        mqttC.publish(Topics.ackdelay, app.values.ack_delay)

    ackdSV = tk.StringVar()
    ackdSV.trace(
        "w",
        lambda name, index, mode, sv=ackdSV: set_ackdelay(ackdSV),
    )
    app.ackdelayEntry = ctk.CTkEntry(
        app.frame,
        font=fonts.entry,
        width=100,
        textvariable=ackdSV,
    )
    app.ackdelayEntry.insert(0, app.values.ack_delay)
    app.ackdUnit = ctk.CTkLabel(
        app.frame,
        text="s",
        font=fonts.units,
        text_color=colors.units,
    )

    app.ackwLabel = ctk.CTkLabel(
        app.frame,
        text="ACK Wait",
        font=fonts.label,
    )

    def set_ackwait(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        app.ackwaitEntry.configure(border_color=color)
        app.values.ack_wait = val
        print(f"ACK wait {app.values.ack_wait}")
        mqttC.publish(Topics.ackwait, app.values.ack_wait)

    ackwSV = tk.StringVar()
    ackwSV.trace("w", lambda name, index, mode, sv=ackwSV: set_ackwait(ackwSV))
    app.ackwaitEntry = ctk.CTkEntry(
        app.frame,
        font=fonts.entry,
        width=100,
        textvariable=ackwSV,
    )
    app.ackwaitEntry.insert(0, app.values.ack_wait)
    app.ackwUnit = ctk.CTkLabel(
        app.frame,
        text="s",
        font=fonts.units,
        text_color=colors.units,
    )
    # RX TIMEOUT ======================================
    app.rxtoLabel = ctk.CTkLabel(
        app.frame,
        text="Rx Timeout",
        font=fonts.label,
    )

    def set_rxtimeout(sv):
        val = to_float(sv.get())
        color = colors.failed if val < 0 else colors.border
        app.rxtoEntry.configure(border_color=color)
        if val > 0:
            app.values.rx_timeout = val
        print(f"Rx timeout {app.values.rx_timeout}")
        mqttC.publish(Topics.rxto, app.values.rx_timeout)

    rxtoSV = tk.StringVar()
    rxtoSV.trace(
        "w",
        lambda name, index, mode, sv=rxtoSV: set_rxtimeout(rxtoSV),
    )
    app.rxtoEntry = ctk.CTkEntry(
        app.frame,
        font=fonts.entry,
        width=100,
        textvariable=rxtoSV,
    )
    app.rxtoEntry.insert(0, app.values.rx_timeout)
    app.rxtoUnit = ctk.CTkLabel(
        app.frame,
        text="s",
        font=fonts.units,
        text_color=colors.units,
    )

    # CHECKSUM ========================================

    def chksumEvent():
        app.values.chksum = has_chksum.get()
        mqttC.publish(Topics.chksum, app.values.chksum)

    app.chksumLabel = ctk.CTkLabel(
        app.frame,
        text="Checksum",
        font=fonts.label,
    )
    has_chksum = ctk.StringVar(value=True)
    app.chksumSwitch = ctk.CTkSwitch(
        app.frame,
        text="",
        command=chksumEvent,
        variable=has_chksum,
        onvalue=True,
        offvalue=False,
    )
    if app.values.chksum:
        app.chksumSwitch.select()
    else:
        app.chksumSwitch.deselect()

    # SUBMIT
    def button_event():
        value, unit = (float(app.freqEntry.get()), app.freqCombo.get())
        freqval = int(value * 1e6 if unit == "MHz" else value)
        mqttC.publish("radio/freq", str(freqval))
        value = bwopts[app.bwOption.get()]
        mqttC.publish("radio/bw", str(value))

    app.button = ctk.CTkButton(
        app.frame,
        text="Submit",
        font=fonts.button,
        command=button_event,
    )


def radio_config(app):
    app.clear_frame()
    app.radioTitle.grid(row=0, column=0, columnspan=5, pady=(20, 40))
    app.freqLabel.grid(row=1, column=0, padx=10, pady=20, sticky="E")
    app.freqEntry.grid(row=1, column=1, padx=10, pady=20, sticky="W")
    app.freqCombo.grid(row=1, column=1, padx=(160, 10), pady=20, sticky="E")
    app.freqRange.grid(row=1, column=2, padx=10, pady=20, sticky="W")
    app.bwLabel.grid(row=2, column=0, padx=10, pady=20, sticky="E")
    app.bwOption.grid(row=2, column=1, padx=10, pady=20, sticky="W")
    app.crLabel.grid(row=3, column=0, padx=10, pady=20, sticky="E")
    app.crOption.grid(row=3, column=1, padx=10, pady=20, sticky="W")
    app.plenLabel.grid(row=4, column=0, padx=10, pady=20, sticky="E")
    app.plenEntry.grid(row=4, column=1, padx=10, pady=20, sticky="W")
    app.plenRange.grid(row=4, column=1, padx=50, pady=20, sticky="E")
    app.sfLabel.grid(row=5, column=0, padx=10, pady=20, sticky="E")
    app.sfSegmented.grid(row=5, column=1, padx=10, pady=20, sticky="W")
    app.txpwrLabel.grid(row=6, column=0, padx=10, pady=20, sticky="E")
    app.txpwrSlider.grid(row=6, column=1, padx=10, pady=20)
    app.txpwrValue.grid(row=6, column=2, padx=10, pady=20, sticky="W")
    app.lnaLabel.grid(row=7, column=0, padx=10, pady=20, sticky="E")
    app.lnaSlider.grid(row=7, column=1, padx=10, pady=20)
    app.lnaValue.grid(row=7, column=2, padx=10, pady=20, sticky="W")
    app.ackdLabel.grid(row=8, column=0, padx=10)
    app.ackdelayEntry.grid(row=9, column=0, padx=10)
    app.ackdUnit.grid(row=9, column=0, padx=(130, 10))
    app.ackwLabel.grid(row=8, column=1, padx=10)
    app.ackwaitEntry.grid(row=9, column=1, padx=10)
    app.ackwUnit.grid(row=9, column=1, padx=(130, 10))
    app.rxtoLabel.grid(row=8, column=2, padx=10)
    app.rxtoEntry.grid(row=9, column=2, padx=10)
    app.rxtoUnit.grid(row=9, column=2, padx=(130, 10))
    app.chksumLabel.grid(row=10, column=0, padx=10, pady=20, sticky="E")
    app.chksumSwitch.grid(row=10, column=1, padx=10, pady=20, sticky="E")
    # app.button.grid(row=11, column=1, padx=(10, 10), pady=20, columnspan=5)
