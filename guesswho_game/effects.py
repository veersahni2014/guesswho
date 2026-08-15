"""Visual feedback effects for the game."""

import random

import streamlit as st


def _floating_items(emoji: str, css_class: str, count: int, duration: float) -> str:
    """Build HTML for emoji items that float upward like Streamlit balloons."""
    items = []
    for index in range(count):
        left = random.randint(2, 92)
        delay = round(index * 0.1 + random.uniform(0, 0.15), 2)
        drift = random.randint(-40, 40)
        size = random.uniform(1.8, 3.2)
        items.append(
            f'<span class="{css_class}" style="left:{left}%;'
            f"animation-delay:{delay}s;animation-duration:{duration}s;"
            f'--drift:{drift}px;font-size:{size}rem;">{emoji}</span>'
        )
    return "".join(items)


def show_football_celebration() -> None:
    """Show footballs floating upward like balloons."""
    footballs = _floating_items("⚽", "floating-football", count=18, duration=4.0)
    st.markdown(
        f"""
        <div class="float-effect-layer" aria-hidden="true">
            {footballs}
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_potty_overlay() -> None:
    """Show potty icons floating upward for a brief moment on a wrong guess."""
    items = []
    for index in range(10):
        left = random.randint(2, 92)
        delay = round(index * 0.08 + random.uniform(0, 0.1), 2)
        drift = random.randint(-35, 35)
        size = random.uniform(2.8, 4.5)
        items.append(
            f'<span class="floating-potty" style="left:{left}%;'
            f"animation-delay:{delay}s;animation-duration:1.2s;"
            f'--drift:{drift}px;font-size:{size}rem;">🚽</span>'
        )
    potties = "".join(items)
    st.markdown(
        f"""
        <div class="float-effect-layer potty-float-layer" aria-hidden="true">
            {potties}
        </div>
        """,
        unsafe_allow_html=True,
    )
