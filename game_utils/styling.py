"""CSS styling for the Football Guess the Player app."""

import streamlit as st


def apply_custom_styles() -> None:
    """Inject dark football-themed CSS into the Streamlit app."""
    st.markdown(
        """
        <style>
            /* Base app colours */
            .stApp {
                background: linear-gradient(180deg, #0d1f0d 0%, #0a0a0a 100%);
                color: #ffffff;
            }

            /* Ensure all Streamlit text is readable on dark background */
            .stApp,
            .stApp p,
            .stApp span,
            .stApp label,
            .stApp h1,
            .stApp h2,
            .stApp h3,
            .stApp h4,
            .stApp h5,
            .stApp h6,
            .stApp li,
            .stApp a {
                color: #f5f5f5;
            }

            [data-testid="stMarkdownContainer"] p,
            [data-testid="stMarkdownContainer"] li,
            [data-testid="stMarkdownContainer"] strong,
            [data-testid="stMarkdownContainer"] h1,
            [data-testid="stMarkdownContainer"] h2,
            [data-testid="stMarkdownContainer"] h3 {
                color: #f5f5f5 !important;
            }

            [data-testid="stSidebar"] p,
            [data-testid="stSidebar"] span,
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] h1,
            [data-testid="stSidebar"] h2,
            [data-testid="stSidebar"] h3,
            [data-testid="stSidebar"] li {
                color: #f0f0f0 !important;
            }

            /* Metrics */
            [data-testid="stMetric"] label {
                color: #c8e6c8 !important;
            }

            [data-testid="stMetric"] [data-testid="stMetricValue"] {
                color: #4ade80 !important;
            }

            /* Form labels: radio, select, text input */
            .stRadio label,
            .stRadio label span,
            .stRadio label p,
            .stSelectbox label,
            .stSelectbox label span,
            .stTextInput label,
            .stTextInput label span {
                color: #f5f5f5 !important;
            }

            /* Expander */
            [data-testid="stExpander"] summary,
            [data-testid="stExpander"] p {
                color: #f5f5f5 !important;
            }

            header[data-testid="stHeader"] {
                background: transparent;
            }

            /* Title styling */
            .game-title {
                font-size: 2.5rem;
                font-weight: 800;
                text-align: center;
                color: #ffffff !important;
                margin-bottom: 0.25rem;
                line-height: 1.2;
            }

            .game-subtitle {
                font-size: 1.1rem;
                text-align: center;
                color: #d4f0d4 !important;
                margin-bottom: 2rem;
            }

            /* Branding */
            .brand-mark {
                text-align: center;
                font-size: 1rem;
                font-weight: 600;
                color: #6ee7a0 !important;
                letter-spacing: 0.12em;
                text-transform: uppercase;
                margin: -0.5rem 0 0.75rem 0;
            }

            .sidebar-brand {
                text-align: center;
                font-size: 0.85rem;
                font-weight: 600;
                color: #6ee7a0 !important;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin: -0.25rem 0 0.5rem 0;
            }

            .brand-footer {
                text-align: center;
                font-size: 0.8rem;
                color: #8fb88f !important;
                margin-top: 2.5rem;
                padding-top: 1rem;
                border-top: 1px solid rgba(61, 139, 61, 0.35);
            }

            .brand-name {
                color: #6ee7a0 !important;
                font-weight: 700;
                letter-spacing: 0.04em;
            }

            /* Stat cards on home screen */
            .stat-card {
                background: rgba(34, 85, 34, 0.55);
                border: 1px solid #3d8b3d;
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
                margin-bottom: 0.5rem;
            }

            .stat-label {
                font-size: 0.85rem;
                color: #d4f0d4 !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .stat-value {
                font-size: 1.75rem;
                font-weight: 700;
                color: #6ee7a0 !important;
            }

            .difficulty-label {
                font-size: 1rem;
                font-weight: 600;
                color: #ffffff !important;
            }

            /* Buttons */
            div.stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
                color: #ffffff !important;
                font-size: 1.25rem;
                font-weight: 700;
                padding: 0.75rem 2rem;
                border-radius: 12px;
                border: none;
                width: 100%;
                min-height: 3.5rem;
            }

            div.stButton > button[kind="primary"]:hover {
                background: linear-gradient(135deg, #4ade80 0%, #22c55e 100%);
                color: #ffffff !important;
                border: none;
            }

            div.stButton > button {
                color: #ffffff !important;
            }

            div.stButton > button[kind="secondary"] {
                background: rgba(34, 85, 34, 0.6);
                color: #ffffff !important;
                font-size: 1rem;
                font-weight: 600;
                border: 1px solid #3d8b3d;
                border-radius: 10px;
                width: 100%;
                min-height: 3rem;
            }

            /* Sidebar */
            section[data-testid="stSidebar"] {
                background: #0f1f0f;
                border-right: 1px solid #2d6a2d;
            }

            section[data-testid="stSidebar"] .block-container {
                padding-top: 1.5rem;
            }

            /* Clue cards */
            .clue-card {
                background: rgba(20, 50, 20, 0.85);
                border: 1px solid #3d8b3d;
                border-radius: 14px;
                padding: 1.25rem 1.5rem;
                margin-bottom: 0.75rem;
            }

            .clue-number {
                font-size: 0.8rem;
                color: #6ee7a0 !important;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin-bottom: 0.5rem;
            }

            .clue-text {
                font-size: 1.35rem;
                font-weight: 600;
                color: #ffffff !important;
                line-height: 1.4;
            }

            .clue-hint {
                text-align: center;
                color: #d4f0d4 !important;
                font-size: 0.95rem;
                margin-top: 0.5rem;
            }

            /* Score display */
            .score-display {
                background: rgba(0, 0, 0, 0.5);
                border: 2px solid #22c55e;
                border-radius: 14px;
                padding: 1rem;
                text-align: center;
                margin-bottom: 1.25rem;
            }

            .score-label {
                display: block;
                font-size: 0.85rem;
                color: #d4f0d4 !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .score-value {
                display: block;
                font-size: 2.5rem;
                font-weight: 800;
                color: #6ee7a0 !important;
            }

            /* Result card */
            .result-card {
                background: rgba(20, 50, 20, 0.85);
                border: 1px solid #3d8b3d;
                border-radius: 14px;
                padding: 1.25rem 1.5rem;
                margin: 1rem 0;
                font-size: 1.1rem;
                line-height: 1.8;
                color: #f5f5f5 !important;
            }

            .result-card p,
            .result-card strong {
                color: #f5f5f5 !important;
            }

            .round-badge,
            .difficulty-badge {
                text-align: center;
                font-size: 0.9rem;
                color: #d4f0d4 !important;
                margin-bottom: 0.5rem;
            }

            .section-label {
                font-size: 0.9rem;
                font-weight: 700;
                color: #a8d5a8 !important;
                text-transform: uppercase;
                letter-spacing: 0.08em;
                margin: 0.5rem 0 0.75rem 0;
            }

            /* Always-visible player facts */
            .base-info-row {
                display: grid;
                grid-template-columns: repeat(3, 1fr);
                gap: 0.5rem;
                margin-bottom: 1rem;
            }

            .base-info-card {
                background: rgba(15, 40, 15, 0.9);
                border: 1px solid #3d8b3d;
                border-radius: 12px;
                padding: 0.75rem 0.5rem;
                text-align: center;
                display: flex;
                flex-direction: column;
                gap: 0.35rem;
            }

            .base-info-label {
                font-size: 0.72rem;
                color: #a8d5a8 !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .base-info-value {
                font-size: 0.95rem;
                font-weight: 700;
                color: #ffffff !important;
                line-height: 1.2;
            }

            /* Timer display */
            .timer-display {
                background: rgba(0, 0, 0, 0.45);
                border: 2px solid #22c55e;
                border-radius: 14px;
                padding: 0.75rem 1rem;
                text-align: center;
                margin-bottom: 1rem;
            }

            .timer-display.timer-urgent {
                border-color: #ef4444;
                background: rgba(80, 10, 10, 0.45);
            }

            .timer-label {
                display: block;
                font-size: 0.8rem;
                color: #d4f0d4 !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .timer-value {
                display: block;
                font-size: 2rem;
                font-weight: 800;
                color: #6ee7a0 !important;
            }

            .timer-urgent .timer-value {
                color: #f87171 !important;
            }

            /* Multiple choice buttons */
            div.stButton > button[kind="secondary"],
            div[data-testid="column"] div.stButton > button {
                min-height: 3.25rem;
                font-size: 1.05rem !important;
                font-weight: 600 !important;
            }

            /* Text input */
            div[data-testid="stTextInput"] input {
                font-size: 1.15rem !important;
                padding: 0.75rem 1rem !important;
                border-radius: 10px !important;
                background-color: #1a2e1a !important;
                color: #ffffff !important;
                border: 1px solid #3d8b3d !important;
            }

            div[data-testid="stTextInput"] input::placeholder {
                color: #9cc49c !important;
            }

            /* Selectbox */
            div[data-baseweb="select"] > div {
                background-color: #1a2e1a !important;
                color: #ffffff !important;
                border-color: #3d8b3d !important;
            }

            /* Alert boxes — keep dark text on light alert backgrounds */
            [data-testid="stAlert"] p,
            [data-testid="stAlert"] div {
                color: inherit !important;
            }

            /* Floating celebration effects (balloon-style) */
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
                filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.35));
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
