from dataclasses import dataclass


@dataclass
class UserNavigationInput:
    choice: int
    is_valid: bool


def get_user_navigation_input(valid_choices: list[int]) -> UserNavigationInput:
    try:
        user_input = input().strip()
        choice = int(user_input)
        if choice in valid_choices:
            return UserNavigationInput(choice, True)
        else:
            return UserNavigationInput(choice, False)
    except ValueError:
        return UserNavigationInput(-1, False)
