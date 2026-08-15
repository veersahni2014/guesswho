"""Football Guess the Player — Streamlit app entry point."""

import sys
from pathlib import Path

# Ensure the app root is importable on Streamlit Cloud
_APP_ROOT = Path(__file__).resolve().parent
if str(_APP_ROOT) not in sys.path:
    sys.path.insert(0, str(_APP_ROOT))

import time
from datetime import timedelta

import streamlit as st

from game_utils.game import (
    DIFFICULTY_LABELS,
    DIFFICULTY_LEVELS,
    GAME_MODE_LABELS,
    GAME_MODES,
    STREAK_BONUS,
    STREAK_BONUS_THRESHOLD,
    TIMER_SECONDS,
    calculate_round_score,
    check_guess,
    clue_score,
    format_player_info,
    generate_multiple_choice_options,
    get_base_player_info,
    get_challenge_rounds,
    get_clues_for_difficulty,
    get_timer_remaining,
    is_challenge_mode,
    load_players,
    select_random_player,
)
from game_utils.effects import show_football_celebration, show_potty_overlay
from game_utils.styling import apply_custom_styles

BRAND_AUTHOR = "Veer Sahni"


def init_session_state() -> None:
    """Set up default session state values used across the app."""
    defaults = {
        "screen": "home",
        "best_score": 0,
        "games_played": 0,
        "correct_guesses": 0,
        "wrong_guesses_total": 0,
        "current_streak": 0,
        "longest_streak": 0,
        "total_points": 0,
        "difficulty": "easy",
        "game_mode": "classic",
        "players": None,
        "player_load_errors": [],
        "recent_player_names": [],
        "current_player": None,
        "clues": [],
        "clues_revealed": 0,
        "wrong_guesses_round": 0,
        "round_won": False,
        "gave_up": False,
        "round_score": 0,
        "streak_bonus": 0,
        "challenge_round": 0,
        "challenge_scores": [],
        "challenge_players": [],
        "challenge_wrong_guesses": 0,
        "guess_input_key": 0,
        "wrong_feedback_active": False,
        "round_start_time": 0.0,
        "timed_out": False,
        "choice_options": [],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def ensure_players_loaded() -> bool:
    """Load player data once and show developer errors if needed."""
    if st.session_state.players is not None:
        return len(st.session_state.players) > 0

    players, errors = load_players()
    st.session_state.players = players
    st.session_state.player_load_errors = errors
    return len(players) > 0


def go_home() -> None:
    """Return to the home screen."""
    st.session_state.screen = "home"
    st.session_state.current_player = None
    st.session_state.challenge_round = 0
    st.session_state.challenge_scores = []
    st.session_state.challenge_players = []
    st.session_state.challenge_wrong_guesses = 0
    st.session_state.timed_out = False
    st.session_state.choice_options = []


def start_new_round() -> None:
    """Select a player and reset round-specific state."""
    player = select_random_player(
        st.session_state.players,
        st.session_state.difficulty,
        st.session_state.recent_player_names,
    )
    if player is None:
        st.error("No players available. Check the player data file.")
        return

    name = player["name"]
    recent = st.session_state.recent_player_names + [name]
    st.session_state.recent_player_names = recent[-5:]

    st.session_state.current_player = player
    st.session_state.clues = get_clues_for_difficulty(player, st.session_state.difficulty)
    st.session_state.clues_revealed = 1
    st.session_state.wrong_guesses_round = 0
    st.session_state.round_won = False
    st.session_state.gave_up = False
    st.session_state.round_score = 0
    st.session_state.streak_bonus = 0
    st.session_state.guess_input_key += 1
    st.session_state.round_start_time = time.time()
    st.session_state.timed_out = False
    if st.session_state.game_mode == "multiple_choice":
        st.session_state.choice_options = generate_multiple_choice_options(
            player,
            st.session_state.players,
        )
    else:
        st.session_state.choice_options = []
    st.session_state.screen = "playing"


def start_game() -> None:
    """Start a classic or challenge game."""
    if not ensure_players_loaded():
        return

    st.session_state.challenge_round = 0
    st.session_state.challenge_scores = []
    st.session_state.challenge_players = []
    st.session_state.challenge_wrong_guesses = 0

    if is_challenge_mode(st.session_state.game_mode):
        st.session_state.challenge_round = 1

    start_new_round()


def finish_round(*, won: bool, gave_up: bool = False, timed_out: bool = False) -> None:
    """Update session stats and move to the round result screen."""
    player = st.session_state.current_player
    if player is None:
        return

    streak_bonus = 0
    if won:
        new_streak = st.session_state.current_streak + 1
        if new_streak >= STREAK_BONUS_THRESHOLD:
            streak_bonus = STREAK_BONUS
        st.session_state.streak_bonus = streak_bonus
        score = calculate_round_score(
            st.session_state.clues_revealed,
            st.session_state.wrong_guesses_round,
            gave_up=False,
            streak_bonus=streak_bonus,
        )
        st.session_state.current_streak = new_streak
        st.session_state.correct_guesses += 1
        st.session_state.longest_streak = max(
            st.session_state.longest_streak,
            st.session_state.current_streak,
        )
    else:
        score = 0
        st.session_state.current_streak = 0

    st.session_state.round_score = score
    st.session_state.round_won = won
    st.session_state.gave_up = gave_up
    st.session_state.timed_out = timed_out
    st.session_state.games_played += 1
    st.session_state.total_points += score
    st.session_state.best_score = max(st.session_state.best_score, score)

    if is_challenge_mode(st.session_state.game_mode):
        st.session_state.challenge_scores.append(score)
        if won:
            st.session_state.challenge_players.append(player["name"])
        st.session_state.challenge_wrong_guesses += st.session_state.wrong_guesses_round

    st.session_state.screen = "round_result"


def handle_guess(guess: str) -> None:
    """Process a player's guess."""
    if not guess or not guess.strip():
        st.warning("Please enter a name before guessing.")
        return

    player = st.session_state.current_player
    if player is None:
        return

    if check_guess(guess, player):
        finish_round(won=True)
        return

    st.session_state.wrong_guesses_round += 1
    st.session_state.wrong_guesses_total += 1
    st.session_state.wrong_feedback_active = True
    st.session_state.guess_input_key += 1


def reveal_next_clue() -> None:
    """Show the next clue if any remain."""
    if st.session_state.clues_revealed < len(st.session_state.clues):
        st.session_state.clues_revealed += 1
    else:
        st.warning("No more clues available.")


def reveal_answer() -> None:
    """End the round with zero points."""
    finish_round(won=False, gave_up=True)


def render_base_player_info(player: dict) -> None:
    """Show country, club, and position — always visible, not revealable clues."""
    info = get_base_player_info(player)
    st.markdown(
        f"""
        <div class="base-info-row">
            <div class="base-info-card">
                <span class="base-info-label">🌍 Country</span>
                <span class="base-info-value">{info["country"]}</span>
            </div>
            <div class="base-info-card">
                <span class="base-info-label">🏟️ Club</span>
                <span class="base-info-value">{info["club"]}</span>
            </div>
            <div class="base-info-card">
                <span class="base-info-label">📍 Position</span>
                <span class="base-info-value">{info["position"]}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_timer_display() -> None:
    """Show and update the 30-second countdown in timer mode."""
    if st.session_state.game_mode != "timer":
        return

    remaining = get_timer_remaining(st.session_state.round_start_time)
    urgent = remaining <= 10
    timer_class = "timer-display timer-urgent" if urgent else "timer-display"

    st.markdown(
        f"""
        <div class="{timer_class}">
            <span class="timer-label">Time left</span>
            <span class="timer-value">{remaining}s</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if remaining <= 0 and not st.session_state.timed_out:
        finish_round(won=False, timed_out=True)
        st.rerun()


@st.fragment(run_every=timedelta(seconds=1))
def timer_tick() -> None:
    """Auto-refresh the countdown every second in timer mode."""
    if st.session_state.screen == "playing" and st.session_state.game_mode == "timer":
        render_timer_display()


def render_score_display() -> None:
    """Show the current potential score during a round."""
    potential = calculate_round_score(
        st.session_state.clues_revealed,
        st.session_state.wrong_guesses_round,
    )
    st.markdown(
        f"""
        <div class="score-display">
            <span class="score-label">Potential score</span>
            <span class="score-value">{potential}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_text_guess() -> None:
    """Text input guessing for classic, timer, and challenge modes."""
    guess = st.text_input(
        "Who is this player?",
        key=f"guess_input_{st.session_state.guess_input_key}",
        placeholder="Type the player's name...",
    )

    col1, col2 = st.columns(2)
    with col1:
        if st.button("GUESS", type="primary", use_container_width=True):
            handle_guess(guess)
            st.rerun()

    with col2:
        if st.session_state.clues_revealed < len(st.session_state.clues):
            if st.button("NEXT CLUE", use_container_width=True):
                reveal_next_clue()
                st.rerun()
        else:
            st.button("NEXT CLUE", use_container_width=True, disabled=True)


def render_multiple_choice_guess() -> None:
    """Button-based guessing — no typing required."""
    st.markdown("**Who is this player?**")
    options = st.session_state.choice_options

    if not options:
        st.warning("No choices available. Go back and start a new game.")
        return

    col1, col2 = st.columns(2)
    for index, name in enumerate(options):
        column = col1 if index % 2 == 0 else col2
        with column:
            if st.button(name, key=f"mc_choice_{st.session_state.guess_input_key}_{index}", use_container_width=True):
                handle_guess(name)
                st.rerun()

    st.markdown("")
    if st.session_state.clues_revealed < len(st.session_state.clues):
        if st.button("NEXT CLUE", use_container_width=True):
            reveal_next_clue()
            st.rerun()
    else:
        st.button("NEXT CLUE", use_container_width=True, disabled=True)


def render_brand_footer() -> None:
    """Show a subtle branded footer on every screen."""
    st.markdown(
        f'<p class="brand-footer">Made by <span class="brand-name">{BRAND_AUTHOR}</span></p>',
        unsafe_allow_html=True,
    )


def render_home_screen() -> None:
    """Display the main home screen with title, stats, and start controls."""
    st.markdown('<p class="game-title">⚽ Guess the Player</p>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="brand-mark">by {BRAND_AUTHOR}</p>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="game-subtitle">How quickly can you figure out who it is?</p>',
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">Best Score</div>
                <div class="stat-value">{st.session_state.best_score}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">Games Played</div>
                <div class="stat-value">{st.session_state.games_played}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            f"""
            <div class="stat-card">
                <div class="stat-label">Current Streak</div>
                <div class="stat-value">{st.session_state.current_streak}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("")

    st.markdown("**Choose difficulty**")
    difficulty_index = (
        DIFFICULTY_LEVELS.index(st.session_state.difficulty)
        if st.session_state.difficulty in DIFFICULTY_LEVELS
        else 0
    )
    difficulty = st.radio(
        "Difficulty",
        options=DIFFICULTY_LEVELS,
        index=difficulty_index,
        format_func=lambda d: DIFFICULTY_LABELS[d],
        label_visibility="collapsed",
    )
    st.session_state.difficulty = difficulty

    st.markdown("")

    st.markdown("**Choose game mode**")
    mode_index = (
        GAME_MODES.index(st.session_state.game_mode)
        if st.session_state.game_mode in GAME_MODES
        else 0
    )
    game_mode = st.radio(
        "Game mode",
        options=GAME_MODES,
        index=mode_index,
        format_func=lambda m: GAME_MODE_LABELS[m],
        label_visibility="collapsed",
    )
    st.session_state.game_mode = game_mode

    st.markdown("")

    if st.button("START GAME", type="primary", use_container_width=True):
        if ensure_players_loaded():
            start_game()
            st.rerun()

    render_brand_footer()


def render_game_screen() -> None:
    """Display the active game with clues and guessing."""
    if st.session_state.wrong_feedback_active:
        show_potty_overlay()
        st.session_state.wrong_feedback_active = False

    player = st.session_state.current_player
    if player is None:
        go_home()
        st.rerun()
        return

    # Header with mode info
    if is_challenge_mode(st.session_state.game_mode):
        total_rounds = get_challenge_rounds(st.session_state.game_mode)
        st.markdown(
            f'<p class="round-badge">Round {st.session_state.challenge_round} of {total_rounds}</p>',
            unsafe_allow_html=True,
        )

    diff_label = DIFFICULTY_LABELS.get(st.session_state.difficulty, "Easy")
    st.markdown(f'<p class="difficulty-badge">{diff_label}</p>', unsafe_allow_html=True)

    timer_tick()
    render_base_player_info(player)

    st.markdown('<p class="section-label">Extra clues</p>', unsafe_allow_html=True)

    render_score_display()

    # Show revealed clues
    clues = st.session_state.clues[: st.session_state.clues_revealed]
    for index, clue in enumerate(clues, start=1):
        st.markdown(
            f"""
            <div class="clue-card">
                <div class="clue-number">Clue {index}</div>
                <div class="clue-text">{clue}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        f'<p class="clue-hint">Clue {st.session_state.clues_revealed} of {len(st.session_state.clues)} · '
        f"Max {clue_score(st.session_state.clues_revealed)} pts</p>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    if st.session_state.game_mode == "multiple_choice":
        render_multiple_choice_guess()
    else:
        render_text_guess()

    st.markdown("")

    if st.button("REVEAL ANSWER", use_container_width=True):
        reveal_answer()
        st.rerun()

    if st.button("← Back to Home", use_container_width=True):
        go_home()
        st.rerun()

    render_brand_footer()


def render_round_result() -> None:
    """Show results after a round ends."""
    player = st.session_state.current_player
    if player is None:
        go_home()
        st.rerun()
        return

    if st.session_state.round_won:
        show_football_celebration()
        st.success("🎉 Correct!")
        st.markdown(f"## {player['name']}")

        bonus_text = ""
        if st.session_state.streak_bonus > 0:
            bonus_text = f"\n\n🔥 Streak bonus: +{st.session_state.streak_bonus}"

        st.markdown(
            f"""
            <div class="result-card">
                <p>⭐ <strong>Score:</strong> {st.session_state.round_score}{bonus_text}</p>
                <p>💡 <strong>Clues used:</strong> {st.session_state.clues_revealed}</p>
                <p>❌ <strong>Wrong guesses:</strong> {st.session_state.wrong_guesses_round}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif st.session_state.gave_up:
        st.warning("Answer revealed")
        st.markdown(f"## {player['name']}")
        st.markdown(
            """
            <div class="result-card">
                <p>⭐ <strong>Score:</strong> 0</p>
                <p>You gave up this round.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.error("⏱️ Time's up!")
        st.markdown(f"## {player['name']}")
        st.markdown(
            """
            <div class="result-card">
                <p>⭐ <strong>Score:</strong> 0</p>
                <p>You ran out of time.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("**About this player**")
    st.markdown(format_player_info(player))

    st.markdown("")

    total_rounds = get_challenge_rounds(st.session_state.game_mode)
    challenge_done = (
        is_challenge_mode(st.session_state.game_mode)
        and len(st.session_state.challenge_scores) >= total_rounds
    )

    if challenge_done:
        if st.button("VIEW RESULTS", type="primary", use_container_width=True):
            st.session_state.screen = "challenge_summary"
            st.rerun()
    elif is_challenge_mode(st.session_state.game_mode):
        if st.button("NEXT PLAYER", type="primary", use_container_width=True):
            st.session_state.challenge_round += 1
            start_new_round()
            st.rerun()
    elif st.session_state.game_mode in ("classic", "timer", "multiple_choice"):
        if st.button("NEXT PLAYER", type="primary", use_container_width=True):
            start_new_round()
            st.rerun()

    if st.button("← Back to Home", use_container_width=True):
        go_home()
        st.rerun()

    render_brand_footer()


def render_challenge_summary() -> None:
    """Show end-of-challenge statistics."""
    scores = st.session_state.challenge_scores
    total = sum(scores)
    average = round(total / len(scores), 1) if scores else 0
    best_round = max(scores) if scores else 0
    total_rounds = get_challenge_rounds(st.session_state.game_mode) or len(scores)
    players_guessed = len(st.session_state.challenge_players)

    title = "10 Player Challenge Complete!" if total_rounds == 10 else "Challenge Complete!"
    st.markdown(f'<p class="game-title">🏆 {title}</p>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="result-card">
            <p>⭐ <strong>Total score:</strong> {total}</p>
            <p>📊 <strong>Average score:</strong> {average}</p>
            <p>✅ <strong>Players guessed:</strong> {players_guessed} / {total_rounds}</p>
            <p>❌ <strong>Wrong guesses:</strong> {st.session_state.challenge_wrong_guesses}</p>
            <p>🏅 <strong>Best round:</strong> {best_round}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if scores:
        st.markdown("**Round scores**")
        for index, score in enumerate(scores, start=1):
            name = (
                st.session_state.challenge_players[index - 1]
                if index <= len(st.session_state.challenge_players)
                else "—"
            )
            st.markdown(f"- Round {index}: **{score}** pts ({name})")

    st.markdown("")

    if st.button("PLAY AGAIN", type="primary", use_container_width=True):
        go_home()
        st.rerun()

    render_brand_footer()


def render_sidebar() -> None:
    """Render sidebar with settings, stats, and how to play."""
    with st.sidebar:
        st.markdown("### ⚽ Guess the Player")
        st.markdown(
            f'<p class="sidebar-brand">by {BRAND_AUTHOR}</p>',
            unsafe_allow_html=True,
        )
        st.markdown("---")

        st.markdown("**Difficulty**")
        diff_index = (
            DIFFICULTY_LEVELS.index(st.session_state.difficulty)
            if st.session_state.difficulty in DIFFICULTY_LEVELS
            else 0
        )
        difficulty = st.selectbox(
            "Difficulty",
            options=DIFFICULTY_LEVELS,
            index=diff_index,
            format_func=lambda d: DIFFICULTY_LABELS[d],
            label_visibility="collapsed",
        )
        st.session_state.difficulty = difficulty

        st.markdown("---")
        st.markdown("**Session stats**")
        st.metric("Best Score", st.session_state.best_score)
        st.metric("Games Played", st.session_state.games_played)
        st.metric("Total Points", st.session_state.total_points)
        st.metric("Current Streak", st.session_state.current_streak)
        st.metric("Longest Streak", st.session_state.longest_streak)
        st.metric("Correct Guesses", st.session_state.correct_guesses)
        st.metric("Wrong Guesses", st.session_state.wrong_guesses_total)

        st.markdown("---")
        st.markdown("**How to play**")
        st.markdown(
            """
            1. Pick a difficulty and game mode.
            2. Tap **START GAME**.
            3. Country, club, and position are always shown.
            4. Reveal extra clues one at a time.
            5. Type your guess — or use **Multiple Choice** mode (no typing!).
            6. **Timer mode:** guess within 30 seconds.
            7. **Baby:** super easy clues. **??:** cryptic mystery clues.
            8. **Impossible:** the toughest standard clues.
            9. Get 3 correct in a row for a +20 bonus!
            """
        )

        if st.session_state.screen != "home":
            if st.button("← Home", use_container_width=True):
                go_home()
                st.rerun()


def main() -> None:
    """Run the Streamlit app."""
    st.set_page_config(
        page_title=f"Guess the Player | {BRAND_AUTHOR}",
        page_icon="⚽",
        layout="centered",
        initial_sidebar_state="auto",
    )

    apply_custom_styles()
    init_session_state()
    ensure_players_loaded()

    # Show developer warnings for bad player data (non-fatal)
    if st.session_state.player_load_errors:
        with st.expander("⚠️ Player data warnings (for developers)"):
            for error in st.session_state.player_load_errors:
                st.warning(error)

    render_sidebar()

    screen = st.session_state.screen
    if screen == "home":
        render_home_screen()
    elif screen == "playing":
        render_game_screen()
    elif screen == "round_result":
        render_round_result()
    elif screen == "challenge_summary":
        render_challenge_summary()
    else:
        go_home()
        st.rerun()


if __name__ == "__main__":
    main()
