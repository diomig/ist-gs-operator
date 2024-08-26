import customtkinter as ctk

from utils import colors, fonts


def change_scaling_event(new_scaling):
    new_scaling_float = int(new_scaling.replace("%", "")) / 97
    ctk.set_widget_scaling(new_scaling_float)


def preferences_create(app):
    """edit UI"""
    #     ctk.set_appearance_mode("light")


    app.scaling_label = ctk.CTkLabel(
        app.frame,
        text="Scaling",
        font=fonts.label,
        anchor="w",
    )

    app.scaling_optionemenu = ctk.CTkOptionMenu(
        app.frame,
        values=["78%", "90%", "100%", "110%", "120%"],
        command=change_scaling_event,
        width=100,
    )

    app.themeLabel = ctk.CTkLabel(
        app.frame,
        text="Theme",
        font=fonts.label,
    )

    app.themeOption = ctk.CTkOptionMenu(
        app.frame,
        values=["dark ☾", "light"],
        command=lambda thm: ctk.set_appearance_mode(thm),
    )

    app.darkmode = ctk.get_appearance_mode() == "Dark"

    def change_theme():
        app.darkmode = not app.darkmode
        mode = "dark" if app.darkmode else "light"
        icon = "☀︎" if app.darkmode else "☾"
        action = f"Change to {'Light' if app.darkmode else 'Dark'} mode"
        ctk.set_appearance_mode(mode)
        app.themeButton.configure(text=icon)
        app.themeMode.configure(text=action)
        print(ctk.get_appearance_mode())

    app.themeButton = ctk.CTkButton(
        app.frame,
        text="☀︎" if app.darkmode else "☾",
        font=fonts.icon,
        command=change_theme,
        width=20,
    )
    app.themeMode = ctk.CTkLabel(
        app.frame,
        text=f"Change to {'Light' if app.darkmode else 'Dark'} mode",
        font=fonts.units,
        text_color=colors.units,
    )


def preferences(app):
    app.clear_frame()
    app.themeLabel.grid(row=3, column=0, padx=50, pady=50)
    # app.themeOption.grid()
    app.themeButton.grid(row=3, column=1, pady=50, sticky="w")
    app.themeMode.grid(row=3, column=2, padx=20)
    app.scaling_label.grid(row=5, column=0, padx=20, pady=(10, 0))
    app.scaling_optionemenu.grid(row=5, column=1, columnspan=3, sticky="w")
