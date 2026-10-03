# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I asked Codex to add a meaningful feature for the Agent Mode requirement
and update the README and this workflow log. Codex chose a session high-score
tracker that keeps a separate record for each difficulty.

My request: "please do this too and update readme", with the Feature
Expansion via Agent Mode rubric requiring a working feature and a log of
the task, modified files, completed work, and manual corrections.

**What did the agent do?**

Codex inspected the app, implemented the tracker, added tests, and ran them.

- `app.py`: Added `record_high_score()` and `render_high_scores()`. Winning
  rounds update the sidebar records only if the score beats the previous
  best. New Game and difficulty changes keep the records for this session.
- `tests/test_app.py`: Added checks for improved and lower winning scores,
  losses, round resets, difficulty changes, reruns, and fresh sessions.
  Updated existing UI checks to target the main game table separately from
  the new sidebar table.
- `README.md`: Added feature details, code references, demo instructions,
  the session-only limitation, and the latest test result.
- `ai_interactions.md`: Recorded the task, changes, and verification here.

```text
.\.venv-1\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
..........                                                               [100%]
10 passed in 3.63s

python -B tools/check_style.py
Basic style check: 0 violations in 5 files.
```

**What did you have to verify or fix manually?**

No manual corrections have been made for this feature yet. Codex ran the
automated checks; I have not reported a separate browser test of the tracker.
For a manual check, I can win a round, click New Game, and confirm the best
score stays while the round score resets. Records are only saved for the
current Streamlit session, not permanently or across different users.

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

**Prompt used:**

```text
At least three pytest cases targeting complex edge cases (e.g., handling
non-numeric strings, negative numbers, or empty inputs) are implemented.
Tests are specific and pass successfully. Terminal output showing all
tests passing is pasted as a fenced code block in the README.
ai_interactions.md records the test-generation prompt(s) and a short
rationale for each edge case chosen. add this too
```

Codex added four separately collected pytest cases through parametrization
in `tests/test_app.py`. Each starts with four wrong guesses on Hard, submits
the invalid input twice, and then wins with 50 on the last allowed attempt.
The checks cover the exact error, unchanged attempts, score, secret, and
valid-guess table, plus the final win and high-score update.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| Empty input (`""`) | Prompt above | `empty-input`: shows "Enter a guess." and preserves the final attempt. | Yes | An accidental empty submission should not end the round. |
| Non-numeric text (`"abc"`) | Prompt above | `non-numeric`: shows "That is not a number." without a crash or score change. | Yes | Typing letters should give a clear error and let the player try again. |
| Negative number (`"-1"`) | Prompt above | `negative-number`: rejects the guess as outside 1–50 and preserves round state. | Yes | Parsing a number does not mean it is valid for the game. |
| Above the Hard range (`"51"`) | Prompt above | `above-hard-range`: rejects 51, then accepts 50 as a final-attempt win. | Yes | This checks both the upper range boundary and winning on the last attempt. |

**Actual terminal output:**

```text
.\.venv-1\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
..............                                                           [100%]
14 passed in 4.30s

python -B tools/check_style.py
Basic style check: 0 violations in 5 files.
```

No game-code changes were needed for these cases. Codex corrected the basic
style checker in `tools/check_style.py` to check spacing before decorators,
instead of incorrectly flagging a decorated test function.

---

## Linting & Style (SF9)

> Document your use of AI for linting or code style improvements.

**Prompt used:**

```
<!-- Paste the prompt you gave the AI -->
AI assistance is used to add professional docstrings to all functions in
logic_utils.py. Code follows PEP 8 style guidelines, and ai_interactions.md
includes the prompt(s) used, the linting output (code block or committed
.txt), and notes on what formatting/naming changes the AI suggested and
which were applied. make these changes
```

**Linting output before:**

```
app.py:5: E302 expected 2 blank lines, found 1
app.py:50: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:3: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:8: E302 expected 2 blank lines, found 1
tests/test_game_logic.py:13: E302 expected 2 blank lines, found 1
```

**Changes applied:**

Codex suggested adding Args, Returns, and Raises sections to all four
functions in logic_utils.py. I used those changes, including notes that
three functions are still placeholders. Codex also wrapped long exception
lines, separated import groups, and added two blank lines before top-level
functions. Those formatting changes were applied. No names were changed
because the existing function and variable names already use snake_case.

**How the checks were run:**

Installing pycodestyle was blocked by network restrictions, and I declined
the installation approval. Codex used a limited local checker instead and
saved it as tools/check_style.py so the check can be repeated. The output
above came from the initial in-memory version, after the docstring edits
but before the blank-line fixes. It checks line length, trailing whitespace,
tabs, and spacing before top-level functions. Import grouping and naming
were reviewed manually; this is not a full pycodestyle or Ruff result.

**Linting output after:**

```text
python -B tools/check_style.py
Basic style check: 0 violations in 5 files.
```

**Tests after the documentation and formatting changes:**

```text
.\.venv-1\Scripts\python.exe -B -m pytest -q -p no:cacheprovider
.......                                                                  [100%]
7 passed in 1.73s
```

---

## Model Comparison (SF11)

> Compare two AI models on the same task.

**Task given to both models:**

<!-- Describe what you asked each model to do -->

| | Model A | Model B |
|-|---------|---------|
| **Model name** | | |
| **Response summary** | | |
| **More Pythonic?** | | |
| **Clearer explanation?** | | |

**Which did you prefer and why?**

<!-- Your conclusion -->
