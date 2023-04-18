from pydantic import BaseModel


class TransactionBase(BaseModel):
    description: str
    date: str
    account: str
    category: str
    amount: int
    currency: str


class Transactions(TransactionBase):
    id: int

    class Config:
        orm_mode = True
