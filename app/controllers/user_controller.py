from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException
from app.models.user import Usuario
from app.utils.hash import hash_password, verify_password
from app.core.security import create_access_token
from app.schemas.user import UserRegister, UserLogin


async def register_user(data: UserRegister, db: AsyncSession):
    stmt = select(Usuario).where(Usuario.correo == data.correo)
    result = await db.execute(stmt)
    if result.scalar():
        raise HTTPException(status_code=400, detail="Correo ya registrado")

    new_user = Usuario(
        correo=data.correo,
        nombre=data.nombre,
        contrasena=hash_password(data.contrasena),
    )
    db.add(new_user)
    await db.commit()
    return {"message": "Usuario registrado correctamente"}


async def login_user(data: UserLogin, db: AsyncSession):
    stmt = select(Usuario).where(Usuario.correo == data.correo)
    result = await db.execute(stmt)
    user = result.scalar()

    if not user or not verify_password(data.contrasena, str(user.contrasena)):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    token = create_access_token({"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
