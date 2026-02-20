import customtkinter as ctk

# ─────────────────────────────────────────────
#  Transition Constants
# ─────────────────────────────────────────────
TRANSITION_NONE  = "none"
TRANSITION_FADE  = "fade"
TRANSITION_SLIDE = "slide"

SLIDE_LEFT  = "left"
SLIDE_RIGHT = "right"
SLIDE_UP    = "up"
SLIDE_DOWN  = "down"

# ─────────────────────────────────────────────
#  Navigation Constants
# ─────────────────────────────────────────────
NAV_NONE   = "none"           # User manages their own navigation triggers
NAV_BOTTOM = "bottom_bar"     # Integrated Bottom App Bar
NAV_DRAWER = "drawer"         # Integrated Navigation Drawer


class NavItem:
    """
    Represents a navigation item (button) for the Bottom Bar or Drawer.

    Attributes:
        screen (str): The name/ID of the screen this item navigates to.
        label (str): Text displayed on the button.
        icon (str): Character or emoji used as an icon (e.g., "🏠", "⚙️").
        style (dict): Kwargs passed to CTkButton for base appearance.
        active_style (dict): Kwargs applied only when the screen is active.
    """
    def __init__(
        self,
        screen: str,
        label: str = "",
        icon: str = "",
        style: dict | None = None,
        active_style: dict | None = None,
    ):
        self.screen       = screen
        self.label        = label
        self.icon         = icon
        self.style        = style or {}
        self.active_style = active_style or {}


class BottomBarStyle:
    """
    Configuration for the visual appearance of the Bottom App Bar.

    Attributes:
        height (int): Bar height in pixels. Default: 60.
        fg_color (str | list): Background color. Supports [light, dark] modes.
        corner_radius (int): Corner radius of the bar.
        padx (int): Internal horizontal padding for buttons.
        pady (int): Internal vertical padding for the bar.
        icon_font (tuple): Font used for icons.
        label_font (tuple): Font used for text labels.
        button_width (int): Fixed width for each button.
        button_height (int): Fixed height for each button.
        layout (str): Display mode: "icon_only", "label_only", or "icon_top".
    """
    def __init__(
        self,
        height: int = 60,
        fg_color: str | list | None = None,
        corner_radius: int = 0,
        padx: int = 10,
        pady: int = 6,
        icon_font: tuple = ("Arial", 20),
        label_font: tuple = ("Arial", 10),
        button_width: int = 80,
        button_height: int = 48,
        layout: str = "icon_top",
    ):
        self.height        = height
        self.fg_color      = fg_color
        self.corner_radius = corner_radius
        self.padx          = padx
        self.pady          = pady
        self.icon_font     = icon_font
        self.label_font    = label_font
        self.button_width  = button_width
        self.button_height = button_height
        self.layout        = layout


class DrawerStyle:
    """
    Configuration for the visual appearance of the Navigation Drawer.

    Attributes:
        width (int): Drawer width in pixels.
        side (str): Side to slide from: "left" or "right".
        fg_color (str | list): Background color of the drawer.
        overlay_color (str | list): Color of the semi-transparent background.
        corner_radius (int): Corner radius of the drawer frame.
        duration (int): Animation duration in milliseconds.
        show_hamburger (bool): Whether to display a floating hamburger button.
        hamburger_style (dict): Customization for the hamburger button.
        enable_swipe (bool): Allows opening/closing via edge dragging.
        swipe_threshold (int): Minimum pixels to trigger a swipe action.
        icon_font (tuple): Font for item icons.
        label_font (tuple): Font for item labels.
        button_height (int): Height of each drawer item.
        layout (str): Display mode: "icon_left", "label_only", or "icon_only".
        item_padx (int): Horizontal padding for items.
        header (str): Optional header text at the top.
        header_font (tuple): Font for the header text.
        header_style (dict): Kwargs for the header label customization.
    """
    def __init__(
        self,
        width: int = 220,
        side: str = "left",
        fg_color: str | list | None = None,
        overlay_color: str | list = "#000000",
        corner_radius: int = 0,
        duration: int = 250,
        show_hamburger: bool = True,
        hamburger_style: dict | None = None,
        enable_swipe: bool = True,
        swipe_threshold: int = 40,
        icon_font: tuple = ("Arial", 18),
        label_font: tuple = ("Arial", 13),
        button_height: int = 44,
        layout: str = "icon_left",
        item_padx: int = 12,
        header: str | None = None,
        header_font: tuple = ("Arial", 15, "bold"),
        header_style: dict | None = None,
    ):
        self.width           = width
        self.side            = side
        self.fg_color        = fg_color
        self.overlay_color   = overlay_color
        self.corner_radius   = corner_radius
        self.duration        = duration
        self.show_hamburger  = show_hamburger
        self.hamburger_style = hamburger_style or {}
        self.enable_swipe    = enable_swipe
        self.swipe_threshold = swipe_threshold
        self.icon_font       = icon_font
        self.label_font      = label_font
        self.button_height   = button_height
        self.layout          = layout
        self.item_padx       = item_padx
        self.header          = header
        self.header_font     = header_font
        self.header_style    = header_style or {}


class ScreensManager:
    """
    Manages application screens with built-in transitions and navigation components.

    This class handles switching between frames (screens) with animations and
    optionally provides a Bottom Bar or a Navigation Drawer.
    """

    def __init__(
        self,
        root: ctk.CTk,
        transition: str = TRANSITION_FADE,
        direction: str = SLIDE_LEFT,
        duration: int = 300,
        nav_mode: str = NAV_NONE,
        nav_items: list[NavItem] | None = None,
        bottom_bar_style: BottomBarStyle | None = None,
        drawer_style: DrawerStyle | None = None,
    ):
        """
        Initializes the ScreensManager.

        Args:
            root: The main CTk window.
            transition: Default transition type (fade, slide, none).
            direction: Default slide direction.
            duration: Animation duration in ms.
            nav_mode: Type of built-in navigation to use.
            nav_items: List of NavItem objects for the navigation menu.
            bottom_bar_style: Custom style for the Bottom Bar.
            drawer_style: Custom style for the Navigation Drawer.
        """
        self.root       = root
        self.transition = transition
        self.direction  = direction
        self.duration   = duration
        self.nav_mode   = nav_mode
        self.nav_items  = nav_items or []

        self.bottom_bar_style = bottom_bar_style or BottomBarStyle()
        self.drawer_style     = drawer_style     or DrawerStyle()

        self.__screens: dict[str, ctk.CTkFrame] = {}
        self.current: str | None = None
        self._on_navigate_callbacks: list = []
        self._animating = False

        # Drawer Internal State
        self._drawer_frame:   ctk.CTkFrame          | None = None
        self._drawer_overlay: ctk.CTkFrame          | None = None
        self._drawer_scroll:  ctk.CTkScrollableFrame | None = None
        self._drawer_open     = False
        self._drawer_buttons: dict[str, ctk.CTkButton] = {}
        self._hamburger_btn:  ctk.CTkButton | None = None
        self._swipe_start_x   = 0

        # Bottom Bar Internal State
        self._bottom_bar: ctk.CTkFrame | None = None
        self._bar_buttons: dict[str, ctk.CTkButton] = {}

        # Base Layout Configuration
        # Screens are contained in _content_frame to separate them from overlay elements
        self._content_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        self._content_frame.grid(row=0, column=0, sticky=ctk.NSEW)
        self._content_frame.grid_rowconfigure(0, weight=1)
        self._content_frame.grid_columnconfigure(0, weight=1)

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    # ──────────────────────────────────────────────────────────────────────
    #  Screen Management
    # ──────────────────────────────────────────────────────────────────────

    def set_screens(self, *names: str, initial: str | None = None):
        """
        Initializes the stack of screens. Replaces any existing screens.

        Args:
            *names: Variable list of screen names.
            initial: The name of the screen to display first.
        """
        # Automatically extract names from nav_items if names are not provided
        if not names and self.nav_items:
            names = tuple(item.screen for item in self.nav_items)

        if not names:
            raise ValueError("Provide at least one screen name or define nav_items.")
        if initial and initial not in names:
            raise ValueError(f"Initial screen '{initial}' not found in provided names.")

        # Cleanup existing attributes and widgets
        for name in list(self.__screens.keys()):
            if hasattr(self, name):
                delattr(self, name)
        for screen in self.__screens.values():
            screen.destroy()
        self.__screens.clear()

        for name in names:
            self.add_screen(name)

        self._build_nav()

        if initial:
            self.navigate(initial, transition=TRANSITION_NONE)

    def add_screen(self, name: str):
        """Creates a new frame for the given screen name."""
        if name in self.__screens:
            raise ValueError(f"Screen '{name}' already exists.")
        
        frame = ctk.CTkFrame(self._content_frame)
        frame.grid(row=0, column=0, sticky=ctk.NSEW)
        frame.grid_forget()
        self.__screens[name] = frame
        setattr(self, name, frame)

    # ──────────────────────────────────────────────────────────────────────
    #  Navigation Logic
    # ──────────────────────────────────────────────────────────────────────

    def navigate(
        self,
        name: str,
        transition: str | None = None,
        direction: str | None = None,
        duration: int | None = None,
    ):
        """
        Navigates to a specific screen with optional animation overrides.

        Args:
            name: Destination screen name.
            transition: Animation type. Defaults to self.transition.
            direction: Slide direction. Defaults to self.direction.
            duration: Animation duration. Defaults to self.duration.
        """
        if name not in self.__screens:
            raise KeyError(f"Screen '{name}' does not exist. Available: {list(self.__screens.keys())}")
        
        if self._animating or name == self.current:
            return

        t  = transition if transition is not None else self.transition
        d  = direction  if direction  is not None else self.direction
        ms = duration   if duration   is not None else self.duration

        incoming = self.__screens[name]
        outgoing = self.__screens.get(self.current) if self.current else None

        self.current = name

        # Execute registered navigation callbacks
        for cb in self._on_navigate_callbacks:
            cb(name)

        self._update_nav_active(name)

        if t == TRANSITION_FADE:
            self._fade(incoming, outgoing, ms)
        elif t == TRANSITION_SLIDE:
            self._slide(incoming, outgoing, d, ms)
        else:
            self._instant(incoming, outgoing)

    def on_navigate(self, callback):
        """Registers a callback function to be called on every navigation event."""
        self._on_navigate_callbacks.append(callback)

    # ──────────────────────────────────────────────────────────────────────
    #  Navigation UI Builders
    # ──────────────────────────────────────────────────────────────────────

    def _build_nav(self):
        """Dispatches navigation construction based on nav_mode."""
        if self.nav_mode == NAV_BOTTOM:
            self._build_bottom_bar()
        elif self.nav_mode == NAV_DRAWER:
            self._build_drawer()

    # — Bottom App Bar Construction ────────────────────────────────────────

    def _build_bottom_bar(self):
        """Creates and places the Bottom Navigation Bar."""
        s = self.bottom_bar_style

        bar_kw = {"height": s.height}
        if s.fg_color:
            bar_kw["fg_color"] = s.fg_color
        if s.corner_radius:
            bar_kw["corner_radius"] = s.corner_radius

        self._bottom_bar = ctk.CTkFrame(self.root, **bar_kw)
        self._bottom_bar.grid(row=1, column=0, sticky="ew")
        self.root.grid_rowconfigure(1, weight=0)

        # Horizontal scrollable container for navigation buttons
        scroll_kw: dict = {
            "orientation": "horizontal",
            "height": s.height,
            "fg_color": "transparent",
        }
        if s.fg_color:
            scroll_kw["scrollbar_fg_color"] = s.fg_color
        
        self._bar_scroll = ctk.CTkScrollableFrame(self._bottom_bar, **scroll_kw)
        self._bar_scroll.pack(fill="both", expand=True)

        # Enable horizontal scrolling with mouse wheel
        self._bar_scroll.bind("<MouseWheel>",    self._bar_on_mousewheel)
        self._bar_scroll.bind("<Button-4>",      self._bar_on_mousewheel)
        self._bar_scroll.bind("<Button-5>",      self._bar_on_mousewheel)

        self._bar_buttons.clear()

        for item in self.nav_items:
            text = self._resolve_button_text(item, s.layout, s.icon_font, s.label_font)

            btn_kw: dict = {
                "width":  s.button_width,
                "height": s.button_height,
                "text":   text,
                **item.style,
            }

            btn = ctk.CTkButton(
                self._bar_scroll,
                command=lambda n=item.screen: self.navigate(n),
                **btn_kw,
            )
            btn.pack(side="left", padx=s.padx, pady=s.pady)
            self._bar_buttons[item.screen] = btn

    def _bar_on_mousewheel(self, event):
        """Redirects vertical scroll events to horizontal scroll for the bottom bar."""
        canvas = self._bar_scroll._parent_canvas
        if event.num == 4:
            canvas.xview_scroll(-1, "units")
        elif event.num == 5:
            canvas.xview_scroll(1, "units")
        else:
            canvas.xview_scroll(int(-event.delta / 120), "units")

    @staticmethod
    def _resolve_button_text(item: NavItem, layout: str, icon_font: tuple, label_font: tuple) -> str:
        """Determines the string content of a button based on the layout style."""
        if layout == "icon_only":
            return item.icon
        if layout == "label_only":
            return item.label
        
        # icon_top: Icon and Label separated by newline
        parts = []
        if item.icon: parts.append(item.icon)
        if item.label: parts.append(item.label)
        return "\n".join(parts)

    # — Navigation Drawer Construction ─────────────────────────────────────

    def _build_drawer(self):
        """Initializes components required for the Navigation Drawer."""
        s = self.drawer_style

        self._hamburger_btn = None
        if s.show_hamburger:
            ham_kw: dict = {
                "text": "☰",
                "width": 36,
                "height": 36,
                "fg_color": ["gray75", "gray25"],
                "text_color": ["gray10", "gray90"],
                "hover_color": ["gray65", "gray35"],
                "command": self.open_drawer,
                **s.hamburger_style,
            }
            self._hamburger_btn = ctk.CTkButton(self.root, **ham_kw)
            
            # Place button floating over content
            self._hamburger_btn.place(
                x=10 if s.side == "left" else 0,
                y=10,
                relx=0 if s.side == "left" else 1,
                anchor="nw" if s.side == "left" else "ne",
            )
            self._hamburger_btn.lift()

        if s.enable_swipe:
            self.root.bind("<ButtonPress-1>",   self._on_swipe_start)
            self.root.bind("<ButtonRelease-1>",  self._on_swipe_end)

    def open_drawer(self):
        """Animates the drawer opening."""
        if self._drawer_open or self._animating:
            return
        
        self._drawer_open = True
        s = self.drawer_style
        w = self.root.winfo_width()

        # Create semi-transparent overlay
        self._drawer_overlay = ctk.CTkFrame(self.root, fg_color=s.overlay_color, corner_radius=0)
        self._drawer_overlay.place(x=0, y=0, relwidth=1, relheight=1)
        self._drawer_overlay.bind("<Button-1>", lambda _: self.close_drawer())

        # Main drawer container
        drawer_kw: dict = {"width": s.width}
        if s.fg_color:
            drawer_kw["fg_color"] = s.fg_color
        if s.corner_radius:
            drawer_kw["corner_radius"] = s.corner_radius

        self._drawer_frame = ctk.CTkFrame(self._drawer_overlay, **drawer_kw)
        self._drawer_frame.place(relheight=1, x=-s.width if s.side == "left" else w, y=0)
        
        self._drawer_overlay.lift()
        self._drawer_frame.lift()

        # Optional Header
        if s.header:
            hdr_kw: dict = {"text": s.header, "font": s.header_font, "anchor": "w", **s.header_style}
            ctk.CTkLabel(self._drawer_frame, **hdr_kw).pack(fill="x", padx=s.item_padx, pady=(16, 8))
            ctk.CTkFrame(self._drawer_frame, height=1, fg_color="gray50").pack(fill="x", padx=s.item_padx, pady=(0, 8))

        # Scrollable area for menu items
        scroll_kw: dict = {"fg_color": "transparent"}
        if s.fg_color:
            scroll_kw["scrollbar_fg_color"] = s.fg_color
        
        self._drawer_scroll = ctk.CTkScrollableFrame(self._drawer_frame, **scroll_kw)
        self._drawer_scroll.pack(fill="both", expand=True, pady=(0, 8))

        # Populating items
        self._drawer_buttons.clear()
        for item in self.nav_items:
            text = self._resolve_drawer_text(item, s.layout)
            btn_kw: dict = {"text": text, "height": s.button_height, "anchor": "w", **item.style}
            
            if item.screen == self.current and item.active_style:
                btn_kw.update(item.active_style)

            btn = ctk.CTkButton(
                self._drawer_scroll,
                command=lambda n=item.screen: (self.close_drawer(), self.navigate(n)),
                **btn_kw,
            )
            btn.pack(fill="x", padx=s.item_padx, pady=2)
            self._drawer_buttons[item.screen] = btn

        # Animation Trigger
        start_x = -s.width if s.side == "left" else w
        end_x   = 0        if s.side == "left" else w - s.width
        steps   = max(10, s.duration // 16)
        step_ms = s.duration // steps
        self._animate_drawer(start_x, end_x, steps, step_ms, 0)

    def close_drawer(self):
        """Animates the drawer closing."""
        if not self._drawer_open or self._animating:
            return
        
        s = self.drawer_style
        w = self.root.winfo_width()

        start_x = 0        if s.side == "left" else w - s.width
        end_x   = -s.width if s.side == "left" else w
        steps   = max(10, s.duration // 16)
        step_ms = s.duration // steps
        self._animate_drawer(start_x, end_x, steps, step_ms, 0, closing=True)

    def _animate_drawer(self, start_x, end_x, steps, step_ms, step, closing=False):
        """Recursive step function for drawer animation."""
        progress = (step + 1) / steps
        ease     = self._ease_out(progress)
        x        = int(start_x + (end_x - start_x) * ease)

        if self._drawer_frame:
            self._drawer_frame.place_configure(x=x)

        if step + 1 < steps:
            self.root.after(
                step_ms,
                lambda: self._animate_drawer(start_x, end_x, steps, step_ms, step + 1, closing)
            )
        else:
            if closing:
                self._drawer_open = False
                if self._drawer_frame:
                    self._drawer_frame.destroy()
                    self._drawer_frame = None
                if self._drawer_overlay:
                    self._drawer_overlay.destroy()
                    self._drawer_overlay = None

    @staticmethod
    def _resolve_drawer_text(item: NavItem, layout: str) -> str:
        """Determines string content for drawer items."""
        if layout == "icon_only":
            return item.icon
        if layout == "label_only":
            return item.label
        
        # icon_left: Icon + Space + Label
        parts = []
        if item.icon: parts.append(item.icon)
        if item.label: parts.append(item.label)
        return "  ".join(parts)

    # — Swipe Handling ────────────────────────────────────────────────────

    def _on_swipe_start(self, event):
        """Records the initial X position of a touch/click."""
        self._swipe_start_x = event.x_root

    def _on_swipe_end(self, event):
        """Calculates distance and triggers drawer if threshold is met."""
        if self._animating:
            return
        
        s     = self.drawer_style
        delta = event.x_root - self._swipe_start_x
        w     = self.root.winfo_width()

        if s.side == "left":
            if not self._drawer_open and delta > s.swipe_threshold and self._swipe_start_x < 40:
                self.open_drawer()
            elif self._drawer_open and delta < -s.swipe_threshold:
                self.close_drawer()
        else:
            if not self._drawer_open and delta < -s.swipe_threshold and self._swipe_start_x > w - 40:
                self.open_drawer()
            elif self._drawer_open and delta > s.swipe_threshold:
                self.close_drawer()

    # — Active State Management ───────────────────────────────────────────

    def _update_nav_active(self, name: str):
        """Refreshes the appearance of nav buttons to highlight the active screen."""
        # Update Bottom Bar buttons
        for screen, btn in self._bar_buttons.items():
            item = next((i for i in self.nav_items if i.screen == screen), None)
            if not item: continue
            
            s = self.bottom_bar_style
            text = self._resolve_button_text(item, s.layout, s.icon_font, s.label_font)
            base_kw = {"text": text, **item.style}
            
            if screen == name and item.active_style:
                base_kw.update(item.active_style)
            
            try: btn.configure(**base_kw)
            except: pass

        # Update Drawer buttons (if drawer exists)
        for screen, btn in self._drawer_buttons.items():
            item = next((i for i in self.nav_items if i.screen == screen), None)
            if not item: continue
            
            s    = self.drawer_style
            text = self._resolve_drawer_text(item, s.layout)
            base_kw = {"text": text, **item.style}
            
            if screen == name and item.active_style:
                base_kw.update(item.active_style)
            
            try: btn.configure(**base_kw)
            except: pass

    # ──────────────────────────────────────────────────────────────────────
    #  Animation Engines
    # ──────────────────────────────────────────────────────────────────────

    def _instant(self, incoming, outgoing):
        """Switch screens immediately without animation."""
        if outgoing:
            outgoing.grid_forget()
        incoming.grid(row=0, column=0, sticky=ctk.NSEW)
        self._content_frame.update_idletasks()

    # — Fade Transition ────────────────────────────────────────────────────

    def _fade(self, incoming, outgoing, duration):
        """Initiates a cross-fade transition."""
        self._animating = True
        steps   = max(10, duration // 16)
        step_ms = duration // steps

        self._reset_frame_color(incoming, 0.0)

        if outgoing:
            self._reset_frame_color(outgoing, 1.0)
            self._fade_out(outgoing, incoming, steps, step_ms, 1.0)
        else:
            incoming.grid(row=0, column=0, sticky=ctk.NSEW)
            self._fade_in(incoming, steps, step_ms, 0.0)

    def _fade_out(self, outgoing, incoming, steps, step_ms, alpha):
        """Recursive step for fading out a frame."""
        alpha = round(alpha - 1 / steps, 3)
        try: outgoing.configure(fg_color=self._alpha_color(alpha))
        except: pass

        if alpha > 0:
            self.root.after(step_ms, lambda: self._fade_out(outgoing, incoming, steps, step_ms, alpha))
        else:
            outgoing.grid_forget()
            try: outgoing.configure(fg_color=self._get_base_color())
            except: pass
            incoming.grid(row=0, column=0, sticky=ctk.NSEW)
            self._fade_in(incoming, steps, step_ms, 0.0)

    def _fade_in(self, incoming, steps, step_ms, alpha):
        """Recursive step for fading in a frame."""
        alpha = round(alpha + 1 / steps, 3)
        try: incoming.configure(fg_color=self._alpha_color(alpha))
        except: pass

        if alpha < 1:
            self.root.after(step_ms, lambda: self._fade_in(incoming, steps, step_ms, alpha))
        else:
            try: incoming.configure(fg_color=self._get_base_color())
            except: pass
            self._animating = False
            self.root.update_idletasks()

    def _reset_frame_color(self, frame, alpha):
        """Utility to apply alpha-based background color."""
        try: frame.configure(fg_color=self._alpha_color(alpha))
        except: pass

    @staticmethod
    def _get_base_color() -> str:
        """Returns the default CTk background color based on the current theme."""
        mode = ctk.get_appearance_mode()
        return "gray86" if mode == "Light" else "gray17"

    @staticmethod
    def _alpha_color(alpha: float) -> str:
        """Calculates a hex color representing a fade between background and foreground."""
        mode = ctk.get_appearance_mode()
        if mode == "Light":
            base, limit = 219, 180
        else:
            base, limit = 43, 80
        value = int(base * alpha + limit * (1 - alpha))
        return f"#{value:02x}{value:02x}{value:02x}"

    # — Slide Transition ───────────────────────────────────────────────────

    def _slide(self, incoming, outgoing, direction, duration):
        """Initiates a slide-in transition."""
        self._animating = True
        w = self._content_frame.winfo_width()
        h = self._content_frame.winfo_height()
        steps   = max(10, duration // 16)
        step_ms = duration // steps

        offsets = {
            SLIDE_LEFT:  (-w, 0,  w, 0),
            SLIDE_RIGHT: ( w, 0, -w, 0),
            SLIDE_UP:    (0, -h,  0, h),
            SLIDE_DOWN:  (0,  h,  0, -h),
        }
        ix, iy, ox, oy = offsets.get(direction, offsets[SLIDE_LEFT])

        incoming.place(x=ix, y=iy, relwidth=1, relheight=1)
        if outgoing:
            outgoing.place(x=0, y=0, relwidth=1, relheight=1)
            outgoing.lift()
        incoming.lift()

        self._slide_step(incoming, outgoing, ix, iy, ox, oy, steps, step_ms, 0)

    def _slide_step(self, incoming, outgoing, ix, iy, ox, oy, steps, step_ms, step):
        """Recursive step for slide animation."""
        progress = (step + 1) / steps
        ease     = self._ease_out(progress)

        incoming.place(x=int(ix * (1 - ease)), y=int(iy * (1 - ease)), relwidth=1, relheight=1)
        if outgoing:
            outgoing.place(x=int(ox * ease), y=int(oy * ease), relwidth=1, relheight=1)

        if step + 1 < steps:
            self.root.after(step_ms, lambda: self._slide_step(
                incoming, outgoing, ix, iy, ox, oy, steps, step_ms, step + 1
            ))
        else:
            incoming.place_forget()
            incoming.grid(row=0, column=0, sticky=ctk.NSEW)
            if outgoing:
                outgoing.place_forget()
                outgoing.grid_forget()
            self._animating = False
            self.root.update_idletasks()

    @staticmethod
    def _ease_out(t: float) -> float:
        """Quadratic ease-out formula for smoother movement."""
        return 1 - (1 - t) ** 2