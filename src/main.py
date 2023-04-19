from fastapi import FastAPI
from controllers import transactions_controller, summary_controller
from models.transactions import Transaction

from database import engine, SessionLocal

Transaction.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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
