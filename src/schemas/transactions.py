import uuid
from pydantic import BaseModel, Field


class TransactionBase(BaseModel):
    description: str
    date: str
    account: str
    category: str
    amount: int
    currency: str


class TransactionCreate(TransactionBase):
    pass


class Transactions(TransactionBase):
    id: uuid.UUID = Field(..., alias="id")

    class Config:
        orm_mode = True
