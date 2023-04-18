from pydantic import BaseModel


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
    id: int

    class Config:
        orm_mode = True
