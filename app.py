"""Blox Fruits Combo Maker — build your loadout, get working combos."""

import sys
from pathlib import Path

_APP_ROOT = Path(__file__).resolve().parent
if str(_APP_ROOT) not in sys.path:
    sys.path.insert(0, str(_APP_ROOT))

import streamlit as st

from combo_utils.engine import (
    STAT_PRESETS,
    BuildInput,
    format_combo_sequence,
    generate_combos,
    get_build_summary,
    list_options,
    load_combo_data,
)
from combo_utils.styling import apply_custom_styles

BRAND = "Blox Fruits Combo Maker"


def init_session_state() -> None:
    defaults = {
        "combos": [],
        "build_generated": False,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def render_step_card(index: int, step, combo_index: int) -> None:
    """Render one combo step."""
    broken_class = " broken" if step.link_margin is not None and not step.link_ok else ""
    ken_html = '<span class="ken-badge">Ken Break</span>' if step.ken_break else ""

    link_html = ""
    if step.link_margin is not None:
        link_class = "link-ok" if step.link_ok else "link-bad"
        status = "Links" if step.link_ok else "Gap risk"
        link_html = (
            f'<div class="step-meta {link_class}">{status} '
            f"(margin: {step.link_margin:+.2f}s)</div>"
        )

    st.markdown(
        f"""
        <div class="step-card{broken_class}">
            <div class="step-number">{index}</div>
            <div>
                <div class="step-key">{step.display_key}{ken_html}</div>
                <div class="step-name">{step.move_name}</div>
                <div class="step-meta">
                    ~{step.scaled_damage:,} dmg · {step.stun:.1f}s stun · {step.startup:.2f}s startup
                </div>
                {link_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_combo(combo, index: int) -> None:
    """Render a full combo card."""
    one_shot = "Yes" if combo.one_shot_potential else "No"
    one_shot_class = "" if combo.one_shot_potential else " danger"

    st.markdown(
        f"""
        <div class="combo-card">
            <div class="combo-header">Combo #{index + 1} — Efficiency {combo.efficiency_score}/100</div>
            <div class="combo-sequence">{format_combo_sequence(combo)}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown(
            f'<div class="stat-card"><div class="stat-label">Total Damage</div>'
            f'<div class="stat-value">{combo.total_damage:,}</div></div>',
            unsafe_allow_html=True,
        )
    with m2:
        st.markdown(
            f'<div class="stat-card"><div class="stat-label">Reliability</div>'
            f'<div class="stat-value">{combo.reliability}%</div></div>',
            unsafe_allow_html=True,
        )
    with m3:
        st.markdown(
            f'<div class="stat-card"><div class="stat-label">Combo Time</div>'
            f'<div class="stat-value">{combo.total_time}s</div></div>',
            unsafe_allow_html=True,
        )
    with m4:
        st.markdown(
            f'<div class="stat-card"><div class="stat-label">One-Shot</div>'
            f'<div class="stat-value{one_shot_class}">{one_shot}</div></div>',
            unsafe_allow_html=True,
        )

    with st.expander("Step-by-step breakdown", expanded=index == 0):
        for step_index, step in enumerate(combo.steps, start=1):
            render_step_card(step_index, step, index)

    if combo.tips:
        st.info("**Tips:** " + " ".join(combo.tips))
    if combo.warnings:
        for warning in combo.warnings:
            st.warning(warning)


def render_build_input(data: dict) -> BuildInput | None:
    """Sidebar and main build form. Returns BuildInput when user generates."""
    options = list_options(data)

    st.markdown("### Your Build")
    st.markdown(
        '<p class="game-subtitle">Pick your fruit, sword, fighting style, and stats — '
        "we'll chain moves that actually link.</p>",
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)
    with col1:
        fruit = st.selectbox("Fruit", options["fruits"], index=options["fruits"].index("Dough") if "Dough" in options["fruits"] else 0)
        sword = st.selectbox("Sword", options["swords"], index=options["swords"].index("Cursed Dual Katana") if "Cursed Dual Katana" in options["swords"] else 0)
        fighting = st.selectbox(
            "Fighting Style",
            options["fighting_styles"],
            index=options["fighting_styles"].index("Godhuman") if "Godhuman" in options["fighting_styles"] else 0,
        )
    with col2:
        gun = st.selectbox("Gun (optional)", options["guns"], index=0)
        race = st.selectbox("Race", options["races"], index=options["races"].index("Cyborg") if "Cyborg" in options["races"] else 0)
        combo_goal = st.selectbox(
            "Combo Goal",
            ["one_shot", "max_damage", "safe"],
            format_func=lambda g: {"one_shot": "One-Shot", "max_damage": "Max Damage", "safe": "Safe / Reliable"}[g],
        )

    st.markdown("**Stat Build**")
    preset_names = options["stat_presets"]
    preset = st.selectbox(
        "Stat preset",
        preset_names,
        index=preset_names.index("Fruit Main") if "Fruit Main" in preset_names else 0,
    )
    preset_stats = STAT_PRESETS[preset]

    if preset == "Custom":
        sc1, sc2, sc3 = st.columns(3)
        with sc1:
            melee_stat = st.number_input("Melee", 0, 2550, preset_stats["melee"], step=50)
            defense_stat = st.number_input("Defense", 0, 2550, preset_stats["defense"], step=50)
        with sc2:
            fruit_stat = st.number_input("Fruit", 0, 2550, preset_stats["fruit"], step=50)
            sword_stat = st.number_input("Sword", 0, 2550, preset_stats["sword"], step=50)
        with sc3:
            gun_stat = st.number_input("Gun", 0, 2550, preset_stats["gun"], step=50)
    else:
        melee_stat = preset_stats["melee"]
        defense_stat = preset_stats["defense"]
        fruit_stat = preset_stats["fruit"]
        sword_stat = preset_stats["sword"]
        gun_stat = preset_stats["gun"]
        st.caption(
            f"Melee {melee_stat} · Defense {defense_stat} · "
            f"Fruit {fruit_stat} · Sword {sword_stat} · Gun {gun_stat}"
        )

    st.markdown("**PvP Settings**")
    pc1, pc2 = st.columns(2)
    with pc1:
        opponent_has_ken = st.checkbox("Opponent has Observation (Ken)", value=True)
    with pc2:
        ping_ms = st.slider("Your ping (ms)", 30, 300, 80, step=10)

    if st.button("GENERATE COMBO", type="primary", use_container_width=True):
        return BuildInput(
            fruit=fruit,
            sword=sword,
            fighting_style=fighting,
            gun=gun,
            race=race,
            stat_preset=preset,
            melee_stat=melee_stat,
            defense_stat=defense_stat,
            fruit_stat=fruit_stat,
            sword_stat=sword_stat,
            gun_stat=gun_stat,
            opponent_has_ken=opponent_has_ken,
            ping_ms=ping_ms,
            combo_goal=combo_goal,
        )
    return None


def render_sidebar(data: dict) -> None:
    with st.sidebar:
        st.markdown("### 🍇 Combo Maker")
        st.markdown("---")
        st.markdown("**How it works**")
        st.markdown(
            """
            1. Select your full build (fruit, sword, style, gun).
            2. Set your stat distribution.
            3. Toggle Ken and ping for accuracy.
            4. Hit **Generate Combo**.

            Combos are validated using **stun ≥ startup** frame logic — if a step shows "Gap risk", the opponent might escape.
            """
        )
        st.markdown("---")
        st.markdown("**Combo structure**")
        st.markdown(
            """
            - **Opener** — stun or Ken-break
            - **Filler** — M1s / sword swap
            - **Damage** — fruit & style moves
            - **Finisher** — highest damage last
            """
        )
        st.markdown("---")
        st.caption(f"Move data: {data['meta']['version']} · Level cap {data['meta']['level_cap']}")


def main() -> None:
    st.set_page_config(
        page_title="Blox Fruits Combo Maker",
        page_icon="🍇",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    apply_custom_styles()
    init_session_state()

    data = load_combo_data()
    render_sidebar(data)

    st.markdown('<p class="game-title">🍇 Blox Fruits Combo Maker</p>', unsafe_allow_html=True)
    st.markdown('<p class="brand-mark">Input your build · Get working PvP combos</p>', unsafe_allow_html=True)

    build = render_build_input(data)

    if build:
        combos = generate_combos(build, data)
        st.session_state.combos = combos
        st.session_state.build_generated = True
        st.session_state.last_build = build

    if st.session_state.build_generated and st.session_state.combos:
        build = st.session_state.get("last_build")
        if build:
            summary = get_build_summary(build, data)
            st.markdown('<div class="build-card">', unsafe_allow_html=True)
            st.markdown("#### Your Loadout")
            for label, value in summary.items():
                st.markdown(f"**{label}:** {value}")
            st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")
        st.markdown("### Generated Combos")
        for index, combo in enumerate(st.session_state.combos):
            render_combo(combo, index)
            if index < len(st.session_state.combos) - 1:
                st.markdown("---")
    elif not st.session_state.build_generated:
        st.markdown(
            """
            <div class="build-card">
            <p>Configure your build above and click <strong>Generate Combo</strong> to see
            step-by-step combos tailored to your fruit, sword, fighting style, and stats.</p>
            <p>Supports popular meta fruits like <strong>Dough</strong>, <strong>Kitsune</strong>,
            <strong>Leopard</strong>, <strong>Dragon</strong>, and more.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        '<p class="brand-footer">Blox Fruits Combo Maker — fan-made tool, not affiliated with Roblox</p>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
