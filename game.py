# game.py

import random
from data import (
    LOCATIONS,
    CLASSES,
    SHOP_ITEMS,
    GENERAL_STORE_ITEMS,
    COMPANIONS,
    SLUICE_HONEYS,
    GAME_BALANCE,
    BAIL_STAGES,
    RIVER_UNLOCK_ORDER,
    CLETUS_REARREST_EVENTS,
    WORLD_EVENT_SETTINGS,
    WORLD_EVENTS,
    DEBBIE_COMPLAINTS,
)

class Hero:
    def __init__(self, name="Unnamed Prospector", hero_class="River Rat"):
        class_data = CLASSES[hero_class]

        self.name = name
        self.hero_class = hero_class

        self.base_max_stamina = 100
        self.max_stamina = self.base_max_stamina + class_data["max_stamina_bonus"]
        self.stamina = self.max_stamina

        self.base_luck = class_data["luck_bonus"]
        self.class_sell_bonus = class_data["sell_bonus"]
        self.chaos = class_data["chaos"]

        self.cash = 2000
        self.bail_paid = 0

        self.equipped_honey = None
        self.owned_honeys = set()
        self.base_capacity = 10
        self.base_cooler_capacity = 2
        self.inventory = []

        self.storage_consumables = []
        self.cooler_consumables = []

        self.equipped_pan = SHOP_ITEMS["Pans"][0]
        self.equipped_container = SHOP_ITEMS["Containers"][0]
        self.equipped_boots = SHOP_ITEMS["Boots"][0]
        self.equipped_cooler = SHOP_ITEMS["Coolers"][0]

        self.owned_pans = {self.equipped_pan["name"]}
        self.owned_containers = {self.equipped_container["name"]}
        self.owned_boots = {self.equipped_boots["name"]}
        self.owned_coolers = {self.equipped_cooler["name"]}

        self.equipped_companion = None
        self.owned_companions = set()

        self.temp_luck_bonus = 0
        self.temp_luck_turns = 0
        self.next_sale_bonus = 0.0

        self.recalculate_stats()

    def recalculate_stats(self):
        companion_capacity = 0
        companion_luck = 0
        companion_sell = 0.0
        companion_stamina = 0


        if self.equipped_companion is not None:
            companion_capacity = self.equipped_companion["capacity_bonus"]
            companion_luck = self.equipped_companion["luck_bonus"]
            companion_sell = self.equipped_companion["sell_bonus"]
            companion_stamina = self.equipped_companion["stamina_reduction"]

        honey_stamina = 0
        honey_sell = 0.0
        honey_luck = 0
        honey_penalty = 0

        if self.equipped_honey is not None:
            honey_stamina = self.equipped_honey["stamina_bonus"]
            honey_sell = self.equipped_honey["sell_bonus"]
            honey_luck = self.equipped_honey["luck_bonus"]
            honey_penalty = self.equipped_honey["stamina_penalty"]

        self.inventory_capacity = (
            self.base_capacity
            + self.equipped_container["capacity_bonus"]
            + companion_capacity
        )

        self.cooler_capacity = self.base_cooler_capacity + self.equipped_cooler["consumable_slots"]
        self.max_stamina = (
            self.base_max_stamina
                + CLASSES[self.hero_class]["max_stamina_bonus"]
                + honey_stamina
                - honey_penalty
    )

        self.gear_luck_bonus = self.equipped_pan["luck_bonus"]
        self.companion_luck_bonus = companion_luck + honey_luck

        self.total_sell_bonus = (
            self.class_sell_bonus
                + companion_sell
                + honey_sell
    )

        self.stamina_reduction = self.equipped_boots["stamina_reduction"] + companion_stamina

        if len(self.inventory) > self.inventory_capacity:
            self.inventory = self.inventory[:self.inventory_capacity]

        while len(self.cooler_consumables) > self.cooler_capacity:
            moved_item = self.cooler_consumables.pop()
            self.storage_consumables.append(moved_item)

    def can_pan(self, cost):
        return self.stamina >= cost

    def rest(self):
        self.stamina = self.max_stamina

    def restore_stamina(self, amount):
        self.stamina = min(self.max_stamina, self.stamina + amount)

    def get_current_luck(self):
        total_luck = (
            self.base_luck
            + self.gear_luck_bonus
            + self.companion_luck_bonus
            + self.temp_luck_bonus
        )
        if self.chaos:
            return total_luck + random.randint(-5, 15)
        return total_luck

    def tick_pan_buffs(self):
        if self.temp_luck_turns > 0:
            self.temp_luck_turns -= 1
            if self.temp_luck_turns == 0:
                self.temp_luck_bonus = 0

    def get_inventory_count(self):
        return len(self.inventory)

    def has_inventory_space(self):
        return self.get_inventory_count() < self.inventory_capacity

    def add_loot(self, loot_name, loot_value):
        if not self.has_inventory_space():
            return False
        self.inventory.append((loot_name, loot_value))
        return True

    def add_storage_consumable(self, item):
        self.storage_consumables.append(item)

    def cooler_has_item(self, item_name):
        return any(item["name"] == item_name for item in self.cooler_consumables)

    def honey_is_active(self):
        if self.equipped_honey is None:
            return False

        requirements = self.equipped_honey["requirements"]
        if not requirements:
            return True

        return all(self.cooler_has_item(req) for req in requirements)

    def get_honey_status_text(self):
        if self.equipped_honey is None:
            return "No Sluice Box Honey equipped."

        if self.honey_is_active():
            return f"{self.equipped_honey['name']} is ACTIVE."

        return f"{self.equipped_honey['name']} is INACTIVE. Missing requirements."

    def can_add_to_cooler(self):
        return len(self.cooler_consumables) < self.cooler_capacity

    def sell_inventory(self):
        if not self.inventory:
            return 0, 0, 0

        base_total = sum(item_value for _, item_value in self.inventory)
        multiplier = 1 + self.next_sale_bonus
        final_total = int(round(base_total * multiplier))
        item_count = len(self.inventory)

        self.cash += final_total
        self.inventory.clear()

        used_bonus = self.next_sale_bonus
        self.next_sale_bonus = 0.0

        return final_total, item_count, used_bonus


class Game:
    def __init__(self):
        self.hero = None
        self.day = 1

        self.bail_stage = 0
        self.bail_target = BAIL_STAGES[self.bail_stage]
        self.daily_expense = GAME_BALANCE["daily_expense"]

        self.unlocked_locations = set(RIVER_UNLOCK_ORDER[:3])
        self.current_location = RIVER_UNLOCK_ORDER[0]

        self.game_over = False
        self.game_won = False

    def create_hero(self, name, hero_class):
        clean_name = name.strip() if name.strip() else "Unnamed Prospector"
        self.hero = Hero(clean_name, hero_class)

    def get_all_locations_in_order(self):
        return RIVER_UNLOCK_ORDER

    def get_current_stage_number(self):
        return self.bail_stage + 1

    def is_location_unlocked(self, location_name):
        return location_name in self.unlocked_locations

    def get_unlocked_locations(self):
        return [name for name in RIVER_UNLOCK_ORDER if name in self.unlocked_locations]

    def get_available_shop_items(self, category):
        current_stage = self.get_current_stage_number()
        return [
            item for item in SHOP_ITEMS[category]
            if item.get("required_stage", 1) <= current_stage
        ]


    def check_fail_state(self):
        if self.hero is None:
            return

        if self.hero.cash < -250:
            self.game_over = True
            self.game_won = False

    def advance_bail_progression(self):
        unlocked_message = ""
        river_message = ""

        if len(self.unlocked_locations) < len(RIVER_UNLOCK_ORDER):
            next_river = RIVER_UNLOCK_ORDER[len(self.unlocked_locations)]
            self.unlocked_locations.add(next_river)
            unlocked_message = f"\nNew River Unlocked: {next_river}"

        rearrest_message = random.choice(CLETUS_REARREST_EVENTS)

        self.bail_stage += 1

        if self.bail_stage >= len(BAIL_STAGES):
            self.game_won = True
            self.game_over = True
            return (
                "Against all odds, you finally cleared Cletus's mountain of legal trouble."
                "\n\nCletus is free."
                "\n\nFor now."
            )

        self.bail_target = BAIL_STAGES[self.bail_stage]
        self.hero.bail_paid = 0

        river_message = unlocked_message if unlocked_message else ""

        return (
            f"You paid off Cletus's bail for this round."
            f"\n\n{rearrest_message}"
            f"{river_message}"
            f"\n\nNew Bail Target: ${self.bail_target}"
        )

    def get_location_data(self):
        return LOCATIONS[self.current_location]

    def set_location(self, location_name):
        if self.game_over:
            return

        if location_name in LOCATIONS and location_name in self.unlocked_locations:
            self.current_location = location_name

    def get_bail_remaining(self):
        if self.hero is None:
            return self.bail_target
        return max(0, self.bail_target - self.hero.bail_paid)
    
    def pay_bail(self, amount=None):
        if self.hero is None:
            return {"success": False, "message": "No hero created yet."}

        if self.game_over:
            return {"success": False, "message": "Run is over."}

        if self.hero.cash <= 0:
            return {"success": False, "message": "You have no cash to pay toward bail."}

        if amount is None:
            amount = self.hero.cash

        amount = min(amount, self.hero.cash, self.get_bail_remaining())

        self.hero.cash -= amount
        self.hero.bail_paid += amount

        if self.hero.bail_paid >= self.bail_target:
            progression_message = self.advance_bail_progression()
            return {
                "success": True,
                "message": f"You pay ${amount} toward Cletus's bail.\n\n{progression_message}"
            }

        return {
            "success": True,
            "message": (
                f"You pay ${amount} toward Cletus's bail."
                f"\nBail Remaining: ${self.get_bail_remaining()}"
            )
        }

    def check_win_loss(self):
        if self.hero is None:
            return

        if self.hero.cash >= self.bail_target:
            self.game_won = True
            self.game_over = True

        if self.hero.cash < -250:
            self.game_over = True
            self.game_won = False

    def get_pan_cost(self):
        location = self.get_location_data()
        base_cost = location["stamina_cost"]
        return max(1, base_cost - self.hero.stamina_reduction)

    def pan_for_gold(self):
        if self.hero is None:
            return {"success": False, "message": "No hero created yet.", "loot": None}

        if self.game_over:
            return {"success": False, "message": "The game is over. Start a new run to continue.", "loot": None}

        stamina_cost = self.get_pan_cost()

        if not self.hero.can_pan(stamina_cost):
            return {"success": False, "message": "You're too worn out. Time to rest.", "loot": None}

        if not self.hero.has_inventory_space():
            return {
                "success": False,
                "message": "Your inventory is full. Sell your haul or call it a night.",
                "loot": None
            }

        self.hero.stamina -= stamina_cost

        current_luck = self.hero.get_current_luck()
        loot_name, loot_value = self.roll_loot(self.get_location_data()["loot_table"], current_luck)

        final_value = int(round(loot_value * (1 + self.hero.total_sell_bonus)))
        added = self.hero.add_loot(loot_name, final_value)

        if not added:
            return {"success": False, "message": "No room left in your pack.", "loot": None}

        class_note = ""
        if self.hero.chaos:
            class_note = f" Chaos luck roll: {current_luck:+d}."

        buff_note = ""
        if self.hero.temp_luck_turns > 0:
            buff_note = (
                f" Buff luck active: +{self.hero.temp_luck_bonus} "
                f"({self.hero.temp_luck_turns} pan(s) left)."
            )

        companion_note = ""
        if self.hero.equipped_companion is not None:
            companion_note = f" {self.hero.equipped_companion['name']} seems pleased."

        event_message = self.maybe_trigger_world_event()
        debbie_message = self.maybe_get_debbie_complaint()

        self.hero.tick_pan_buffs()
        self.hero.recalculate_stats()

        full_message = (
            f"You found: {loot_name} worth ${final_value}."
            f"{class_note}{buff_note}{companion_note}"
)

        if event_message:
            full_message += f"\n\nWORLD EVENT: {event_message}"

        if debbie_message:
            full_message += f"\n\n{debbie_message}"

        return {
            "success": True,
            "message": full_message,
            "loot": (loot_name, final_value)
}

    def sell_inventory(self):
        if self.hero is None:
            return {"success": False, "message": "No hero created yet."}

        if self.game_over:
            return {"success": False, "message": "The game is over. Start a new run to continue."}

        total_value, item_count, used_bonus = self.hero.sell_inventory()

        if item_count == 0:
            return {"success": False, "message": "You have nothing to sell."}

        self.check_win_loss()

        bonus_note = ""
        if used_bonus > 0:
            bonus_note = f" The pawnbroker squints and pays an extra {int(used_bonus * 100)}%."

        win_note = ""
        if self.game_won:
            win_note = " You finally scraped together enough money to bail Cletus out of jail."

        return {
            "success": True,
            "message": f"You sold {item_count} item(s) for ${total_value}.{bonus_note}{win_note}",
            "total_value": total_value,
            "item_count": item_count
        }

    def rest_hero(self):
        if self.hero is None:
            return {"success": False, "message": "No hero created yet."}

        if self.game_over:
            return {"success": False, "message": "The game is over. Start a new run to continue."}

        self.hero.rest()
        self.day += 1
        self.hero.cash -= self.daily_expense

        weekly_note = ""
        if self.day % GAME_BALANCE["weekly_day_interval"] == 0:
            self.bail_target += GAME_BALANCE["weekly_bail_increase"]
            weekly_note = (
                f"\n\nCletus caused more trouble from inside. "
                f"Bail increased by ${GAME_BALANCE['weekly_bail_increase']}."
            )

        self.check_fail_state()

        if self.game_over:
            return {
                "success": False,
                "message": (
                    f"Day {self.day} begins, but the bills keep stacking up."
                    f"\nYou are broke beyond reason."
                    f"\nCletus remains jailed."
                )
            }

        return {
            "success": True,
            "message": (
                f"You rest for the night. Day {self.day} begins."
                f"\nDaily expenses hit for ${self.daily_expense}."
                f"{weekly_note}"
            )
        }

    def buy_item(self, category, item_name):
        if self.hero is None:
            return {"success": False, "message": "No hero created yet."}

        if self.game_over:
            return {"success": False, "message": "The game is over. Start a new run to continue."}

        item = None

        for shop_item in self.get_available_shop_items(category):
            if shop_item["name"] == item_name:
                item = shop_item
                break

        if item is None:
            return {"success": False, "message": "That item does not exist."}

        if category == "Pans" and item_name in self.hero.owned_pans:
            self.hero.equipped_pan = item
            self.hero.recalculate_stats()
            return {"success": True, "message": f"You equip the {item_name}."}

        if category == "Containers" and item_name in self.hero.owned_containers:
            self.hero.equipped_container = item
            self.hero.recalculate_stats()
            return {"success": True, "message": f"You equip the {item_name}."}

        if category == "Boots" and item_name in self.hero.owned_boots:
            self.hero.equipped_boots = item
            self.hero.recalculate_stats()
            return {"success": True, "message": f"You equip the {item_name}."}

        if category == "Coolers" and item_name in self.hero.owned_coolers:
            self.hero.equipped_cooler = item
            self.hero.recalculate_stats()
            return {"success": True, "message": f"You equip the {item_name}."}

        if self.hero.cash < item["cost"]:
            return {"success": False, "message": f"You need ${item['cost']} for the {item_name}."}

        self.hero.cash -= item["cost"]

        if category == "Pans":
            self.hero.owned_pans.add(item_name)
            self.hero.equipped_pan = item
        elif category == "Containers":
            self.hero.owned_containers.add(item_name)
            self.hero.equipped_container = item
        elif category == "Boots":
            self.hero.owned_boots.add(item_name)
            self.hero.equipped_boots = item
        elif category == "Coolers":
            self.hero.owned_coolers.add(item_name)
            self.hero.equipped_cooler = item

        self.hero.recalculate_stats()
        self.check_win_loss()
        return {"success": True, "message": f"You bought and equipped {item_name} for ${item['cost']}."}

    def buy_general_store_item(self, item_name):
        if self.hero is None:
            return {"success": False, "message": "No hero created yet."}

        if self.game_over:
            return {"success": False, "message": "The game is over. Start a new run to continue."}

        item = None
        for store_item in GENERAL_STORE_ITEMS:
            if store_item["name"] == item_name:
                item = store_item
                break

        if item is None:
            return {"success": False, "message": "That store item does not exist."}

        if self.hero.cash < item["cost"]:
            return {"success": False, "message": f"You need ${item['cost']} for {item_name}."}

        self.hero.cash -= item["cost"]
        self.hero.add_storage_consumable(item.copy())
        self.check_win_loss()
        return {"success": True, "message": f"You bought {item_name} for ${item['cost']} and stashed it at home."}

    def move_storage_to_cooler(self, index):
        if self.hero is None:
            return {"success": False, "message": "No hero created yet."}

        if self.game_over:
            return {"success": False, "message": "The game is over. Start a new run to continue."}

        if index < 0 or index >= len(self.hero.storage_consumables):
            return {"success": False, "message": "That storage item does not exist."}

        if not self.hero.can_add_to_cooler():
            return {
                "success": False,
                "message": f"Your cooler is full ({len(self.hero.cooler_consumables)}/{self.hero.cooler_capacity})."
            }

        item = self.hero.storage_consumables.pop(index)
        self.hero.cooler_consumables.append(item)
        self.hero.recalculate_stats()
        return {"success": True, "message": f"You pack {item['name']} into the cooler."}

    def move_cooler_to_storage(self, index):
        if self.hero is None:
            return {"success": False, "message": "No hero created yet."}

        if self.game_over:
            return {"success": False, "message": "The game is over. Start a new run to continue."}

        if index < 0 or index >= len(self.hero.cooler_consumables):
            return {"success": False, "message": "That cooler item does not exist."}

        item = self.hero.cooler_consumables.pop(index)
        self.hero.storage_consumables.append(item)
        self.hero.recalculate_stats()
        return {"success": True, "message": f"You move {item['name']} back into home storage."}

    def use_cooler_consumable(self, index):
        if self.hero is None:
            return {"success": False, "message": "No hero created yet."}

        if self.game_over:
            return {"success": False, "message": "The game is over. Start a new run to continue."}

        if index < 0 or index >= len(self.hero.cooler_consumables):
            self.hero.recalculate_stats()
            return {"success": False, "message": "That cooler item does not exist."}

        item = self.hero.cooler_consumables.pop(index)

        if item["type"] == "stamina":
            before = self.hero.stamina
            self.hero.restore_stamina(item["value"])
            restored = self.hero.stamina - before
            self.hero.recalculate_stats()
            return {"success": True, "message": f"You use {item['name']} and restore {restored} stamina."}

        if item["type"] == "luck_buff":
            self.hero.temp_luck_bonus += item["value"]
            self.hero.temp_luck_turns = max(self.hero.temp_luck_turns, item["duration"])
            self.hero.recalculate_stats()
            return {
                "success": True,
                "message": f"You use {item['name']}. +{item['value']} luck for the next {item['duration']} pans."
            }

        if item["type"] == "sell_buff":
            self.hero.next_sale_bonus += item["value"]
            self.hero.recalculate_stats()
            return {
                "success": True,
                "message": f"You use {item['name']}. Your next sale gets +{int(item['value'] * 100)}% value."
            }


        return {"success": False, "message": "That item had no effect somehow."}

    def buy_companion(self, companion_name):
        if self.hero is None:
            return {"success": False, "message": "No hero created yet."}

        if self.game_over:
            return {"success": False, "message": "The game is over. Start a new run to continue."}

        companion = None
        for entry in COMPANIONS:
            if entry["name"] == companion_name:
                companion = entry
                break

        if companion is None:
            return {"success": False, "message": "That companion does not exist."}

        if companion_name in self.hero.owned_companions:
            self.hero.equipped_companion = companion
            self.hero.recalculate_stats()
            return {"success": True, "message": f"{companion_name} joins you again."}

        if self.hero.cash < companion["cost"]:
            return {"success": False, "message": f"You need ${companion['cost']} for {companion_name}."}

        self.hero.cash -= companion["cost"]
        self.hero.owned_companions.add(companion_name)
        self.hero.equipped_companion = companion
        self.hero.recalculate_stats()
        self.check_win_loss()

        return {
            "success": True,
            "message": f"You bought {companion_name} for ${companion['cost']}. It now follows you around."
        }

    def buy_honey(self, honey_name):
        if self.hero is None:
            return {"success": False, "message": "No hero created yet."}

        if self.game_over:
            return {"success": False, "message": "The game is over. Start a new run to continue."}

        honey = None
        for entry in SLUICE_HONEYS:
            if entry["name"] == honey_name:
                honey = entry
                break

        if honey is None:
            return {"success": False, "message": "That honey does not exist."}

        if honey_name in self.hero.owned_honeys:
            self.hero.equipped_honey = honey
            self.hero.recalculate_stats()

            if self.hero.honey_is_active():
                return {"success": True, "message": f"{honey_name} is back and ready to cause trouble."}
            return {"success": True, "message": f"{honey_name} is equipped, but her requirements are not met."}

        if self.hero.cash < honey["cost"]:
            return {"success": False, "message": f"You need ${honey['cost']} for {honey_name}."}

        self.hero.cash -= honey["cost"]
        self.hero.owned_honeys.add(honey_name)
        self.hero.equipped_honey = honey
        self.hero.recalculate_stats()

        if self.hero.honey_is_active():
            return {"success": True, "message": f"You hired {honey_name} for ${honey['cost']}."}
        return {
            "success": True,
            "message": f"You hired {honey_name} for ${honey['cost']}, but she refuses to help until her requirements are met."
        }

    def roll_loot(self, loot_table, luck_bonus=0):
        adjusted_table = []

        for name, value, weight in loot_table:
            adjusted_weight = weight

            if value > 0 and luck_bonus != 0:
                adjusted_weight += max(0, luck_bonus)

            if name == "Mud" and luck_bonus > 0:
                adjusted_weight = max(1, weight - luck_bonus)

            if luck_bonus < 0 and value > 20:
                adjusted_weight = max(1, weight + luck_bonus)

            adjusted_table.append((name, value, adjusted_weight))

        names = [item[0] for item in adjusted_table]
        weights = [item[2] for item in adjusted_table]

        chosen_name = random.choices(names, weights=weights, k=1)[0]

        for name, value, _ in adjusted_table:
            if name == chosen_name:
                return name, value

        return "Mud", 0
    
    def maybe_trigger_world_event(self):
        if self.hero is None or self.game_over:
            return None

        if random.random() >= WORLD_EVENT_SETTINGS["pan_event_chance"]:
            return None

        event = random.choice(WORLD_EVENTS)
        hero = self.hero

        if event["type"] == "stamina_zero":
            hero.stamina = 0
            return event["description"]

        if event["type"] == "luck_buff":
            hero.temp_luck_bonus += event["value"]
            hero.temp_luck_turns = max(hero.temp_luck_turns, event["duration"])
            hero.recalculate_stats()
            return event["description"]

        if event["type"] == "full_stamina":
            hero.stamina = hero.max_stamina
            return event["description"]

        if event["type"] == "stamina_loss":
            hero.stamina = max(0, hero.stamina - event["value"])
            return event["description"]

        if event["type"] == "next_sale_buff":
            hero.next_sale_bonus += event["value"]
            return event["description"]

        if event["type"] == "lose_random_cooler_item":
            if hero.cooler_consumables:
                stolen_item = random.choice(hero.cooler_consumables)
                hero.cooler_consumables.remove(stolen_item)
                hero.recalculate_stats()
                return f"{event['description']} The crow got away with your {stolen_item['name']}."
            return "A crow swoops down to steal from you, but your cooler is already empty."

        if event["type"] == "luck_penalty":
            hero.temp_luck_bonus -= event["value"]
            hero.temp_luck_turns = max(hero.temp_luck_turns, event["duration"])
            hero.recalculate_stats()
            return event["description"]

        if event["type"] == "cash_bonus":
            hero.cash += event["value"]
            self.check_win_loss()
            return event["description"]

        return None


    def maybe_get_debbie_complaint(self):
        if self.hero is None:
            return None

        honey = self.hero.equipped_honey
        if honey is None:
            return None

        if honey["name"] != "Debbie Downstream":
            return None

        if not self.hero.honey_is_active():
            return None

        if random.random() < 0.30:
            return f'Debbie Downstream grumbles: "{random.choice(DEBBIE_COMPLAINTS)}"'

        return None