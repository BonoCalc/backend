from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.session import get_db
from app.schemas.user import UserRegister, UserLogin, TokenResponse
from app.controllers.user_controller import register_user, login_user
from app.core.security import get_current_user
from app.schemas.user import UserResponse
from app.models.user import Usuario


router = APIRouter()


@router.post("/register", status_code=201)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    return await register_user(data, db)


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    return await login_user(data, db)


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user
