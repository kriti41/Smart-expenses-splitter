from sqlalchemy import Column, String
from app.database import Base
from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import relationship
class User(Base):

    __tablename__ = "users"

    id = Column(String, primary_key=True)

    name = Column(String)

    email = Column(String, unique=True)
    
class Expense(Base):

    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)

    description = Column(String)

    amount_paise = Column(Integer)

    payer_id = Column(String)

    group_id = Column(String)

    shares = relationship(
        "ExpenseShare",
        back_populates="expense"
    )
class ExpenseShare(Base):

    __tablename__ = "expense_shares"

    id = Column(Integer, primary_key=True)

    expense_id = Column(
        Integer,
        ForeignKey("expenses.id")
    )

    user_id = Column(String)

    owed_paise = Column(Integer)

    expense = relationship(
        "Expense",
        back_populates="shares"
    )