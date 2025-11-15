import sys
from typing import Tuple
from generator import generate_password
from ui import get_length, get_case, use_digits, pause_action, use_symbols, error_msg

# Prompt the user to input all parameters required for password generation and return them.
def generator_params() -> Tuple[bool, bool, bool, bool, bool]:
    """
       Collect all password generation parameters from the user.

       Returns:
           Tuple containing (length, use_upper, use_lower, use_digits, use_symbols).
       """
    length = get_length()
    upper, lower = get_case()
    digits = use_digits()
    symbols = use_symbols()
    return (length, upper, lower, digits, symbols)

# Return empty tuple for functions without parameters.
def no_params() -> tuple:
    return ()

# Gracefully exit the program after displaying a farewell message.
def bye() -> None:
    pause_action(2, True, False)
    print("Thank for usingxx passforge! See you later!")
    sys.exit(0)

# Map each function and its parameters to the action it corresponds to.
command_map = {
    "generate": (generate_password, generator_params),
    "quit": (bye, no_params),
}

# Main interactive loop that keeps the program running until the user quits.
def menu() -> None:
    valid = {
        "generate": [
            "gen",
            "generate",
            "create",
            "make",
            "generate password",
            "generate a password",
            "1",
        ],
        "quit": ["quit", "leave", "exit", "bye", "qui", "q", "qu", "2"],
    }

    while True:
        actions = (
            input(
                """
Select an Option:
[1] Generate a password
[2] Quit

"""
            )
            .lower()
            .strip()
        )

        found = False
        for action, option in valid.items():
            if actions in option:
                func, param_func = command_map[action]
                params = param_func()
                output = func(*params)
                if output is not None:
                    print(output)
                pause_action(2, True, True)
                found = True
                break

        if not found:
            error_msg("Please enter one of the listed actions only!")
            pause_action(0.5, True, True)


print("Welcome to Passforge\n")
enter = input("Press any key to continue! ")
pause_action(1.5, True, False)
menu()
