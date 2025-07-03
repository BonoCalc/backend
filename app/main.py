from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.user_routes import router as user_router
from app.routes.bono_routes import router as bono_router
from app.routes.flujo_routes import router as flujo_router
from app.routes.valoracion_routes import router as valoracion_router
from app.routes.configuracion_routes import router as configuracion_router

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:4200",  
    "https://tu-frontend.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,           
    allow_credentials=True,           
    allow_methods=["*"],             
    allow_headers=["*"],              
)

app.include_router(user_router, prefix="/auth", tags=["Auth"])
app.include_router(bono_router, prefix="/bonos", tags=["Bonos"])
app.include_router(flujo_router, prefix="/flujo", tags=["flujo"])
app.include_router(valoracion_router, prefix="/valoraciones", tags=["valoraciones"])
app.include_router(configuracion_router, prefix="/configuracion", tags=["Configuración"])
