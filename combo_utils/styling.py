"""CSS styling for the Blox Fruits Combo Maker."""

import streamlit as st


def apply_custom_styles() -> None:
    """Inject ocean-themed glass UI for Blox Fruits."""
    st.markdown(
        """
        <style>
            :root {
                --glass-bg: rgba(255, 255, 255, 0.06);
                --glass-border: rgba(56, 189, 248, 0.28);
                --glass-border-soft: rgba(255, 255, 255, 0.12);
                --ocean-glow: rgba(14, 165, 233, 0.35);
                --ocean-glow-soft: rgba(56, 189, 248, 0.15);
                --fruit-red: #ef4444;
                --fruit-red-glow: rgba(239, 68, 68, 0.35);
                --text-primary: #ffffff;
                --text-secondary: #e2e8f0;
                --text-muted: #94a3b8;
                --accent: #38bdf8;
                --accent-deep: #0ea5e9;
                --radius-lg: 20px;
                --radius-md: 16px;
                --blur: blur(18px);
            }

            .stApp {
                background-color: #050a12;
                background-image:
                    radial-gradient(ellipse 90% 60% at 15% 0%, rgba(14, 165, 233, 0.16) 0%, transparent 55%),
                    radial-gradient(ellipse 70% 50% at 85% 100%, rgba(239, 68, 68, 0.1) 0%, transparent 50%),
                    radial-gradient(ellipse 50% 40% at 50% 45%, rgba(255, 255, 255, 0.03) 0%, transparent 60%),
                    linear-gradient(165deg, #0c1929 0%, #050a12 45%, #0a1020 100%);
                color: var(--text-primary);
            }

            [data-testid="stAppViewContainer"] > section.main,
            [data-testid="stMainBlockContainer"] {
                background: transparent;
            }

            .stApp, .stApp p, .stApp span, .stApp label,
            .stApp h1, .stApp h2, .stApp h3, .stApp li {
                color: var(--text-primary);
            }

            [data-testid="stMarkdownContainer"] p,
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
            [data-testid="stSidebar"] h3 {
                color: var(--text-secondary) !important;
            }

            [data-testid="stMetric"] label {
                color: var(--text-secondary) !important;
            }

            [data-testid="stMetric"] [data-testid="stMetricValue"] {
                color: var(--accent) !important;
                text-shadow: 0 0 16px var(--ocean-glow-soft);
            }

            header[data-testid="stHeader"] {
                background: transparent !important;
            }

            section[data-testid="stSidebar"] {
                background: rgba(5, 10, 18, 0.6) !important;
                backdrop-filter: blur(20px);
                border-right: 1px solid var(--glass-border);
            }

            .game-title {
                font-size: 2.4rem;
                font-weight: 800;
                text-align: center;
                color: #ffffff !important;
                margin-bottom: 0.25rem;
                text-shadow: 0 0 30px var(--ocean-glow), 0 0 20px var(--fruit-red-glow);
            }

            .game-subtitle {
                font-size: 1.05rem;
                text-align: center;
                color: var(--text-secondary) !important;
                margin-bottom: 1.5rem;
            }

            .brand-mark {
                text-align: center;
                font-weight: 600;
                color: var(--accent) !important;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                margin: -0.25rem 0 1rem 0;
            }

            .stat-card,
            .combo-card,
            .step-card,
            .build-card,
            .result-card {
                background: var(--glass-bg) !important;
                backdrop-filter: var(--blur);
                border: 1px solid var(--glass-border);
                border-radius: var(--radius-md);
                box-shadow: 0 8px 32px rgba(0, 0, 0, 0.25), 0 0 24px var(--ocean-glow-soft);
            }

            .stat-card {
                padding: 0.85rem;
                text-align: center;
                margin-bottom: 0.5rem;
            }

            .stat-label {
                font-size: 0.78rem;
                color: var(--text-secondary) !important;
                text-transform: uppercase;
                letter-spacing: 0.05em;
            }

            .stat-value {
                font-size: 1.5rem;
                font-weight: 700;
                color: var(--accent) !important;
            }

            .stat-value.danger {
                color: var(--fruit-red) !important;
            }

            .combo-card {
                padding: 1.25rem;
                margin-bottom: 1rem;
            }

            .combo-header {
                font-size: 1.1rem;
                font-weight: 700;
                color: #7dd3fc !important;
                margin-bottom: 0.75rem;
            }

            .combo-sequence {
                font-size: 1.05rem;
                font-weight: 600;
                line-height: 1.6;
                color: #ffffff !important;
                padding: 0.75rem;
                background: rgba(14, 165, 233, 0.08);
                border-radius: 12px;
                border: 1px solid rgba(56, 189, 248, 0.2);
                margin-bottom: 0.75rem;
            }

            .step-card {
                padding: 0.75rem 1rem;
                margin-bottom: 0.5rem;
                display: flex;
                gap: 0.75rem;
                align-items: flex-start;
            }

            .step-card.broken {
                border-color: rgba(239, 68, 68, 0.5) !important;
                background: rgba(239, 68, 68, 0.08) !important;
            }

            .step-number {
                min-width: 2rem;
                height: 2rem;
                border-radius: 50%;
                background: rgba(14, 165, 233, 0.25);
                color: #7dd3fc !important;
                font-weight: 800;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 0.9rem;
            }

            .step-key {
                font-weight: 700;
                color: #fde68a !important;
                font-size: 0.95rem;
            }

            .step-name {
                color: #ffffff !important;
                font-size: 0.95rem;
            }

            .step-meta {
                color: var(--text-muted) !important;
                font-size: 0.8rem;
                margin-top: 0.2rem;
            }

            .ken-badge {
                display: inline-block;
                background: rgba(239, 68, 68, 0.2);
                color: #fca5a5 !important;
                font-size: 0.7rem;
                font-weight: 700;
                padding: 0.1rem 0.45rem;
                border-radius: 6px;
                margin-left: 0.35rem;
                text-transform: uppercase;
            }

            .link-ok {
                color: #4ade80 !important;
            }

            .link-bad {
                color: #f87171 !important;
            }

            .build-card {
                padding: 1rem 1.25rem;
                margin-bottom: 1rem;
            }

            div.stButton > button[kind="primary"] {
                background: linear-gradient(135deg, rgba(14, 165, 233, 0.95) 0%, rgba(2, 132, 199, 0.9) 100%) !important;
                color: #0c1929 !important;
                font-weight: 700;
                border-radius: var(--radius-lg) !important;
                border: 1px solid rgba(56, 189, 248, 0.5) !important;
                box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3), 0 0 28px var(--ocean-glow);
            }

            div.stButton > button[kind="primary"]:hover {
                box-shadow: 0 12px 32px rgba(0, 0, 0, 0.35), 0 0 40px rgba(14, 165, 233, 0.45);
            }

            div[data-baseweb="select"] > div,
            div[data-testid="stTextInput"] input,
            div[data-testid="stNumberInput"] input {
                background: var(--glass-bg) !important;
                color: #ffffff !important;
                border-color: var(--glass-border) !important;
                border-radius: var(--radius-md) !important;
            }

            .brand-footer {
                text-align: center;
                font-size: 0.8rem;
                color: var(--text-muted) !important;
                margin-top: 2rem;
                padding-top: 1rem;
                border-top: 1px solid var(--glass-border-soft);
            }

            @media (max-width: 768px) {
                .game-title { font-size: 1.9rem; }
                .combo-sequence { font-size: 0.95rem; }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
