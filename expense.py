from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from datetime import datetime
from ..database import Base


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True)
    description = Column(String, nullable=False)

    amount = Column(Integer, nullable=False)

    payer_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"))

    split_type = Column(String, nullable=False)
    currency = Column(String, default="INR")

    created_at = Column(DateTime, default=datetime.utcnow)