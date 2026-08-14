"""Visual feedback effects for the game."""

import streamlit as st


def show_football_celebration() -> None:
    """Show falling footballs instead of the default balloon animation."""
    footballs = "".join(
        f'<span class="falling-football" style="left:{i * 7 + 3}%; animation-delay:{i * 0.15}s;">⚽</span>'
        for i in range(14)
    )
    st.markdown(
        f"""
        <div class="football-celebration" aria-hidden="true">
            {footballs}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_potty_overlay() -> None:
    """Show a large potty icon overlay for one second on a wrong guess."""
    st.markdown(
        """
        <div class="potty-overlay" aria-hidden="true">
            <div class="potty-icon">🚽</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
