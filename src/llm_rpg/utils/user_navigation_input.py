class UserNavigationInput:
    def __init__(self, choice: int, is_valid: bool):
        self.choice = choice
        self.is_valid = is_valid


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
