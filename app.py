"""Football Guess the Player — Streamlit app entry point."""

import streamlit as st

from utils.game import (
    STREAK_BONUS,
    STREAK_BONUS_THRESHOLD,
    calculate_round_score,
    check_guess,
    clue_score,
    format_player_info,
    get_clues_for_difficulty,
    load_players,
    select_random_player,
)
from utils.styling import apply_custom_styles

CHALLENGE_ROUNDS = 5


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
    st.session_state.screen = "playing"


def start_game() -> None:
    """Start a classic or challenge game."""
    if not ensure_players_loaded():
        return

    st.session_state.challenge_round = 0
    st.session_state.challenge_scores = []
    st.session_state.challenge_players = []
    st.session_state.challenge_wrong_guesses = 0

    if st.session_state.game_mode == "challenge":
        st.session_state.challenge_round = 1

    start_new_round()


def finish_round(*, won: bool, gave_up: bool = False) -> None:
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
    st.session_state.games_played += 1
    st.session_state.total_points += score
    st.session_state.best_score = max(st.session_state.best_score, score)

    if st.session_state.game_mode == "challenge":
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
    st.error("❌ Not quite! Try again or reveal another clue.")
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


def render_home_screen() -> None:
    """Display the main home screen with title, stats, and start controls."""
    st.markdown('<p class="game-title">⚽ Guess the Player</p>', unsafe_allow_html=True)
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
    difficulty = st.radio(
        "Difficulty",
        options=["easy", "medium", "hard"],
        index=["easy", "medium", "hard"].index(st.session_state.difficulty),
        format_func=lambda d: {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"}[d],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.difficulty = difficulty

    st.markdown("")

    st.markdown("**Choose game mode**")
    game_mode = st.radio(
        "Game mode",
        options=["classic", "challenge"],
        index=["classic", "challenge"].index(st.session_state.game_mode),
        format_func=lambda m: {
            "classic": "Classic — Guess one player",
            "challenge": "5 Player Challenge — Guess five players",
        }[m],
        label_visibility="collapsed",
    )
    st.session_state.game_mode = game_mode

    st.markdown("")

    if st.button("START GAME", type="primary", use_container_width=True):
        if ensure_players_loaded():
            start_game()
            st.rerun()


def render_game_screen() -> None:
    """Display the active game with clues and guessing."""
    player = st.session_state.current_player
    if player is None:
        go_home()
        st.rerun()
        return

    # Header with mode info
    if st.session_state.game_mode == "challenge":
        st.markdown(
            f'<p class="round-badge">Round {st.session_state.challenge_round} of {CHALLENGE_ROUNDS}</p>',
            unsafe_allow_html=True,
        )

    diff_label = st.session_state.difficulty.capitalize()
    st.markdown(f'<p class="difficulty-badge">{diff_label} mode</p>', unsafe_allow_html=True)

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

    # Guessing interface
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

    st.markdown("")

    if st.button("REVEAL ANSWER", use_container_width=True):
        reveal_answer()
        st.rerun()

    if st.button("← Back to Home", use_container_width=True):
        go_home()
        st.rerun()


def render_round_result() -> None:
    """Show results after a round ends."""
    player = st.session_state.current_player
    if player is None:
        go_home()
        st.rerun()
        return

    if st.session_state.round_won:
        st.success("🎉 Correct!")
        st.balloons()
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
    else:
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

    st.markdown("**About this player**")
    st.markdown(format_player_info(player))

    st.markdown("")

    challenge_done = (
        st.session_state.game_mode == "challenge"
        and len(st.session_state.challenge_scores) >= CHALLENGE_ROUNDS
    )

    if challenge_done:
        if st.button("VIEW RESULTS", type="primary", use_container_width=True):
            st.session_state.screen = "challenge_summary"
            st.rerun()
    elif st.session_state.game_mode == "challenge":
        if st.button("NEXT PLAYER", type="primary", use_container_width=True):
            st.session_state.challenge_round += 1
            start_new_round()
            st.rerun()
    elif st.session_state.game_mode == "classic":
        if st.button("NEXT PLAYER", type="primary", use_container_width=True):
            start_new_round()
            st.rerun()

    if st.button("← Back to Home", use_container_width=True):
        go_home()
        st.rerun()


def render_challenge_summary() -> None:
    """Show end-of-challenge statistics."""
    scores = st.session_state.challenge_scores
    total = sum(scores)
    average = round(total / len(scores), 1) if scores else 0
    best_round = max(scores) if scores else 0
    players_guessed = len(st.session_state.challenge_players)

    st.markdown('<p class="game-title">🏆 Challenge Complete!</p>', unsafe_allow_html=True)

    st.markdown(
        f"""
        <div class="result-card">
            <p>⭐ <strong>Total score:</strong> {total}</p>
            <p>📊 <strong>Average score:</strong> {average}</p>
            <p>✅ <strong>Players guessed:</strong> {players_guessed} / {CHALLENGE_ROUNDS}</p>
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


def render_sidebar() -> None:
    """Render sidebar with settings, stats, and how to play."""
    with st.sidebar:
        st.markdown("### ⚽ Guess the Player")
        st.markdown("---")

        st.markdown("**Difficulty**")
        difficulty = st.selectbox(
            "Difficulty",
            options=["easy", "medium", "hard"],
            index=["easy", "medium", "hard"].index(st.session_state.difficulty),
            format_func=lambda d: {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"}[d],
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
            3. Read clues one at a time.
            4. Type your guess — fewer clues means more points!
            5. Wrong guesses cost points.
            6. Get 3 correct in a row for a +20 bonus!
            7. Beat your best score.
            """
        )

        if st.session_state.screen != "home":
            if st.button("← Home", use_container_width=True):
                go_home()
                st.rerun()


def main() -> None:
    """Run the Streamlit app."""
    st.set_page_config(
        page_title="Guess the Player",
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
