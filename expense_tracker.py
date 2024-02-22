from expense import Expense
import calendar
import datetime

def main():
    # Get user to input their expense.
    expense_file_path = input('What would you like to call your csv file? ')
    expense_file_path = expense_file_path + '.csv'
    budget = float(input("Enter your monthly budget: "))
    flag = True


    while flag:
        expense = get_expense()

        # Write their expense to a file.
        save_expense_to_file(expense, expense_file_path)


        # Read the file and summarize expense.
        summarize_expense(expense_file_path, budget)

        inputText = input('Do you have more expenses? (Y/N) ')

        flag = (inputText == 'Y' or inputText == 'y')

    print("Your csv has been made: ", expense_file_path)


def green(text):
    return f"\033[92m{text}\033[0m"
    

def red(text):
    return f"\033[91m{text}\033[0m"


def get_expense():
    expense_name = input("Enter expense name: ")

    expense_amount = None

    while not expense_amount or not expense_amount.isdigit():
        expense_amount = input("Enter a valid expense amount: ")

    expense_categories = [
        "Food 🌭",
        "Home 🏡",
        "Work 💼",
        "Fun 🥳",
        "Miscellaneous❓"
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f" {i + 1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"
        selected_index = int(input(f"Enter a category number {value_range}: ")) - 1

        if selected_index in range(len(expense_categories)):
            selected_category = expense_categories[selected_index]
            new_expense = Expense(name=expense_name, category=selected_category, amount=expense_amount)
            return new_expense
        else:
            print("Invalid category, please try again")


def save_expense_to_file(expense, expense_file_path):
    print(f"Saving User expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expense(expense_file_path, budget):
    expenses = []
    with open(expense_file_path, "r") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expenses = Expense(name = expense_name, amount= float(expense_amount), category= expense_category)
            expenses.append(line_expenses)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount 
        else:
            amount_by_category[key] = expense.amount 
    
    print("Expenses by category:")
    for key, amount in amount_by_category.items():
        print(f"  {key}: ${amount:.2f}")
    
    total_spent = sum([x.amount for x in expenses])
    print(f"Total Spent: ${total_spent:.2f}")
    remaining_budget = budget - total_spent
    if remaining_budget < 0:
        print(red(f"You have over spent by ${abs(remaining_budget):.2f} this month"))
    else: 
        now = datetime.datetime.now()
        days_in_month = calendar.monthrange(now.year, now.month)[1]
        remaning_days = days_in_month - now.day
        daily_budget = remaining_budget / remaning_days
        print(f"Budget Remaining: {remaining_budget:.2f}")
        print(green(f"Budget Per Day: ${daily_budget:.2f}"))



if __name__ == "__main__":
    main()

