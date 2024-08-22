import customtkinter as ctk
import matplotlib.backends.backend_tkagg as tkagg  # import FigureCanvasTkAgg
import numpy as np
from matplotlib.figure import Figure

from utils import colors, fonts


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
    app.ax.set_rticks(elticks, [90 - e for e in elticks])  # Less radial ticks
    # Move radial labels away from plotted line
    app.ax.set_rlabel_position(-22.5)
    app.ax.grid(True)

    #     ticks = np.pi/180. * np.linspace(180,  -180, 8, endpoint=False)
    #     app.ax.set_xticks(ticks)
    app.ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2])
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
