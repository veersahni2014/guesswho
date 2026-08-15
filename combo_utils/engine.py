"""Combo generation and validation for Blox Fruits."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "combo_moves.json"

CATEGORY_LABELS = {
    "fruit": "Fruit",
    "sword": "Sword",
    "fighting": "Fighting Style",
    "gun": "Gun",
    "melee_m1": "Melee M1",
    "sword_m1": "Sword M1",
}

STAT_PRESETS = {
    "Fruit Main": {"melee": 400, "defense": 400, "fruit": 1750, "sword": 0, "gun": 0},
    "Sword Main": {"melee": 400, "defense": 400, "fruit": 0, "sword": 1750, "gun": 0},
    "Gun Main": {"melee": 400, "defense": 400, "fruit": 0, "sword": 0, "gun": 1750},
    "Hybrid (Fruit + Sword)": {"melee": 400, "defense": 400, "fruit": 875, "sword": 875, "gun": 0},
    "Custom": {"melee": 400, "defense": 400, "fruit": 1750, "sword": 0, "gun": 0},
}


@dataclass
class MoveStep:
    """One step in a combo sequence."""

    key: str
    label: str
    move_name: str
    category: str
    damage: int
    stun: float
    startup: float
    ken_break: bool
    role: str
    notes: str
    scaled_damage: int = 0
    link_margin: float | None = None
    link_ok: bool = True

    @property
    def display_key(self) -> str:
        return f"{CATEGORY_LABELS.get(self.category, self.category)} {self.key}"


@dataclass
class ComboResult:
    """A generated combo with stats and execution tips."""

    steps: list[MoveStep]
    total_damage: int
    total_time: float
    reliability: float
    ken_break_used: bool
    efficiency_score: float
    one_shot_potential: bool
    tips: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


@dataclass
class BuildInput:
    """User build configuration."""

    fruit: str
    sword: str
    fighting_style: str
    gun: str
    race: str
    stat_preset: str
    melee_stat: int
    defense_stat: int
    fruit_stat: int
    sword_stat: int
    gun_stat: int
    opponent_has_ken: bool
    ping_ms: int
    combo_goal: str  # "one_shot", "safe", "max_damage"


def load_combo_data(path: Path | None = None) -> dict[str, Any]:
    """Load move database from JSON."""
    file_path = path or DATA_PATH
    with file_path.open(encoding="utf-8") as file:
        return json.load(file)


def list_options(data: dict[str, Any]) -> dict[str, list[str]]:
    """Return selectable item names per category."""
    return {
        "fruits": sorted(data["fruits"].keys()),
        "swords": sorted(data["swords"].keys()),
        "fighting_styles": sorted(data["fighting_styles"].keys()),
        "guns": sorted(data["guns"].keys()),
        "races": sorted(data["races"].keys()),
        "stat_presets": list(STAT_PRESETS.keys()),
    }


def _scale_damage(base_damage: int, category: str, build: BuildInput) -> int:
    """Scale move damage based on stat investment (simplified formula)."""
    if base_damage <= 0:
        return 0

    meta_cap = 2550
    if category in ("fruit",):
        stat = build.fruit_stat
        multiplier = 1.0 + (stat / meta_cap) * 1.8
    elif category in ("sword", "sword_m1"):
        stat = build.sword_stat
        multiplier = 1.0 + (stat / meta_cap) * 1.8
    elif category in ("fighting", "melee_m1"):
        stat = build.melee_stat
        multiplier = 1.0 + (stat / meta_cap) * 1.6
    elif category == "gun":
        stat = build.gun_stat
        multiplier = 1.0 + (stat / meta_cap) * 1.5
    else:
        multiplier = 1.0

    return int(base_damage * multiplier)


def _resolve_move(
    token: str,
    build: BuildInput,
    data: dict[str, Any],
) -> MoveStep | None:
    """
    Resolve a move token like 'Fruit V' or 'Melee M1 x4' into a MoveStep.

    Token format: '<Category> <Key>' e.g. 'Fruit C', 'Sword M1x3', 'Fighting Z'
    """
    parts = token.strip().split(maxsplit=1)
    if len(parts) != 2:
        return None

    category_word, move_key = parts[0].lower(), parts[1]

    if category_word == "fruit":
        item_data = data["fruits"].get(build.fruit, {})
        category = "fruit"
        prefix = build.fruit
    elif category_word == "sword":
        if move_key.startswith("M1"):
            item_data = data["swords"].get(build.sword, {})
            category = "sword_m1"
            prefix = build.sword
        else:
            item_data = data["swords"].get(build.sword, {})
            category = "sword"
            prefix = build.sword
    elif category_word in ("fighting", "melee"):
        item_data = data["fighting_styles"].get(build.fighting_style, {})
        category = "fighting" if not move_key.startswith("M1") else "melee_m1"
        prefix = build.fighting_style
    elif category_word == "gun":
        item_data = data["guns"].get(build.gun, {})
        category = "gun"
        prefix = build.gun
    else:
        return None

    if not item_data or build.sword == "None" and category_word == "sword":
        return None
    if build.gun == "None" and category_word == "gun":
        return None

    # Normalize M1 keys
    lookup_key = move_key.replace(" ", "")
    moves = item_data.get("moves", {})
    move = moves.get(lookup_key) or moves.get(move_key)
    if not move:
        return None

    scaled = _scale_damage(move["damage"], category, build)
    return MoveStep(
        key=move_key,
        label=f"{prefix} {move_key}",
        move_name=move["name"],
        category=category,
        damage=move["damage"],
        stun=move["stun"],
        startup=move["startup"],
        ken_break=move.get("ken_break", False),
        role=move.get("role", "damage"),
        notes=move.get("notes", ""),
        scaled_damage=scaled,
    )


def _collect_available_moves(build: BuildInput, data: dict[str, Any]) -> list[MoveStep]:
    """Gather all moves available for the user's build."""
    moves: list[MoveStep] = []

    def add_from_item(item_name: str, category_prefix: str, item_category: str) -> None:
        if item_name == "None":
            return
        bucket = {
            "fruit": data["fruits"],
            "sword": data["swords"],
            "fighting": data["fighting_styles"],
            "gun": data["guns"],
        }[item_category]
        item = bucket.get(item_name, {})
        for key, move in item.get("moves", {}).items():
            cat = item_category
            if key.startswith("M1"):
                cat = "sword_m1" if item_category == "sword" else "melee_m1"
            moves.append(
                MoveStep(
                    key=key,
                    label=f"{item_name} {key}",
                    move_name=move["name"],
                    category=cat,
                    damage=move["damage"],
                    stun=move["stun"],
                    startup=move["startup"],
                    ken_break=move.get("ken_break", False),
                    role=move.get("role", "damage"),
                    notes=move.get("notes", ""),
                    scaled_damage=_scale_damage(move["damage"], cat, build),
                )
            )

    add_from_item(build.fruit, "Fruit", "fruit")
    add_from_item(build.sword, "Sword", "sword")
    add_from_item(build.fighting_style, "Fighting", "fighting")
    add_from_item(build.gun, "Gun", "gun")
    return moves


def _ping_buffer(build: BuildInput, data: dict[str, Any]) -> float:
    """Convert ping to seconds plus base buffer."""
    base_ms = data["meta"].get("ping_buffer_ms", 80)
    return (build.ping_ms + base_ms) / 1000.0


def _can_link(previous: MoveStep, current: MoveStep, ping_buffer: float) -> tuple[bool, float]:
    """Check if current move links after previous (true combo)."""
    margin = previous.stun - current.startup - ping_buffer
    return margin >= 0, round(margin, 3)


def validate_combo(steps: list[MoveStep], build: BuildInput, data: dict[str, Any]) -> tuple[list[MoveStep], list[str]]:
    """Validate links between steps and annotate margins."""
    if not steps:
        return [], ["No moves in combo."]

    ping_buffer = _ping_buffer(build, data)
    warnings: list[str] = []
    validated: list[MoveStep] = []

    for index, step in enumerate(steps):
        if index == 0:
            step.link_ok = True
            step.link_margin = None
            validated.append(step)
            continue

        prev = validated[-1]
        ok, margin = _can_link(prev, step, ping_buffer)
        step.link_ok = ok
        step.link_margin = margin
        validated.append(step)

        if not ok:
            warnings.append(
                f"Step {index + 1} ({step.label}) may not link — "
                f"need {step.startup + ping_buffer:.2f}s stun, previous gives {prev.stun:.2f}s."
            )

    return validated, warnings


def _score_combo(steps: list[MoveStep], build: BuildInput, data: dict[str, Any]) -> ComboResult:
    """Calculate combo stats and tips."""
    steps, warnings = validate_combo(steps, build, data)
    total_damage = sum(step.scaled_damage for step in steps)
    total_time = sum(step.startup for step in steps)
    total_stun = sum(step.stun for step in steps)

    link_checks = [step for step in steps if step.link_margin is not None]
    links_ok = sum(1 for step in link_checks if step.link_ok)
    reliability = round((links_ok / max(1, len(link_checks))) * 100, 1)

    ken_break_used = any(step.ken_break for step in steps[:2])

    # Efficiency: DPS × stun factor + ken break bonus
    dps = total_damage / max(total_time, 0.1)
    stun_factor = min(total_stun, 6.0) * 1.5
    ken_bonus = 25 if ken_break_used else 0
    efficiency = round(min(100, (dps / 120) + stun_factor + ken_bonus), 1)

    # Rough HP estimate at max level (~12k effective)
    one_shot = total_damage >= 11000

    tips: list[str] = []
    if build.opponent_has_ken and not ken_break_used:
        warnings.append("Opponent has Observation — lead with a Ken-break move or they may auto-dodge.")
    elif ken_break_used:
        tips.append("Opens with Ken-break — good vs Observation users.")

    if build.sword != "None":
        tips.append("Use sword swap (press 3) between fruit cooldowns to extend stun with M1s.")

    if build.race == "Cyborg":
        tips.append("Cyborg V4 disables Observation — activate before engaging for free opener.")

    if build.ping_ms > 150:
        tips.append(f"High ping ({build.ping_ms}ms) — dash-cancel between moves to compensate.")

    if build.combo_goal == "safe" and reliability < 90:
        tips.append("For safer combos, reduce filler or pick moves with longer stun.")

    if build.combo_goal == "one_shot" and not one_shot:
        tips.append("This combo may not one-shot — add a finisher (Fruit V or Fighting C).")

    return ComboResult(
        steps=steps,
        total_damage=total_damage,
        total_time=round(total_time, 2),
        reliability=reliability,
        ken_break_used=ken_break_used,
        efficiency_score=efficiency,
        one_shot_potential=one_shot,
        tips=tips,
        warnings=warnings,
    )


def _move_priority(move: MoveStep, build: BuildInput) -> float:
    """Score a move for greedy combo building."""
    score = move.scaled_damage * 0.4 + move.stun * 2000
    if build.combo_goal == "safe":
        score = move.stun * 3500 + move.scaled_damage * 0.15
    if move.ken_break and build.opponent_has_ken:
        score += 3000
    if move.role == "opener":
        score += 1500
    if move.role == "finisher":
        score += 800
    if move.role == "filler":
        score += 400
    if move.role == "stun":
        score += 1200
    return score


def _greedy_build_combo(build: BuildInput, data: dict[str, Any]) -> list[MoveStep]:
    """Build a combo greedily from available moves."""
    available = _collect_available_moves(build, data)
    if not available:
        return []

    ping_buffer = _ping_buffer(build, data)
    chain: list[MoveStep] = []

    # Pick opener
    openers = [m for m in available if m.role in ("opener", "stun") or m.ken_break]
    if build.opponent_has_ken:
        ken_openers = [m for m in openers if m.ken_break]
        if ken_openers:
            openers = ken_openers

    if not openers:
        openers = sorted(available, key=lambda m: m.stun, reverse=True)[:3]

    opener = max(openers, key=lambda m: _move_priority(m, build))
    chain.append(opener)
    used_labels = {opener.label}

    # Alternate fruit/sword/fighting for realistic combos
    max_steps = 8
    while len(chain) < max_steps:
        candidates = [m for m in available if m.label not in used_labels]

        # Prefer fillers after opener
        if len(chain) == 1 and build.fighting_style:
            fillers = [m for m in candidates if m.role == "filler"]
            if fillers:
                best_filler = max(fillers, key=lambda m: m.stun)
                chain.append(best_filler)
                used_labels.add(best_filler.label)
                continue

        # Filter linkable moves
        prev = chain[-1]
        linkable = []
        for move in candidates:
            ok, _ = _can_link(prev, move, ping_buffer)
            if ok or len(chain) < 3:  # allow slightly risky mid-chain
                linkable.append(move)

        if not linkable:
            break

        # Prefer high damage finishers near end
        if len(chain) >= 5:
            finishers = [m for m in linkable if m.role in ("finisher", "damage")]
            if finishers:
                next_move = max(finishers, key=lambda m: m.scaled_damage)
            else:
                next_move = max(linkable, key=lambda m: _move_priority(m, build))
        else:
            next_move = max(linkable, key=lambda m: _move_priority(m, build))

        chain.append(next_move)
        used_labels.add(next_move.label)

        # Sword filler between fruit moves
        if (
            len(chain) < max_steps - 1
            and build.sword != "None"
            and next_move.category == "fruit"
        ):
            sword_fillers = [
                m
                for m in available
                if m.category == "sword_m1" and m.label not in used_labels
            ]
            if sword_fillers:
                filler = sword_fillers[0]
                ok, _ = _can_link(chain[-1], filler, ping_buffer)
                if ok:
                    chain.append(filler)
                    used_labels.add(filler.label)

    return chain


def _from_preset(build: BuildInput, data: dict[str, Any]) -> list[MoveStep] | None:
    """Try to load a preset combo for the fruit."""
    presets = data.get("preset_combos", {}).get(build.fruit, [])
    for preset in presets:
        steps: list[MoveStep] = []
        for token in preset:
            step = _resolve_move(token, build, data)
            if step:
                steps.append(step)
        if len(steps) >= 4:
            return steps
    return None


def generate_combos(build: BuildInput, data: dict[str, Any] | None = None) -> list[ComboResult]:
    """Generate up to 3 combo variants for the user's build."""
    db = data or load_combo_data()
    results: list[ComboResult] = []

    # Preset-based combo
    preset_steps = _from_preset(build, db)
    if preset_steps:
        result = _score_combo(preset_steps, build, db)
        result.tips.insert(0, "Meta preset combo for your fruit.")
        results.append(result)

    # Greedy auto-generated
    greedy_steps = _greedy_build_combo(build, db)
    if greedy_steps:
        greedy_result = _score_combo(greedy_steps, build, db)
        greedy_result.tips.insert(0, "Auto-generated from your build's available moves.")
        results.append(greedy_result)

    # Safe variant: longer stun chains, fewer risky gaps
    safe_steps = _greedy_build_combo(
        BuildInput(**{**build.__dict__, "combo_goal": "safe", "opponent_has_ken": build.opponent_has_ken}),
        db,
    )
    if safe_steps:
        safe_result = _score_combo(safe_steps, build, db)
        safe_result.tips.insert(0, "Safer variant — prioritizes stun duration and link margins.")
        results.append(safe_result)

    # Deduplicate by step sequence
    seen: set[str] = set()
    unique: list[ComboResult] = []
    for combo in sorted(results, key=lambda c: (-c.efficiency_score, -c.total_damage)):
        key = " -> ".join(step.label for step in combo.steps)
        if key not in seen:
            seen.add(key)
            unique.append(combo)

    return unique[:3]


def format_combo_sequence(combo: ComboResult) -> str:
    """Return a copy-paste friendly combo string."""
    parts = []
    for step in combo.steps:
        parts.append(step.display_key)
    return " → ".join(parts)


def get_build_summary(build: BuildInput, data: dict[str, Any]) -> dict[str, str]:
    """Human-readable build summary."""
    race_info = data["races"].get(build.race, {})
    return {
        "Fruit": build.fruit,
        "Sword": build.sword,
        "Fighting Style": build.fighting_style,
        "Gun": build.gun,
        "Race": f"{build.race} — {race_info.get('notes', '')}",
        "Stats": (
            f"Melee {build.melee_stat} | Defense {build.defense_stat} | "
            f"Fruit {build.fruit_stat} | Sword {build.sword_stat} | Gun {build.gun_stat}"
        ),
    }
