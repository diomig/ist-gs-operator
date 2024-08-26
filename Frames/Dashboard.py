import customtkinter as ctk
import matplotlib.backends.backend_tkagg as tkagg  # import FigureCanvasTkAgg
import numpy as np
from matplotlib.figure import Figure

from utils import colors, fonts


def dash_create(app):
    """Dashboard widget"""
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
    app.ax.tick_params(axis='y', colors='#888888')

    # HACK: don't forget that elevation goes the other way around
    # 90º -> 0º inside-out
    # so, r = 90 - el
    elticks = [0, 30, 60, 90]
    app.ax.set_rticks(elticks, [90 - e for e in elticks])  # Less radial ticks
    # Move radial labels away from plotted line
    app.ax.set_rlabel_position(-22.5)
    app.ax.grid(True, color='gray')

    #     ticks = np.pi/180. * np.linspace(180,  -180, 8, endpoint=False)
    #     app.ax.set_xticks(ticks)
    app.ax.set_xticks([0, np.pi / 2, np.pi, 3 * np.pi / 2])
    app.ax.set_xticklabels(["E", "N", "W", "S"])  # Labels for the ticks
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

    def update_marker():
        try:
            # Get the values from the entries
            r = 90 - float(app.elEntry.get())
            # Convert degrees to radians
            theta = np.radians(float(app.azEntry.get()))

            # Update the marker position
            app.ax.plot(theta, r, marker="o")
            app.canvas.draw()

        except ValueError:
            # Handle invalid input
            print("Please enter valid numeric values for r and θ.")

    # Button to update the marker
    app.updatemarkerButton = ctk.CTkButton(
        app.control_frame, text="Update Marker", command=update_marker
    )


def dash(app):
    app.clear_frame()
    app.canvas.get_tk_widget().grid(row=2, column=0, padx=10)
    app.control_frame.grid(row=2, column=1, padx=10)
    app.azLabel.grid()
    app.azEntry.grid()
    app.elLabel.grid()
    app.elEntry.grid()
    app.updatemarkerButton.grid()
    app.tlmLabel.grid(row=4, column=0, padx=20)
    app.telemetryBox.grid(row=5, column=0, columnspan=4, padx=10)
