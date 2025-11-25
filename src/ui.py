import subprocess
import logging
import platform
import time
from typing import Tuple
from rich.console import Console

console = Console()


def cont() -> None:
    """Pause program flow until user presses any key."""
    input("Press any key to continue! ")


def error_msg(message: str) -> None:
    """Display a prominent error message in red."""
    console.print(f"[bold red]{message}[/bold red]")


def caution_msg(message: str) -> None:
    """Show a cautionary message in yellow to alert the user."""
    console.print(f"[yellow]{message}[/yellow]")


def success_msg(message: str) -> None:
    """Display a success confirmation in green."""
    console.print(f"[bold green]{message}[/bold green]")


def pause_action(
    wait: float = 1.5, do_clear: bool = True, do_pause: bool = False
) -> None:
    """
    Pause execution with optional user prompt and screen clearing.

    Args:
        wait (float): Seconds to wait before proceeding.
        do_clear (bool): Clear console screen after wait.
        do_pause (bool): Pause and wait for user keypress before waiting.
    """
    if do_pause:
        cont()
    time.sleep(wait)
    if do_clear:
        cmd = ["cls"] if platform.system() == "Windows" else ["clear"]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            logging.error(f"Command failed with exit code {e.returncode}: {cmd}")
        except Exception as e:
            logging.error(f"Unexpected error running command {cmd}: {e}")


YES = {"yes", "ye", "y", "", "yeah", "yea"}
NO = {"no", "n", "nah"}

success = "Updating choice...\nSuccessfully updated!"


def caution_length(length: int) -> bool:
    """
    Warn user about insecure short password lengths and get confirmation.

    Args:
        length (int): Password length to confirm.

    Returns:
        bool: True if user accepts risk and continues, False if canceled.
    """
    while True:
        caution_msg(
            "CAUTION: Passwords with a length of 10 and under are not recommended!"
        )
        length_warning = input("Are you sure you want to continue? ").strip().lower()

        if length_warning in YES:
            success_msg(success)
            pause_action(1.5, True, False)
            return True

        if length_warning in NO:
            pause_action(1.5, True, False)
            return False

        caution_msg("Please enter either 'yes' or 'no'. Check your spelling!")
        pause_action(2, True, True)


def get_length() -> int:
    """
    Prompt for and validate password length input, including warnings.

    Enforces minimum length, warns on short but allowed lengths.

    Returns:
        int: Validated password length.
    """
    pause_action(2, True, False)

    while True:
        try:
            length = int(input("What length do you want the password to be? "))
        except ValueError:
            error_msg("Please enter an integer!")
            pause_action(2, True, True)
            continue

        if length <= 6:
            error_msg(
                "ERROR: Passwords with a length of 6 and under are not permitted!"
            )
            pause_action(0.5, True, True)
            continue

        if length <= 10:
            if caution_length(length):
                return length
            continue

        # Valid length over 10
        success_msg(success)
        pause_action(1.8, True, False)
        return length


def get_yes_no(prompt: str) -> bool:
    """
    Obtain a validated yes/no response from the user.

    Args:
        prompt (str): Question to present to the user.

    Returns:
        bool: True for affirmative, False for negative.
    """
    while True:
        response = input(prompt).lower().strip()
        if response in YES:
            success_msg(success)
            pause_action(2, True, False)
            return True
        elif response in NO:
            success_msg(success)
            pause_action(2, True, False)
            return False
        else:
            error_msg("Please enter one of the following(y/n)!")
            pause_action(2, True, True)


def use_letters() -> bool:
    """
    Ask if the user wants to include letters in the password.

    Returns:
        bool: True if letters should be included.
    """
    pause_action(1.6, True, False)
    return get_yes_no("Do you want to use letters in your password? ")


def get_case() -> Tuple[bool, bool]:
    """
    Prompt user to specify desired letter casing.

    Returns:
        Tuple[bool, bool]: Flags for use_uppercase, use_lowercase.
    """
    if use_letters():
        while True:
            case_valid = [
                ["upper", "high", "big", "uppercase"],
                ["lower", "low", "small", "lowercase"],
                ["both", "upper and lower", "all cases"],
            ]
            case = (
                input("What case do you want your password to be(upper, lower, both)? ")
                .strip()
                .lower()
            )
            if any(case in sub for sub in case_valid):
                success_msg(success)
                pause_action(2.2, True, False)
                if case in case_valid[0]:
                    return True, False
                elif case in case_valid[1]:
                    return False, True
                elif case in case_valid[2]:
                    return True, True
            else:
                error_msg("Please enter one of the options(upper, lower, both)!")
                pause_action(2.3, True, True)
    else:
        return False, False


def use_digits() -> bool:
    """
    Ask if the user wants to include digits in the password.

    Returns:
        bool: True if digits should be included.
    """
    pause_action(1.6, True, False)
    return get_yes_no("Do you want to use digits in your password? ")


def use_symbols() -> bool:
    """
    Ask if the user wants to include symbols in the password.

    Returns:
        bool: True if symbols should be included.
    """
    pause_action(1.6, True, False)
    return get_yes_no("Do you want to use symbols in your password? ")
