
def calculate_balances(expenses):
    balances = {}

    for expense in expenses:
        payer = expense.payer_id

        if payer not in balances:
            balances[payer] = 0

        balances[payer] += expense.amount

    return balances