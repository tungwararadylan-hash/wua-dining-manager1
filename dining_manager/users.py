class User:
    meal_limit = 0
    role = "User"

    def __init__(self, user_id):
        self.user_id = user_id


class Student(User):
    meal_limit = 2
    role = "Student"


class Staff(User):
    meal_limit = 1
    role = "Staff"


class KitchenAdmin(User):
    meal_limit = 0
    role = "Admin"


class UserFactory:
    """Factory: creates the right user type from a role string."""
    _types = {"student": Student, "staff": Staff, "admin": KitchenAdmin}

    @staticmethod
    def create(role, user_id):
        try:
            return UserFactory._types[role.lower()](user_id)
        except KeyError:
            raise ValueError(f"Unknown role: {role}")
