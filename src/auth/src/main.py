from fastapi import FastAPI

from src.routes import auth_router

api_version="v1"
app=FastAPI(
    title="Video Convertor Auth API",
    description="Auth services for Video Convertor",
    version=api_version
)

app.include_router(prefix=f"/api/{api_version}", router=auth_router)