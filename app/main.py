from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.metricas import router as metricas_router

app = FastAPI(title="API Métricas de Influencers")

origins = [
    "*"
    #"http://localhost:3000", # El frontend que intenta acceder a la API
    #"http://127.0.0.1:3000",
    # Puedes añadir la URL de producción aquí cuando la tengas
    # "https://tu-dominio-frontend.com", 
]

# 3. Aplicar el middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # Lista de orígenes permitidos (frontend)
    allow_credentials=True, # Permitir cookies (si usas autenticación)
    allow_methods=["*"], # Permitir todos los métodos (GET, POST, PUT, DELETE)
    allow_headers=["*"], # Permitir todos los encabezados, incluyendo Content-Type
)

app.include_router(metricas_router, prefix="/metricas")
