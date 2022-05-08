class Category:

    def __init__(self, name, ledger=[]):
        self.name = name
        self.ledger = []
        self.funds = 0

    def __str__(self):
        name_length = len(self.name)
        start = (30 - name_length) // 2
        stars = ""

        for i in range(start):
            stars = "*" + stars
        result = stars + self.name + stars + "\n"
        for i in range(len(self.ledger)):
            extra_space = ""

            float_modified = float(self.ledger[i]["amount"])
            format_float = "{:.2f}".format(float_modified)

            for j in range(30 - len(format_float) - len(self.ledger[i]["description"][:23])):
                if str(self.ledger[i]["amount"])[0] == "-":
                    j = j + 1
                extra_space = extra_space + " "
            global total
            total = 0
            for item in self.ledger:
                total = total + item["amount"]

            result = result + self.ledger[i]["description"][:23] + extra_space + format_float + "\n"

        result = result + "Total: " + str(total)
        return result

    def deposit(self, amount, description=""):
        deposit_dict = dict()
        deposit_dict["amount"] = amount
        deposit_dict["description"] = description
        self.ledger.append(deposit_dict)
        self.funds = self.funds + amount

    def withdraw(self, amount, description=""):

        if self.check_funds(amount):
            withdraw_dict = dict()
            withdraw_dict["amount"] = 0 - amount
            withdraw_dict["description"] = description
            self.ledger.append(withdraw_dict)
            self.funds = self.funds - amount
            return True
        else:
            return False

    def get_balance(self):
        return self.funds

    def transfer(self, amount, destination):
        if not self.check_funds(amount):
            return False
        self.withdraw(amount, "Transfer to " + destination.name)
        destination.deposit(amount, "Transfer from " + self.name)
        return True

    def check_funds(self, amount):
        if self.funds >= amount:
            return True
        return False


def create_spend_chart(categories):
    # prepare the header
    header = "Percentage spent by category" + "\n"

    # prepare the percentages
    categories_percentage = dict()
    categories_costs = dict()
    total_spent = 0
    for category in categories:
        amount_spent_by_cat = 0
        for transaction in category.ledger:
            if transaction["amount"] < 0:
                amount_spent_by_cat = amount_spent_by_cat + transaction["amount"]

            categories_costs[category.name] = round(amount_spent_by_cat, 2)
            total_spent = total_spent + round(amount_spent_by_cat, 2)

    for k, v in categories_costs.items():
        categories_percentage[k] = (((v / total_spent) * 10) // 1) * 10

    # prepare the footer
    footer = "    "
    for i in range(len(categories_percentage) * 3 + 1):
        footer = footer + "-"
    footer = footer + "\n"

    footer = footer + "     "
    longest_string = 0
    for k in categories_percentage:
        if len(k) > longest_string:
            longest_string = len(k)

    for i in range(longest_string):

        for k in categories_percentage:

            if len(k) <= i:
                footer = footer + "   "
                continue
            footer = footer + k[i] + "  "
        if i == longest_string - 1:
            break
        footer = footer + "\n"
        footer = footer + "     "

    # prepare the body

    body = ""
    per = 100
    for i in range(11):
        space = ""

        if 100 > per > 0:
            space = space + " "
        elif per == 0:
            space = space + "  "
        body = body + space + str(per) + "|"
        for k, v in categories_percentage.items():
            if v == per or v == 1000:
                body = body + " o "
                categories_percentage[k] = 1000
            else:
                body = body + "   "

        body = body + " \n"
        per = per - 10

    return header + body + footer
