import os
import platform
import sys
import time
from typing import Tuple
from rich.console import Console

console = Console()


def cont() -> None:
    input("Press any key to continue! ")


def error_msg(message: str) -> None:
    console.print(f"[bold red]{message}[/bold red]")


def caution_msg(message: str) -> None:
    console.print(f"[yellow]{message}[/yellow]")


def success_msg(message: str) -> None:
    console.print(f"[bold green]{message}[/bold green]")


def pause_action(
    wait: float = 1.5, do_clear: bool = True, do_pause: bool = False
) -> None:
    """
    Handles user pause and screen clear logic.

    Args:
        wait (float): Seconds to wait before clearing (default: 1.5)
        do_clear (bool): Whether to clear the screen after waiting
        do_pause (bool): Whether to prompt 'Press any key to continue'
    """
    if do_pause:
        cont()
    time.sleep(wait)
    if do_clear:
        try:
            os.system("cls" if platform.system() == "Windows" else "clear")
        except Exception:
            pass
        if sys.stdout.isatty():
            print("\033[H\033[J", end="")


YES = {"yes", "ye", "y", "", "yeah", "yea"}
NO = {"no", "n", "nah"}


def get_length() -> int:
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
        elif length <= 10:
            while True:
                caution_msg(
                    "CAUTION: Passwords with a length of 10 and under are not recommended!"
                )
                length_warning = input("Are you sure you want to continue? ")
                if length_warning in YES:
                    success_msg("Updating choice...\nSuccessfully updated!")
                    pause_action(1.5, True, False)
                    return length
                elif length_warning in NO:
                    pause_action(1.5, True, False)
                    break
                else:
                    caution_msg(
                        "Please enter either 'yes' or 'no'. Check your spelling!"
                    )
                    pause_action(2, True, True)
                    continue
            continue
        else:
            success_msg("Updating choice...\nSuccessfully updated!")
            pause_action(1.8, True, False)
            return length


def get_yes_no(prompt: str) -> bool:
    while True:
        response = input(prompt).lower().strip()
        if response in YES:
            success_msg("Updating choice...\nSuccessfully updated!")
            pause_action(2, True, False)
            return True
        elif response in NO:
            success_msg("Updating choice...\nSuccessfully updated!")
            pause_action(2, True, False)
            return False
        else:
            error_msg("Please enter one of the following(y/n)!")
            pause_action(2, True, True)
            continue


def use_letters() -> bool:
    pause_action(1.6, True, False)
    return get_yes_no("Do you want to use letters in your password? ")


def get_case() -> Tuple[bool, bool]:
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
                success_msg("Updating choice...\nSuccessfully updated!")
                pause_action(2.2, True, False)
                if case in case_valid[0]:
                    return True, False
                elif case in case_valid[1]:
                    return False, True
                elif case in case_valid[2]:
                    return True, True
            else:
                error_msg(
                    "Please enter one of the options(upper, lower, both)!"
                )
                pause_action(2.3, True, True)
                continue
    else:
        return False, False


def use_digits() -> bool:
    pause_action(1.6, True, False)
    return get_yes_no("Do you want to use digits in your password? ")


def use_symbols() -> bool:
    pause_action(1.6, True, False)
    return get_yes_no("Do you want to use symbols in your password? ")
