import random

import streamlit as st

from logic_utils import check_guess


def get_range_for_difficulty(difficulty: str):
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 50
    return 1, 100


def parse_guess(raw: str):
    if raw is None:
        return False, None, "Enter a guess."

    if raw == "":
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            value = int(float(raw))
        else:
            value = int(raw)
    except Exception:
        return False, None, "That is not a number."

    return True, value, None


def update_score(current_score: int, outcome: str, attempt_number: int):
    if outcome == "Win":
        points = 100 - 10 * (attempt_number + 1)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


def reset_game(difficulty):
    low, high = get_range_for_difficulty(difficulty)
    st.session_state.game_difficulty = difficulty
    st.session_state.status = "playing"
    st.session_state.attempts = 0
    st.session_state.secret = random.randint(low, high)
    st.session_state.score = 0
    st.session_state.history = []
    st.session_state[f"guess_input_{difficulty}"] = ""


def render_hint(outcome):
    """Show a direction using both text and a distinct color."""
    if outcome == "Too High":
        st.warning("📉 Too high — Go LOWER!")
    elif outcome == "Too Low":
        st.info("📈 Too low — Go HIGHER!")
    else:
        st.success("🎯 Correct guess!")


def render_round_summary(attempt_limit, show_hint):
    """Display round metrics and valid guesses without revealing the secret."""
    st.subheader("Your round")
    attempts = st.session_state.attempts
    used, remaining, score = st.columns(3)
    used.metric("Guesses used", attempts)
    remaining.metric("Attempts left", max(0, attempt_limit - attempts))
    score.metric("Score", st.session_state.score)
    st.progress(min(1.0, attempts / attempt_limit))

    guesses = [
        guess for guess in st.session_state.history
        if isinstance(guess, int)
    ]
    if not guesses:
        st.caption("Your guesses will appear here. Make your first guess!")
        return

    rows = []
    for number, guess in enumerate(guesses, 1):
        row = {"Attempt": number, "Guess": guess}
        if show_hint:
            outcome = check_guess(guess, st.session_state.secret)
            row["Result"] = {
                "Win": "🎯 Correct",
                "Too High": "📉 Too high — try lower",
                "Too Low": "📈 Too low — try higher",
            }[outcome]
        rows.append(row)
    st.table(rows)


st.set_page_config(page_title="Glitchy Guesser", page_icon="🎮")

st.title("🎮 Game Glitch Investigator")
st.caption("Find the secret number. Use each hint to narrow your next guess.")

st.sidebar.header("Settings")

difficulty = st.sidebar.selectbox(
    "Difficulty",
    ["Easy", "Normal", "Hard"],
    index=1,
)

attempt_limit_map = {
    "Easy": 6,
    "Normal": 8,
    "Hard": 5,
}
attempt_limit = attempt_limit_map[difficulty]

low, high = get_range_for_difficulty(difficulty)

st.sidebar.caption(f"Range: {low} to {high}")
st.sidebar.caption(f"Attempts allowed: {attempt_limit}")

if (
    "secret" not in st.session_state
    or st.session_state.get("game_difficulty") != difficulty
    or not low <= st.session_state.secret <= high
):
    reset_game(difficulty)

if "attempts" not in st.session_state:
    st.session_state.attempts = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "status" not in st.session_state:
    st.session_state.status = "playing"

if "history" not in st.session_state:
    st.session_state.history = []

st.subheader("Make a guess")

attempts_banner = st.empty()
attempts_banner.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {attempt_limit - st.session_state.attempts}"
)

raw_guess = st.text_input(
    "Enter your guess:",
    key=f"guess_input_{difficulty}"
)

col1, col2, col3 = st.columns(3)
with col1:
    submit = st.button(
        "Submit Guess 🚀",
        disabled=st.session_state.status != "playing",
    )
with col2:
    st.button("New Game 🔁", on_click=reset_game, args=(difficulty,))
with col3:
    show_hint = st.checkbox("Show hint", value=True)

if submit and st.session_state.status == "playing":
    ok, guess_int, err = parse_guess(raw_guess)

    if not ok:
        st.session_state.history.append(raw_guess)
        st.error(err)
    elif not low <= guess_int <= high:
        st.error(f"Enter a number between {low} and {high}.")
    else:
        st.session_state.attempts += 1
        st.session_state.history.append(guess_int)

        outcome = check_guess(guess_int, st.session_state.secret)
        if show_hint:
            render_hint(outcome)

        st.session_state.score = update_score(
            current_score=st.session_state.score,
            outcome=outcome,
            attempt_number=st.session_state.attempts,
        )

        if outcome == "Win":
            st.balloons()
            st.session_state.status = "won"
        else:
            if st.session_state.attempts >= attempt_limit:
                st.session_state.status = "lost"

if st.session_state.status == "won":
    st.success(
        f"🏆 You won! The secret was {st.session_state.secret}. "
        f"Final score: {st.session_state.score}"
    )
elif st.session_state.status == "lost":
    st.error(
        f"Out of attempts! The secret was {st.session_state.secret}. "
        f"Score: {st.session_state.score}"
    )
if st.session_state.status != "playing":
    st.caption("Click New Game to start another round.")

attempts_banner.info(
    f"Guess a number between {low} and {high}. "
    f"Attempts left: {max(0, attempt_limit - st.session_state.attempts)}"
)

st.divider()
render_round_summary(attempt_limit, show_hint)
