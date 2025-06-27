from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.bono_routes import router as bono_router
from app.routes.flujo_routes import router as flujo_router
from app.routes.valoracion_routes import router as valoracion_router

app = FastAPI()

app.include_router(user_router, prefix="/auth", tags=["Auth"])
app.include_router(bono_router, prefix="/bonos", tags=["Bonos"])
app.include_router(flujo_router, prefix="/flujo", tags=["flujo"])
app.include_router(valoracion_router, prefix="/valoraciones", tags=["valoraciones"])
