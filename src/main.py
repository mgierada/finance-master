from fastapi import FastAPI
from controllers import transactions_controller, summary_controller

app = FastAPI()

app.include_router(
    summary_controller.router,
    prefix="/summary",
    tags=["summary"],
)
app.include_router(
    transactions_controller.router,
    prefix="/transactions",
    tags=["transactions"],
)
