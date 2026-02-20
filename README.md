# Screens Manager for CustomTkinter

A lightweight screen and navigation manager for desktop applications built with CustomTkinter.  
This module provides animated screen transitions and built-in navigation patterns such as a bottom app bar and a navigation drawer.

## ✨ Features

- Screen registration and lifecycle management
- Built-in animated transitions:
  - Fade transition
  - Slide transition (left, right, up, down)
- Two navigation modes:
  - Bottom App Bar (mobile-like navigation)
  - Navigation Drawer (side menu with hamburger button)
- Swipe gesture support for opening/closing the drawer
- Highly customizable styles for navigation components
- Fully type-annotated and documented API

---

## 📦 Installation

Copy the file `screens_manager.py` into your project:

```bash
project/
├── screens_manager.py
├── main.py
```

Make sure you have `customtkinter` installed:

```bash
pip install customtkinter
```

---

## 🚀 Basic Usage

```python
import customtkinter as ctk
from screens_manager import *

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.geometry("500x500")

items = [
    NavItem(screen="home", label="Home", icon="🏠"),
    NavItem(screen="search", label="Search", icon="🔍"),
    NavItem(screen="profile", label="Profile", icon="👤"),
]

manager = ScreensManager(
    app,
    transition=TRANSITION_FADE,
    nav_mode=NAV_BOTTOM,
    nav_items=items,
)

manager.set_screens(initial="home")

ctk.CTkLabel(manager.home, text="Home").pack(expand=True)
ctk.CTkLabel(manager.search, text="Search").pack(expand=True)
ctk.CTkLabel(manager.profile, text="Profile").pack(expand=True)

app.mainloop()
```

---

## 🧭 Navigation Modes

### Bottom App Bar

```python
manager = ScreensManager(
    app,
    nav_mode=NAV_BOTTOM,
    nav_items=items,
    bottom_bar_style=BottomBarStyle(
        layout="icon_top",
        fg_color="#1a1a2e",
    )
)
```



https://github.com/user-attachments/assets/f297ca01-58db-4b07-aff0-6937181ace25



https://github.com/user-attachments/assets/8f499fe2-09f1-4228-9388-248dfd219102



https://github.com/user-attachments/assets/3fb86d5e-0829-4e43-a4d2-d743d39b4a70



### Navigation Drawer

```python
manager = ScreensManager(
    app,
    nav_mode=NAV_DRAWER,
    nav_items=items,
    drawer_style=DrawerStyle(
        side="left",
        header="Menu",
        enable_swipe=True,
    )
)
```


https://github.com/user-attachments/assets/008eec76-5165-43eb-85e7-17fa01fb0eda


https://github.com/user-attachments/assets/64df0030-b834-4cdc-8344-98dcfd7c3237


---

## 🎞️ Transitions

Available transitions:

- TRANSITION_NONE
- TRANSITION_FADE
- TRANSITION_SLIDE

Slide directions:

- SLIDE_LEFT
- SLIDE_RIGHT
- SLIDE_UP
- SLIDE_DOWN

```python
manager.navigate("profile", transition=TRANSITION_SLIDE, direction=SLIDE_LEFT)
```

---

## 🧩 API Overview

```python
ScreensManager(
    root,
    transition=TRANSITION_FADE,
    direction=SLIDE_LEFT,
    duration=300,
    nav_mode=NAV_NONE,
    nav_items=None,
    bottom_bar_style=None,
    drawer_style=None,
)
```

Main methods:

- set_screens(*names, initial=None)
- add_screen(name)
- navigate(name, transition=None, direction=None, duration=None)
- on_navigate(callback)

---

## 🎨 Styling

### BottomBarStyle

```python
BottomBarStyle(
    height=60,
    fg_color=None,
    button_width=80,
    button_height=48,
    layout="icon_top",
)
```

### DrawerStyle

```python
DrawerStyle(
    width=220,
    side="left",
    enable_swipe=True,
    header="Menu",
    layout="icon_left",
)
```

---

## ⚠️ Notes

- Screen names must match NavItem.screen values.
- For NAV_BOTTOM and NAV_DRAWER, nav_items is required.
- Avoid calling navigate() while an animation is running.
- The manager attaches frames as attributes (e.g., manager.home, manager.profile).

---

## 🙌 Credits

Built on top of the CustomTkinter framework.
