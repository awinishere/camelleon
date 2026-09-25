from pydantic import BaseModel, EmailStr

class VerificationEmailRequest(BaseModel):
    email: EmailStr
    code_otp: str

class VerificationEmailResponse(BaseModel):
    message: str