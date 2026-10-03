from pathlib import Path

from streamlit.testing.v1 import AppTest


APP = str(Path(__file__).resolve().parents[1] / "app.py")


def test_difficulty_change_starts_round_in_displayed_range():
    app = AppTest.from_file(APP).run()
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
    app = AppTest.from_file(APP).run()
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
    app = AppTest.from_file(APP).run()
    app.session_state.secret = 50
    for remaining in (7, 6):
        app.text_input[0].set_value("9")
        app.button[0].click().run()
        assert not app.exception
        assert "Go HIGHER!" in app.warning[0].value
        assert f"Attempts left: {remaining}" in app.info[0].value


def test_invalid_guesses_do_not_use_attempts():
    app = AppTest.from_file(APP).run()
    for guess in ("abc", "101", "-1"):
        app.text_input[0].set_value(guess)
        app.button[0].click().run()
        assert not app.exception
        assert app.error
        assert app.session_state.attempts == 0
        assert "Attempts left: 8" in app.info[0].value
