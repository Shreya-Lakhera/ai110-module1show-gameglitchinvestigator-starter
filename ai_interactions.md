# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

---

## Test Generation (SF7)

> Document how you used AI to help generate or improve tests.

| Edge Case | Prompt Used | AI-Suggested Test | Did It Pass? | Your Reasoning |
|-----------|-------------|-------------------|--------------|----------------|
| | | | | |
| | | | | |
| | | | | |

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
