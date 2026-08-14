"""Football Guess the Player — Streamlit app entry point."""

import streamlit as st

from utils.styling import apply_custom_styles


def init_session_state() -> None:
    """Set up default session state values used across the app."""
    defaults = {
        "best_score": 0,
        "games_played": 0,
        "current_streak": 0,
        "difficulty": "easy",
        "game_mode": "classic",
        "game_active": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_home_screen() -> None:
    """Display the main home screen with title, stats, and start controls."""
    st.markdown('<p class="game-title">⚽ Guess the Player</p>', unsafe_allow_html=True)
    st.markdown(
        '<p class="game-subtitle">How quickly can you figure out who it is?</p>',
        unsafe_allow_html=True,
    )

    # Session stats row
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

    # Difficulty selection
    st.markdown("**Choose difficulty**")
    difficulty = st.radio(
        "Difficulty",
        options=["easy", "medium", "hard"],
        format_func=lambda d: {"easy": "🟢 Easy", "medium": "🟡 Medium", "hard": "🔴 Hard"}[d],
        horizontal=True,
        label_visibility="collapsed",
    )
    st.session_state.difficulty = difficulty

    st.markdown("")

    # Game mode selection
    st.markdown("**Choose game mode**")
    game_mode = st.radio(
        "Game mode",
        options=["classic", "challenge"],
        format_func=lambda m: {
            "classic": "Classic — Guess one player",
            "challenge": "5 Player Challenge — Guess five players",
        }[m],
        label_visibility="collapsed",
    )
    st.session_state.game_mode = game_mode

    st.markdown("")

    # Start button (placeholder for Stage 2+)
    if st.button("START GAME", type="primary", use_container_width=True):
        st.session_state.game_active = True
        st.info("Game logic coming in the next stage! Difficulty and mode are saved.")


def render_sidebar() -> None:
    """Render sidebar with settings, stats, and how to play."""
    with st.sidebar:
        st.markdown("### ⚽ Guess the Player")
        st.markdown("---")

        st.markdown("**Session stats**")
        st.metric("Best Score", st.session_state.best_score)
        st.metric("Games Played", st.session_state.games_played)
        st.metric("Current Streak", st.session_state.current_streak)

        st.markdown("---")
        st.markdown("**How to play**")
        st.markdown(
            """
            1. Pick a difficulty and game mode.
            2. Tap **START GAME**.
            3. Read clues one at a time.
            4. Type your guess — fewer clues means more points!
            5. Beat your best score.
            """
        )


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
    render_sidebar()
    render_home_screen()


if __name__ == "__main__":
    main()
