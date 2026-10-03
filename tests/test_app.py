from pathlib import Path

import pytest
from streamlit.testing.v1 import AppTest


APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_difficulty_change_starts_round_in_displayed_range():
    app = AppTest.from_file(APP, default_timeout=10).run()
    app.session_state.secret = 72
    app.session_state.attempts = 4
    app.session_state.status = "lost"
    app.sidebar.selectbox[0].select("Hard").run()
    assert not app.exception
    assert 1 <= app.session_state.secret <= 50
    assert app.session_state.status == "playing"
    assert app.session_state.attempts == 0
    assert "Attempts left: 5" in app.info[0].value


def test_last_attempt_updates_banner_and_new_game_is_playable():
    app = AppTest.from_file(APP, default_timeout=10).run()
    app.sidebar.selectbox[0].select("Hard").run()
    app.session_state.secret = 50
    for remaining in range(4, -1, -1):
        app.text_input[0].set_value("45")
        app.button[0].click().run()
        assert not app.exception
        assert f"Attempts left: {remaining}" in app.info[0].value
    assert app.session_state.status == "lost"
    assert "secret was 50" in app.error[0].value
    app.button[1].click().run()
    assert app.session_state.status == "playing"
    assert app.session_state.attempts == 0
    assert app.session_state.score == 0
    assert app.session_state.history == []
    assert app.text_input[0].value == ""
    app.text_input[0].set_value(str(app.session_state.secret))
    app.button[0].click().run()
    assert app.session_state.status == "won"
    app.button[1].click().run()
    assert not app.exception
    assert app.session_state.status == "playing"


def test_even_attempt_uses_numeric_comparison():
    app = AppTest.from_file(APP, default_timeout=10).run()
    app.session_state.secret = 50
    for remaining in (7, 6):
        app.text_input[0].set_value("9")
        app.button[0].click().run()
        assert not app.exception
        assert "Go HIGHER!" in app.info[1].value
        assert f"Attempts left: {remaining}" in app.info[0].value


def test_invalid_guesses_do_not_use_attempts():
    app = AppTest.from_file(APP, default_timeout=10).run()
    for guess in ("abc", "101", "-1"):
        app.text_input[0].set_value(guess)
        app.button[0].click().run()
        assert not app.exception
        assert app.error
        assert app.session_state.attempts == 0
        assert "Attempts left: 8" in app.info[0].value


@pytest.mark.parametrize(
    "raw_guess, expected_error",
    [
        pytest.param("", "Enter a guess.", id="empty-input"),
        pytest.param("abc", "That is not a number.", id="non-numeric"),
        pytest.param(
            "-1", "Enter a number between 1 and 50.", id="negative-number"
        ),
        pytest.param(
            "51", "Enter a number between 1 and 50.", id="above-hard-range"
        ),
    ],
)
def test_invalid_input_preserves_last_attempt(raw_guess, expected_error):
    """Rejected input must not exhaust a round or prevent a final win."""
    app = AppTest.from_file(APP, default_timeout=10).run()
    app.sidebar.selectbox[0].select("Hard").run()
    app.session_state.secret = 50
    for _ in range(4):
        app.text_input[0].set_value("40")
        app.button[0].click().run()
    score_before = app.session_state.score
    history_before = app.main.table[0].value.copy()

    # Repeated bad submissions must leave the last valid attempt available.
    for _ in range(2):
        app.text_input[0].set_value(raw_guess)
        app.button[0].click().run()
        assert not app.exception
        assert app.error[0].value == expected_error
        assert app.session_state.attempts == 4
        assert app.session_state.score == score_before
        assert app.session_state.secret == 50
        assert app.session_state.status == "playing"
        assert app.session_state.high_scores == {}
        assert app.main.table[0].value.equals(history_before)
        assert "Attempts left: 1" in app.info[0].value

    # The upper boundary is valid, and a win on the last attempt counts.
    app.text_input[0].set_value("50")
    app.button[0].click().run()
    assert not app.exception
    assert not app.error
    assert app.session_state.status == "won"
    assert app.session_state.attempts == 5
    assert "Attempts left: 0" in app.info[0].value
    assert len(app.main.table[0].value) == 5
    assert app.session_state.high_scores["Hard"] == app.session_state.score


def test_summary_tracks_guesses_and_respects_hidden_hints():
    app = AppTest.from_file(APP, default_timeout=10).run()
    app.session_state.secret = 50
    assert not app.main.table
    for guess in (60, 40):
        app.text_input[0].set_value(str(guess))
        app.button[0].click().run()
        assert not app.exception
    rows = app.main.table[0].value
    assert rows["Guess"].tolist() == [60, 40]
    assert "Too high" in rows["Result"].iloc[0]
    assert "Too low" in rows["Result"].iloc[1]
    assert app.main.metric[0].value == "2"
    assert app.main.metric[1].value == "6"
    app.checkbox[0].uncheck().run()
    assert "Result" not in app.main.table[0].value.columns
    app.text_input[0].set_value("50")
    app.button[0].click().run()
    assert app.session_state.status == "won"
    app.run()
    assert not app.exception
    assert app.button[0].disabled
    assert "You won!" in app.success[0].value
    assert len(app.main.table[0].value) == 3
    app.button[1].click().run()
    assert not app.exception
    assert not app.main.table
    assert not app.button[0].disabled
    assert app.main.metric[0].value == "0"


def test_high_scores_keep_best_win_and_survive_round_resets():
    app = AppTest.from_file(APP, default_timeout=10).run()
    assert app.session_state.high_scores == {}
    assert app.sidebar.metric[0].value == "—"
    # A second-attempt win earns 65 with the existing scoring rules.
    app.session_state.secret = 50
    for guess in (40, 50):
        app.text_input[0].set_value(str(guess))
        app.button[0].click().run()
    assert app.session_state.high_scores == {"Normal": 65}
    assert app.sidebar.metric[0].value == "65"
    app.button[1].click().run()
    assert app.session_state.score == 0
    assert app.session_state.high_scores == {"Normal": 65}
    # A better win replaces the record.
    app.text_input[0].set_value(str(app.session_state.secret))
    app.button[0].click().run()
    assert app.session_state.high_scores == {"Normal": 80}
    # A lower win cannot reduce the record.
    app.button[1].click().run()
    app.session_state.secret = 50
    for guess in (40, 50):
        app.text_input[0].set_value(str(guess))
        app.button[0].click().run()
    assert app.session_state.high_scores == {"Normal": 80}
    app.sidebar.selectbox[0].select("Hard").run()
    assert app.sidebar.metric[0].value == "—"
    app.text_input[0].set_value(str(app.session_state.secret))
    app.button[0].click().run()
    assert app.session_state.high_scores == {"Normal": 80, "Hard": 80}
    app.sidebar.selectbox[0].select("Normal").run()
    assert app.sidebar.metric[0].value == "80"
    app.run()
    assert not app.exception
    assert app.session_state.high_scores == {"Normal": 80, "Hard": 80}


def test_losses_do_not_record_scores_and_new_sessions_start_empty():
    app = AppTest.from_file(APP, default_timeout=10).run()
    app.sidebar.selectbox[0].select("Hard").run()
    app.session_state.secret = 50
    for _ in range(5):
        app.text_input[0].set_value("40")
        app.button[0].click().run()
    assert not app.exception
    assert app.session_state.status == "lost"
    assert app.session_state.high_scores == {}
    app.button[1].click().run()
    app.text_input[0].set_value(str(app.session_state.secret))
    app.button[0].click().run()
    assert app.session_state.high_scores == {"Hard": 80}
    fresh = AppTest.from_file(APP, default_timeout=10).run()
    assert not fresh.exception
    assert fresh.session_state.high_scores == {}
