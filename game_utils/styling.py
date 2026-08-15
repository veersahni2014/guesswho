"""CSS styling for the Football Guess the Player app."""

import streamlit as st


def apply_custom_styles() -> None:
    """Inject liquid glass theme with transparency and subtle glow."""
    st.markdown(
        """
        <style>
            :root {
                --glass-bg: rgba(255, 255, 255, 0.06);
                --glass-bg-strong: rgba(255, 255, 255, 0.1);
                --glass-border: rgba(250, 204, 21, 0.28);
                --glass-border-soft: rgba(255, 255, 255, 0.12);
                --gold-glow: rgba(234, 179, 8, 0.35);
                --gold-glow-soft: rgba(250, 204, 21, 0.15);
                --text-primary: #ffffff;
                --text-secondary: #e8e8e8;
                --text-muted: #b0b0b0;
                --accent: #facc15;
                --accent-deep: #eab308;
                --radius-lg: 20px;
                --radius-md: 16px;
                --blur: blur(18px);
            }

            /* Liquid mesh background */
            .stApp {
                background-color: #080808;
                background-image:
                    radial-gradient(ellipse 90% 60% at 15% 0%, rgba(234, 179, 8, 0.14) 0%, transparent 55%),
                    radial-gradient(ellipse 70% 50% at 85% 100%, rgba(234, 179, 8, 0.1) 0%, transparent 50%),
                    radial-gradient(ellipse 50% 40% at 50% 45%, rgba(255, 255, 255, 0.04) 0%, transparent 60%),
                    linear-gradient(165deg, #121212 0%, #0a0a0a 45%, #0d0d0d 100%);
                color: var(--text-primary);
            }

            .stApp::before {
                content: "";
                position: fixed;
                inset: 0;
                background: radial-gradient(circle at 30% 70%, rgba(234, 179, 8, 0.06) 0%, transparent 40%);
                pointer-events: none;
                z-index: 0;
            }

            [data-testid="stAppViewContainer"] > section.main {
                background: transparent;
            }

            [data-testid="stMainBlockContainer"] {
                background: transparent;
            }

            /* Readable text on glass */
            .stApp,
            .stApp p,
            .stApp span,
            .stApp label,
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp h4,
            .stApp li,
            .stApp a {
                color: var(--text-primary);
            }

            [data-testid="stMarkdownContainer"] p,
            [data-testid="stMarkdownContainer"] li,
            [data-testid="stMarkdownContainer"] strong,
            [data-testid="stMarkdownContainer"] h1,
            [data-testid="stMarkdownContainer"] h2,
            [data-testid="stMarkdownContainer"] h3 {
                color: var(--text-primary) !important;
            }

            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] li {
                color: var(--text-secondary) !important;
            }

            [data-testid="stMetric"] label {
                color: var(--text-secondary) !important;
            }

            [data-testid="stMetric"] [data-testid="stMetricValue"] {
                color: var(--accent) !important;
                text-shadow: 0 0 16px var(--gold-glow-soft);
            }

            .stRadio label,
            .stRadio label span,
            .stRadio label p,
            .stSelectbox label,
            .stSelectbox label span,
            .stTextInput label,
            .stTextInput label span {
                color: var(--text-primary) !important;
            }

            [data-testid="stExpander"] summary,
            [data-testid="stExpander"] p {
                color: var(--text-primary) !important;
            }

            header[data-testid="stHeader"] {
                background: transparent !important;
            }

            /* Shared liquid glass panel */
            .stat-card,
            .clue-card,
            .result-card,
            .base-info-card,
            .score-display,
            .timer-display {
                background: var(--glass-bg) !important;
                backdrop-filter: var(--blur);
                -webkit-backdrop-filter: var(--blur);
                border: 1px solid var(--glass-border);
                box-shadow:
                    0 8px 32px rgba(0, 0, 0, 0.25),
                    0 0 24px var(--gold-glow-soft),
                    inset 0 1px 0 rgba(255, 255, 255, 0.08);
            }

            .game-title {
                font-size: 2.5rem;
                font-weight: 800;
                text-align: center;
                color: #ffffff !important;
                margin-bottom: 0.25rem;
                line-height: 1.2;
                text-shadow: 0 0 30px var(--gold-glow), 0 0 60px rgba(234, 179, 8, 0.12);
            }

            .game-subtitle {
                font-size: 1.1rem;
                text-align: center;
                color: var(--text-secondary) !important;
                margin-bottom: 2rem;
            }

            .brand-mark,
            .sidebar-brand {
                text-align: center;
                font-weight: 600;
                color: var(--accent) !important;
                text-transform: uppercase;
                text-shadow: 0 0 18px var(--gold-glow-soft);
            }

            .brand-mark {
                font-size: 1rem;
                letter-spacing: 0.12em;
                margin: -0.5rem 0 0.75rem 0;
            }

            .sidebar-brand {
                font-size: 0.85rem;
                letter-spacing: 0.1em;
                margin: -0.25rem 0 0.5rem 0;
            }

            .brand-footer {
                text-align: center;
                font-size: 0.8rem;
                color: var(--text-muted) !important;
                margin-top: 2.5rem;
                padding-top: 1rem;
                border-top: 1px solid var(--glass-border-soft);
            }

            .brand-name {
                color: var(--accent) !important;
                font-weight: 700;
                letter-spacing: 0.04em;
                text-shadow: 0 0 12px var(--gold-glow-soft);
            }

            .stat-card {
                border-radius: var(--radius-md);
                padding: 1rem;
                text-align: center;
                margin-bottom: 0.5rem;
                transition: box-shadow 0.3s ease, transform 0.3s ease;
            }

            .stat-card:hover {
                box-shadow:
                    0 12px 40px rgba(0, 0, 0, 0.3),
                    0 0 32px var(--gold-glow-soft);
            }

            .stat-label {
                font-size: 0.85rem;
                color: var(--text-secondary) !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .stat-value {
                font-size: 1.75rem;
                font-weight: 700;
                color: var(--accent) !important;
                text-shadow: 0 0 20px var(--gold-glow-soft);
            }

            /* Liquid glass buttons */
            div.stButton > button[kind="primary"] {
                background: linear-gradient(
                    135deg,
                    rgba(234, 179, 8, 0.9) 0%,
                    rgba(202, 138, 4, 0.85) 100%
                ) !important;
                color: #1a1a1a !important;
                font-size: 1.25rem;
                font-weight: 700;
                padding: 0.75rem 2rem;
                border-radius: var(--radius-lg) !important;
                border: 1px solid rgba(250, 204, 21, 0.5) !important;
                width: 100%;
                min-height: 3.5rem;
                box-shadow:
                    0 8px 24px rgba(0, 0, 0, 0.3),
                    0 0 28px var(--gold-glow);
                backdrop-filter: blur(8px);
                transition: all 0.3s ease;
            }

            div.stButton > button[kind="primary"]:hover {
                background: linear-gradient(
                    135deg,
                    rgba(250, 204, 21, 0.95) 0%,
                    rgba(234, 179, 8, 0.9) 100%
                ) !important;
                box-shadow:
                    0 12px 32px rgba(0, 0, 0, 0.35),
                    0 0 40px rgba(234, 179, 8, 0.45);
                transform: translateY(-1px);
            }

            div.stButton > button {
                color: var(--text-primary) !important;
                transition: all 0.3s ease;
            }

            div.stButton > button[kind="secondary"],
            div[data-testid="column"] div.stButton > button {
                background: var(--glass-bg) !important;
                backdrop-filter: var(--blur);
                -webkit-backdrop-filter: var(--blur);
                color: var(--text-primary) !important;
                font-size: 1rem;
                font-weight: 600;
                border: 1px solid var(--glass-border) !important;
                border-radius: var(--radius-md) !important;
                width: 100%;
                min-height: 3.25rem;
                box-shadow:
                    0 4px 20px rgba(0, 0, 0, 0.2),
                    0 0 16px var(--gold-glow-soft),
                    inset 0 1px 0 rgba(255, 255, 255, 0.06);
            }

            div.stButton > button[kind="secondary"]:hover,
            div[data-testid="column"] div.stButton > button:hover {
                box-shadow:
                    0 8px 28px rgba(0, 0, 0, 0.28),
                    0 0 28px var(--gold-glow-soft);
                border-color: rgba(250, 204, 21, 0.45) !important;
            }

            /* Glass sidebar */
            section[data-testid="stSidebar"] {
                background: rgba(10, 10, 10, 0.55) !important;
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
                border-right: 1px solid var(--glass-border);
                box-shadow: 4px 0 32px rgba(0, 0, 0, 0.2), 0 0 24px var(--gold-glow-soft);
            }

            section[data-testid="stSidebar"] .block-container {
                padding-top: 1.5rem;
            }

            .clue-card {
                border-radius: var(--radius-lg);
                padding: 1.25rem 1.5rem;
                margin-bottom: 0.75rem;
            }

            .clue-number {
                font-size: 0.8rem;
                color: var(--accent) !important;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.5rem;
                text-shadow: 0 0 10px var(--gold-glow-soft);
            }

            .clue-text {
                font-size: 1.35rem;
                font-weight: 600;
                color: #ffffff !important;
                line-height: 1.4;
            }

            .clue-hint {
                text-align: center;
                color: var(--text-secondary) !important;
                font-size: 0.95rem;
                margin-top: 0.5rem;
            }

            .score-display {
                border-radius: var(--radius-lg);
                padding: 1rem;
                text-align: center;
                margin-bottom: 1.25rem;
                border-width: 1px !important;
            }

            .score-label {
                display: block;
                font-size: 0.85rem;
                color: var(--text-secondary) !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .score-value {
                display: block;
                font-size: 2.5rem;
                font-weight: 800;
                color: var(--accent) !important;
                text-shadow: 0 0 24px var(--gold-glow);
            }

            .result-card {
                border-radius: var(--radius-lg);
                padding: 1.25rem 1.5rem;
                margin: 1rem 0;
                font-size: 1.1rem;
                line-height: 1.8;
                color: var(--text-primary) !important;
            }

            .result-card p,
            .result-card strong {
                color: var(--text-primary) !important;
            }

            .round-badge,
            .difficulty-badge {
                text-align: center;
                font-size: 0.9rem;
                color: #fde68a !important;
                margin-bottom: 0.5rem;
                text-shadow: 0 0 12px var(--gold-glow-soft);
            }

            .section-label {
                font-size: 0.9rem;
                font-weight: 700;
                color: #fde68a !important;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin: 0.5rem 0 0.75rem 0;
            }

            .base-info-row {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 0.5rem;
                margin-bottom: 1rem;
            }

            .base-info-card {
                border-radius: var(--radius-md);
                padding: 0.75rem 0.5rem;
                text-align: center;
                display: flex;
                flex-direction: column;
                gap: 0.35rem;
            }

            .base-info-label {
                font-size: 0.72rem;
                color: #fde68a !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .base-info-value {
                font-size: 0.95rem;
                font-weight: 700;
                color: #ffffff !important;
                line-height: 1.2;
            }

            .timer-display {
                border-radius: var(--radius-lg);
                padding: 0.75rem 1rem;
                text-align: center;
                margin-bottom: 1rem;
            }

            .timer-display.timer-urgent {
                border-color: rgba(239, 68, 68, 0.5) !important;
                background: rgba(239, 68, 68, 0.1) !important;
                box-shadow:
                    0 8px 32px rgba(0, 0, 0, 0.25),
                    0 0 24px rgba(239, 68, 68, 0.2),
                    inset 0 1px 0 rgba(255, 255, 255, 0.08);
            }

            .timer-label {
                display: block;
                font-size: 0.8rem;
                color: var(--text-secondary) !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .timer-value {
                display: block;
                font-size: 2rem;
                font-weight: 800;
                color: var(--accent) !important;
                text-shadow: 0 0 20px var(--gold-glow-soft);
            }

            .timer-urgent .timer-value {
                color: #f87171 !important;
                text-shadow: 0 0 20px rgba(239, 68, 68, 0.35);
            }

            /* Glass inputs */
            div[data-testid="stTextInput"] input {
                font-size: 1.15rem !important;
                padding: 0.75rem 1rem !important;
                border-radius: var(--radius-md) !important;
                background: var(--glass-bg) !important;
                backdrop-filter: var(--blur);
                -webkit-backdrop-filter: var(--blur);
                color: #ffffff !important;
                border: 1px solid var(--glass-border) !important;
                box-shadow: 0 0 16px var(--gold-glow-soft), inset 0 1px 0 rgba(255, 255, 255, 0.06);
            }

            div[data-testid="stTextInput"] input:focus {
                border-color: rgba(250, 204, 21, 0.55) !important;
                box-shadow: 0 0 24px var(--gold-glow), inset 0 1px 0 rgba(255, 255, 255, 0.1);
            }

            div[data-testid="stTextInput"] input::placeholder {
                color: var(--text-muted) !important;
            }

            div[data-baseweb="select"] > div {
                background: var(--glass-bg) !important;
                backdrop-filter: var(--blur);
                color: #ffffff !important;
                border-color: var(--glass-border) !important;
                border-radius: var(--radius-md) !important;
                box-shadow: 0 0 16px var(--gold-glow-soft);
            }

            [data-testid="stAlert"] p,
            [data-testid="stAlert"] div {
                color: inherit !important;
            }

            .float-effect-layer {
                position: fixed;
                top: 0;
                left: 0;
                width: 100vw;
                height: 100vh;
                pointer-events: none;
                z-index: 999999;
                overflow: hidden;
            }

            .floating-football,
            .floating-potty {
                position: absolute;
                bottom: -12%;
                line-height: 1;
                animation-name: float-up;
                animation-timing-function: ease-in;
                animation-fill-mode: forwards;
                will-change: transform, opacity;
            }

            .floating-football {
                filter: drop-shadow(0 0 12px var(--gold-glow-soft));
            }

            .floating-potty {
                filter: drop-shadow(0 6px 12px rgba(0, 0, 0, 0.4));
            }

            @keyframes float-up {
                0% {
                    transform: translateY(0) translateX(0) rotate(0deg);
                    opacity: 1;
                }
                25% {
                    transform: translateY(-30vh) translateX(calc(var(--drift, 0px) * 0.3)) rotate(8deg);
                    opacity: 1;
                }
                75% {
                    transform: translateY(-90vh) translateX(var(--drift, 0px)) rotate(-6deg);
                    opacity: 0.85;
                }
                100% {
                    transform: translateY(-125vh) translateX(calc(var(--drift, 0px) * 1.2)) rotate(10deg);
                    opacity: 0;
                }
            }

            @media (max-width: 768px) {
                .game-title {
                    font-size: 2rem;
                }

                .game-subtitle {
                    font-size: 1rem;
                }

                .stat-value {
                    font-size: 1.5rem;
                }

                .clue-text {
                    font-size: 1.2rem;
                }

                .score-value {
                    font-size: 2rem;
                }

                .base-info-row {
                    grid-template-columns: 1fr;
                }

                .base-info-value {
                    font-size: 1.05rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
