# main.py

import os
import sys
import tkinter as tk
from tkinter import ttk
from game import Game
from data import CLASSES, LOCATIONS, SHOP_ITEMS, GENERAL_STORE_ITEMS, COMPANIONS, SLUICE_HONEYS, GAME_STORY
from PIL import Image, ImageTk


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class SluiceBoxJunkyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sluice Box Junky")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        self.game = Game()

        self.creation_frame = None
        self.game_frame = None
        self.notebook = None

        self.name_entry = None
        self.story_text = None
        self.class_var = tk.StringVar(value="River Rat")
        self.location_var = tk.StringVar(value="Nooksack River")

        self.hero_label = None
        self.class_label = None
        self.day_label = None
        self.location_label = None
        self.location_flavor_label = None
        self.stamina_label = None
        self.gold_label = None
        self.inventory_label = None
        self.progress_label = None
        self.equipment_label = None
        self.buff_label = None
        self.result_label = None
        self.storage_listbox = None
        self.cooler_listbox = None
        self.loot_log = None
        self.inventory_text = None
        self.cooler_text = None
        self.storage_text = None
        self.gear_text = None
        self.cooler_text_inventory = None
        self.store_status_label = None
        self.tabs = {}
        self.nav_buttons = {}
        self.current_tab_name = "River"

        self.tab_colors = {
            "River": "#1f3b73",
            "Inventory / Gear": "#d4af37",
            "Store": "#8b1e1e",
            "Sluice Box Honeys": "#09eb41"
        }
        self.honey_image_refs = {}
        self.honey_inventory_image_label = None
        self.honey_status_label = None
        self.honey_notes_text = None

        self.pan_button = None
        self.sell_button = None
        self.rest_button = None

        self.build_character_creation_ui()

    
    def load_tk_image(self, path, size=(180, 300)):
        fallback = "assets/honeys/placeholder.png"

        resolved_path = resource_path(path)
        resolved_fallback = resource_path(fallback)

        final_path = resolved_path if os.path.exists(resolved_path) else resolved_fallback

        if not os.path.exists(final_path):
            return None

        try:
            img = Image.open(final_path)
            img = img.resize(size)
            return ImageTk.PhotoImage(img)
        except Exception:
            return None
        
    def setup_notebook_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        # Hide the default notebook tabs
        style.layout("Hidden.TNotebook.Tab", [])

    def build_tab_bar(self, parent):
        tab_bar = tk.Frame(parent, bg="#1a1a1a", bd=2, relief="ridge")
        tab_bar.pack(fill="x", pady=(0, 10))

        tab_order = ["River", "Inventory / Gear", "Store", "Sluice Box Honeys"]

        for tab_name in tab_order:
            bg_color = self.tab_colors[tab_name]
            fg_color = "black" if tab_name in ("Inventory / Gear", "Sluice Box Honeys") else "white"

            btn = tk.Button(
                tab_bar,
                text=tab_name,
                font=("Segoe UI", 13, "bold"),
                bg=bg_color,
                fg=fg_color,
                activebackground=bg_color,
                activeforeground=fg_color,
                relief="raised",
                bd=4,
                padx=20,
                pady=10,
                command=lambda name=tab_name: self.select_tab(name)
            )
            btn.pack(side="left", padx=6, pady=6)

            self.nav_buttons[tab_name] = btn

    def select_tab(self, tab_name):
        self.current_tab_name = tab_name
        self.notebook.select(self.tabs[tab_name])
        self.update_tab_bar()

    def update_tab_bar(self):
        for tab_name, btn in self.nav_buttons.items():
            if tab_name == self.current_tab_name:
                btn.config(relief="sunken", bd=5)
            else:
                btn.config(relief="raised", bd=4)

    def build_character_creation_ui(self):
        self.creation_frame = ttk.Frame(self.root, padding=20)
        self.creation_frame.pack(fill="both", expand=True)

        ttk.Label(
            self.creation_frame,
            text="Sluice Box Junky",
            font=("Arial", 24, "bold")
        ).pack(pady=(5, 15))

        top_area = ttk.Frame(self.creation_frame)
        top_area.pack(fill="both", expand=True)

        left = ttk.Frame(top_area)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = ttk.Frame(top_area)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(
            left,
            text="Create your washed-up legend.",
            font=("Arial", 12)
        ).pack(pady=(0, 15), anchor="w")

        name_frame = ttk.Frame(left)
        name_frame.pack(pady=10, anchor="w")

        ttk.Label(name_frame, text="Hero Name:").pack(side="left", padx=(0, 10))
        self.name_entry = ttk.Entry(name_frame, width=30)
        self.name_entry.pack(side="left")
        self.name_entry.insert(0, "Sluice Box Junky")

        class_frame = ttk.LabelFrame(left, text="Choose Your Class", padding=15)
        class_frame.pack(fill="x", pady=10)

        for class_name, class_data in CLASSES.items():
            ttk.Radiobutton(
                class_frame,
                text=f"{class_name} - {class_data['description']}",
                variable=self.class_var,
                value=class_name
            ).pack(anchor="w", pady=4)

        ttk.Button(
            left,
            text="Start Digging",
            command=self.start_game
        ).pack(pady=20, anchor="w")

        story_frame = ttk.LabelFrame(right, text=GAME_STORY["title"], padding=10)
        story_frame.pack(fill="both", expand=True)

        self.story_text = tk.Text(story_frame, wrap="word", height=20)
        self.story_text.insert("1.0", GAME_STORY["intro"])
        self.story_text.config(state="disabled")
        self.story_text.pack(fill="both", expand=True)

    def start_game(self):
        hero_name = self.name_entry.get()
        hero_class = self.class_var.get()

        self.game.create_hero(hero_name, hero_class)

        self.creation_frame.destroy()
        self.build_game_ui()
        self.update_display()
        self.log_message(
            f"{self.game.hero.name} the {self.game.hero.hero_class} hits the dirt running."
        )

    def build_game_ui(self):
        container = ttk.Frame(self.root)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, highlightthickness=0)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.game_frame = ttk.Frame(canvas, padding=10)

        canvas_window = canvas.create_window(
            (0, 0),
            window=self.game_frame,
            anchor="nw"
    )

        def _update_scrollregion(event):
            canvas.configure(scrollregion=canvas.bbox("all"))

        def _resize_frame_to_canvas(event):
            canvas.itemconfigure(canvas_window, width=event.width)

        self.game_frame.bind("<Configure>", _update_scrollregion)
        canvas.bind("<Configure>", _resize_frame_to_canvas)

        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        canvas.configure(yscrollcommand=scrollbar.set)

        ttk.Label(
            self.game_frame,
            text="Sluice Box Junky",
            font=("Arial", 20, "bold")
        ).pack(pady=(0, 10))

        self.setup_notebook_style()
        self.build_tab_bar(self.game_frame)

        self.notebook = ttk.Notebook(self.game_frame, style="Hidden.TNotebook")
        self.notebook.pack(fill="both", expand=True)

        river_tab = ttk.Frame(self.notebook, padding=10)
        inventory_tab = ttk.Frame(self.notebook, padding=10)
        store_tab = ttk.Frame(self.notebook, padding=10)
        honey_tab = ttk.Frame(self.notebook, padding=10)

        self.tabs = {
            "River": river_tab,
            "Inventory / Gear": inventory_tab,
            "Store": store_tab,
            "Sluice Box Honeys": honey_tab
        }

        self.notebook.add(river_tab, text="River")
        self.notebook.add(inventory_tab, text="Inventory / Gear")
        self.notebook.add(store_tab, text="Store")
        self.notebook.add(honey_tab, text="Sluice Box Honeys")

        self.build_river_tab(river_tab)
        self.build_inventory_tab(inventory_tab)
        self.build_store_tab(store_tab)
        self.build_honey_tab(honey_tab)

        self.select_tab("River")

    def build_river_tab(self, parent):
        left = ttk.Frame(parent)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = ttk.Frame(parent)
        right.pack(side="left", fill="both", expand=True)

        info_frame = ttk.Frame(left)
        info_frame.pack(fill="x", pady=5)

        self.hero_label = ttk.Label(info_frame, text="")
        self.hero_label.pack(anchor="w")

        self.class_label = ttk.Label(info_frame, text="")
        self.class_label.pack(anchor="w")

        self.day_label = ttk.Label(info_frame, text="")
        self.day_label.pack(anchor="w")

        self.location_label = ttk.Label(info_frame, text="")
        self.location_label.pack(anchor="w")

        self.location_flavor_label = ttk.Label(info_frame, text="")
        self.location_flavor_label.pack(anchor="w", pady=(0, 5))

        self.stamina_label = ttk.Label(info_frame, text="")
        self.stamina_label.pack(anchor="w")

        self.gold_label = ttk.Label(info_frame, text="")
        self.gold_label.pack(anchor="w")

        self.inventory_label = ttk.Label(info_frame, text="")
        self.inventory_label.pack(anchor="w")

        self.progress_label = ttk.Label(info_frame, text="", justify="left")
        self.progress_label.pack(anchor="w", pady=(6, 6))

        self.equipment_label = ttk.Label(info_frame, text="", justify="left")
        self.equipment_label.pack(anchor="w", pady=(8, 8))

        self.buff_label = ttk.Label(info_frame, text="", justify="left")
        self.buff_label.pack(anchor="w", pady=(0, 10))

        location_frame = ttk.LabelFrame(left, text="Choose Location", padding=10)
        location_frame.pack(fill="x", pady=10)

        location_menu = ttk.OptionMenu(
            location_frame,
            self.location_var,
            self.game.current_location,
            *LOCATIONS.keys(),
            command=self.change_location
        )
        location_menu.pack(anchor="w")

        button_frame = ttk.Frame(left)
        button_frame.pack(pady=10)

        self.pan_button = ttk.Button(button_frame, text="Pan for Gold", command=self.start_pan)
        self.pan_button.pack(side="left", padx=5)

        self.sell_button = ttk.Button(button_frame, text="Sell Inventory", command=self.sell_inventory)
        self.sell_button.pack(side="left", padx=5)

        self.rest_button = ttk.Button(button_frame, text="Rest for the Night", command=self.rest_hero)
        self.rest_button.pack(side="left", padx=5)

        self.pay_bail_button = ttk.Button(
            button_frame,
            text="Pay Toward Bail",
            command=self.pay_bail
)
        self.pay_bail_button.pack(side="left", padx=5)

        self.result_label = ttk.Label(left, text="The river awaits...", font=("Arial", 11))
        self.result_label.pack(pady=10)

        log_frame = ttk.LabelFrame(left, text="Loot Log", padding=10)
        log_frame.pack(fill="both", expand=True)

        self.loot_log = tk.Text(log_frame, height=18, state="disabled", wrap="word")
        self.loot_log.pack(fill="both", expand=True)

        river_right_top = ttk.LabelFrame(right, text="Current Loot Bag", padding=10)
        river_right_top.pack(fill="both", expand=True, pady=(0, 10))

        self.inventory_text = tk.Text(
            river_right_top,
            width=40,
            height=16,
            state="disabled",
            wrap="word"
        )
        self.inventory_text.pack(fill="both", expand=True)

        river_right_bottom = ttk.LabelFrame(right, text="Cooler Loadout (River Use Only)", padding=10)
        river_right_bottom.pack(fill="both", expand=True)

        self.cooler_text = tk.Text(
            river_right_bottom,
            width=40,
            height=12,
            state="disabled",
            wrap="word"
        )
        self.cooler_text.pack(fill="both", expand=True)

        for index in range(8):
            ttk.Button(
                river_right_bottom,
                text=f"Use Cooler Slot {index + 1}",
                command=lambda i=index: self.use_cooler_consumable(i)
            ).pack(fill="x", pady=2)

    def build_inventory_tab(self, parent):
        left = ttk.Frame(parent)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        middle = ttk.Frame(parent)
        middle.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = ttk.Frame(parent)
        right.pack(side="left", fill="both", expand=True)

        gear_frame = ttk.LabelFrame(left, text="Equipped Gear & Companion", padding=10)
        gear_frame.pack(fill="x", pady=(0, 10))

        self.gear_text = tk.Text(gear_frame, height=14, state="disabled", wrap="word")
        self.gear_text.pack(fill="both", expand=True)

        storage_frame = ttk.LabelFrame(middle, text="Home Storage Consumables", padding=10)
        storage_frame.pack(fill="both", expand=True)

        self.storage_listbox = tk.Listbox(storage_frame, height=18, exportselection=False)
        self.storage_listbox.pack(fill="both", expand=True, pady=(0, 10))

        ttk.Button(
            storage_frame,
            text="Pack Selected → Cooler",
            command=self.pack_selected_to_cooler
        ).pack(fill="x")

        cooler_frame = ttk.LabelFrame(right, text="Cooler Loadout", padding=10)
        cooler_frame.pack(fill="both", expand=True)

        self.cooler_listbox = tk.Listbox(cooler_frame, height=18, exportselection=False)
        self.cooler_listbox.pack(fill="both", expand=True, pady=(0, 10))

        ttk.Button(
            cooler_frame,
            text="← Move Selected Back to Storage",
            command=self.move_selected_to_storage
        ).pack(fill="x")

    def build_store_tab(self, parent):
        parent.columnconfigure(0, weight=2)
        parent.columnconfigure(1, weight=2)
        parent.columnconfigure(2, weight=1)
        parent.rowconfigure(0, weight=1)

        left = ttk.Frame(parent)
        left.grid(row=0, column=0, sticky="nsew", padx=(0, 10))

        middle = ttk.Frame(parent)
        middle.grid(row=0, column=1, sticky="nsew", padx=(0, 10))

        right = ttk.Frame(parent)
        right.grid(row=0, column=2, sticky="nsew")

        left.columnconfigure(0, weight=1)
        left.columnconfigure(1, weight=1)

        gear_shop_frame = ttk.LabelFrame(left, text="Gear Store", padding=10)
        gear_shop_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        gear_inner_left = ttk.Frame(gear_shop_frame)
        gear_inner_left.pack(side="left", fill="both", expand=True, padx=(0, 8))

        gear_inner_right = ttk.Frame(gear_shop_frame)
        gear_inner_right.pack(side="left", fill="both", expand=True)

        categories = list(SHOP_ITEMS.items())
        left_categories = categories[:2]
        right_categories = categories[2:]

        for category, items in left_categories:
            cat_frame = ttk.LabelFrame(gear_inner_left, text=category, padding=8)
            cat_frame.pack(fill="x", pady=6)

            for item in items:
                line = self.format_store_item_text(category, item)

                ttk.Label(cat_frame, text=line, justify="left").pack(anchor="w")
                ttk.Button(
                    cat_frame,
                    text=f"Buy / Equip {item['name']}",
                    command=lambda c=category, n=item["name"]: self.buy_shop_item(c, n)
                ).pack(anchor="w", pady=(0, 6))

        for category, items in right_categories:
            cat_frame = ttk.LabelFrame(gear_inner_right, text=category, padding=8)
            cat_frame.pack(fill="x", pady=6)

            for item in items:
                line = self.format_store_item_text(category, item)

                ttk.Label(cat_frame, text=line, justify="left").pack(anchor="w")
                ttk.Button(
                    cat_frame,
                    text=f"Buy / Equip {item['name']}",
                    command=lambda c=category, n=item["name"]: self.buy_shop_item(c, n)
                ).pack(anchor="w", pady=(0, 6))

        general_store_frame = ttk.LabelFrame(middle, text="Gas Station / Pawn Counter", padding=10)
        general_store_frame.pack(fill="both", expand=True)

        for item in GENERAL_STORE_ITEMS:
            line = self.format_general_store_item_text(item)
            ttk.Label(general_store_frame, text=line, justify="left").pack(anchor="w")
            ttk.Button(
                general_store_frame,
                text=f"Buy {item['name']}",
                command=lambda n=item["name"]: self.buy_general_store_item(n)
            ).pack(anchor="w", pady=(0, 8))

        companion_store_frame = ttk.LabelFrame(right, text="Companions", padding=10)
        companion_store_frame.pack(fill="both", expand=True)

        for companion in COMPANIONS:
            bonus_parts = []
            if companion["luck_bonus"]:
                bonus_parts.append(f"Luck +{companion['luck_bonus']}")
            if companion["capacity_bonus"]:
                bonus_parts.append(f"Capacity +{companion['capacity_bonus']}")
            if companion["sell_bonus"]:
                bonus_parts.append(f"Sell +{int(companion['sell_bonus'] * 100)}%")
            if companion["stamina_reduction"]:
                bonus_parts.append(f"Stamina Cost -{companion['stamina_reduction']}")

            bonus_text = ", ".join(bonus_parts) if bonus_parts else "No bonuses"

            line = (
                f"{companion['name']} - ${companion['cost']}\n"
                f"{companion['description']}\n"
                f"Bonuses: {bonus_text}"
            )
            ttk.Label(companion_store_frame, text=line, justify="left").pack(anchor="w")
            ttk.Button(
                companion_store_frame,
                text=f"Buy / Equip {companion['name']}",
                command=lambda n=companion["name"]: self.buy_companion(n)
            ).pack(anchor="w", pady=(0, 8))

        self.store_status_label = ttk.Label(parent, text="")
        self.store_status_label.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(10, 0))

    def build_honey_tab(self, parent):
        left = ttk.Frame(parent)
        left.pack(side="left", fill="both", expand=True, padx=(0, 10))

        right = ttk.Frame(parent)
        right.pack(side="left", fill="both", expand=True)

        info_frame = ttk.LabelFrame(left, text="Current Honey", padding=10)
        info_frame.pack(fill="x", pady=(0, 10))

        self.honey_inventory_image_label = ttk.Label(info_frame, text="No Honey Equipped")
        self.honey_inventory_image_label.pack(pady=5)

        self.honey_status_label = ttk.Label(info_frame, text="", justify="left")
        self.honey_status_label.pack(anchor="w")

        owned_frame = ttk.LabelFrame(left, text="Honey Notes", padding=10)
        owned_frame.pack(fill="both", expand=True)

        self.honey_notes_text = tk.Text(
            owned_frame,
            height=18,
            wrap="word",
            state="disabled"
    )
        self.honey_notes_text.pack(fill="both", expand=True)

        shop_frame = ttk.LabelFrame(right, text="Available Sluice Box Honeys", padding=10)
        shop_frame.pack(fill="both", expand=True)

        for honey in SLUICE_HONEYS:
            card = tk.Frame(
                shop_frame,
                bg="#2b2b2b",
                bd=3,
                relief="ridge"
        )
            card.pack(fill="x", pady=10, padx=6)

            top_row = tk.Frame(card, bg="#2b2b2b")
            top_row.pack(fill="x", pady=6)

            img = self.load_tk_image(honey.get("image", "assets/honeys/placeholder.png"))

            if img is not None:
                self.honey_image_refs[honey["name"]] = img
                tk.Label(top_row, image=img, bg="#2b2b2b").pack(side="left", padx=8, pady=4)
            else:
                tk.Label(top_row, text="[No Image]", bg="#2b2b2b", fg="white").pack(side="left", padx=8)

            text_area = tk.Frame(top_row, bg="#2b2b2b")
            text_area.pack(side="left", fill="both", expand=True, padx=8)

            tk.Label(
                text_area,
                text=honey["name"],
                font=("Segoe UI", 14, "bold"),
                fg="#ffd700",
                bg="#2b2b2b"
            ).pack(anchor="w")

            tk.Label(
                text_area,
                text=honey["description"],
                wraplength=350,
                justify="left",
                fg="white",
                bg="#2b2b2b"
            ).pack(anchor="w", pady=(4, 2))

            tk.Label(
                text_area,
                text=honey["requirement_text"],
                wraplength=350,
                justify="left",
                fg="#ffaaaa",
                bg="#2b2b2b"
            ).pack(anchor="w", pady=(0, 4))

            tk.Label(
                text_area,
                text=(
                    f"Stamina +{honey['stamina_bonus']}   "
                    f"Sell +{int(honey['sell_bonus'] * 100)}%   "
                    f"Luck +{honey['luck_bonus']}   "
                    f"Penalty -{honey['stamina_penalty']}"
            ),
                fg="#aaffaa",
                bg="#2b2b2b"
            ).pack(anchor="w", pady=(0, 6))

            tk.Button(
                text_area,
                text=f"Hire / Equip (${honey['cost']})",
                command=lambda n=honey["name"]: self.buy_honey(n),
                bg="#444",
                fg="white",
                activebackground="#666"
            ).pack(anchor="w", pady=(4, 8))

    def update_display(self):
        hero = self.game.hero
        location_data = self.game.get_location_data()
        bail_remaining = self.game.get_bail_remaining()

        self.hero_label.config(text=f"Hero: {hero.name}")
        self.class_label.config(text=f"Class: {hero.hero_class}")
        self.day_label.config(text=f"Day: {self.game.day}")
        self.location_label.config(
            text=f"Location: {self.game.current_location} | Pan Cost: {self.game.get_pan_cost()} stamina"
        )
        self.location_flavor_label.config(text=f"Area Notes: {location_data['flavor']}")
        self.stamina_label.config(text=f"Stamina: {hero.stamina}/{hero.max_stamina}")
        self.gold_label.config(
            text=f"Cash: ${hero.cash}\nBail Paid: ${hero.bail_paid}"
            )
        self.inventory_label.config(
            text=(
                f"Loot Bag: {hero.get_inventory_count()}/{hero.inventory_capacity} | "
                f"Cooler: {len(hero.cooler_consumables)}/{hero.cooler_capacity}"
            )
        )

        state_text = "Run Active"
        if self.game.game_won:
            state_text = "YOU WON"
        elif self.game.game_over:
            state_text = "RUN FAILED"

        self.progress_label.config(
            text=(
                f"Bail Goal: ${self.game.bail_target}\n"
                f"Bail Remaining: ${bail_remaining}\n"
                f"Daily Expense: ${self.game.daily_expense}\n"
                f"Run Status: {state_text}"
            )
        )

        companion_name = (
            hero.equipped_companion["name"]
            if hero.equipped_companion is not None
            else "None"
        )

        self.equipment_label.config(
            text=(
                f"Pan: {hero.equipped_pan['name']}\n"
                f"Container: {hero.equipped_container['name']}\n"
                f"Boots: {hero.equipped_boots['name']}\n"
                f"Cooler: {hero.equipped_cooler['name']}\n"
                f"Companion: {companion_name}"
            )
        )

        luck_buff_text = (
            f"Active Luck Buff: +{hero.temp_luck_bonus} for {hero.temp_luck_turns} pan(s)\n"
            if hero.temp_luck_turns > 0 else
            "Active Luck Buff: None\n"
        )

        sale_buff_text = (
            f"Next Sale Bonus: +{int(hero.next_sale_bonus * 100)}%"
            if hero.next_sale_bonus > 0 else
            "Next Sale Bonus: None"
        )

        self.buff_label.config(
            text=(
                f"Total Luck: +{hero.base_luck + hero.gear_luck_bonus + hero.companion_luck_bonus + hero.temp_luck_bonus}\n"
                f"Stamina Reduction: {hero.stamina_reduction}\n"
                f"Sell Bonus: +{int(hero.total_sell_bonus * 100)}%\n"
                f"{luck_buff_text}{sale_buff_text}"
            )
        )

        self.update_inventory_display()
        self.update_cooler_display()
        self.update_storage_display()
        self.update_gear_display()
        self.update_honey_display()

    def update_inventory_display(self):
        hero = self.game.hero

        self.inventory_text.config(state="normal")
        self.inventory_text.delete("1.0", "end")

        if not hero.inventory:
            self.inventory_text.insert("end", "Your bag is empty.\n")
        else:
            total_value = 0
            for index, (item_name, item_value) in enumerate(hero.inventory, start=1):
                self.inventory_text.insert("end", f"{index}. {item_name} - ${item_value}\n")
                total_value += item_value

            self.inventory_text.insert("end", "\n")
            self.inventory_text.insert("end", f"Unsold haul value: ${total_value}\n")

        self.inventory_text.config(state="disabled")

    def update_cooler_display(self):
        hero = self.game.hero

    # River tab text widget
        self.cooler_text.config(state="normal")
        self.cooler_text.delete("1.0", "end")

        if not hero.cooler_consumables:
            self.cooler_text.insert("end", "Your cooler is empty.\n")
        else:
            for index, item in enumerate(hero.cooler_consumables, start=1):
                self.cooler_text.insert(
                    "end",
                    f"{index}. {item['name']}\n   {item['description']}\n\n"
            )

        self.cooler_text.config(state="disabled")

    # Inventory tab listbox
        if self.cooler_listbox is not None:
            self.cooler_listbox.delete(0, tk.END)

            if not hero.cooler_consumables:
                self.cooler_listbox.insert(tk.END, "[Cooler is empty]")
            else:
                for item in hero.cooler_consumables:
                    self.cooler_listbox.insert(
                        tk.END,
                        f"{item['name']} - {item['description']}"
                )

    def update_storage_display(self):
        hero = self.game.hero

        if self.storage_listbox is None:
            return

        self.storage_listbox.delete(0, tk.END)

        if not hero.storage_consumables:
            self.storage_listbox.insert(tk.END, "[Storage is empty]")
            return

        for item in hero.storage_consumables:
            self.storage_listbox.insert(
                tk.END,
                f"{item['name']} - {item['description']}"
            )

    def update_gear_display(self):
        hero = self.game.hero
        companion_name = "None"
        companion_desc = "No companion equipped."

        if hero.equipped_companion is not None:
            companion_name = hero.equipped_companion["name"]
            companion_desc = hero.equipped_companion["description"]

        honey_name = "None"
        honey_desc = "No Sluice Box Honey equipped."
        honey_status = "Inactive"

        if hero.equipped_honey is not None:
            honey_name = hero.equipped_honey["name"]
            honey_desc = hero.equipped_honey["description"]
            honey_status = "ACTIVE" if hero.honey_is_active() else "INACTIVE"

        text = (
            f"Equipped Pan: {hero.equipped_pan['name']}\n"
            f"Equipped Container: {hero.equipped_container['name']}\n"
            f"Equipped Boots: {hero.equipped_boots['name']}\n"
            f"Equipped Cooler: {hero.equipped_cooler['name']} "
            f"({hero.cooler_capacity} slots)\n"
            f"Equipped Companion: {companion_name}\n"
            f"Companion Notes: {companion_desc}\n"
            f"Equipped Honey: {honey_name}\n"
            f"Honey Status: {honey_status}\n"
            f"Honey Notes: {honey_desc}\n\n"
            f"Owned Honeys: {', '.join(sorted(hero.owned_honeys)) if hero.owned_honeys else 'None'}\n"
            f"Owned Coolers: {', '.join(sorted(hero.owned_coolers))}\n"
            f"Owned Companions: {', '.join(sorted(hero.owned_companions)) if hero.owned_companions else 'None'}\n"
            f"Owned Pans: {', '.join(sorted(hero.owned_pans))}\n"
            f"Owned Containers: {', '.join(sorted(hero.owned_containers))}\n"
            f"Owned Boots: {', '.join(sorted(hero.owned_boots))}"
        )

        self.gear_text.config(state="normal")
        self.gear_text.delete("1.0", "end")
        self.gear_text.insert("1.0", text)
        self.gear_text.config(state="disabled")

    def update_honey_display(self):
        hero = self.game.hero

        if hero.equipped_honey is None:
            self.honey_inventory_image_label.config(image="", text="No Honey Equipped")
            self.honey_status_label.config(text="No Sluice Box Honey equipped.")

            if self.honey_notes_text is not None:
                self.honey_notes_text.config(state="normal")
                self.honey_notes_text.delete("1.0", "end")
                self.honey_notes_text.insert("1.0", "No honey hired yet.\n\nGet yourself some company.")
                self.honey_notes_text.config(state="disabled")
            return

        image = self.load_tk_image(
            hero.equipped_honey.get("image", "assets/honeys/placeholder.png")
    )

        if image is not None:
            self.honey_image_refs["inventory_honey"] = image
            self.honey_inventory_image_label.config(image=image, text="")
        else:
            self.honey_inventory_image_label.config(image="", text="[No Image]")

        status = "ACTIVE" if hero.honey_is_active() else "INACTIVE"

        self.honey_status_label.config(
            text=(
                f"{hero.equipped_honey['name']}\n"
                f"Status: {status}\n"
                f"{hero.equipped_honey['description']}\n"
                f"{hero.equipped_honey['requirement_text']}"
        )
    )

        if self.honey_notes_text is not None:
            notes = (
                f"Equipped Honey: {hero.equipped_honey['name']}\n"
                f"Status: {status}\n\n"
                f"Requirements: {', '.join(hero.equipped_honey['requirements']) if hero.equipped_honey['requirements'] else 'None'}\n\n"
                f"Owned Honeys: {', '.join(sorted(hero.owned_honeys)) if hero.owned_honeys else 'None'}"
        )

            self.honey_notes_text.config(state="normal")
            self.honey_notes_text.delete("1.0", "end")
            self.honey_notes_text.insert("1.0", notes)
            self.honey_notes_text.config(state="disabled")

    def log_message(self, message):
        self.loot_log.config(state="normal")
        self.loot_log.insert("end", message + "\n")
        self.loot_log.see("end")
        self.loot_log.config(state="disabled")

    def update_action_buttons(self):
        disabled = "disabled" if self.game.game_over else "normal"
        self.pan_button.config(state=disabled)
        self.sell_button.config(state=disabled)
        self.rest_button.config(state=disabled)

    def pack_selected_to_cooler(self):
        selection = self.storage_listbox.curselection()
        if not selection:
            self.show_message("Select an item in storage first.")
            return

        index = selection[0]
        result = self.game.move_storage_to_cooler(index)
        self.show_message(result["message"])


    def move_selected_to_storage(self):
        selection = self.cooler_listbox.curselection()
        if not selection:
            self.show_message("Select an item in the cooler first.")
            return

        index = selection[0]
        result = self.game.move_cooler_to_storage(index)
        self.show_message(result["message"])

    def show_message(self, message):
        self.result_label.config(text=message)
        if self.store_status_label is not None:
            self.store_status_label.config(text=message)
        self.log_message(message)
        self.update_display()
        self.update_action_buttons()

    def change_location(self, selected_location):
        self.game.set_location(selected_location)
        self.show_message(
            f"You head toward {selected_location}. Hope, mud, and poor decisions await."
        )
    
    def format_store_item_text(self, category, item):
        if category == "Pans":
            stats = f"Luck Bonus: +{item['luck_bonus']}"
        elif category == "Containers":
            stats = f"Inventory Capacity: +{item['capacity_bonus']}"
        elif category == "Boots":
            stats = f"Stamina Cost Reduction: -{item['stamina_reduction']}"
        elif category == "Coolers":
            total_slots = 2 + item["consumable_slots"]
            stats = (
                f"Cooler Slots Added: +{item['consumable_slots']}\n"
                f"Total Cooler Capacity: {total_slots}"
            )
        else:
            stats = "No stats"

        return (
            f"{item['name']} - ${item['cost']}\n"
            f"{item['description']}\n"
            f"{stats}"
    )


    def format_general_store_item_text(self, item):
        effect = "No effect listed"

        if item["type"] == "stamina":
            effect = f"Restores {item['value']} stamina"
        elif item["type"] == "luck_buff":
            effect = f"+{item['value']} luck for {item['duration']} pans"
        elif item["type"] == "sell_buff":
            effect = f"+{int(item['value'] * 100)}% on next sale"
        elif item["type"] == "requirement":
            effect = "Used to satisfy special honey requirements"

        return (
            f"{item['name']} - ${item['cost']}\n"
            f"{item['description']}\n"
            f"Effect: {effect}"
    )

    def start_pan(self):
        if self.game.game_over:
            return
        self.result_label.config(text="Panning...")
        self.pan_button.config(state="disabled")
        self.root.after(2000, self.finish_pan)

    def finish_pan(self):
        result = self.game.pan_for_gold()
        self.result_label.config(text=result["message"])
        self.log_message(result["message"])
        self.update_display()
        self.update_action_buttons()

    def sell_inventory(self):
        result = self.game.sell_inventory()
        self.show_message(result["message"])

    def rest_hero(self):
        result = self.game.rest_hero()
        self.show_message(result["message"])

    def pay_bail(self):
        result = self.game.pay_bail()
        self.show_message(result["message"])

    def buy_shop_item(self, category, item_name):
        result = self.game.buy_item(category, item_name)
        self.show_message(result["message"])

    def buy_general_store_item(self, item_name):
        result = self.game.buy_general_store_item(item_name)
        self.show_message(result["message"])

    def buy_companion(self, companion_name):
        result = self.game.buy_companion(companion_name)
        self.show_message(result["message"])

    def buy_honey(self, honey_name):
        result = self.game.buy_honey(honey_name)
        self.show_message(result["message"])

    def use_cooler_consumable(self, index):
        result = self.game.use_cooler_consumable(index)
        self.show_message(result["message"])


if __name__ == "__main__":
    root = tk.Tk()
    app = SluiceBoxJunkyApp(root)
    root.mainloop()