class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def deposit(self, amount, description=""):
        self.ledger.append({"amount": amount, "description": description})

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            self.ledger.append({"amount": -amount, "description": description})
            return True
        return False

    def get_balance(self):
        return sum(item["amount"] for item in self.ledger)

    def transfer(self, amount, category):
        if self.check_funds(amount):
            self.withdraw(amount, f"Transfer to {category.name}")
            category.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        return self.get_balance() >= amount

    def __str__(self):
        title = f"{self.name:*^30}\n"
        items = []
        for item in self.ledger:
            desc = item["description"][:23].ljust(23)
            amount = f"{item['amount']:.2f}".rjust(7)
            items.append(f"{desc}{amount}")
        total = f"Total: {self.get_balance():.2f}"
        return title + "\n".join(items) + "\n" + total


def create_spend_chart(categories):
    # Calculate total withdrawals for each category
    withdrawals = []
    for category in categories:
        total = 0
        for item in category.ledger:
            if item["amount"] < 0:
                total += abs(item["amount"])
        withdrawals.append(total)
    
    total_withdrawals = sum(withdrawals)
    
    # Calculate percentages (rounded down to nearest 10)
    percentages = []
    for amount in withdrawals:
        if total_withdrawals == 0:
            percentages.append(0)
        else:
            percent = (amount / total_withdrawals) * 100
            percentages.append(int(percent // 10 * 10))
    
    # Build the chart lines
    chart = ["Percentage spent by category"]
    for level in range(100, -10, -10):
        line = f"{level:3}| "
        for percent in percentages:
            line += "o  " if percent >= level else "   "
        chart.append(line)
    
    # Add horizontal line
    max_len = len(categories) * 3 + 1
    horizontal_line = "    " + "-" * max_len
    chart.append(horizontal_line)
    
    # Determine the maximum name length
    max_name_length = max(len(category.name) for category in categories)
    
    # Build category names lines
    for i in range(max_name_length):
        line = "     "
        for category in categories:
            if i < len(category.name):
                line += category.name[i] + "  "
            else:
                line += "   "
        chart.append(line)
    
    return "\n".join(chart)
