

ENTITIES = {
    "homestead": {
        "sprite": "homestead.png",
        "attributes": {
            "max_health": 50,
            "health_regen": 1,
        }
    },
    "player": {
        "sprite": "player.png",
        "attributes": {
            "max_health": 30,
            "health_regen": 1,
            "move_speed": 5,
            "damage": 10,
            "attack_speed": 0.5,
            "attack_range": 10,
        }
    },
    "enemy": {
        "sprite": "zombie.png",
        "attributes": {
            "max_health": 10,
            "move_speed": 0.75,
            "damage": 10,
            "attack_range": 1.0,
            "attack_speed": 0.5,
        },
        "scaling": {
            "max_health": lambda default, t: default * (1.0 + (t / 15.0)),
            "damage": lambda default, t: default * (1.0 + (t / 30.0)),
        }
    },
    "powerup": {
        "sprite": "powerup.png",
        "bonuses": [
            ["damage", 10],
            ["damage", 10],
            ["damage", 10],
            ["max_health", 10],
            ["attack_speed", 0.5],
            ["move_speed", 0.5],
        ],
    },
}
