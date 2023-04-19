import uuid
from pydantic import BaseModel


class TransactionBase(BaseModel):
    uuid: uuid.UUID
    description: str
    date: str
    account: str
    category: str
    amount: int
    currency: str


class TransactionCreate(TransactionBase):
    pass


class Transactions(TransactionBase):
    # uuid: uuid.UUID
    pass

    class Config:
        orm_mode = True
