from sqlalchemy import Column, Integer, ForeignKey
from ..database import Base


class ExpenseShare(Base):
    __tablename__ = "expense_shares"

    id = Column(Integer, primary_key=True)

    expense_id = Column(Integer, ForeignKey("expenses.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    share_amount = Column(Integer, nullable=False)