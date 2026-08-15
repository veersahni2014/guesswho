# Blox Fruits Combo Maker

A fan-made **Blox Fruits PvP combo generator** built with Python and Streamlit. Input your build (fruit, sword, fighting style, gun, stats, race) and get working combo sequences validated with stun/startup frame logic.

## What it does

- Select your full loadout: fruit, sword, fighting style, optional gun, and race
- Choose a stat preset (Fruit Main, Sword Main, Hybrid, etc.) or customize points
- Toggle Observation (Ken) and ping for realistic combo validation
- Generate up to 3 combo variants: meta preset, auto-generated, and safe/reliable
- See step-by-step breakdown with damage estimates, stun windows, and link margins

## Project structure

```
├── app.py                    # Streamlit UI
├── requirements.txt
├── data/
│   └── combo_moves.json      # Move database (fruits, swords, styles, guns)
└── combo_utils/
    ├── engine.py             # Combo generation & validation
    └── styling.py            # Ocean-themed UI
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

Open `http://localhost:8501` in your browser.

## How combos are built

Combos follow the standard PvP structure:

1. **Opener** — stun or Ken-break move (required vs Observation users)
2. **Filler** — M1 chains or sword swap during cooldowns
3. **Damage** — fruit and fighting style abilities
4. **Finisher** — highest damage move last

A move **links** to the next when: `stun_duration ≥ next_startup + ping_buffer`

## Supported items

**Fruits:** Dough, Kitsune, Dragon, Leopard, Venom, Gas, Control, Portal, Light, Magma, Buddha

**Swords:** Cursed Dual Katana, True Triple Katana, Shark Anchor, Spikey Trident, Dark Blade

**Fighting Styles:** Godhuman, Sanguine Art, Electric Claw, Superhuman, Death Step

**Guns:** Soul Guitar, Kabucha

## Deploy to Streamlit Cloud

1. Push to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Set main file to `app.py`
4. Deploy

## Disclaimer

This is a fan-made tool for educational purposes. Move values are approximations and may not match the live game after updates. Not affiliated with Roblox or Blox Fruits.
