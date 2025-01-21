from src.secret import Config
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from src.routers import health_check
from src.routers.automation import auto_organize


config = Config()


app = FastAPI(
    root_path="/api/v1",
    title="Custom Blender Add-Ons Backend Application",
    description="Backend application for Custom Blender.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(SessionMiddleware, secret_key=config.MIDDLEWARE_SECRET_KEY)

app.include_router(health_check.router)
app.include_router(auto_organize.router)
