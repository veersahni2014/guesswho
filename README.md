# ⚽ Football Guess the Player

**by Veer Sahni**

A fun football guessing game built with Python and Streamlit. Read clues about a footballer and try to identify them before you run out of points!

## What this project does

You see clues about a football player — nationality, clubs, achievements, and more — and try to guess who it is. Fewer clues and fewer wrong guesses mean a higher score. Play Classic mode for a single round, or take on the **5 Player Challenge** to test yourself over five rounds.

### Features

- Three difficulty levels (Easy, Medium, Hard)
- Clues revealed one at a time
- Forgiving answer matching (ignores capitals, accents, extra spaces)
- Scoring that rewards early guesses
- Penalties for wrong guesses
- Streak bonus (+20 for 3 correct in a row)
- Session statistics tracked in your browser
- Mobile-friendly dark football theme

## Project structure

```
├── app.py              # Main Streamlit entry point
├── requirements.txt    # Python dependencies
├── README.md
├── data/
│   └── players.json    # Player database (55 players)
└── guesswho_game/
    ├── __init__.py
    ├── game.py         # Game logic, scoring, answer checking
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

## How to play

1. Choose a difficulty (Easy, Medium, or Hard).
2. Pick Classic or 5 Player Challenge.
3. Tap **START GAME**.
4. Read the clues and type your guess.
5. Use **NEXT CLUE** if you need help (each clue lowers your max score).
6. Wrong guesses cost points — try again or reveal another clue.
7. Get 3 correct in a row for a +20 streak bonus!

### Scoring

| Clues used | Max points |
|------------|------------|
| 1          | 100        |
| 2          | 80         |
| 3          | 60         |
| 4          | 40         |
| 5          | 20         |

**Wrong guess penalties:** -10, -15, -20 (minimum score is 0).

## How to add players

Edit `data/players.json`. Each player needs:

```json
{
  "name": "Player Name",
  "nationality": "Country",
  "position": "Forward",
  "clubs": ["Club A", "Club B"],
  "birth_year": 1990,
  "world_cup_winner": false,
  "ballon_dor_wins": 0,
  "alternate_names": ["nickname"],
  "info": "A short interesting fact.",
  "clues": {
    "easy": ["Clue 1", "Clue 2", "Clue 3"],
    "medium": ["Clue 1", "Clue 2", "Clue 3"],
    "hard": ["Clue 1", "Clue 2", "Clue 3"]
  }
}
```

The app validates player data on startup and skips any entries with missing fields.

## Deploy to Streamlit Community Cloud

1. Push this repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io).
3. Click **New app** and connect your GitHub repo.
4. Set the main file path to `app.py`.
5. Click **Deploy**.

No secrets or database are required for Version 1.

## Tech stack

- Python 3
- Streamlit
- JSON file for player data (no database)
- `st.session_state` for session statistics
