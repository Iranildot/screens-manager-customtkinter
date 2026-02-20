import customtkinter as ctk
from screens_manager import *

# Set global appearance mode
ctk.set_appearance_mode("dark")

# Create application window
app = ctk.CTk()
app.geometry("1200x700")
app.title("Navigation Drawer Example")

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

# Initialize the screen manager with a navigation drawer
manager = ScreensManager(
    app,
    transition=TRANSITION_SLIDE,
    direction=SLIDE_LEFT,
    duration=250,
    nav_mode=NAV_DRAWER,
    nav_items=items,
    drawer_style=DrawerStyle(
        width=230,
        side="left",  # Change to "right" to test the other side
        fg_color="#1a1a2e",
        overlay_color="#111111",
        duration=280,
        show_hamburger=True,
        hamburger_style={"fg_color": "transparent", "text_color": "white", "hover_color": "gray25"},
        enable_swipe=True,
        swipe_threshold=35,
        layout="icon_left",
        header="Menu",
        header_font=("Arial", 16, "bold"),
        header_style={"text_color": "#4FC3F7"},
        item_padx=16,
        button_height=46,
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