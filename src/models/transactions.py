from sqlalchemy import Column, Integer, String

from database import Base


class Transactions(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    date = Column(String)
    account = Column(String)
    category = Column(String)
    amount = Column(Integer)
    currency = Column(String)
