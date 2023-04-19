from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID

from database import Base
import uuid


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(
        UUID(as_uuid=True),
        # String,
        primary_key=True,
        index=True,
        default=uuid.uuid4,
        unique=True,
    )
    description = Column(String)
    date = Column(String)
    account = Column(String)
    category = Column(String)
    amount = Column(Integer)
    currency = Column(String)
