from pydantic import BaseModel
from typing import List

class ExpenseShare(BaseModel):
    user_id: str
    owed_paise: int

class ExpenseCreate(BaseModel):

    description: str

    amount_paise: int

    payer_id: str

    group_id: str

    shares: List[ExpenseShare]