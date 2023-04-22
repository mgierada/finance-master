from fastapi import FastAPI
from controllers import (
    db_controller,
    tax_controller,
    transactions_controller,
    summary_controller,
)
from models.transactions import Transaction
from database import engine

Transaction.metadata.create_all(bind=engine)

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
app.include_router(
    db_controller.router,
    prefix="/db",
    tags=["db"],
)
app.include_router(
    tax_controller.router,
    prefix="/tax",
    tags=["tax"],
)
