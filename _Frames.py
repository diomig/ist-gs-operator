import tkinter as tk

import customtkinter as ctk
import matplotlib.backends.backend_tkagg as tkagg  # import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure

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


def dash(app):
    """Dashboard widget"""
    app.clear_frame()
    app.tlmLabel = ctk.CTkLabel(
        app.frame,
        text="Raw Telemetry",
        font=fonts.label,
    )

    app.telemetryBox = ctk.CTkTextbox(
        app.frame,
        width=500,
        height=300,
    )
    #     app.telemetryBox.insert('0.0', 'new telemetry message')
    #     app.telemetryBox.configure(state='disabled')

    fig = Figure(figsize=(5, 4), dpi=100)
    fig.patch.set_facecolor(colors.transparent)  # colors.bg)
    app.ax = fig.add_subplot(projection="polar")
    # NOTE: this is how you plot
    # app.ax.plot(np.pi, 1, marker="x")
    app.ax.set_rmax(90)
    app.ax.set_ylim(0, 90)
    # HACK: don't forget that elevation goes the other way around
    # 90º -> 0º inside-out
    # so, r = 90 - el
    elticks = [0, 30, 60, 90]
    app.ax.set_rticks(elticks, [90-e for e in elticks])  # Less radial ticks
    # Move radial labels away from plotted line
    app.ax.set_rlabel_position(-22.5)
    app.ax.grid(True)

    #     ticks = np.pi/180. * np.linspace(180,  -180, 8, endpoint=False)
    #     app.ax.set_xticks(ticks)
    app.ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2]
                       )  # Positions for N, E, S, W
    app.ax.set_xticklabels(["E", "N", "W", "S"])  # Labels for the ticks
    app.ax.tick_params(axis="x", colors="white")
    app.canvas = tkagg.FigureCanvasTkAgg(fig, master=app.frame)
    app.canvas.get_tk_widget().configure(bg=colors.bg)
    app.canvas.draw()
    app.canvas.get_tk_widget().grid()

    # ++++++++++++++++++++++++ JUST FOR TESTING ++++++++++++++++++++++++++++++
    def create_controls(app):
        # Frame to hold the controls
        control_frame = ctk.CTkFrame(app.frame)
        control_frame.grid()

        # Entry for r
        ctk.CTkLabel(control_frame, text="r:").grid()
        app.r_entry = ctk.CTkEntry(control_frame, width=100)
        app.r_entry.grid()

        # Entry for theta
        ctk.CTkLabel(control_frame, text="θ (degrees):").grid()
        app.theta_entry = ctk.CTkEntry(control_frame, width=100)
        app.theta_entry.grid()

        # Button to update the marker
        update_button = ctk.CTkButton(
            control_frame, text="Update Marker", command=update_marker
        )
        update_button.grid()

    def update_marker():
        try:
            # Get the values from the entries
            r = float(app.r_entry.get())
            # Convert degrees to radians
            theta = np.radians(float(app.theta_entry.get()))

            # Update the marker position
            app.ax.plot(theta, r, marker="o")
            app.canvas.draw()

        except ValueError:
            # Handle invalid input
            print("Please enter valid numeric values for r and θ.")

    create_controls(app)

    app.tlmLabel.grid()
    app.telemetryBox.grid()


#  app.frame   ----> statement widget


def mqtt_setup_create(app):
    """MQTT Setup Widget"""
    host = app.values.host
    port = app.values.port
    app.hostLabel = ctk.CTkLabel(app.frame, text="Host", font=fonts.label)
    app.hostEntry = ctk.CTkEntry(
        app.frame,
        placeholder_text=("Host" if not host else host),
        font=fonts.entry,
        width=300,
    )

    app.portLabel = ctk.CTkLabel(app.frame, text="Port", font=fonts.label)
    app.portEntry = ctk.CTkEntry(
        app.frame,
        placeholder_text=("Port" if not port else port),
        font=fonts.entry,
        width=200,
    )

    app.usrLabel = ctk.CTkLabel(app.frame, text="Username", font=fonts.label)
    app.usrEntry = ctk.CTkEntry(
        app.frame, placeholder_text="Username", font=fonts.entry, width=300
    )

    app.pwLabel = ctk.CTkLabel(app.frame, text="Password", font=fonts.label)
    app.pwEntry = ctk.CTkEntry(
        app.frame, placeholder_text="Password", font=fonts.entry, width=300
    )

    # Connect
    def connect_event():
        new_host = app.hostEntry.get()
        new_port = app.portEntry.get()
        print(f"Connecting to {new_host}:{new_port}...")
        try:
            mqttC.connect(
                app.hostEntry.get(),
                int(app.portEntry.get()),
            )
            mqttC.loop_start()
            print("Connected")
            success = True
        except Exception:
            print("CONNECTION FAILED!")
            success = False
        color = colors.connected if success else colors.failed
        app.hostEntry.configure(
            border_color=color,
            placeholder_text_color=color,
        )
        app.portEntry.configure(
            border_color=color,
            placeholder_text_color=color,
        )
        if success:
            app.connectionIndicator.configure(
                text="MQTT\nConnected\n✔️", text_color=colors.connected
            )
        app.values.host = new_host
        app.values.port = new_port
        app.values.usr = app.usrEntry.get()
        app.values.pw = app.pwEntry.get()
        if success:
            app.connected = True
            app.connectButton.grid_forget()
            app.disconnectButton.grid(row=8, column=0, columnspan=4, pady=100)

    app.connectButton = ctk.CTkButton(
        app.frame, text="Connect", font=fonts.button, command=connect_event
    )

    def disconnect_event():
        print("time to go...")
        mqttC.loop_stop()
        mqttC.disconnect()
        app.connected = False
        app.hostEntry.configure(border_color=colors.border)
        app.portEntry.configure(border_color=colors.border)
        app.connectionIndicator.configure(
            text="MQTT\nNOT Connected\n❌", text_color=colors.failed
        )
        app.disconnectButton.grid_forget()
        app.connectButton.grid(row=8, column=0, columnspan=4, pady=100)

    app.disconnectButton = ctk.CTkButton(
        app.frame,
        text="Disconnect",
        font=fonts.button,
        command=disconnect_event,
        fg_color=colors.disconnect,
        hover_color=colors.disconnect_hover,
    )
    app.mqttTitle = ctk.CTkLabel(
        app.frame, text="Connect to the MQTT broker", font=fonts.header
    )


def mqtt_setup(app):
    app.clear_frame()
    app.mqttTitle.grid(row=0, column=0, columnspan=4, pady=100)
    app.hostLabel.grid(row=1, column=0, padx=10, sticky='W')
    app.hostEntry.grid(row=2, column=0, padx=10)
    app.portLabel.grid(row=1, column=1, padx=10, sticky='W')
    app.portEntry.grid(row=2, column=1, padx=10)
    app.usrLabel.grid(row=3, column=0, padx=10, pady=(50, 2), sticky='W')
    app.usrEntry.grid(row=4, column=0, padx=10)
    app.pwLabel.grid(row=5, column=0, padx=10, pady=(20, 2), sticky='W')
    app.pwEntry.grid(row=6, column=0, padx=10)
    if not app.connected:
        app.connectButton.grid(row=8, column=0, columnspan=4, pady=100)
    else:
        app.disconnectButton.grid(row=8, column=0, columnspan=4, pady=100)


#  app.frame   ----> categories widget


def categories(app):
    """Categories Management Widget"""
    app.clear_frame()
    # ----------------------------------------------------------------
    #     r = np.arange(0, 2, 0.01)
    #     theta = 2 * np.pi * r


# ----------------------------------------------------------------

#   app.frame ----> GS config


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
        text="Preamble Length",
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
        text="Spreading Factor",
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
    app.radioTitle.grid(row=0, column=0, columnspan=5)
    app.freqLabel.grid(row=1, column=0, padx=10, pady=20, sticky='E')
    app.freqEntry.grid(row=1, column=1, padx=10, pady=20, sticky='W')
    app.freqCombo.grid(row=1, column=1, padx=(160, 10), pady=20, sticky='E')
    app.freqRange.grid(row=1, column=2, padx=10, pady=20, sticky='W')
    app.bwLabel.grid(row=2, column=0, padx=10, pady=20, sticky='E')
    app.bwOption.grid(row=2, column=1, padx=10, pady=20, sticky='W')
    app.crLabel.grid(row=3, column=0, padx=10, pady=20, sticky='E')
    app.crOption.grid(row=3, column=1, padx=10, pady=20, sticky='W')
    app.plenLabel.grid(row=4, column=0, padx=10, pady=20, sticky='E')
    app.plenEntry.grid(row=4, column=1, padx=10, pady=20, sticky='W')
    app.plenRange.grid(row=4, column=1, padx=50, pady=20, sticky='E')
    app.sfLabel.grid(row=5, column=0, padx=10, pady=20, sticky='E')
    app.sfSegmented.grid(row=5, column=1, padx=10, pady=20, sticky='W')
    app.txpwrLabel.grid(row=6, column=0, padx=10, pady=20, sticky='E')
    app.txpwrSlider.grid(row=6, column=1, padx=10, pady=20)
    app.txpwrValue.grid(row=6, column=2, padx=10, pady=20, sticky='W')
    app.lnaLabel.grid(row=7, column=0, padx=10, pady=20, sticky='E')
    app.lnaSlider.grid(row=7, column=1, padx=10, pady=20)
    app.lnaValue.grid(row=7, column=2, padx=10, pady=20, sticky='W')
    app.ackdLabel.grid(row=8, column=0, padx=10)
    app.ackdelayEntry.grid(row=9, column=0, padx=10)
    app.ackdUnit.grid(row=9, column=0, padx=(130, 10))
    app.ackwLabel.grid(row=8, column=1, padx=10)
    app.ackwaitEntry.grid(row=9, column=1, padx=10)
    app.ackwUnit.grid(row=9, column=1, padx=(130, 10))
    app.rxtoLabel.grid(row=8, column=2, padx=10)
    app.rxtoEntry.grid(row=9, column=2, padx=10)
    app.rxtoUnit.grid(row=9, column=2, padx=(130, 10))
    app.chksumLabel.grid(row=10, column=0, padx=10, pady=20, sticky='E')
    app.chksumSwitch.grid(row=10, column=1, padx=10, pady=20, sticky='E')
    app.button.grid(row=11, column=1, padx=(10, 10), pady=20, columnspan=5)


# ===================================================


def rot_config_create(app):

    def update(data):
        # Clear the listbox
        app.my_list.delete(0, 'end')

        # Add modelopts to listbox
        for item in data:
            app.my_list.insert('end', item)

    # Update entry box with listbox clicked
    def fillout(e):
        # Delete whatever is in the entry box
        app.my_entry.delete(0, 'end')

        # Add clicked list item to entry box
        selected = app.my_list.get('anchor')
        app.my_entry.insert(0, "  ".join(selected.split()))
        app.modelselectLabel.grid(row=3, column=1, padx=30, sticky='E')
        print('Selected: ', selected)
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
    app.rotmodelLabel.grid(row=2, column=0, pady=(50, 5))
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


# ===================================================


def decoders(app):
    app.clear_frame()

    def update(data):
        # Clear the listbox
        app.decList.delete(0, 'end')

        # Add modelopts to listbox
        for item in data:
            app.decList.insert('end', item)

    # Update entry box with listbox clicked
    def fillout(e):
        # Delete whatever is in the entry box
        app.decEntry.delete(0, 'end')

        # Add clicked list item to entry box
        selected = app.decList.get('anchor')
        app.decEntry.insert(0, "  ".join(selected.split()))
        app.decoderselectLabel.grid(row=3, column=1, padx=30, sticky='E')
        print('Selected: ', selected)
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
        width=70,
        bg=colors.bg,
        fg="#ffffff",
        highlightcolor="#666666",
        font=fonts.listbox,
        # selectbackground="#aaaaaa",
    )

    decoderopts = ['decoder1', 'decoder2',
                   'decoder3', 'another one',
                   'last entry',
                   'SIKE, this one is the last tho']
    # Add the modelopts to our list
    update(decoderopts)

    # Create a binding on the listbox onclick
    app.decList.bind("<<ListboxSelect>>", fillout)

    # Create a binding on the entry box
    app.decEntry.bind("<KeyRelease>", check)

    app.decLabel.grid()
    app.decoderselectLabel.grid()
    app.decEntry.grid()
    app.decList.grid()


# ===================================================
# Change scaling of all widget 80% to 120%


def change_scaling_event(new_scaling):
    new_scaling_float = int(new_scaling.replace("%", "")) / 100
    ctk.set_widget_scaling(new_scaling_float)


def view(app):
    """edit UI"""
    app.clear_frame()
    app.scaling_label = ctk.CTkLabel(
        app.frame,
        text="UI Scaling:",
        anchor="w",
    )
    app.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))

    app.scaling_optionemenu = ctk.CTkOptionMenu(
        app.frame,
        values=["80%", "90%", "100%", "110%", "120%"],
        command=change_scaling_event,
    )

    app.scaling_optionemenu.grid(
        row=8,
        column=0,
        padx=20,
        pady=(10, 20),
        sticky="s",
    )
