from enum import Enum


class TypePurpose(str, Enum):
    Email_Verification = "email_verification"
    Password_Reset = "password_reset"