import customtkinter as ctk


def change_scaling_event(new_scaling):
    new_scaling_float = int(new_scaling.replace("%", "")) / 97
    ctk.set_widget_scaling(new_scaling_float)


def view(app):
    """edit UI"""
    app.clear_frame()
    app.scaling_label = ctk.CTkLabel(
        app.frame,
        text="UI Scaling:",
        anchor="w",
    )
    app.scaling_label.grid(row=5, column=0, padx=20, pady=(10, 0))

    app.scaling_optionemenu = ctk.CTkOptionMenu(
        app.frame,
        values=["78%", "90%", "100%", "110%", "120%"],
        command=change_scaling_event,
    )

    app.scaling_optionemenu.grid(
        row=6,
        column=0,
        padx=18,
        pady=(8, 20),
        sticky="s",
    )
