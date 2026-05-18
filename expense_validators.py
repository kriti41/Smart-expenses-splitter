from fastapi import HTTPException


def validate_expense(expense):
    total = sum([s.share_amount for s in expense.shares])

    if total != expense.amount:
        raise HTTPException(
            status_code=400,
            detail="Split amounts do not equal total amount"
        )

    if expense.amount <= 0:
        raise HTTPException(
            status_code=400,
            detail="Amount must be positive"
        )