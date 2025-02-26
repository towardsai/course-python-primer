# Personal Budget Tracker

# Friendly greeting
print("Welcome to your Personal Budget Tracker!")

# Prompt the user to enter daily income
daily_income = float(input("Enter your daily income: "))

# Prompt the user to enter daily expenses
daily_expenses = float(input("Enter your daily expenses (excluding rent): "))

# Prompt the user to enter rent expense
rent_expense = float(input("Enter today's rent expense: "))

# Prompt the user to enter an optional note
day_note = input("Enter any note or comment for today (optional): ")

# Prompt the user to enter a future savings goal
goal_amount = float(input("Enter your future savings goal: "))

# Calculate total expenses
total_expenses = daily_expenses + rent_expense

# Calculate net savings
net_savings = daily_income - total_expenses

# Print out the results
print("\n--- Summary of Your Day ---")
print("Total Income for the day: ", daily_income)
print("Total Expenses for the day (including rent): ", total_expenses)
print("Net Savings for the day: ", net_savings)

# Print a final summary
print(f"Today you earned {daily_income}, spent {total_expenses}, and your net savings is {net_savings}.")

# Print the user's note
if day_note.strip():  # Check if the note is not empty
    print("Your note for the day is:", day_note)

# Print the user's savings goal
print("Your future savings goal is:", goal_amount)