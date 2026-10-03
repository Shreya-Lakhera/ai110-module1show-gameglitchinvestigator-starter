# 🎮 Game Glitch Investigator: The Impossible Guesser

## 🚨 The Situation

You asked an AI to build a simple "Number Guessing Game" using Streamlit.
It wrote the code, ran away, and now the game is unplayable. 

- You can't win.
- The hints lie to you.
- The secret number seems to have commitment issues.

## 🛠️ Setup

1. Install dependencies: `pip install -r requirements.txt`
2. Run the broken app: `python -m streamlit run app.py`

## 🕵️‍♂️ Your Mission

1. **Play the game.** Open the "Developer Debug Info" tab in the app to see the secret number. Try to win.
2. **Find the State Bug.** Why does the secret number change every time you click "Submit"? Ask ChatGPT: *"How do I keep a variable from resetting in Streamlit when I click a button?"*
3. **Fix the Logic.** The hints ("Higher/Lower") are wrong. Fix them.
4. **Refactor & Test.** - Move the logic into `logic_utils.py`.
   - Run `pytest` in your terminal.
   - Keep fixing until all tests pass!

## 📝 Document Your Experience

- [ ] Describe the game's purpose.

A number-guessing game where players choose a difficulty and try to find a secret number within a limited number of attempts.

- [ ] Detail which bugs you found.

Reversed hints, text-based comparisons on alternating attempts, incomplete New Game resets, incorrect ranges when restarting, and unimplemented functions in logic_utils.py.

- [ ] Explain what fixes you applied.

Corrected the hint directions, made New Game reset the status, attempts, score, history, and input, and ensured new secrets match the selected difficulty. Also corrected the initial attempt count and displayed range, and removed Developer Debug Info.

## 📸 Demo Walkthrough

Describe your fixed game in numbered steps so a reader can follow along without watching a video:

1. Launch the app using python -m streamlit run app.py.
2. Choose Easy, Normal, or Hard, then click New Game to start a round using that difficulty.
3. Enter a whole number within the displayed range and click Submit Guess. With hints enabled, “Too High” now says “Go LOWER!” and “Too Low” says “Go HIGHER!”
4. Continue guessing until you win or run out of attempts. Alternating attempts can still misclassify guesses because the text-comparison bug remains.
5. Click New Game again. The input, score, history, and attempts clear, and you can play again after either winning or losing.


## 🧪 Test Results

```
# Paste your pytest output here, e.g.:
# pytest tests/
# Initial run collected three tests, and all failed because check_guess() was a placeholder.
```

## 🚀 Stretch Features

- [ ] [If you choose to complete Challenge 4, describe the Enhanced UI changes here — a screenshot is optional]
