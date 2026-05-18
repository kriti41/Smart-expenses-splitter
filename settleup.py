def minimize_transactions(balances):

    debtors = []
    creditors = []

    for user, amount in balances.items():

        if amount < 0:
            debtors.append([user, -amount])

        elif amount > 0:
            creditors.append([user, amount])

    settlements = []

    i = 0
    j = 0

    while i < len(debtors) and j < len(creditors):

        debtor, debt_amount = debtors[i]

        creditor, credit_amount = creditors[j]

        settled_amount = min(
            debt_amount,
            credit_amount
        )

        settlements.append({
            "from": debtor,
            "to": creditor,
            "amount": settled_amount
        })

        debtors[i][1] -= settled_amount
        creditors[j][1] -= settled_amount

        if debtors[i][1] == 0:
            i += 1

        if creditors[j][1] == 0:
            j += 1

    return settlements


balances = {
    "aman": -500,
    "priya": 300,
    "rahul": 200
}

result = minimize_transactions(balances)

print(result)