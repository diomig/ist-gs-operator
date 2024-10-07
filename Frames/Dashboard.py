import customtkinter as ctk
import matplotlib.backends.backend_tkagg as tkagg  # import FigureCanvasTkAgg
import numpy as np
from colorama import Fore
from matplotlib.figure import Figure

from Frames.RadioConfig import to_float, to_int
from rotClient import Rotator
from utils import colors, fonts


class RotPanel(ctk.CTkTabview):
    def __init__(self, master, top, **kwargs):
        super().__init__(master, **kwargs)

        # create tabs
        self.add("Auto")
        self.add("Manual")

        self.azimuth = 0
        self.elevation = 90

        # add widgets on tabs
        self.autoAZ = ctk.CTkLabel(
            self.tab("Auto"),
            text="Az: ---°",
            font=fonts.display,
        )
        self.autoEL = ctk.CTkLabel(
            self.tab("Auto"),
            text="El: --°",
            font=fonts.display,
        )

        self.elLabel = ctk.CTkLabel(
            self.tab("Manual"),
            text="El [°]:",
            font=fonts.label,
        )
        self.elEntry = ctk.CTkEntry(self.tab("Manual"), width=100)

        # Entry for theta
        self.azLabel = ctk.CTkLabel(
            self.tab("Manual"),
            text="Az [°]:",
            font=fonts.label,
        )
        self.azEntry = ctk.CTkEntry(self.tab("Manual"), width=100)

        def set_pos():
            try:
                az = to_float(self.azEntry.get())
                el = to_float(self.elEntry.get())
                if az < 0 or az > 360:
                    return
                if el < 0 or el > 90:
                    return

                # Get the values from the entries
                r = 90 - el
                # Convert degrees to radians
                theta = np.radians(az)

                # Update the marker position
                top.ax.lines.clear()
                top.ax.plot(theta, r, marker="o", color=colors.marker)
                top.canvas.draw()

                print(top.rot.set_position(az, el))

            except ValueError:
                # Handle invalid input
                print("Please enter valid numeric values for r and θ.")

        # Button to update the marker
        self.setposButton = ctk.CTkButton(
            self.tab("Manual"), text="Set Position", command=set_pos
        )

        self.autoAZ.grid()
        self.autoEL.grid()
        self.azLabel.grid(row=0, column=0, padx=10, pady=20)
        self.azEntry.grid(row=0, column=1, padx=10, pady=20)
        self.elLabel.grid(row=1, column=0, padx=10, pady=20)
        self.elEntry.grid(row=1, column=1, padx=10, pady=20)
        self.setposButton.grid(row=2, column=0, columnspan=2, padx=30, pady=20)


class MsgPanel(ctk.CTkTabview):
    def __init__(self, master, top, **kwargs):
        super().__init__(master, **kwargs)

        _raw = "Raw"
        _decoded = "Decoded"
        # create tabs
        self.add(_raw)
        self.add(_decoded)

        self.raw_box = ctk.CTkTextbox(
            self.tab(_raw),
            width=590,
            height=390,
        )

        self.decoded_box = ctk.CTkTextbox(
            self.tab(_decoded),
            width=600,
            height=400,
        )

        self.raw_box.grid()
        self.decoded_box.grid()


def dash_create(app):
    """Dashboard widget"""

    fig = Figure(figsize=(4, 4), dpi=100)
    fig.patch.set_facecolor(colors.transparent)  # colors.bg)
    app.ax = fig.add_subplot(projection="polar")
    # NOTE: this is how you plot
    # app.ax.plot(np.pi, 1, marker="x")
    app.ax.set_rmax(90)
    app.ax.set_ylim(0, 90)
    app.ax.tick_params(axis="y", colors="#888888")

    # HACK: don't forget that elevation goes the other way around
    # 90º -> 0º inside-out
    # so, r = 90 - el
    elticks = [0, 30, 60, 90]
    app.ax.set_rticks(elticks, [90 - e for e in elticks])  # Less radial ticks
    # Move radial labels away from plotted line
    app.ax.set_rlabel_position(-22.5)
    app.ax.grid(True, color="gray")

    #     ticks = np.pi/180. * np.linspace(180,  -180, 8, endpoint=False)
    #     app.ax.set_xticks(ticks)
    app.ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2])
    app.ax.set_theta_zero_location("N")  # North corresponds to az=0
    app.ax.set_theta_direction(-1)  # set direction to clockwise
    app.ax.set_xticklabels(["N", "E", "S", "W"])  # Labels for the ticks
    app.ax.tick_params(axis="x", colors="white")
    app.canvas = tkagg.FigureCanvasTkAgg(fig, master=app.frame)
    app.canvas.get_tk_widget().configure(bg=colors.bg)
    app.canvas.draw()

    # ++++++++++++++++++++++++ JUST FOR TESTING ++++++++++++++++++++++++++++++
    # Frame to hold the controls
    app.control_frame = ctk.CTkFrame(app.frame)

    # Entry for r
    app.elLabel = ctk.CTkLabel(app.control_frame, text="El [°]:")
    app.elEntry = ctk.CTkEntry(app.control_frame, width=100)

    # Entry for theta
    app.azLabel = ctk.CTkLabel(app.control_frame, text="Az [°]:")
    app.azEntry = ctk.CTkEntry(app.control_frame, width=100)

    app.az = 0
    app.el = 90

    def update_marker():
        try:
            mode = app.rot_panel.get()
            el = float(app.elEntry.get()) if mode == "Manual" else app.el
            r = 90 - el

            az = float(app.azEntry.get()) if mode == "Manual" else app.az
            theta = np.radians(az)

            app.ax.lines.clear()
            app.ax.plot(theta, r, marker="o", color=colors.marker)
            app.canvas.draw()

        except ValueError:
            # Handle invalid input
            print("Please enter valid numeric values for Az and El!")

    # Button to update the marker
    app.updatemarkerButton = ctk.CTkButton(
        app.control_frame, text="Set Position", command=update_marker
    )

    app.rot_panel = RotPanel(app.frame, top=app, width=300)
    app.msg_panel = MsgPanel(app.frame, top=app, width=600, height=400)
    app.connectionStatus = ctk.CTkLabel(
        app.frame,
        text="Connected to the daemon",
    )


def dash(app):
    def update_marker():
        if app.rot_panel.get() == "Manual":
            return
        try:
            # Get the values from the entries
            el = app.el
            r = 90 - float(el)

            az = app.az
            theta = np.radians(float(az))

            # Update the marker position
            app.ax.lines.clear()
            app.ax.plot(theta, r, marker="o", color=colors.marker)
            app.canvas.draw()

        except ValueError:
            # Handle invalid input
            print("Please enter valid numeric values for Az and El!")

    def update_pos():
        if not app.rot.connected:
            app.rot.open_socket()
        try:
            app.az, app.el = app.rot.get_position().split()
            app.rot_panel.autoAZ.configure(text_color=colors.connected)
            app.rot_panel.autoEL.configure(text_color=colors.connected)
            app.rot_panel.autoAZ.configure(text=f"Az: {app.az}°")
            app.rot_panel.autoEL.configure(text=f"El: {app.el}°")
        except Exception:
            app.rot_panel.autoAZ.configure(text_color=colors.failed)
            app.rot_panel.autoEL.configure(text_color=colors.failed)
            app.rot.connected = False
        app.after(1000, update_pos)
        update_marker()

    app.rot = Rotator(app.values.rothost, app.values.rotport)

    print(app.values.rothost)
    print(app.values.rotport)
    app.clear_frame()
    app.canvas.get_tk_widget().grid(row=2, column=0)
    #     app.control_frame.grid(row=2, column=1, padx=10, sticky="W")
    #     app.azLabel.grid()
    #     app.azEntry.grid()
    #     app.elLabel.grid()
    #     app.elEntry.grid()
    app.updatemarkerButton.grid()

    app.rot_panel.grid(row=2, column=1, sticky="W")
    update_pos()
    app.msg_panel.grid(row=4, column=0, columnspan=4)
