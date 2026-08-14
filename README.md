# ⚽ Football Guess the Player

A fun football guessing game built with Python and Streamlit. Read clues about a footballer and try to identify them before you run out of points!

## What this project does

You see clues about a football player — nationality, clubs, achievements, and more — and try to guess who it is. Fewer clues and fewer wrong guesses mean a higher score.

## Project structure

```
football-guess-player/
├── app.py              # Main Streamlit entry point
├── requirements.txt    # Python dependencies
├── README.md
├── data/
│   └── players.json    # Player database (added in Stage 2)
└── utils/
    ├── __init__.py
    ├── game.py         # Game logic (added in later stages)
    └── styling.py      # Custom CSS styling
```

## How to run locally

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Start the app

```bash
streamlit run app.py
```

Your browser should open automatically. If not, go to `http://localhost:8501`.

## Current status

**Stage 1 complete** — Basic Streamlit app with home screen, dark football theme, difficulty/mode selection, and session stat placeholders.

Upcoming stages will add player data, game mechanics, scoring, and the 5 Player Challenge.

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Click **New app** and connect your GitHub repo.
4. Set the main file path to `app.py`.
5. Click **Deploy**.

No secrets or database are required for Version 1.

## Adding players (coming in Stage 2)

Player data will live in `data/players.json`. Each player needs a name, nationality, position, clubs, and clues for easy, medium, and hard difficulties.
