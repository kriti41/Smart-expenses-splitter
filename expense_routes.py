from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from app.schemas.expense_schema import ExpenseCreate
from app.dependencies import get_db
from app.models.models import Expense, ExpenseShare
from app.algorithms.settleup import minimize_transactions 

print("NEW EXPENSE ROUTE LOADED")

router = APIRouter()

@router.post("/")
def create_expense(
    expense: ExpenseCreate,
    db: Session = Depends(get_db)
):
    total = sum(share.owed_paise for share in expense.shares)

    if total != expense.amount_paise:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Split mismatch. Total shares sum to {total}, but amount is {expense.amount_paise}"
        )

    # Save expense
    new_expense = Expense(
        description=expense.description,
        amount_paise=expense.amount_paise,
        payer_id=expense.payer_id,
        group_id=expense.group_id
    )
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    # Save shares
    for share in expense.shares:
        expense_share = ExpenseShare(
            expense_id=new_expense.id,
            user_id=share.user_id,
            owed_paise=share.owed_paise
        )
        db.add(expense_share)
    
    db.commit()

    return {
        "success": True,
        "expense_id": new_expense.id
    }


@router.get("/settlements/{group_id}")
def get_settlements(group_id: str, db: Session = Depends(get_db)):
    # STEP 1: Compute balances
    balances = defaultdict(int)

    # FIXED: Added joinedload(Expense.shares) to fetch shares efficiently in 1 query
    expenses = db.query(Expense).options(
        joinedload(Expense.shares)
    ).filter(
        Expense.group_id == group_id
    ).all()

    for exp in expenses:
        # Payer gets credited the full amount
        balances[exp.payer_id] += exp.amount_paise

        # Each participant gets debited what they owe
        for share in exp.shares:
            balances[share.user_id] -= share.owed_paise

    # STEP 2: Convert defaultdict → standard dict
    balances = dict(balances)

    # STEP 3: Run greedy/network-flow transaction minimization algorithm
    result = minimize_transactions(balances)

    return {
        "group_id": group_id,
        "balances": balances,
        "settlements": result
    }