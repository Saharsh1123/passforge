import secrets
import string
import random
from typing import Tuple

from ui import error_msg


def generate_pools(
    use_upper: bool, use_lower: bool, use_digits: bool, use_symbols: bool
) -> Tuple:
    """
    Build the active character pools based on the user's selections.

    The function collects each enabled character category (uppercase, lowercase,
    digits, symbols) into a tuple of pools and counts how many were chosen.

    Args:
        use_upper: Include uppercase letters.
        use_lower: Include lowercase letters.
        use_digits: Include digits.
        use_symbols: Include ASCII punctuation (minus a small blacklist).

    Returns:
        (tuple_of_pools, count_enabled):
            tuple_of_pools — a tuple where each element is a string of valid characters.
            count_enabled — how many categories were selected.

        If no categories were selected, returns (empty_tuple, 0) and emits an error.
    """
    pools = []
    num_true = 0

    # Handle letter pools first (uppercase, lowercase, or both).
    if use_upper or use_lower:
        if use_upper and use_lower:
            letter_pool = string.ascii_letters
        elif use_lower:
            letter_pool = string.ascii_lowercase
        else:  # use_upper only
            letter_pool = string.ascii_uppercase

        pools.append(letter_pool)
        num_true += 1

    # Digits (0–9).
    if use_digits:
        pools.append(string.digits)
        num_true += 1

    # Symbols (punctuation with unsafe characters removed).
    if use_symbols:
        remove = {'"', "'", "(", ")", "+", ",", "[", "]", "{", "}"}
        symbols_pool = "".join(c for c in string.punctuation if c not in remove)
        pools.append(symbols_pool)
        num_true += 1

    # No category selected → cannot generate a password.
    if num_true == 0:
        error_msg("You didn't select any character categories!")
        return (), 0

    return tuple(pools), num_true


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    """
    Generate a randomized password from the enabled character pools.

    The algorithm:
    1. Builds active character pools.
    2. Divides the requested length evenly across enabled pools.
    3. Distributes leftover characters randomly.
    4. Fills the password list using cryptographically secure randomness.
    5. Shuffles to remove patterns, then returns a formatted string.

    Args:
        length: Desired password length.
        use_upper: Whether uppercase letters are allowed.
        use_lower: Whether lowercase letters are allowed.
        use_digits: Whether digits are allowed.
        use_symbols: Whether symbols are allowed.

    Returns:
        A string containing the fully randomized password, or a failure message
        if no character categories were selected.
    """
    passwd = []

    # Build pools and validate category selection.
    active_pools, num_true = generate_pools(
        use_upper, use_lower, use_digits, use_symbols
    )
    if num_true == 0:
        return "Password generation failed — no character types selected."

    # Base count ensures every enabled category gets at least a fair share.
    base = length // num_true
    leftover = length - (base * num_true)

    # Fill characters from each pool, distributing leftovers randomly.
    for pool in active_pools:
        extra = random.randint(0, leftover) if leftover > 0 else 0
        n_chars = base + extra
        leftover -= extra

        for _ in range(n_chars):
            passwd.append(secrets.choice(pool))

    # If rounding leaves the list short, fill arbitrarily.
    while len(passwd) < length:
        pool = random.choice(active_pools)
        passwd.append(secrets.choice(pool))

    # Shuffle to avoid predictable ordering (e.g., letters → digits → symbols).
    random.shuffle(passwd)

    return f"Your password: {''.join(passwd)}"

