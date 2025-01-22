from fastapi import FastAPI
from src.secret import Config
from utils.exception import register_exception_handlers
from src.routers import health_check
from src.routers.automation import auto_cluster
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware


config = Config()


app = FastAPI(
    root_path="/api/v1",
    title="DFactory Custom Blender Add-Ons Backend Application",
    description="Backend application for DFactory Custom Blender.",
    version="1.0.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app=app)
app.add_middleware(SessionMiddleware, secret_key=config.MIDDLEWARE_SECRET_KEY)
app.include_router(health_check.router)
app.include_router(auto_cluster.router)
