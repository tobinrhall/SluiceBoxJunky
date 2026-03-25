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
    "daily_expense": 25,      
    "weekly_bail_increase": 200,
    "weekly_day_interval": 7
}

BAIL_STAGES = [
    2000,
    4000,
    6500,
    9000,
    12000,
    16000,
    20000,
]

RIVER_UNLOCK_ORDER = [
    "Nooksack River",
    "Frozen Creek",
    "The Swamp",
    "Mississippi River",
    "Abandoned Mine Runoff",
]

CLETUS_REARREST_EVENTS = [
    "You bailed Cletus out, but he was arrested again after trying to use a riding mower as a fishing vessel.",
    "Cletus learned a new river spot from an inmate named Fishhook Darryl before getting arrested again behind a bait shop.",
    "Cletus traded jail pudding for directions to a better panning location, then got locked up again for public indecency.",
    "Cletus gave a guard an all-access pass to his body and somehow came back with directions to a new river.",
    "You got Cletus out for six whole hours before he was arrested again for trying to sell counterfeit medicinal crystals at a gas station.",
    "Cletus overheard two old-timers in lockup talking about a rich runoff spot, then immediately caught another charge.",
    "Cletus got arrested again after threatening a jukebox with a tire iron, but not before learning about a new panning spot.",
]

WORLD_EVENT_SETTINGS = {
    "pan_event_chance": 0.04
}

WORLD_EVENTS = [
    {
        "name": "Fall Into Water",
        "type": "stamina_zero",
        "description": "You slip on a mossy rock and plunge straight into the water. Your day is ruined."
    },
    {
        "name": "Eagle Blessing",
        "type": "luck_buff",
        "value": 10,
        "duration": 5,
        "description": "An eagle circles overhead like a divine sign. +10 luck for the next 5 pans."
    },
    {
        "name": "Mysterious Herb",
        "type": "full_stamina",
        "description": "You chew a mysterious herb from the riverbank. Against all reason, it fully restores your stamina."
    },
    {
        "name": "Panner Ambush",
        "type": "stamina_loss",
        "value": 25,
        "description": "Another panner claims you're on his turf and jumps you. Lose 25 stamina."
    },
    {
        "name": "Pawn Ticket",
        "type": "next_sale_buff",
        "value": 0.15,
        "description": "You find a crumpled pawn ticket in the mud. Next sale gets +15% value."
    },
    {
        "name": "Crow Theft",
        "type": "lose_random_cooler_item",
        "description": "A crow swoops in and steals something from your cooler."
    },
    {
        "name": "Mosquito Swarm",
        "type": "luck_penalty",
        "value": 5,
        "duration": 3,
        "description": "A black cloud of mosquitoes descends on you. -5 luck for the next 3 pans."
    },
    {
        "name": "Buried Cash Tin",
        "type": "cash_bonus",
        "value": 35,
        "description": "You dig up an old tobacco tin with a few soggy bills inside. Gain $35 cash."
    }
]

DEBBIE_COMPLAINTS = [
    "Suga, can we go home yet?",
    "My bunions are acting up again.",
    "Do you have a torch, baby? Mama needs her torch.",
    "I hate the wilderness.",
    "Can this get any more boring?",
    "I forgot to feed my 3 kids this morning.",
    "That's the last time I use a lightbulb.",
    "My needle marks are really itchy today.",
    "I'm bored.",
    "We should take that sluice box apart and sell it for scrap.",
    "Both of my teeth are hurting.",
    "If I see one more mosquito, I'm filing a complaint.",
    "You call this prospecting? I call this loitering with mud.",
    "I ain't built for nature. I'm built for indoor disappointment.",
    "If I die out here, sell my shoes."
]

CLASSES = {
    "Greenhorn": {
        "luck_bonus": 2,
        "max_stamina_bonus": 10,
        "sell_bonus": 0.00,
        "chaos": False,
        "description": "New to the game, but eager and optimistic.",
        "image": "assets/classes/greenhorn.png"
    },
    "Tracker": {
        "luck_bonus": 3,
        "max_stamina_bonus": 5,
        "sell_bonus": 0.00,
        "chaos": False,
        "description": "Knows the land and follows the signs.",
        "image": "assets/classes/tracker.png"
    },
    "Hillbilly": {
        "luck_bonus": 1,
        "max_stamina_bonus": 20,
        "sell_bonus": 0.05,
        "chaos": False,
        "description": "Rough, tough, and built for the grind.",
        "image": "assets/classes/hillbilly.png"
    },
    "Mad Miner": {
        "luck_bonus": 5,
        "max_stamina_bonus": -5,
        "sell_bonus": 0.00,
        "chaos": True,
        "description": "Unstable, unpredictable, but hits big.",
        "image": "assets/classes/mad_miner.png"
    }
}

LOCATIONS = {
    "Nooksack River": {
        "stamina_cost": 10,
        "image": "assets/rivers/nooksack.png",
        "description": "Cold, fast, and full of promise.",
        "loot_table": [
            ("Mud", 0, 30),
            ("Tiny Fleck", 5, 30),
            ("Small Flake", 10, 20),
            ("Pebble", 20, 12),
            ("Chunk", 40, 6),
            ("Nugget", 75, 2),
        ]
    },
    "Frozen Creek": {
        "stamina_cost": 8,
        "image": "assets/rivers/frozen_creek.png",
        "description": "Hard ground, better rewards.",
        "loot_table": [
            ("Mud", 0, 28),
            ("Tiny Fleck", 5, 25),
            ("Small Flake", 11, 22),
            ("Pebble", 22, 14),
            ("Chunk", 42, 8),
            ("Nugget", 80, 3),
        ]
    },
    "The Swamp": {
        "stamina_cost": 14,
        "image": "assets/rivers/swamp.png",
        "description": "Smells awful, pays decent.",
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
    "Mississippi River": {
        "stamina_cost": 12,
        "image": "assets/rivers/mississippi.png",
        "description": "Wide, muddy, and unpredictable.",
        "loot_table": [
            ("Mud", 0, 35),
            ("Dust",3, 10),
            ("Tiny Fleck", 4, 28),
            ("Small Flake", 9, 18),
            ("Pebble", 18, 11),
            ("Chunk", 35, 6),
            ("Nugget", 65, 2),
        ]
    },
    "Abandoned Mine Runoff": {
        "stamina_cost": 16,
        "image": "assets/rivers/mine_runoff.png",
        "description": "Dangerous waters, big payouts.",
        "loot_table": [
            ("Mud", 0, 22),
            ("Tiny Fleck", 7, 20),
            ("Small Flake", 14, 20),
            ("Pebble", 28, 16),
            ("Chunk", 55, 12),
            ("Nugget", 110, 7),
            ("Heavy Nugget", 150, 3),
        ]
    }
}
SHOP_ITEMS = {
    "Pans": [
        {
            "name": "Rusty Pan",
            "cost": 0,
            "luck_bonus": 0,
            "required_stage": 1,
            "description": "Barely holds dirt, but it works."
        },
        {
            "name": "Copper Pan",
            "cost": 75,
            "luck_bonus": 3,
            "required_stage": 1,
            "description": "A little cleaner, a little luckier."
        },
        {
            "name": "Prospector's Pan",
            "cost": 175,
            "luck_bonus": 6,
            "required_stage": 2,
            "description": "A respectable pan for serious mud enjoyers."
        },
        {
            "name": "Lucky Strike Pan",
            "cost": 350,
            "luck_bonus": 10,
            "required_stage": 4,
            "description": "Feels heavy with destiny."
        }
    ],
    "Containers": [
        {
            "name": "Old Bucket",
            "cost": 0,
            "capacity_bonus": 0,
            "required_stage": 1,
            "description": "Leaky, dented, loyal."
        },
        {
            "name": "Supply Sack",
            "cost": 60,
            "capacity_bonus": 3,
            "required_stage": 1,
            "description": "A little more room for your river treasures."
        },
        {
            "name": "Mule Crate",
            "cost": 140,
            "capacity_bonus": 6,
            "required_stage": 2,
            "description": "Carry more, complain less."
        },
        {
            "name": "Hoarder's Chest",
            "cost": 275,
            "capacity_bonus": 10,
            "required_stage": 4,
            "description": "Now you're thinking like a true junky."
        }
    ],
    "Boots": [
        {
            "name": "Wet Sneakers",
            "cost": 0,
            "stamina_reduction": 0,
            "required_stage": 1,
            "description": "Terrible idea, honestly."
        },
        {
            "name": "Rubber Boots",
            "cost": 80,
            "stamina_reduction": 1,
            "required_stage": 1,
            "description": "Keeps your feet dry-ish."
        },
        {
            "name": "Hip Waders",
            "cost": 180,
            "stamina_reduction": 2,
            "required_stage": 3,
            "description": "Less suffering per scoop."
        },
        {
            "name": "River Warden Waders",
            "cost": 320,
            "stamina_reduction": 3,
            "required_stage": 5,
            "description": "Stride into the current like a legend."
        }
    ],
    "Coolers": [
        {
            "name": "Lunch Cooler",
            "cost": 0,
            "consumable_slots": 2,
            "required_stage": 1,
            "description": "A beat-up little cooler with just enough room for poor planning."
        },
        {
            "name": "Cheap Foam Cooler",
            "cost": 70,
            "consumable_slots": 2,
            "required_stage": 1,
            "description": "Barely insulated, but technically useful."
        },
        {
            "name": "River Cooler",
            "cost": 155,
            "consumable_slots": 4,
            "required_stage": 3,
            "description": "Enough room for a proper bad decision."
        },
        {
            "name": "Party Barge Cooler",
            "cost": 295,
            "consumable_slots": 8,
            "required_stage": 5,
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