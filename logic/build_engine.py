"""
calc_engine.py — MuRuZ Character Build Helper
Optimization engine that recommends stat distributions using formula-derived scoring.
"""

import math
from logic.game_data import (
    BASE_STAT_VALUE, RESET_BONUS_POINTS, POINTS_PER_LEVEL,
    CLASS_PARTIALS, BUILD_WEIGHTS, HAS_CMD,
    stat_names_for, total_stat_points, compute_derived,
    CLASS_DAMAGE_STAT, CLASS_SPEED_FORMULA, CLASS_DEFENSE_FORMULA,
)
from core.locales import get_text


# ──────────────────────────────────────────────
# Input validation
# ──────────────────────────────────────────────

def validate_input(class_name, resets, level, stats_dict, remaining, lang="en"):
    """
    Validate user inputs. Returns (is_valid, error_message, bonus_points).
    """
    errors = []
    bonus = 0

    if level < 1 or level > 400:
        errors.append(get_text(lang, "err_lvl"))

    if resets < 0:
        errors.append(get_text(lang, "err_rst"))

    if remaining < 0:
        errors.append(get_text(lang, "err_rem"))

    snames = stat_names_for(class_name)
    for sn in snames:
        val = stats_dict.get(sn, BASE_STAT_VALUE)
        if val < BASE_STAT_VALUE:
            errors.append(get_text(lang, "err_base", stat=sn.upper(), base=BASE_STAT_VALUE))

    # Check total points consistency
    formula_total = total_stat_points(class_name, level, resets)
    spent = sum(stats_dict.get(sn, BASE_STAT_VALUE) - BASE_STAT_VALUE for sn in snames)
    actual_total = spent + remaining    # what the player actually has

    if actual_total > formula_total:
        # Player has bonus points from in-game sources (MMA, quests, etc.)
        bonus = actual_total - formula_total
    elif actual_total < formula_total:
        # Player has fewer points than expected. Just inform, don't block.
        diff = formula_total - actual_total
        errors.append(get_text(lang, "err_miss", form=formula_total, act=actual_total, diff=diff))

    if errors:
        return False, "\n".join(errors), bonus
    return True, "", bonus


# ──────────────────────────────────────────────
# Scoring & marginal-benefit computation
# ──────────────────────────────────────────────

def _compute_marginal_benefits(class_name, stats, level, build_type):
    partials = CLASS_PARTIALS[class_name]
    weights  = BUILD_WEIGHTS[build_type]
    derived  = compute_derived(
        class_name,
        stats.get("str", BASE_STAT_VALUE),
        stats.get("agi", BASE_STAT_VALUE),
        stats.get("vit", BASE_STAT_VALUE),
        stats.get("ene", BASE_STAT_VALUE),
        stats.get("cmd", BASE_STAT_VALUE),
        level,
    )

    benefits = {}
    for stat_name in stat_names_for(class_name):
        if stat_name not in partials:
            benefits[stat_name] = -1.0
            continue
        b = 0.0
        for derived_name, coeff in partials[stat_name].items():
            w = weights.get(derived_name, 0.0)
            d_val = derived.get(derived_name, 0.0)
            if w > 0 and coeff > 0:
                b += w * coeff / (1.0 + abs(d_val))
        benefits[stat_name] = b

    return benefits


# ──────────────────────────────────────────────
# Greedy optimizer with adaptive chunking
# ──────────────────────────────────────────────

def optimize_build(class_name, total_points, level, build_type, allow_vit=True):
    """Greedy optimizer: allocate total_points across stats from base."""
    snames = stat_names_for(class_name)
    stats = {s: BASE_STAT_VALUE for s in snames}
    remaining = total_points

    chunk = max(1, remaining // 50)

    while remaining > 0:
        alloc = min(chunk, remaining)
        benefits = _compute_marginal_benefits(class_name, stats, level, build_type)

        if not allow_vit and "vit" in benefits:
            # Force optimizer to never pick VIT
            benefits["vit"] = -1.0

        best_stat = max(benefits, key=benefits.get)
        stats[best_stat] += alloc
        remaining -= alloc

        if remaining < total_points * 0.3 and chunk > 10:
            chunk = max(10, chunk // 3)
        if remaining < total_points * 0.05 and chunk > 1:
            chunk = 1

    return stats


# ──────────────────────────────────────────────
# Public API — generate all 3 builds
# ──────────────────────────────────────────────

BUILD_TYPES = ["farm", "pve", "pvp"]

def generate_builds(class_name, level, resets, bonus_points=0, allow_vit=True, lang="en"):
    """
    Generate optimized builds for all 3 build types.
    """
    formula_pts = total_stat_points(class_name, level, resets)
    total_pts = formula_pts + bonus_points
    results = []

    for bt in BUILD_TYPES:
        stats = optimize_build(class_name, total_pts, level, bt, allow_vit)
        derived = compute_derived(
            class_name,
            stats["str"], stats["agi"], stats["vit"], stats["ene"],
            stats.get("cmd", BASE_STAT_VALUE), level,
        )
        explanation = _build_explanation(
            class_name, bt, stats, derived, level, resets,
            total_pts, formula_pts, bonus_points, allow_vit, lang
        )

        results.append({
            "type":        bt,
            "label":       get_text(lang, f"{bt}_lbl"),
            "focus":       get_text(lang, f"{bt}_focus"),
            "stats":       stats,
            "derived":     derived,
            "explanation": explanation,
            "total_pts":   total_pts,
        })

    return results


def _build_explanation(class_name, build_type, stats, derived, level, resets,
                       total_pts, formula_pts, bonus_points, allow_vit, lang):
    """Generate localized, human-readable explanation."""
    snames = stat_names_for(class_name)
    dmg_stat = CLASS_DAMAGE_STAT[class_name]
    spd_formula = CLASS_SPEED_FORMULA[class_name]
    def_formula = CLASS_DEFENSE_FORMULA[class_name]

    allocations = {s: stats[s] - BASE_STAT_VALUE for s in snames}
    primary = max(allocations, key=allocations.get)
    pct = {s: round(100 * allocations[s] / max(1, total_pts), 1) for s in snames}

    lines = []
    lines.append(get_text(lang, "exp_total", pts=total_pts))
    lines.append(get_text(lang, "exp_form", lvl=level, ppl=POINTS_PER_LEVEL[class_name], rst=resets, form=formula_pts))
    if bonus_points > 0:
        lines.append(get_text(lang, "exp_bonus", bonus=bonus_points))
    lines.append("")

    lines.append(get_text(lang, "exp_alloc"))
    for s in snames:
        lines.append(f"  {s.upper():>3}: {stats[s]:>6,}  ({pct[s]}{get_text(lang, 'exp_pct')})")
    lines.append("")

    lines.append(get_text(lang, "exp_der"))
    lines.append(f"  {get_text(lang, 'der_dmg'):<20} {derived.get('avg_damage', 0):,.1f}")
    if "combo_dmg" in derived:
        lines.append(f"  {get_text(lang, 'der_combo'):<20} {derived['combo_dmg']:,.1f}")
    lines.append(f"  {get_text(lang, 'der_spd'):<20} {derived.get('speed', 0):,.1f}")
    lines.append(f"  {get_text(lang, 'der_def'):<20} {derived.get('defense', 0):,.1f}")
    lines.append(f"  {get_text(lang, 'der_hp'):<20} {derived.get('hp', 0):,.1f}")
    lines.append(f"  {get_text(lang, 'der_sd'):<20} {derived.get('sd', 0):,.1f}")
    lines.append(f"  {get_text(lang, 'der_skill'):<20} {derived.get('skill_pct', 0):,.1f}%")
    
    if build_type in ("farm", "pve"):
        lines.append(f"  {get_text(lang, 'der_pvm_ar'):<20} {derived.get('pvm_ar', 0):,.1f}")
        lines.append(f"  {get_text(lang, 'der_pvm_dr'):<20} {derived.get('pvm_dr', 0):,.1f}")
    if build_type == "pvp":
        lines.append(f"  {get_text(lang, 'der_pvp_ar'):<20} {derived.get('pvp_ar', 0):,.1f}")
        lines.append(f"  {get_text(lang, 'der_pvp_dr'):<20} {derived.get('pvp_dr', 0):,.1f}")
    lines.append("")

    lines.append(get_text(lang, "exp_rsn"))
    
    if not allow_vit:
        lines.append(f"  {get_text(lang, 'r_vit_skip')}")

    if build_type == "farm":
        lines.append(f"  {get_text(lang, 'r_f_prim', stat=dmg_stat)}")
        lines.append(f"  {get_text(lang, 'r_f_spd', form=spd_formula)}")
        lines.append(f"  {get_text(lang, 'r_f_aoe')}")
        if allow_vit: lines.append(f"  {get_text(lang, 'r_f_vit')}")
        lines.append(f"  {get_text(lang, 'r_f_high', stat=primary.upper(), pct=pct[primary])}")
    elif build_type == "pve":
        lines.append(f"  {get_text(lang, 'r_e_bal', stat=dmg_stat)}")
        lines.append(f"  {get_text(lang, 'r_e_def', form=def_formula)}")
        if allow_vit: lines.append(f"  {get_text(lang, 'r_e_vit')}")
        lines.append(f"  {get_text(lang, 'r_e_skill')}")
        lines.append(f"  {get_text(lang, 'r_e_high', stat=primary.upper(), pct=pct[primary])}")
    elif build_type == "pvp":
        lines.append(f"  {get_text(lang, 'r_p_brst', stat=dmg_stat)}")
        lines.append(f"  {get_text(lang, 'r_p_ar')}")
        lines.append(f"  {get_text(lang, 'r_p_dr')}")
        lines.append(f"  {get_text(lang, 'r_p_sd')}")
        lines.append(f"  {get_text(lang, 'r_p_high', stat=primary.upper(), pct=pct[primary])}")

    return "\n".join(lines)
