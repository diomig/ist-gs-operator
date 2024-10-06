import tkinter as tk
from os.path import basename, expanduser

import customtkinter as ctk

from MQTT import mqttC, tlsC
from utils import colors, fonts
import ssl

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

    class UsrPwFrame(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            # add widgets onto the frame, for example:
            self.label = ctk.CTkLabel(
                self,
                text="Authentication",
                font=fonts.label,
            )
            self.label.grid(row=0, column=0, padx=20)

    app.usrpwFrame = UsrPwFrame(master=app.frame)
    app.usrLabel = ctk.CTkLabel(app.usrpwFrame, text="Username", font=fonts.label)
    app.usrEntry = ctk.CTkEntry(
        app.usrpwFrame, placeholder_text="Username", font=fonts.entry, width=300
    )
    app.pwLabel = ctk.CTkLabel(app.usrpwFrame, text="Password", font=fonts.label)
    app.pwEntry = ctk.CTkEntry(
        app.usrpwFrame,
        placeholder_text="Password",
        show=fonts.bullet,
        font=fonts.entry,
        width=300,
    )

    class TlsFrame(ctk.CTkFrame):
        def __init__(self, master, **kwargs):
            super().__init__(master, **kwargs)

            # add widgets onto the frame, for example:
            self.label = ctk.CTkLabel(
                self,
                text="TLS",
                font=fonts.label,
            )
            self.tlsSwitch = ctk.CTkSwitch(
                self,
                text="",
                onvalue="on",
                offvalue="off",
            )
            self.label.grid(row=0, column=0, padx=20)
            self.tlsSwitch.grid(row=0, column=1)

    app.tlsFrame = TlsFrame(master=app.frame)

    def open_cafile():
        file = tk.filedialog.askopenfile(
            mode="r",
            initialdir=expanduser("~"),
            title="Select a file",
            filetypes=[("Certificate Files", "*.crt"), ("all files", "*.*")],
        )
        tlsC.cafile = file.name
        app.rmCaFileBtn.configure(text=basename(tlsC.cafile) + "   ❌")
        app.rmCaFileBtn.grid(row=1, column=1)

    def open_certfile():
        file = tk.filedialog.askopenfile(
            mode="r",
            initialdir=expanduser("~"),
            title="Select a file",
            filetypes=[("Certificate Files", "*.crt"), ("all files", "*.*")],
        )
        tlsC.cert = file.name
        app.rmCrtBtn.configure(text=basename(tlsC.cert) + "   ❌")
        app.rmCrtBtn.grid(row=2, column=1)

    def open_keyfile():
        file = tk.filedialog.askopenfile(
            mode="r",
            initialdir=expanduser("~"),
            title="Select a file",
            filetypes=[("Key Files", "*.key"), ("all files", "*.*")],
        )
        tlsC.key = file.name
        app.rmKeyBtn.configure(text=basename(tlsC.key) + "   ❌")
        app.rmKeyBtn.grid(row=3, column=1)

    app.caFileBtn = ctk.CTkButton(
        app.tlsFrame,
        text="Server Certificate\n(CA)",
        font=fonts.button,
        command=open_cafile,
    )
    app.clientCrtBtn = ctk.CTkButton(
        app.tlsFrame,
        text="Client Certificate",
        font=fonts.button,
        command=open_certfile,
    )
    app.clientKeyBtn = ctk.CTkButton(
        app.tlsFrame,
        text="Client Key",
        font=fonts.button,
        command=open_keyfile,
    )

    def rm_cafile():
        tlsC.cafile = None
        app.rmCaFileBtn.grid_forget()

    def rm_certfile():
        tlsC.cert = None
        app.rmCrtBtn.grid_forget()

    def rm_keyfile():
        tlsC.key = None
        app.rmKeyBtn.grid_forget()

    app.rmCaFileBtn = ctk.CTkButton(
        app.tlsFrame,
        text="",
        fg_color="transparent",
        hover_color=colors.red,
        command=rm_cafile,
    )
    app.rmCrtBtn = ctk.CTkButton(
        app.tlsFrame,
        text="",
        fg_color="transparent",
        hover_color=colors.red,
        command=rm_certfile,
    )
    app.rmKeyBtn = ctk.CTkButton(
        app.tlsFrame,
        text="",
        fg_color="transparent",
        hover_color=colors.red,
        command=rm_keyfile,
    )
    # Connect

    def connect_event():
        new_host = app.hostEntry.get()
        new_port = app.portEntry.get()
        print(f"Connecting to {new_host}:{new_port}...")

        if app.tlsFrame.tlsSwitch.get() == 'on':
            print('TLS')
            mqttC.tls_set(
                ca_certs='tls/mosquitto.org.crt',
                certfile="tls/client.crt",
                keyfile="tls/client.key",
                tls_version=ssl.PROTOCOL_TLSv1_2,
            )
            mqttC.tls_insecure_set(False)


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
            app.values.rothost = app.values.host

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
    app.mqttTitle.grid(row=0, column=0, columnspan=4, padx=30, pady=(20, 60))
    app.hostLabel.grid(row=1, column=0, padx=10, sticky="W")
    app.hostEntry.grid(row=2, column=0, padx=10)
    app.portLabel.grid(row=1, column=1, padx=10, sticky="W")
    app.portEntry.grid(row=2, column=1, padx=10)
    app.usrpwFrame.grid(row=3, column=0, padx=10, pady=60)
    app.usrLabel.grid(row=1, column=0, padx=10, pady=20, sticky="W")
    app.usrEntry.grid(row=2, column=0, padx=10)
    app.pwLabel.grid(row=3, column=0, padx=10, pady=(20, 2), sticky="W")
    app.pwEntry.grid(row=4, column=0, padx=10, pady=(2, 50))
    app.tlsFrame.grid(row=3, column=1, padx=10, pady=60)
    app.caFileBtn.grid(row=1, column=0, pady=10)
    app.clientCrtBtn.grid(row=2, column=0, pady=10)
    app.clientKeyBtn.grid(row=3, column=0, pady=10)
    if not app.connected:
        app.connectButton.grid(row=8, column=0, columnspan=4, pady=100)
    else:
        app.disconnectButton.grid(row=8, column=0, columnspan=4, pady=100)
