import customtkinter as ctk

from MQTT import mqttC
from utils import colors, fonts


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
    app.hostLabel.grid(row=1, column=0, padx=10, sticky="W")
    app.hostEntry.grid(row=2, column=0, padx=10)
    app.portLabel.grid(row=1, column=1, padx=10, sticky="W")
    app.portEntry.grid(row=2, column=1, padx=10)
    app.usrLabel.grid(row=3, column=0, padx=10, pady=(50, 2), sticky="W")
    app.usrEntry.grid(row=4, column=0, padx=10)
    app.pwLabel.grid(row=5, column=0, padx=10, pady=(20, 2), sticky="W")
    app.pwEntry.grid(row=6, column=0, padx=10)
    if not app.connected:
        app.connectButton.grid(row=8, column=0, columnspan=4, pady=100)
    else:
        app.disconnectButton.grid(row=8, column=0, columnspan=4, pady=100)
