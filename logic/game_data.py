"""
game_data.py — MuRuZ Character Build Helper
All class definitions, base stats, and formulas extracted from reference documents.

Sources:
  - MU_Gold_Rules.rtf           → level points, reset bonus, base stats
  - Character_Reset_Requirements.rtf → 350 pts/reset
  - MU_Character_Hunter.rtf     → Hunter formulas
  - MU_Character_Slayer.rtf     → Slayer formulas
  - MU_Other_Characters.rtf     → DK, DW, Elf, MG, DL, Summoner, RF, GL formulas
  - MU_Legacy_Server_Logic.rtf  → server-specific formula overrides
"""

# ──────────────────────────────────────────────
# Constants
# ──────────────────────────────────────────────
MAX_LEVEL = 400
RESET_BONUS_POINTS = 350        # per Character_Reset_Requirements.rtf
BASE_STAT_VALUE = 25            # every stat starts at 25

# Points per level by class (from MU_Gold_Rules.rtf)
POINTS_PER_LEVEL = {
    "Hunter": 7,
    "Slayer": 7,
    "Dark Knight": 5,
    "Dark Wizard": 5,
    "Elf": 5,
    "Summoner": 5,
    "Magic Gladiator": 7,
    "Dark Lord": 7,
    "Rage Fighter": 7,
    "Grow Lancer": 7,
}

CLASS_LIST = list(POINTS_PER_LEVEL.keys())

# Only Dark Lord has Command
HAS_CMD = {c: (c == "Dark Lord") for c in CLASS_LIST}

STAT_NAMES_BASE = ["str", "agi", "vit", "ene"]
STAT_NAMES_DL   = ["str", "agi", "vit", "ene", "cmd"]

def stat_names_for(class_name):
    return STAT_NAMES_DL if HAS_CMD[class_name] else STAT_NAMES_BASE

# ──────────────────────────────────────────────
# Total available stat points
# ──────────────────────────────────────────────
def total_stat_points(class_name, level, resets):
    """Return distributable stat points (excluding base 25 per stat)."""
    ppl = POINTS_PER_LEVEL[class_name]
    level_pts = (level - 1) * ppl
    reset_pts = resets * RESET_BONUS_POINTS
    return level_pts + reset_pts


# ──────────────────────────────────────────────
# Derived-stat computation per class
# ──────────────────────────────────────────────
def _compute_hunter(s, a, v, e, _c, lvl):
    defense = a / 4
    return {
        "min_damage":   s / 4,
        "max_damage":   s / 3,
        "avg_damage":   s * 7 / 24,           # (1/4+1/3)/2
        "speed":        a / 50,
        "defense":      defense,
        "pvm_dr":       a / 3,
        "pvm_ar":       lvl * 5 + (a * 3) / 2 + s / 4,
        "pvp_dr":       lvl * 2 + a,
        "pvp_ar":       lvl * 3 + a * 4,
        "hp":           v * 2.5,
        "mana":         e * 2,
        "sd":           (s + a + v + e) * 1.2 + defense / 2 + (lvl ** 2) / 30,
        "skill_pct":    200 + e / 8,
    }

def _compute_slayer(s, a, v, e, _c, lvl):
    defense = a / 4
    return {
        "min_damage":   s / 5,
        "max_damage":   s / 3,
        "avg_damage":   s * 4 / 15,           # (1/5+1/3)/2
        "combo_dmg":    s * 1.6 + e * 1.6,
        "speed":        a / 15,
        "defense":      defense,
        "pvm_dr":       a / 4,
        "pvm_ar":       lvl * 5 + (a * 3) / 2 + s / 4,
        "pvp_dr":       lvl * 2 + a * 0.5,
        "pvp_ar":       lvl * 3 + a * 5,
        "hp":           v * 3,
        "mana":         e * 1.5,
        "sd":           (s + a + v + e) * 1.2 + defense / 2 + (lvl ** 2) / 30,
        "skill_pct":    200 + e / 5,
        "weapon_skill": 200 + e / 15,
    }

def _compute_dk(s, a, v, e, _c, lvl):
    defense = a / 3
    return {
        "min_damage":   s / 6,
        "max_damage":   s / 4,
        "avg_damage":   s * 5 / 24,           # (1/6+1/4)/2
        "combo_dmg":    s * 1.5 + a + e,
        "speed":        a / 15,
        "defense":      defense,
        "pvm_dr":       a / 3,
        "pvm_ar":       lvl * 5 + a * 1.5 + s / 4,
        "pvp_dr":       lvl * 2 + a / 2,
        "pvp_ar":       lvl * 3 + a * 4.5,
        "hp":           v * 3,
        "mana":         e * 1,
        "sd":           (s + a + v + e) * 1.2 + defense / 2 + (lvl ** 2) / 30,
        "skill_pct":    200 + e / 10,
    }

def _compute_dw(s, a, v, e, _c, lvl):
    defense = a / 4
    return {
        "min_damage":   e / 9,
        "max_damage":   e / 4,
        "avg_damage":   e * 13 / 72,          # (1/9+1/4)/2
        "speed":        a / 10,
        "defense":      defense,
        "pvm_dr":       a / 3,
        "pvm_ar":       lvl * 5 + a * 1.5 + s / 4,
        "pvp_dr":       lvl * 2 + a / 4,
        "pvp_ar":       lvl * 3 + a * 4,
        "hp":           v * 2,
        "mana":         e * 2,
        "sd":           (s + a + v + e) * 1.2 + defense / 2 + (lvl ** 2) / 30,
        "skill_pct":    100 + e / 80,
        "soul_barrier": 30 + e / 1000,
    }

def _compute_elf(s, a, v, e, _c, lvl):
    defense = a / 8
    return {
        "min_damage":   s / 3 + a / 5,
        "max_damage":   s / 2 + a / 3,
        "avg_damage":   s * 5 / 12 + a * 4 / 15,
        "speed":        a / 50,
        "defense":      defense,
        "pvm_dr":       a / 4,
        "pvm_ar":       lvl * 5 + a * 1.5 + s / 4,
        "pvp_dr":       lvl * 2 + a / 10,
        "pvp_ar":       lvl * 3 + a * 3,
        "hp":           v * 2,
        "mana":         e * 1.5,
        "sd":           (s + a + v + e) * 1.2 + defense / 2 + (lvl ** 2) / 30,
        "skill_pct":    200 + e / 10,
    }

def _compute_summoner(s, a, v, e, _c, lvl):
    defense = a / 4
    return {
        "min_damage":   e / 8,
        "max_damage":   e / 3,
        "avg_damage":   e * 11 / 48,
        "speed":        a / 20,
        "defense":      defense,
        "pvm_dr":       a / 3,
        "pvm_ar":       lvl * 5 + a * 1.5 + s / 4,
        "pvp_dr":       lvl * 2 + a / 4,
        "pvp_ar":       lvl * 3 + a * 3.5,
        "hp":           v * 2,
        "mana":         e * 2,
        "sd":           (s + a + v + e) * 1.2 + defense / 2 + (lvl ** 2) / 30,
        "skill_pct":    200 + e / 800,
        "berserker":    e / 50,
    }

def _compute_mg(s, a, v, e, _c, lvl):
    defense = a / 4
    phys_avg = s * 5 / 24
    mag_avg  = e * 13 / 72
    return {
        "min_damage":   s / 6,
        "max_damage":   s / 4,
        "avg_damage":   max(phys_avg, mag_avg),
        "phys_damage":  phys_avg,
        "magic_damage": mag_avg,
        "speed":        a / 15,
        "defense":      defense,
        "pvm_dr":       a / 3,
        "pvm_ar":       lvl * 5 + a * 1.5 + s / 4,
        "pvp_dr":       lvl * 2 + a / 4,
        "pvp_ar":       lvl * 3 + a * 3.5,
        "hp":           v * 3.5,
        "mana":         e * 2,
        "sd":           (s + a + v + e) * 1.2 + defense / 2 + (lvl ** 2) / 30,
        "phys_skill":   150 + e / 12,
        "magic_skill":  100 + e / 75,
        "skill_pct":    max(150 + e / 12, 100 + e / 75),
    }

def _compute_dl(s, a, v, e, c, lvl):
    defense = a / 7
    return {
        "min_damage":   (s * 2 + e) / 14,
        "max_damage":   (s * 2 + e) / 10,
        "avg_damage":   (s * 2 + e) * 3 / 35,
        "speed":        a / 10,
        "defense":      defense,
        "pvm_dr":       a / 3,
        "pvm_ar":       lvl * 5 + a * 3 + s / 4 + c / 10,
        "pvp_dr":       lvl * 2 + a / 2,
        "pvp_ar":       lvl * 3 + a * 4,
        "hp":           v * 3,
        "mana":         e * 1.5,
        "sd":           (s + a + v + e + c) * 1.2 + defense / 2 + (lvl ** 2) / 30,
        "skill_pct":    200 + e / 15,
        "chaotic_pct":  200 + e / 40,
    }

def _compute_rf(s, a, v, e, _c, lvl):
    defense = a / 5
    return {
        "min_damage":   s / 7 + v / 15,
        "max_damage":   s / 5 + v / 12,
        "avg_damage":   s * 6 / 35 + v * 9 / 60,
        "speed":        a / 9,
        "defense":      defense,
        "pvm_dr":       a / 3,
        "pvm_ar":       lvl * 5 + a * 1.5 + s / 4,
        "pvp_dr":       lvl * 2 + a / 2,
        "pvp_ar":       lvl * 2.6 + a * 3.6,
        "hp":           v * 3,
        "mana":         e * 1,
        "sd":           (s + a + v + e) * 1.2 + defense / 2 + (lvl ** 2) / 30,
        "skill_pct":    200 + e / 10,
        "dark_side":    200 + a / 35 + e / 15,
    }

def _compute_gl(s, a, v, e, _c, lvl):
    defense = a / 3
    return {
        "min_damage":   s / 8,
        "max_damage":   s / 4,
        "avg_damage":   s * 3 / 16,
        "speed":        a / 20,
        "defense":      defense,
        "pvm_dr":       a / 3,
        "pvm_ar":       lvl * 5 + a * 1.5 + s / 4,
        "pvp_dr":       lvl * 2 + a / 2,
        "pvp_ar":       lvl * 3 + a * 2,
        "hp":           v * 3,
        "mana":         e * 1.5,
        "sd":           (s + a + v + e) * 1.2 + defense / 2 + (lvl ** 2) / 30,
        "skill_pct":    100 + s / 10,      # Retaliation uses STR
        "rage_skill":   100 + a / 10,
    }


COMPUTE_FN = {
    "Hunter":           _compute_hunter,
    "Slayer":           _compute_slayer,
    "Dark Knight":      _compute_dk,
    "Dark Wizard":      _compute_dw,
    "Elf":              _compute_elf,
    "Summoner":         _compute_summoner,
    "Magic Gladiator":  _compute_mg,
    "Dark Lord":        _compute_dl,
    "Rage Fighter":     _compute_rf,
    "Grow Lancer":      _compute_gl,
}


def compute_derived(class_name, str_v, agi_v, vit_v, ene_v, cmd_v, level):
    """Return dict of all derived stats for the given class and allocation."""
    fn = COMPUTE_FN[class_name]
    return fn(str_v, agi_v, vit_v, ene_v, cmd_v, level)


# ──────────────────────────────────────────────
# Partial derivatives  (d derived / d stat)
# Used by the optimizer to compute marginal benefits.
# All formulas are linear so partials are constants.
# ──────────────────────────────────────────────
def _hunter_partials():
    return {
        "str": {"avg_damage": 7/24, "pvm_ar": 0.25, "sd": 1.2},
        "agi": {"speed": 1/50, "defense": 0.25, "pvm_dr": 1/3,
                "pvm_ar": 1.5, "pvp_dr": 1.0, "pvp_ar": 4.0, "sd": 1.2 + 0.125},
        "vit": {"hp": 2.5, "sd": 1.2},
        "ene": {"skill_pct": 1/8, "mana": 2.0, "sd": 1.2},
    }

def _slayer_partials():
    return {
        "str": {"avg_damage": 4/15, "combo_dmg": 1.6, "pvm_ar": 0.25, "sd": 1.2},
        "agi": {"speed": 1/15, "defense": 0.25, "pvm_dr": 0.25,
                "pvm_ar": 1.5, "pvp_dr": 0.5, "pvp_ar": 5.0, "sd": 1.2 + 0.125},
        "vit": {"hp": 3.0, "sd": 1.2},
        "ene": {"skill_pct": 1/5, "combo_dmg": 1.6, "weapon_skill": 1/15, "mana": 1.5, "sd": 1.2},
    }

def _dk_partials():
    return {
        "str": {"avg_damage": 5/24, "combo_dmg": 1.5, "pvm_ar": 0.25, "sd": 1.2},
        "agi": {"speed": 1/15, "defense": 1/3, "pvm_dr": 1/3,
                "pvm_ar": 1.5, "pvp_dr": 0.5, "pvp_ar": 4.5, "sd": 1.2 + 1/6, "combo_dmg": 1.0},
        "vit": {"hp": 3.0, "sd": 1.2},
        "ene": {"skill_pct": 1/10, "mana": 1.0, "sd": 1.2, "combo_dmg": 1.0},
    }

def _dw_partials():
    return {
        "str": {"pvm_ar": 0.25, "sd": 1.2},
        "agi": {"speed": 1/10, "defense": 0.25, "pvm_dr": 1/3,
                "pvm_ar": 1.5, "pvp_dr": 0.25, "pvp_ar": 4.0, "sd": 1.2 + 0.125},
        "vit": {"hp": 2.0, "sd": 1.2},
        "ene": {"avg_damage": 13/72, "skill_pct": 1/80, "soul_barrier": 1/1000,
                "mana": 2.0, "sd": 1.2},
    }

def _elf_partials():
    return {
        "str": {"avg_damage": 5/12, "pvm_ar": 0.25, "sd": 1.2},
        "agi": {"avg_damage": 4/15, "speed": 1/50, "defense": 1/8,
                "pvm_dr": 0.25, "pvm_ar": 1.5, "pvp_dr": 0.1, "pvp_ar": 3.0,
                "sd": 1.2 + 1/16},
        "vit": {"hp": 2.0, "sd": 1.2},
        "ene": {"skill_pct": 1/10, "mana": 1.5, "sd": 1.2},
    }

def _summoner_partials():
    return {
        "str": {"pvm_ar": 0.25, "sd": 1.2},
        "agi": {"speed": 1/20, "defense": 0.25, "pvm_dr": 1/3,
                "pvm_ar": 1.5, "pvp_dr": 0.25, "pvp_ar": 3.5, "sd": 1.2 + 0.125},
        "vit": {"hp": 2.0, "sd": 1.2},
        "ene": {"avg_damage": 11/48, "skill_pct": 1/800, "berserker": 1/50,
                "mana": 2.0, "sd": 1.2},
    }

def _mg_partials():
    return {
        "str": {"avg_damage": 5/24, "pvm_ar": 0.25, "sd": 1.2},
        "agi": {"speed": 1/15, "defense": 0.25, "pvm_dr": 1/3,
                "pvm_ar": 1.5, "pvp_dr": 0.25, "pvp_ar": 3.5, "sd": 1.2 + 0.125},
        "vit": {"hp": 3.5, "sd": 1.2},
        "ene": {"avg_damage": 13/72, "phys_skill": 1/12, "magic_skill": 1/75,
                "mana": 2.0, "sd": 1.2},
    }

def _dl_partials():
    return {
        "str": {"avg_damage": 6/35, "pvm_ar": 0.25, "sd": 1.2},
        "agi": {"speed": 1/10, "defense": 1/7, "pvm_dr": 1/3,
                "pvm_ar": 3.0, "pvp_dr": 0.5, "pvp_ar": 4.0, "sd": 1.2 + 1/14},
        "vit": {"hp": 3.0, "sd": 1.2},
        "ene": {"avg_damage": 3/35, "skill_pct": 1/15, "chaotic_pct": 1/40,
                "mana": 1.5, "sd": 1.2},
        "cmd": {"pvm_ar": 0.1, "sd": 1.2},
    }

def _rf_partials():
    return {
        "str": {"avg_damage": 6/35, "pvm_ar": 0.25, "sd": 1.2},
        "agi": {"speed": 1/9, "defense": 1/5, "pvm_dr": 1/3,
                "pvm_ar": 1.5, "pvp_dr": 0.5, "pvp_ar": 3.6,
                "dark_side": 1/35, "sd": 1.2 + 1/10},
        "vit": {"avg_damage": 9/60, "hp": 3.0, "sd": 1.2},
        "ene": {"skill_pct": 1/10, "dark_side": 1/15, "mana": 1.0, "sd": 1.2},
    }

def _gl_partials():
    return {
        "str": {"avg_damage": 3/16, "skill_pct": 1/10, "pvm_ar": 0.25, "sd": 1.2},
        "agi": {"speed": 1/20, "defense": 1/3, "pvm_dr": 1/3,
                "pvm_ar": 1.5, "pvp_dr": 0.5, "pvp_ar": 2.0,
                "rage_skill": 1/10, "sd": 1.2 + 1/6},
        "vit": {"hp": 3.0, "sd": 1.2},
        "ene": {"mana": 1.5, "sd": 1.2},
    }


CLASS_PARTIALS = {
    "Hunter":           _hunter_partials(),
    "Slayer":           _slayer_partials(),
    "Dark Knight":      _dk_partials(),
    "Dark Wizard":      _dw_partials(),
    "Elf":              _elf_partials(),
    "Summoner":         _summoner_partials(),
    "Magic Gladiator":  _mg_partials(),
    "Dark Lord":        _dl_partials(),
    "Rage Fighter":     _rf_partials(),
    "Grow Lancer":      _gl_partials(),
}


# ──────────────────────────────────────────────
# Build-type weights on derived stats
# ──────────────────────────────────────────────
# These weights define what matters for each build archetype.
# Higher weight = the optimizer values that derived stat more.

BUILD_WEIGHTS = {
    "farm": {
        "avg_damage":   8.0,     # need to one-shot mobs
        "combo_dmg":    3.0,
        "speed":       15.0,     # faster kills per second
        "defense":      1.0,
        "pvm_dr":       1.0,
        "pvm_ar":       4.0,     # must hit mobs
        "pvp_dr":       0.0,
        "pvp_ar":       0.0,
        "hp":           1.5,     # just enough to survive
        "mana":         0.5,
        "sd":           0.5,
        "skill_pct":    6.0,     # AoE skill damage multiplier
        "weapon_skill": 4.0,
        "phys_skill":   5.0,
        "magic_skill":  5.0,
        "berserker":    4.0,
        "dark_side":    5.0,
        "rage_skill":   4.0,
        "chaotic_pct":  3.0,
        "soul_barrier":  0.0,
        "phys_damage":  4.0,
        "magic_damage": 4.0,
    },
    "pve": {
        "avg_damage":   6.0,
        "combo_dmg":    4.0,
        "speed":        5.0,
        "defense":      5.0,     # reduce damage from bosses
        "pvm_dr":       4.0,
        "pvm_ar":       4.0,
        "pvp_dr":       0.0,
        "pvp_ar":       0.0,
        "hp":           6.0,     # survive boss hits
        "mana":         1.0,
        "sd":           4.0,
        "skill_pct":    5.0,
        "weapon_skill": 4.0,
        "phys_skill":   4.0,
        "magic_skill":  4.0,
        "berserker":    4.0,
        "dark_side":    4.0,
        "rage_skill":   4.0,
        "chaotic_pct":  3.0,
        "soul_barrier":  2.0,
        "phys_damage":  3.0,
        "magic_damage": 3.0,
    },
    "pvp": {
        "avg_damage":   7.0,     # burst damage
        "combo_dmg":    6.0,     # combo is key in PvP
        "speed":        4.0,
        "defense":      4.0,
        "pvm_dr":       0.0,
        "pvm_ar":       0.0,
        "pvp_dr":       8.0,     # dodge enemy attacks
        "pvp_ar":       9.0,     # must hit players
        "hp":           4.0,
        "mana":         1.0,
        "sd":           6.0,     # shield defense critical in PvP
        "skill_pct":    4.0,
        "weapon_skill": 4.0,
        "phys_skill":   3.0,
        "magic_skill":  3.0,
        "berserker":    5.0,
        "dark_side":    5.0,
        "rage_skill":   3.0,
        "chaotic_pct":  4.0,
        "soul_barrier":  5.0,
        "phys_damage":  3.0,
        "magic_damage": 3.0,
    },
}


# ──────────────────────────────────────────────
# Build explanation templates per class
# ──────────────────────────────────────────────
# Primary damage stat for description purposes
CLASS_DAMAGE_STAT = {
    "Hunter":          "STR",
    "Slayer":          "STR+ENE",
    "Dark Knight":     "STR",
    "Dark Wizard":     "ENE",
    "Elf":             "STR+AGI",
    "Summoner":        "ENE",
    "Magic Gladiator": "STR or ENE",
    "Dark Lord":       "STR+ENE",
    "Rage Fighter":    "STR+VIT",
    "Grow Lancer":     "STR",
}

CLASS_SPEED_FORMULA = {
    "Hunter":          "AGI / 50",
    "Slayer":          "AGI / 15",
    "Dark Knight":     "AGI / 15",
    "Dark Wizard":     "AGI / 10",
    "Elf":             "AGI / 50",
    "Summoner":        "AGI / 20",
    "Magic Gladiator": "AGI / 15",
    "Dark Lord":       "AGI / 10",
    "Rage Fighter":    "AGI / 9",
    "Grow Lancer":     "AGI / 20",
}

CLASS_DEFENSE_FORMULA = {
    "Hunter":          "AGI / 4",
    "Slayer":          "AGI / 4",
    "Dark Knight":     "AGI / 3",
    "Dark Wizard":     "AGI / 4",
    "Elf":             "AGI / 8",
    "Summoner":        "AGI / 4",
    "Magic Gladiator": "AGI / 4",
    "Dark Lord":       "AGI / 7",
    "Rage Fighter":    "AGI / 5",
    "Grow Lancer":     "AGI / 3",
}
