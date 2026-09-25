from enum import Enum

class Roles(str, Enum):
    User = "user"
    Admin = "admin"