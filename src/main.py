from fastapi import FastAPI
from controllers import (
    category_controller,
    db_controller,
    take_home_pay_controller,
    tax_controller,
    transactions_controller,
    summary_controller,
    ex_ante_controller,
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
app.include_router(
    take_home_pay_controller.router,
    prefix="/take-home-pay",
    tags=["take-home-pay"],
)
app.include_router(
    ex_ante_controller.router,
    prefix="/ex-ante",
    tags=["ex-ante"],
)
app.include_router(
    category_controller.router,
    prefix="/category",
    tags=["catagory"],
)
