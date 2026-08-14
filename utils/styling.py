"""CSS styling for the Football Guess the Player app."""

import streamlit as st


def apply_custom_styles() -> None:
    """Inject dark football-themed CSS into the Streamlit app."""
    st.markdown(
        """
        <style>
            /* Main app background */
            .stApp {
                background: linear-gradient(180deg, #0d1f0d 0%, #0a0a0a 100%);
                color: #ffffff;
            }

            /* Hide default Streamlit header/footer clutter */
            header[data-testid="stHeader"] {
                background: transparent;
            }

            /* Title styling */
            .game-title {
                font-size: 2.5rem;
                font-weight: 800;
                text-align: center;
                color: #ffffff;
                margin-bottom: 0.25rem;
                line-height: 1.2;
            }

            .game-subtitle {
                font-size: 1.1rem;
                text-align: center;
                color: #a8d5a8;
                margin-bottom: 2rem;
            }

            /* Stat cards on home screen */
            .stat-card {
                background: rgba(34, 85, 34, 0.35);
                border: 1px solid #2d6a2d;
                border-radius: 12px;
                padding: 1rem;
                text-align: center;
                margin-bottom: 0.5rem;
            }

            .stat-label {
                font-size: 0.85rem;
                color: #a8d5a8;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .stat-value {
                font-size: 1.75rem;
                font-weight: 700;
                color: #4ade80;
            }

            /* Difficulty option labels */
            .difficulty-label {
                font-size: 1rem;
                font-weight: 600;
                color: #ffffff;
            }

            /* Large primary buttons */
            div.stButton > button[kind="primary"] {
                background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%);
                color: #ffffff;
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
                color: #ffffff;
                border: none;
            }

            /* Secondary buttons */
            div.stButton > button[kind="secondary"] {
                background: rgba(34, 85, 34, 0.4);
                color: #ffffff;
                font-size: 1rem;
                font-weight: 600;
                border: 1px solid #2d6a2d;
                border-radius: 10px;
                width: 100%;
                min-height: 3rem;
            }

            /* Radio buttons for difficulty */
            div[data-testid="stRadio"] label {
                font-size: 1.05rem !important;
                color: #ffffff !important;
            }

            /* Sidebar styling */
            section[data-testid="stSidebar"] {
                background: #0f1f0f;
                border-right: 1px solid #2d6a2d;
            }

            section[data-testid="stSidebar"] .block-container {
                padding-top: 1.5rem;
            }

            /* Mobile-friendly text sizing */
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
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
