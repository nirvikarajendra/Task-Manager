from pydantic import BaseModel, EmailStr

class RegisterModel(BaseModel):
    username: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str
    class Config:
        from_attribute = True

class LoginModel(BaseModel):
    email : EmailStr
    password : str

class PasswordModel(BaseModel):
    password : str
    new_password : str