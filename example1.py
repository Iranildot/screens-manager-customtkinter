import customtkinter as ctk
from screens_manager import *

# Set global appearance mode
ctk.set_appearance_mode("dark")

# Create application window
app = ctk.CTk()
app.geometry("1200x700")
app.title("Bottom App Bar Example")

# Shared navigation items
items = [
    NavItem(
        screen="home",
        label="Home",
        icon="🏠",
        style={"fg_color": "transparent", "text_color": "gray70", "hover_color": "gray25"},
        active_style={"text_color": "#4FC3F7", "fg_color": "transparent"},
    ),
    NavItem(
        screen="search",
        label="Search",
        icon="🔍",
        style={"fg_color": "transparent", "text_color": "gray70", "hover_color": "gray25"},
        active_style={"text_color": "#4FC3F7", "fg_color": "transparent"},
    ),
    NavItem(
        screen="profile",
        label="Profile",
        icon="👤",
        style={"fg_color": "transparent", "text_color": "gray70", "hover_color": "gray25"},
        active_style={"text_color": "#4FC3F7", "fg_color": "transparent"},
    ),
]

# Initialize the screen manager with bottom navigation
manager = ScreensManager(
    app,
    transition=TRANSITION_SLIDE,
    direction=SLIDE_RIGHT,
    duration=250,
    nav_mode=NAV_BOTTOM,
    nav_items=items,
    bottom_bar_style=BottomBarStyle(
        height=64,
        layout="icon_top",
        fg_color="#1a1a2e",
        button_width=90,
        button_height=52,
        icon_font=("Arial", 20),
        label_font=("Arial", 10),
    ),
)

# Register screens based on nav_items
manager.set_screens(initial="home")

# Populate screen content
ctk.CTkLabel(manager.home,    text="🏠 Home",   font=("Arial", 28)).pack(expand=True)
ctk.CTkLabel(manager.search,  text="🔍 Search", font=("Arial", 28)).pack(expand=True)
ctk.CTkLabel(manager.profile, text="👤 Profile", font=("Arial", 28)).pack(expand=True)

# Start the application loop
app.mainloop()