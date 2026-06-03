SCREEN_WIDTH  = 1920
SCREEN_HEIGHT = 1080
FPS           = 60
TITLE         = "Baldi's Coding Basics"

import os
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR     = os.path.join(BASE_DIR, "assets", "maps")
MAP_DATA_FILE = os.path.join(BASE_DIR, "map_data.json")
MAP_FILE      = "FullMap.png"
MAP_KEY       = "FullMap"

CHUNK_SIZE = 512

HB_COLORS = {
    "walls":               (255,  60,  60),
    "doors":               ( 60, 200, 255),
    "computers":           ( 60, 220,  80),
    "spawns":              (255, 220,  40),
    "monster_spawns":      (180,  60, 255),
    "baldi_checkpoints":   (255, 140,   0),   # orange dots
}

INTERACT_DIST = 120

SCORE_CORRECT = 100
SCORE_WRONG   = -25

DIFFICULTY = {
    "Beginner": {
        "computers":      4,
        "score_correct":  150,
        "score_wrong":    -10,
        "enemy_speed":    1.5,
        "label_color":    (80, 220, 120),
    },
    "Medium": {
        "computers":      6,
        "score_correct":  100,
        "score_wrong":    -25,
        "enemy_speed":    2.5,
        "label_color":    (255, 200, 60),
    },
    "Chase Level": {
        "computers":      8,
        "score_correct":  75,
        "score_wrong":    -50,
        "enemy_speed":    4.0,
        "label_color":    (255, 60, 60),
    },
}

LANGUAGES    = ["Python", "Ruby", "Arduino"]
DIFFICULTIES = list(DIFFICULTY.keys())