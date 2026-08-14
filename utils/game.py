"""Game logic for Football Guess the Player."""

from __future__ import annotations

import json
import random
import re
import time
import unicodedata
from pathlib import Path
from typing import Any

# Points available based on how many clues have been revealed (1-indexed)
CLUE_SCORES = [100, 80, 60, 40, 20]

# Penalty applied on each wrong guess in a round
WRONG_GUESS_PENALTIES = [10, 15, 20]

# Bonus awarded when the player gets three correct answers in a row
STREAK_BONUS = 20
STREAK_BONUS_THRESHOLD = 3

# Seconds allowed per round in timer mode
TIMER_SECONDS = 30

DIFFICULTY_LEVELS = ["easy", "medium", "hard", "impossible"]

DIFFICULTY_LABELS = {
    "easy": "🟢 Easy",
    "medium": "🟡 Medium",
    "hard": "🔴 Hard",
    "impossible": "💀 Impossible",
}

GAME_MODES = ["classic", "challenge", "timer"]

GAME_MODE_LABELS = {
    "classic": "Classic — Guess one player",
    "challenge": "5 Player Challenge — Guess five players",
    "timer": "⏱️ Timer — 30 seconds per player",
}

REQUIRED_PLAYER_FIELDS = {
    "name",
    "nationality",
    "position",
    "clubs",
    "birth_year",
    "world_cup_winner",
    "ballon_dor_wins",
    "clues",
}

REQUIRED_CLUE_LEVELS = {"easy", "medium", "hard"}

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "players.json"


def normalize_text(text: str) -> str:
    """Lowercase text, strip accents, and collapse extra whitespace."""
    if not text:
        return ""
    # Decompose accented characters and remove combining marks
    decomposed = unicodedata.normalize("NFD", text)
    without_accents = "".join(
        char for char in decomposed if unicodedata.category(char) != "Mn"
    )
    collapsed = re.sub(r"\s+", " ", without_accents.strip().lower())
    return collapsed


def load_players(path: Path | None = None) -> tuple[list[dict[str, Any]], list[str]]:
    """
    Load and validate players from JSON.

    Returns a tuple of (valid_players, error_messages).
    Invalid individual entries are skipped with descriptive errors.
    """
    file_path = path or DATA_PATH
    errors: list[str] = []

    if not file_path.exists():
        return [], [f"Player data file not found: {file_path}"]

    try:
        with file_path.open(encoding="utf-8") as file:
            raw_data = json.load(file)
    except json.JSONDecodeError as exc:
        return [], [f"Invalid JSON in {file_path}: {exc}"]
    except OSError as exc:
        return [], [f"Could not read {file_path}: {exc}"]

    if not isinstance(raw_data, list):
        return [], ["Player data must be a JSON array of player objects."]

    valid_players: list[dict[str, Any]] = []
    seen_names: set[str] = set()

    for index, player in enumerate(raw_data, start=1):
        label = f"Player #{index}"
        if not isinstance(player, dict):
            errors.append(f"{label}: entry is not an object.")
            continue

        name = player.get("name", "Unknown")
        label = f"Player '{name}'"

        missing = REQUIRED_PLAYER_FIELDS - set(player.keys())
        if missing:
            errors.append(f"{label}: missing fields {sorted(missing)}.")
            continue

        clues = player.get("clues")
        if not isinstance(clues, dict):
            errors.append(f"{label}: 'clues' must be an object.")
            continue

        missing_levels = REQUIRED_CLUE_LEVELS - set(clues.keys())
        if missing_levels:
            errors.append(f"{label}: missing clue levels {sorted(missing_levels)}.")
            continue

        for level in REQUIRED_CLUE_LEVELS:
            level_clues = clues.get(level)
            if not isinstance(level_clues, list) or not level_clues:
                errors.append(f"{label}: '{level}' clues must be a non-empty list.")
                break
        else:
            normalized_name = normalize_text(name)
            if normalized_name in seen_names:
                errors.append(f"{label}: duplicate player name.")
                continue

            seen_names.add(normalized_name)
            valid_players.append(player)

    if not valid_players and not errors:
        errors.append("No players found in the data file.")

    return valid_players, errors


def get_acceptable_answers(player: dict[str, Any]) -> set[str]:
    """Build the set of normalized answers that count as correct."""
    answers: set[str] = set()

    name = player.get("name", "")
    normalized_name = normalize_text(name)
    if normalized_name:
        answers.add(normalized_name)

    # Allow matching on last name (e.g. "messi" -> "Lionel Messi")
    parts = normalized_name.split()
    if len(parts) > 1:
        answers.add(parts[-1])

    # Optional alternate names / nicknames from data
    for alt in player.get("alternate_names", []):
        normalized_alt = normalize_text(str(alt))
        if normalized_alt:
            answers.add(normalized_alt)

    return answers


def check_guess(guess: str, player: dict[str, Any]) -> bool:
    """Return True if the guess matches the player (forgiving but strict)."""
    normalized_guess = normalize_text(guess)
    if not normalized_guess:
        return False

    acceptable = get_acceptable_answers(player)

    if normalized_guess in acceptable:
        return True

    # Allow guesses that match a multi-word alternate exactly
    for answer in acceptable:
        if " " in answer and normalized_guess == answer:
            return True

    return False


def get_clues_for_difficulty(player: dict[str, Any], difficulty: str) -> list[str]:
    """Return the clue list for the chosen difficulty."""
    clues = player.get("clues", {})
    if difficulty == "impossible":
        return list(clues.get("impossible", clues.get("hard", clues.get("easy", []))))
    return list(clues.get(difficulty, clues.get("easy", [])))


def get_club_display(player: dict[str, Any]) -> str:
    """Return the club label shown in the always-visible player info."""
    if player.get("retired"):
        if player.get("ballon_dor_wins", 0) > 0 or player.get("world_cup_winner"):
            return "🏆 Icon"
        return "⭐ Hero"

    clubs = player.get("clubs", [])
    return clubs[-1] if clubs else "—"


def get_base_player_info(player: dict[str, Any]) -> dict[str, str]:
    """Return the three always-visible facts: country, club, position."""
    return {
        "country": player.get("nationality", "—"),
        "club": get_club_display(player),
        "position": player.get("position", "—"),
    }


def get_timer_remaining(round_start_time: float) -> int:
    """Seconds left in the current timer round."""
    elapsed = time.time() - round_start_time
    return max(0, TIMER_SECONDS - int(elapsed))


def clue_score(clues_revealed: int) -> int:
    """Maximum score based on how many clues are currently visible."""
    index = max(0, min(clues_revealed, len(CLUE_SCORES))) - 1
    if index < 0:
        return CLUE_SCORES[0]
    return CLUE_SCORES[index]


def wrong_guess_penalty(wrong_guesses: int) -> int:
    """Penalty points for the given wrong-guess count (1-indexed)."""
    if wrong_guesses <= 0:
        return 0
    index = min(wrong_guesses - 1, len(WRONG_GUESS_PENALTIES) - 1)
    return WRONG_GUESS_PENALTIES[index]


def calculate_round_score(
    clues_revealed: int,
    wrong_guesses: int,
    *,
    gave_up: bool = False,
    streak_bonus: int = 0,
) -> int:
    """Calculate the final score for a round."""
    if gave_up:
        return 0

    base = clue_score(clues_revealed)
    penalty = sum(wrong_guess_penalty(i) for i in range(1, wrong_guesses + 1))
    total = base - penalty + streak_bonus
    return max(0, total)


def select_random_player(
    players: list[dict[str, Any]],
    difficulty: str,
    recent_names: list[str],
) -> dict[str, Any] | None:
    """
    Pick a random player for the given difficulty.

    Avoids players used in the last 5 rounds when possible.
    """
    if not players:
        return None

    recent_normalized = {normalize_text(name) for name in recent_names}

    pool = [
        player
        for player in players
        if normalize_text(player["name"]) not in recent_normalized
    ]

    if not pool:
        pool = players

    # Prefer players with clues for the chosen difficulty
    with_clues = [
        player
        for player in pool
        if get_clues_for_difficulty(player, difficulty)
    ]
    if with_clues:
        pool = with_clues

    return random.choice(pool)


def format_player_info(player: dict[str, Any]) -> str:
    """Return a short info blurb about the player for the results screen."""
    clubs = ", ".join(player.get("clubs", []))
    birth_year = player.get("birth_year", "—")
    wc = "Yes" if player.get("world_cup_winner") else "No"
    ballon = player.get("ballon_dor_wins", 0)

    lines = [
        f"**Nationality:** {player.get('nationality', '—')}",
        f"**Position:** {player.get('position', '—')}",
        f"**Clubs:** {clubs}",
        f"**Born:** {birth_year}",
        f"**World Cup winner:** {wc}",
        f"**Ballon d'Or wins:** {ballon}",
    ]

    extra = player.get("info")
    if extra:
        lines.append(f"\n{extra}")

    return "\n\n".join(lines)
