import secrets
import string
import random
from typing import Tuple

from ui import error_msg


def generate_pools(
    use_upper: bool, use_lower: bool, use_digits: bool, use_symbols: bool
) -> Tuple:
    pools = []
    num_true = 0


    if use_upper or use_lower:
        if use_upper and use_lower:
            letter_pool = string.ascii_letters
        elif use_lower:
            letter_pool = string.ascii_lowercase
        elif use_upper:
            letter_pool = string.ascii_uppercase
        num_true += 1
        pools.append(letter_pool)

    if use_digits:
        digits_pool = string.digits
        num_true += 1
        pools.append(digits_pool)

    if use_symbols:
        symbols_pool = string.punctuation
        num_true += 1
        remove = {'"', "'", "(", ")", "+", ",", "[", "]", "{", "}"}
        symbols_pool = "".join(c for c in string.punctuation if c not in remove)
        pools.append(symbols_pool)

    # If the user didn’t select any character types, show an error message and stop password generation.
    if num_true == 0:
        error_msg(
            "You didn't select any options! Please enter one next time to generate a password!"
        )
        return (), 0

    return tuple(pools), num_true


def generate_password(
    length: int = 16,
    use_upper: bool = True,
    use_lower: bool = True,
    use_digits: bool = True,
    use_symbols: bool = True,
) -> str:
    passwd = []

    active_pools, num_true = generate_pools(
        use_upper, use_lower, use_digits, use_symbols
    )

    if num_true == 0:
        return "Password generation failed — no character types selected."

    base = int(length / num_true)
    leftover = length - (base * num_true)

    for pool in active_pools:
        extra = random.randint(0, leftover) if leftover > 0 else 0
        n_chars = base + extra
        leftover -= extra
        for j in range(n_chars):
            passwd.append(secrets.choice(pool))

    while len(passwd) < length:
        pool = random.choice(active_pools)
        passwd.append(secrets.choice(pool))

    random.shuffle(passwd)
    password = "".join(passwd)
    return f"Your password: {password}"
