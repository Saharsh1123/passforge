import sys
from typing import Tuple
from generator import generate_password
from ui import get_length, get_case, use_digits, pause_action, use_symbols, error_msg


def generator_params() -> Tuple[int, bool, bool, bool, bool]:
    """
    Prompt user for all parameters required to generate a password.

    Returns:
        Tuple containing password length, use_uppercase, use_lowercase,
        use_digits, and use_symbols flags.
    """
    # Ask user for password length and character set preferences
    length = get_length()
    upper, lower = get_case()
    digits = use_digits()
    symbols = use_symbols()
    return (length, upper, lower, digits, symbols)


def bye() -> None:
    """
    Display farewell message, pause briefly, then exit program gracefully.
    """
    pause_action(2, True, False)
    print("Thank for using passforge! See you later!")
    sys.exit(0)


# Map commands to their handling functions and parameter-gathering functions
command_map = {
    "generate": (generate_password, generator_params),
    "quit": (bye, lambda: ()),
}


def menu() -> None:
    """
    Main interactive loop prompting user for commands.

    Matches user input against valid commands,
    calls appropriate functions with gathered parameters,
    handles invalid input with error messages and pauses.
    """
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
        # Prompt user for their action choice
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
        for action, options in valid.items():
            # Check if input matches any valid command alias
            if actions in options:
                func, param_func = command_map[action]  # Get associated functions
                params = param_func()  # Gather parameters if any
                output = func(*params)  # Execute action
                if output is not None:
                    print(output)  # Show output if returned
                pause_action(2, True, True)  # Pause and clear screen
                found = True
                break

        if not found:
            # Handle invalid input
            error_msg("Please enter one of the listed actions only!")
            pause_action(0.5, True, True)


if __name__ == "__main__":
    print("Welcome to Passforge\n")
    input("Press any key to continue! ")
    pause_action(1.5, True, False)
    menu()

