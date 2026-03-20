"""Quick verification test for MuRuZ Build Helper logic."""
import sys
sys.path.insert(0, '.')

from logic.game_data import total_stat_points, compute_derived, CLASS_LIST, stat_names_for
from logic.build_engine import validate_input, generate_builds

print("=" * 60)
print("  MuRuZ Character Build Helper — Verification Tests")
print("=" * 60)

# Test 1: Total stat points calculation
print("\n--- Test 1: Point Calculations ---")
pts = total_stat_points("Hunter", 400, 4)
assert pts == 4193, f"Expected 4193, got {pts}"
print(f"  Hunter Lv400 R4: {pts} pts  OK")

pts = total_stat_points("Dark Knight", 400, 10)
assert pts == 5495, f"Expected 5495, got {pts}"
print(f"  DK Lv400 R10:    {pts} pts  OK")

# Test 2: Derived stats
print("\n--- Test 2: Formula Verification ---")
d = compute_derived("Hunter", 1000, 2000, 500, 200, 0, 400)
assert abs(d["min_damage"] - 250.0) < 0.01
assert abs(d["max_damage"] - 333.33) < 0.1
assert abs(d["speed"] - 40.0) < 0.01
assert abs(d["defense"] - 500.0) < 0.01
assert abs(d["hp"] - 1250.0) < 0.01
print(f"  Hunter formulas verified  OK")

d = compute_derived("Dark Wizard", 100, 300, 400, 2000, 0, 400)
assert abs(d["min_damage"] - 2000/9) < 0.1
assert abs(d["speed"] - 30.0) < 0.01
print(f"  Dark Wizard formulas verified  OK")

# Test 3: Build generation (all classes)
print("\n--- Test 3: Build Generation ---")
for cls in CLASS_LIST:
    builds = generate_builds(cls, 400, 10)
    assert len(builds) == 3, f"{cls}: expected 3 builds"
    for b in builds:
        snames = stat_names_for(cls)
        total_alloc = sum(b["stats"][s] - 25 for s in snames)
        expected = total_stat_points(cls, 400, 10)
        assert total_alloc == expected, (
            f"{cls} {b['type']}: allocated {total_alloc}, expected {expected}")
        for s in snames:
            assert b["stats"][s] >= 25, f"{cls} {b['type']}: {s}={b['stats'][s]} < 25"
    print(f"  {cls:20s} — 3 builds, points match  OK")

# Test 4: Bonus points detection
print("\n--- Test 4: Bonus Points Detection ---")
# Player has more points than formula says -> bonus detected
ok, msg, bonus = validate_input("Hunter", 4, 400, {"str": 1000, "agi": 2000, "vit": 500, "ene": 800}, 100)
# spent = 975+1975+475+775 = 4200, remaining = 100 -> actual = 4300, formula = 4193
# bonus = 4300 - 4193 = 107
assert ok, f"Should be valid, got: {msg}"
assert bonus == 107, f"Expected 107 bonus pts, got {bonus}"
print(f"  Bonus points detected: {bonus}  OK")

# Exact match -> OK, no bonus
ok, msg, bonus = validate_input("Hunter", 4, 400, {"str": 1000, "agi": 2000, "vit": 500, "ene": 718}, 0)
# spent = 975+1975+475+693 = 4118, remaining = 0, actual = 4118, formula = 4193
# actual < formula -> warning
assert not ok, "Should warn about missing points"
assert bonus == 0
print(f"  Missing points warning works  OK")

# Build with bonus points
builds = generate_builds("Hunter", 400, 10, bonus_points=500)
expected_total = total_stat_points("Hunter", 400, 10) + 500
for b in builds:
    total_alloc = sum(b["stats"][s] - 25 for s in stat_names_for("Hunter"))
    assert total_alloc == expected_total, f"Expected {expected_total}, got {total_alloc}"
print(f"  Builds with bonus points correct  OK")

print("\n" + "=" * 60)
print("  ALL TESTS PASSED")
print("=" * 60)
