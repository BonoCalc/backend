from pydantic import BaseModel, EmailStr


class UserRegister(BaseModel):
    correo: EmailStr
    nombre: str
    contrasena: str


class UserLogin(BaseModel):
    correo: EmailStr
    contrasena: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
