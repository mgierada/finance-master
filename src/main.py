from fastapi import FastAPI

from src.controllers import summary_controller

app = FastAPI()

app.include_router(summary_controller.router, prefix="/summary", tags=["summary"])
