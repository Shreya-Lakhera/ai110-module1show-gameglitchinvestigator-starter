def get_range_for_difficulty(difficulty: str):
    """Describe the inclusive bounds for a difficulty (not implemented).

    Args:
        difficulty (str): Difficulty label: Easy, Normal, or Hard.

    Returns:
        tuple[int, int]: Intended lower and upper bounds, inclusive.

    Raises:
        NotImplementedError: Always; this helper is still a placeholder.
    """
    raise NotImplementedError(
        "Refactor this function from app.py into logic_utils.py"
    )


def parse_guess(raw: str):
    """Describe parsing a guess into an integer (not implemented).

    Args:
        raw (str): User-entered guess text.

    Returns:
        tuple[bool, int | None, str | None]: Intended success flag, parsed
        guess, and error message. A successful parse has no error message;
        a failed parse has no integer value.

    Raises:
        NotImplementedError: Always; this helper is still a placeholder.
    """
    raise NotImplementedError(
        "Refactor this function from app.py into logic_utils.py"
    )


def check_guess(guess, secret):
    """Compare a numeric guess with the secret and return its outcome.

    Args:
        guess (int): Player's numeric guess.
        secret (int): Target number for the current round.

    Returns:
        str: "Win" for equality, "Too High" when the guess exceeds the
        secret, or "Too Low" when the guess is below the secret.

    Raises:
        TypeError: If the values cannot be ordered against each other.

    Note:
        Inputs must already be numeric; this function does not parse text
        or validate the selected difficulty's range.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int):
    """Describe updating a round's score (not implemented).

    Args:
        current_score (int): Score before processing the guess.
        outcome (str): Guess result: Win, Too High, or Too Low.
        attempt_number (int): One-based number of the submitted attempt.

    Returns:
        int: Intended score after applying the scoring rules.

    Raises:
        NotImplementedError: Always; this helper is still a placeholder.
    """
    raise NotImplementedError(
        "Refactor this function from app.py into logic_utils.py"
    )
