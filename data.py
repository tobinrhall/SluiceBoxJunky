# data.py

GAME_STORY = {
    "title": "Why You're Here",
    "intro": (
        "Your son, Cletus, has been arrested after a spectacular run of poor "
        "life choices. Charges include public intoxication, public indecency, "
        "resisting arrest, petty theft, disturbing the peace, unlawful possession "
        "of a traffic cone, reckless operation of a riding mower, and one incident "
        "the sheriff refused to describe in writing.\n\n"
        "Bail has been set high. Your wallet is empty. Your dignity is negotiable.\n\n"
        "There is only one path left: head to the river, sift mud like a man "
        "possessed, and earn enough money to drag Cletus back out into society."
    )
}

GAME_BALANCE = {
    "starting_bail": 18000,   # 👈 bumped up
    "daily_expense": 35,      # slightly harsher economy
    "weekly_bail_increase": 1000,
    "weekly_day_interval": 7
}

CLASSES = {
    "River Rat": {
        "description": "Tough and tireless. Starts with extra stamina.",
        "max_stamina_bonus": 25,
        "luck_bonus": 0,
        "sell_bonus": 0.00,
        "chaos": False
    },
    "Prospector": {
        "description": "Knows where the good stuff hides. Better luck.",
        "max_stamina_bonus": 0,
        "luck_bonus": 8,
        "sell_bonus": 0.00,
        "chaos": False
    },
    "Hustler": {
        "description": "Can talk a fish into buying water. Better gold value.",
        "max_stamina_bonus": 0,
        "luck_bonus": 0,
        "sell_bonus": 0.15,
        "chaos": False
    },
    "Washed-Up Legend": {
        "description": "A mystery wrapped in river mud. Random bonuses each pan.",
        "max_stamina_bonus": 0,
        "luck_bonus": 0,
        "sell_bonus": 0.00,
        "chaos": True
    }
}

LOCATIONS = {
    "Nooksack River": {
        "stamina_cost": 10,
        "flavor": "Cold water, steady current, and honest dirt.",
        "loot_table": [
            ("Mud", 0, 30),
            ("Tiny Fleck", 5, 30),
            ("Small Flake", 10, 20),
            ("Pebble", 20, 12),
            ("Chunk", 40, 6),
            ("Nugget", 75, 2),
        ]
    },
    "Mississippi River": {
        "stamina_cost": 12,
        "flavor": "Big water, big sediment, and plenty of junk.",
        "loot_table": [
            ("Mud", 0, 35),
            ("Tiny Fleck", 4, 28),
            ("Small Flake", 9, 18),
            ("Pebble", 18, 11),
            ("Chunk", 35, 6),
            ("Nugget", 65, 2),
        ]
    },
    "The Swamp": {
        "stamina_cost": 14,
        "flavor": "Mosquitoes, mystery, and suspicious bubbling.",
        "loot_table": [
            ("Mud", 0, 25),
            ("Tiny Fleck", 6, 24),
            ("Small Flake", 12, 20),
            ("Pebble", 24, 14),
            ("Chunk", 50, 10),
            ("Swamp Nugget", 95, 5),
            ("Legendary Boot", 1, 2),
        ]
    },
    "Abandoned Mine Runoff": {
        "stamina_cost": 16,
        "flavor": "Dangerous, ugly, and maybe worth it.",
        "loot_table": [
            ("Mud", 0, 22),
            ("Tiny Fleck", 7, 20),
            ("Small Flake", 14, 20),
            ("Pebble", 28, 16),
            ("Chunk", 55, 12),
            ("Nugget", 110, 7),
            ("Heavy Nugget", 150, 3),
        ]
    },
    "Frozen Creek": {
        "stamina_cost": 8,
        "flavor": "Easy pace, numb fingers, decent odds.",
        "loot_table": [
            ("Mud", 0, 28),
            ("Tiny Fleck", 5, 25),
            ("Small Flake", 11, 22),
            ("Pebble", 22, 14),
            ("Chunk", 42, 8),
            ("Nugget", 80, 3),
        ]
    }
}

SHOP_ITEMS = {
    "Pans": [
        {
            "name": "Rusty Pan",
            "cost": 0,
            "luck_bonus": 0,
            "description": "Barely holds dirt, but it works."
        },
        {
            "name": "Copper Pan",
            "cost": 75,
            "luck_bonus": 3,
            "description": "A little cleaner, a little luckier."
        },
        {
            "name": "Prospector's Pan",
            "cost": 175,
            "luck_bonus": 6,
            "description": "A respectable pan for serious mud enjoyers."
        },
        {
            "name": "Lucky Strike Pan",
            "cost": 350,
            "luck_bonus": 10,
            "description": "Feels heavy with destiny."
        }
    ],
    "Containers": [
        {
            "name": "Old Bucket",
            "cost": 0,
            "capacity_bonus": 0,
            "description": "Leaky, dented, loyal."
        },
        {
            "name": "Supply Sack",
            "cost": 60,
            "capacity_bonus": 3,
            "description": "A little more room for your river treasures."
        },
        {
            "name": "Mule Crate",
            "cost": 140,
            "capacity_bonus": 6,
            "description": "Carry more, complain less."
        },
        {
            "name": "Hoarder's Chest",
            "cost": 275,
            "capacity_bonus": 10,
            "description": "Now you're thinking like a true junky."
        }
    ],
    "Boots": [
        {
            "name": "Wet Sneakers",
            "cost": 0,
            "stamina_reduction": 0,
            "description": "Terrible idea, honestly."
        },
        {
            "name": "Rubber Boots",
            "cost": 80,
            "stamina_reduction": 1,
            "description": "Keeps your feet dry-ish."
        },
        {
            "name": "Hip Waders",
            "cost": 180,
            "stamina_reduction": 2,
            "description": "Less suffering per scoop."
        },
        {
            "name": "River Warden Waders",
            "cost": 320,
            "stamina_reduction": 3,
            "description": "Stride into the current like a legend."
        }
    ],
    "Coolers": [
        {
            "name": "Lunch Cooler",
            "cost": 0,
            "consumable_slots": 2,
            "description": "One sad drink and a dream."
        },
        {
            "name": "Cheap Foam Cooler",
            "cost": 70,
            "consumable_slots": 2,
            "description": "Barely insulated, but technically useful."
        },
        {
            "name": "River Cooler",
            "cost": 155,
            "consumable_slots": 4,
            "description": "Enough room for a proper bad decision."
        },
        {
            "name": "Party Barge Cooler",
            "cost": 295,
            "consumable_slots": 8,
            "description": "Now you're provisioning like a champion."
        }
    ]
}

GENERAL_STORE_ITEMS = [
    {
        "name": "Gas Station Energy Drink",
        "cost": 25,
        "type": "stamina",
        "value": 25,
        "description": "Restores 25 stamina. Tastes like battery acid and hope."
    },
    {
        "name": "Cigarettes",
        "cost": 12,
        "type": "requirement",
        "value": 0,
        "description": "A carton of bad decisions."
    },
    {
        "name": "Liquor",
        "cost": 22,
        "type": "requirement",
        "value": 0,
        "description": "Questionable fuel for questionable company."
    },
    {
        "name": "Questionable Jerky",
        "cost": 18,
        "type": "stamina",
        "value": 15,
        "description": "Restores 15 stamina. Chewy and concerning."
    },
    {
        "name": "Lucky Rabbit Foot",
        "cost": 40,
        "type": "luck_buff",
        "value": 5,
        "duration": 3,
        "description": "Gain +5 luck for the next 3 pans."
    },
    {
        "name": "Pawn Shop Scale Polish",
        "cost": 35,
        "type": "sell_buff",
        "value": 0.10,
        "duration": 1,
        "description": "Next sale gives +10% more cash."
    }
]

COMPANIONS = [
    {
        "name": "Chicken",
        "cost": 90,
        "luck_bonus": 2,
        "capacity_bonus": 0,
        "sell_bonus": 0.00,
        "stamina_reduction": 0,
        "description": "Pecks at the dirt like it knows something."
    },
    {
        "name": "Ferret",
        "cost": 140,
        "luck_bonus": 1,
        "capacity_bonus": 2,
        "sell_bonus": 0.00,
        "stamina_reduction": 0,
        "description": "Slim, chaotic, and weirdly helpful."
    },
    {
        "name": "Raccoon",
        "cost": 175,
        "luck_bonus": 0,
        "capacity_bonus": 0,
        "sell_bonus": 0.08,
        "stamina_reduction": 0,
        "description": "Understands trash and negotiations equally well."
    },
    {
        "name": "Swamp Possum",
        "cost": 220,
        "luck_bonus": 0,
        "capacity_bonus": 0,
        "sell_bonus": 0.00,
        "stamina_reduction": 1,
        "description": "Too mean to get tired."
    },
    {
        "name": "Lynx",
        "cost": 325,
        "luck_bonus": 4,
        "capacity_bonus": 1,
        "sell_bonus": 0.00,
        "stamina_reduction": 0,
        "description": "Silent, expensive, and probably judging you."
    }
]
SLUICE_HONEYS = [
    {
        "name": "Tammy Two-Smokes",
        "cost": 400,
        "stamina_bonus": 25,
        "sell_bonus": 0.0,
        "luck_bonus": 0,
        "stamina_penalty": 0,
        "requirements": ["Cigarettes", "Liquor"],
        "description": "Chain-smoking legend. Hits like a mule, complains like one too.",
        "requirement_text": "Requires Cigarettes + Liquor in cooler at all times.",
        "image": "assets/honeys/tammy.png"
    },
    {
        "name": "Debbie Downstream",
        "cost": 350,
        "stamina_bonus": 0,
        "sell_bonus": 0.1,
        "luck_bonus": 0,
        "stamina_penalty": 20,
        "requirements": [],
        "description": "Negotiates like a pro, drains your will to live.",
        "requirement_text": "No requirements, just constant negativity.",
        "image": "assets/honeys/debbie.png"
    }
]