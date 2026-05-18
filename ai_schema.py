from pydantic import BaseModel
from typing import List


class AIExpenseSchema(BaseModel):

    description: str

    amount: int

    payer: str

    participants: List[str]