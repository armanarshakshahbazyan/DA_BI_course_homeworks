def calcullate_savings(monthly_income,monthly_expenses):
    savings = monthly_income - monthly_expenses
    if savings > 0.20 * monthly_income:             
        print("You are saving enough!")
        return savings
    else:
        print("You need to save more.")
        return savings

# Subtask 2

if __name__ == "__main__":
    monthly_income = int(input("Enter monthly income: "))
    monthly_expenses = int(input("Enter monthly expenses: "))
    savings=calcullate_savings(monthly_income,monthly_expenses,)


