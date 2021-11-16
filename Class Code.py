from matplotlib import pyplot as plt
import numpy as np
import random


class Time:
    def __init__(self, current_month):
        self.current_month = current_month

    def update_month(self):
        self.current_month += 1


class conditions:
    def __init__(self, interest, loan, incubator_cost, training_cost, transport_cost, aditional_costs, chick_price,
                 feed_price,
                 laying_rate, hatch_rate, tray_size, price_per_tray, price_per_chick,
                 kg_feed, cost_per_kg, feeders_and_drinkers, vaccination_per_chicken, poultry_pen
                 , repayment, new_chick_percentage, price_per_grownchicken_sold, pen_capacity, grown_chick_selling_age):
        self.incubator_cost = incubator_cost
        self.training_cost = training_cost
        self.transport_cost = transport_cost
        self.aditional_costs = aditioanl_costs
        self.interest = interest
        self.loan = loan
        self.chick_price = chick_price
        self.feed_price = feed_price
        self.laying_rate = laying_rate
        self.hatch_rate = hatch_rate
        self.tray_size = tray_size
        self.price_per_tray = price_per_tray
        self.price_per_chick = price_per_chick
        self.kg_feed = kg_feed
        self.cost_per_kg = cost_per_kg
        self.feeders_and_drinkers = feeders_and_drinkers
        self.vaccination_per_chicken = vaccination_per_chicken
        self.poultry_pen = poultry_pen
        self.repayment = repayment
        self.new_chick_percentage = new_chick_percentage
        self.price_per_grownchicken_sold = price_per_grownchicken_sold
        self.pen_capacity = pen_capacity
        self.grown_chick_selling_age = grown_chick_selling_age


class incubator:
    def __init__(self, capacity, hatch_rate, price):
        self.capacity = capacity
        self.hatch_rate = hatch_rate
        self.price = price


class Loan:
    def __init__(self, loan_value, interest, split, months):
        self.loan_value = loan_value
        self.interest = interest
        self.split = split
        self.months = months
        self.debt_log = []


class Revenues:
    def __init__(self):
        self.egg_revenue_log = []
        self.chick_revenue_log = []
        self.total_revenue_log = []
        self.total_profit_log = []

    def egg_revenue(self):
        size = stock.outputing_size()
        eggs = eggrevenue = 0
        y = random.randrange(conditions.laying_rate - 1, conditions.laying_rate + 1)
        eggs += y * size
        if eggs < incubator.capacity:
            eggs = 0
        eggrevenue = (eggs / conditions.tray_size) * conditions.price_per_tray
        return eggrevenue

    def chick_revenue(self):
        z = incubator.hatch_rate * 100
        x = random.randrange(int(0.9 * z), int(1.1 * z), 1) / 100 * (1 - conditions.new_chick_percentage)

        return round(incubator.capacity * x) * conditions.price_per_chick

    def total_revenue(self):
        return self.egg_revenue() + self.chick_revenue()


class Costs:
    def __init__(self):
        self.cogs_log = []
        self.running_costs_log = []
        self.vaccinations_log = []

    def cogs(self):
        feed = 0
        if time.current_month > 0:
            # a = stock.remove_chickens_number(3)
            feed = ((len(
                stock.chickens))) / 50 * 120 * conditions.cost_per_kg  # 2.4 is the kg per chicken ration in the startup phase
        return feed

    def running_costs(self):
        running_costs = 0
        # if time.current_month == 1:
        #     running_costs = conditions.feeders_and_drinkers + conditions.poultry_pen
        # else:
        if time.current_month >= 1:
            running_costs = 0  # conditions.repayment
            new_chickens = stock.added_chickens_log[-1]
            running_costs += conditions.vaccination_per_chicken * new_chickens
        return running_costs


class Stock:
    def __init__(self):
        self.chickens = {}
        self.chicken_log = []
        self.outputting_log = []
        self.added_chickens_log = []
        self.sold_chickens_log = []

    def new_chicks(self):
        z = incubator.hatch_rate * 100
        x = random.randrange(int(0.9 * z), int(1.1 * z), 1) / 100
        ccc = round(incubator.capacity * (x)) * conditions.new_chick_percentage  # 5% of new chicks are saved for growth
        return ccc

    def remove_chickens(self, x, age):
        c = 0
        copy = self.chickens
        keys = list(self.chickens.keys())
        values = list(self.chickens.values())
        for item in range(len(values)):
            if values[item] == age and c < x:
                copy.pop(keys[item], None)
                c += 1
        self.chickens = copy

    def remove_chickens_number(self, age):  # gives number of chickens under given age
        c = 0
        copy = self.chickens
        keys = list(self.chickens.keys())
        values = list(self.chickens.values())
        for item in range(len(values)):
            if values[item] <= age:
                c += 1
        return c

    def remove_chickens_number_over(self, age):  # gives number of chickens over given age
        c = 0
        copy = self.chickens
        keys = list(self.chickens.keys())
        values = list(self.chickens.values())
        for item in range(len(values)):
            if values[item] >= age:
                c += 1
        return c

    def add_chickens(self, x, age):
        keys = list(self.chickens.keys())
        values = list(self.chickens.values())
        for item in range(x):
            self.chickens[f"chicken{random.randrange(100000, 500000)}"] = age

    def increase_age(self, age):
        values = list(self.chickens.values())
        keys = list(self.chickens.keys())
        for item in range(len(values)):
            self.chickens[keys[item]] = values[item] + age

    def reset_stock(self):
        self.chickens = {}
        self.add_chickens(50, 5)

    def outputing_size(self):
        values = list(self.chickens.values())
        c = 0
        for age in values:
            if age >= 5:
                c += 1
        return c


def Initialize2(entries):
    b = float(entries['Interest Rate (%)'].get()) / 100
    c = float(entries['Simulation Months'].get())
    conditions.laying_rate = float(entries['Laying Rate (eggs/chicken/month)'].get())
    conditions.incubator_cost = float(entries['Incubator Cost'].get())
    a1 = conditions.incubator_cost
    conditions.training_cost = float(entries['Training Cost'].get())
    a2 = conditions.training_cost
    conditions.transport_cost = float(entries['Transport Cost'].get())
    a3 = conditions.transport_cost
    conditions.aditional_cost = float(entries['Aditional Costs'].get())
    a4 = conditions.aditional_cost
    a5 = conditions.feeders_and_drinkers = float(entries['Feeders and drinkers Cost (USD)'].get())
    a6 = conditions.poultry_pen = float(entries['Poultry Pen Price (USD)'].get())
    a = a1 + a2 + a3 + a4 + a5 + a6
    conditions.tray_size = 30
    conditions.kg_feed = 120
    conditions.new_chick_percentage = float(entries['% of chicks kept each month'].get()) / 100
    conditions.price_per_tray = float(entries['Price per tray of Eggs sold (30)(USD)'].get())
    conditions.price_per_chick = float(entries['Price per Chick sold (USD)'].get())
    incubator.hatch_rate = (float(entries['Hatch Rate (%) '].get()) / 100)
    incubator.capacity = float(entries['Incubator Capacity'].get())
    conditions.cost_per_kg = float(entries['Price per Kg Feed (USD)'].get())
    conditions.vaccination_per_chicken = float(entries['Vaccination per chicken costs (USD)'].get())
    conditions.repayment = float(entries['Monthly Repayment (USD)'].get())
    conditions.price_per_grownchicken_sold = float(entries['Price per Grown Chicken Sold (USD)'].get())
    conditions.pen_capacity = float(entries['Poultry Pen Capacity'].get())
    conditions.grown_chick_selling_age = float(entries['Selling Age Grown Chicken(months)'].get())
    global loan
    loan = Loan(a, b, 0, c)  # loan size,interest,spplit
    global stock
    stock = Stock()
    costs = Costs()
    revenue = Revenues()
    r = []
    r.append(loan)
    r.append(stock)
    r.append(costs)
    r.append(revenue)
    return r


# Initialize()
time = Time(0)


def cycles(entries):
    c = Initialize2(entries)
    loan = c[0]
    stock = c[1]
    stock.reset_stock()  # resets and puts all initial 50 chickens
    costs = c[2]
    revenue = c[3]
    balance = [0, 0]
    stock.chicken_log = [50]
    stock.added_chickens_log = [50]
    costs.running_costs_log = [0]
    costs.cogs_log = [0]
    total_costs_log = [-100]
    monthly_repayments = [0]
    revenue.egg_revenue_log = [0]
    revenue.chick_revenue_log = [0]
    revenue.total_revenue_log = [0]
    grown_chick_revenue_log = [0]
    grown_chick_sold_log = [0]
    revenue.total_profit_log = [0]
    loan.debt_log = [loan.loan_value * (1 + loan.interest)]
    # --------------------------------------------------------- DO NOT CHANGE UNDER THIS LINE ------------------------------------------
    for x in range(int(loan.months)):
        newc = round(stock.new_chicks())
        stock.add_chickens(newc, 0)
        set_value = conditions.pen_capacity
        selling_age = conditions.grown_chick_selling_age
        if len(stock.chickens) > set_value:
            delta = len(stock.chickens) - set_value
            grown_birds_sold = stock.remove_chickens_number_over(selling_age)
            if grown_birds_sold > delta:  # if there are more birds able to b sold that the ones we want to
                stock.remove_chickens(delta, selling_age)
                number_sold_birds = delta
            else:  # if there are less or the same amount of birds able to be sold to the ones we want to
                stock.remove_chickens(grown_birds_sold, selling_age)
                number_sold_birds = grown_birds_sold
        else:
            number_sold_birds = 0
        stock.added_chickens_log.append(newc)  # this valus is before selling chicks
        stock.chicken_log.append(len(stock.chickens))
        rc = costs.running_costs()
        costssold = costs.cogs()
        costs.running_costs_log.append(rc)
        costs.cogs_log.append(costssold)
        eggrev = revenue.egg_revenue()
        chirev = revenue.chick_revenue()  # + grown_birds_sold * conditions.price_per_grownchicken_sold
        gchickrev = number_sold_birds * conditions.price_per_grownchicken_sold
        grown_chick_revenue_log.append(gchickrev)  # !!!!
        grown_chick_sold_log.append(number_sold_birds)  # !!!!
        revenue.egg_revenue_log.append(eggrev)
        revenue.chick_revenue_log.append(chirev)
        revenue.total_revenue_log.append(eggrev + chirev + gchickrev)
        revenue.total_profit_log.append(eggrev + chirev + gchickrev - rc - costssold - conditions.repayment)
        total_costs_log.append(- rc - costssold - conditions.repayment)
        if (revenue.total_profit_log[-1]) > 0:
            loan.debt_log.append(
                loan.debt_log[-1] - conditions.repayment)  # if there was profit, the farmer repays the set amount
        else:
            loan.debt_log.append(loan.debt_log[
                                     -1] + revenue.total_revenue() - rc - costssold - conditions.repayment)  # if no profit, the farmer repays but there is accumulated debt
        time.update_month()
        stock.increase_age(1)
        balance.append(balance[-1] + revenue.total_profit_log[-1])
    # --------------------------------------------------------- DO NOT CHANGE OVER THIS LINE ------------------------------------------
    print('monthly profits', revenue.total_profit_log)
    print('debt: ', loan.debt_log)
    print('-------------------1--------------------')
    print('stock.chicken_log: ', stock.chicken_log)
    print('stock.added.chcikens log', stock.added_chickens_log)
    print('sold grown chicks: ', grown_chick_sold_log)
    print('grown chick revenue', grown_chick_revenue_log)
    print('1 month chick revenue', revenue.chick_revenue_log)
    print('eggs revenue', revenue.egg_revenue_log)
    print('total', revenue.total_revenue_log)
    print(stock.chickens)
    print('-----------------------------------------')
    # plt.plot(loan.debt_log, label='debt')
    plt.plot(costs.running_costs_log, label="running costs")
    plt.plot(costs.cogs_log, label='COGS')
    plt.plot(revenue.egg_revenue_log, label='Egg Revenue')
    plt.plot(revenue.chick_revenue_log, label='1 month Chick revenue')
    plt.plot(grown_chick_revenue_log, label=f"{int(conditions.grown_chick_selling_age)} month Chick revenue")
    plt.plot(revenue.total_revenue_log, label='Monthly Revenues')
    plt.plot(revenue.total_profit_log, label='Monthly Profits')
    plt.plot([0] * len(loan.debt_log), 'black')
    plt.plot(stock.chicken_log, label='Number of chickens')
    plt.xticks(np.arange(0, len(loan.debt_log), 2))
    plt.legend(bbox_to_anchor=(0., 0.99, 1., .102), loc='lower left',
               ncol=2, mode="expand", borderaxespad=0.)

    plt.show()


def excel(entries):
    c = Initialize2(entries)
    loan = c[0]
    stock = c[1]
    stock.reset_stock()  # resets and puts all initial 50 chickens
    costs = c[2]
    revenue = c[3]
    balance = ['Balance', 0, 0]
    stock.chicken_log = ['Number of Chickens', 50]
    stock.added_chickens_log = ['Added Chickens', 50]
    costs.running_costs_log = ['Running Costs', 0]
    costs.cogs_log = ['Cost of Goods Sold', 0]
    total_costs_log = ['Total Costs', -100]
    monthly_repayments = ['Monthly Repayment', 0]
    revenue.egg_revenue_log = ['Revenue from Eggs', 0]
    revenue.chick_revenue_log = ['Revenue from Chicks', 0]
    revenue.total_revenue_log = ['Total Revenue', 0]
    revenue.total_profit_log = ['Total Profits', 0]
    grown_chick_revenue_log = ['Revenue From Grown Chicks', 0]
    grown_chick_sold_log = ['Number of Sold Chickens', 0]
    loan.debt_log = ['LOAN LEFT', loan.loan_value * (1 + loan.interest)]
    for x in range(int(loan.months)):
        newc = round(stock.new_chicks())
        stock.add_chickens(newc, 0)
        set_value = conditions.pen_capacity
        selling_age = conditions.grown_chick_selling_age
        if len(stock.chickens) > set_value:
            delta = len(stock.chickens) - set_value
            grown_birds_sold = stock.remove_chickens_number_over(selling_age)
            if grown_birds_sold > delta:  # if there are more birds able to b sold that the ones we want to
                stock.remove_chickens(delta, selling_age)
                number_sold_birds = delta
            else:  # if there are less or the same amount of birds able to be sold to the ones we want to
                stock.remove_chickens(grown_birds_sold, selling_age)
                number_sold_birds = grown_birds_sold
        else:
            number_sold_birds = 0
        stock.added_chickens_log.append(newc)  # this valus is before selling chicks
        stock.chicken_log.append(len(stock.chickens))
        rc = costs.running_costs()
        costssold = costs.cogs()
        costs.running_costs_log.append(rc)
        costs.cogs_log.append(costssold)
        eggrev = revenue.egg_revenue()
        chirev = revenue.chick_revenue()  # + grown_birds_sold * conditions.price_per_grownchicken_sold
        gchickrev = number_sold_birds * conditions.price_per_grownchicken_sold
        grown_chick_revenue_log.append(gchickrev)  # !!!!
        grown_chick_sold_log.append(number_sold_birds)  # !!!!
        revenue.egg_revenue_log.append(eggrev)
        revenue.chick_revenue_log.append(chirev)
        revenue.total_revenue_log.append(eggrev + chirev + gchickrev)
        revenue.total_profit_log.append(eggrev + chirev + gchickrev - rc - costssold - conditions.repayment)
        total_costs_log.append(- rc - costssold - conditions.repayment)
        if (revenue.total_profit_log[-1]) > 0:
            loan.debt_log.append(loan.debt_log[-1] - conditions.repayment)  # if there was profit, the farmer repays the set amount
        else:
            loan.debt_log.append(loan.debt_log[-1] + revenue.total_revenue() - rc - costssold - conditions.repayment)  # if no profit, the farmer repays but there is accumulated debt
        time.update_month()
        stock.increase_age(1)
        balance.append(balance[-1] + revenue.total_profit_log[-1])
    # -------------------------------------------------------------------------------------------------------------------------------
    chickprices = ['Price Per Chick'] + [1.2] * (len(stock.added_chickens_log) - 1)
    income = ['REVENUE'] + [] * len(stock.added_chickens_log)
    costss = ['COSTS'] + [] * len(stock.added_chickens_log)
    space = [] * len(stock.added_chickens_log)
    monthlypayments = ['Monthly Payments'] + [conditions.repayment] * (len(stock.added_chickens_log) - 1)

    x = conditions.repayment = str(entries['Excel Filename'].get())
    print(balance)
    with open(x + '.csv', 'a') as f:
        f.write('Balance Sheet' + '\n')
        f.write(str(['Month'] + list(range(1, time.current_month + 1))).strip("'[]''") + '\n')
        f.write(str(balance).strip("'[]''") + '\n')
        f.write(str(stock.added_chickens_log).strip("'[]'").strip('""') + '\n')
        f.write(str(stock.chicken_log).strip("'[]'") + '\n')
        f.write(str(chickprices).strip("'[]''") + '\n')
        f.write(str(income).strip("'[]''") + '\n')
        f.write(str(revenue.chick_revenue_log).strip("'[]''") + '\n')
        f.write(str(revenue.egg_revenue_log).strip("'[]''") + '\n')
        f.write(str(revenue.total_revenue_log).strip("'[]''") + '\n')
        f.write(str(costss).strip("'[]''") + '\n')
        f.write(str(costs.running_costs_log).strip("'[]''") + '\n')
        f.write(str(costs.cogs_log).strip("'[]''") + '\n')
        f.write(str(monthlypayments).strip("'[]''") + '\n')
        f.write(str(total_costs_log).strip("'[]''") + '\n')
        f.write(str(space).strip("'[]''") + '\n')
        f.write(str(revenue.total_profit_log).strip("'[]''") + '\n')
        f.write(str(loan.debt_log).strip("'[]''") + '\n')


def revenues(entries):
    c = Initialize2(entries)
    loan = c[0]
    stock = c[1]
    stock.reset_stock()  # resets and puts all initial 50 chickens
    costs = c[2]
    revenue = c[3]
    balance = [0, 0]
    stock.chicken_log = [50]
    stock.added_chickens_log = [50]
    costs.running_costs_log = [0]
    costs.cogs_log = [0]
    total_costs_log = [-100]
    monthly_repayments = [0]
    revenue.egg_revenue_log = [0]
    revenue.chick_revenue_log = [0]
    revenue.total_revenue_log = [0]
    revenue.total_profit_log = [0]
    loan.debt_log = [loan.loan_value * (1 + loan.interest)]
    grown_chick_revenue_log = [0]  # !!!!!!NEW!!!!!!!!

    for x in range(int(loan.months)):
        newc = round(stock.new_chicks())
        stock.add_chickens(newc, 0)
        stock.added_chickens_log.append(newc)  # this valus is before selling chicks
        stock.chicken_log.append(len(stock.chickens))
        rc = costs.running_costs()
        costssold = costs.cogs()
        costs.running_costs_log.append(rc)
        costs.cogs_log.append(costssold)
        eggrev = revenue.egg_revenue()
        chirev = revenue.chick_revenue()
        revenue.egg_revenue_log.append(eggrev)
        revenue.chick_revenue_log.append(chirev)
        revenue.total_revenue_log.append(eggrev + chirev)
        revenue.total_profit_log.append(eggrev + chirev - rc - costssold - conditions.repayment)
        total_costs_log.append(- rc - costssold - conditions.repayment)
        if (revenue.total_profit_log[-1]) > 0:
            loan.debt_log.append(
                loan.debt_log[-1] - conditions.repayment)  # if there was profit, the farmer repays the set amount
        else:
            loan.debt_log.append(loan.debt_log[
                                     -1] + revenue.total_revenue() - rc - costssold - conditions.repayment)  # if no profit, the farmer repays but there is accumulated debt
        time.update_month()
        stock.increase_age(1)
        balance.append(balance[-1] + revenue.total_profit_log[-1])
    R = random.randrange(0, 100, 1) / 100
    G = random.randrange(0, 100, 1) / 100
    B = random.randrange(0, 100, 1) / 100
    plt.plot(revenue.total_revenue_log, label=f"Montly Revenues {incubator.hatch_rate * 100}% Hatch Rate",
             color=(R, G, B), linewidth=2)
    plt.plot(revenue.total_profit_log, label=f"Montly Profits {incubator.hatch_rate * 100}% Hatch Rate",
             color=(R, G, B, 0.4), linewidth=2)
    plt.plot([0] * len(loan.debt_log), 'black')
    plt.xticks(np.arange(0, len(loan.debt_log), 2))
    plt.legend(bbox_to_anchor=(0., 0.99, 1., .102), loc='lower left',
               ncol=2, mode="expand", borderaxespad=0.)
    plt.show()


def costs(entries):
    c = Initialize2(entries)
    loan = c[0]
    stock = c[1]
    stock.reset_stock()  # resets and puts all initial 50 chickens
    costs = c[2]
    revenue = c[3]
    balance = [0, 0]
    stock.chicken_log = [50]
    stock.added_chickens_log = [50]
    costs.running_costs_log = [0]
    costs.cogs_log = [0]
    total_costs_log = [-100]
    monthly_repayments = [0]
    revenue.egg_revenue_log = [0]
    revenue.chick_revenue_log = [0]
    revenue.total_revenue_log = [0]
    revenue.total_profit_log = [0]
    loan.debt_log = [loan.loan_value * (1 + loan.interest)]
    grown_chick_revenue_log = [0]  # !!!!!!NEW!!!!!!!!

    for x in range(int(loan.months)):
        newc = round(stock.new_chicks())
        stock.add_chickens(newc, 0)
        stock.added_chickens_log.append(newc)  # this valus is before selling chicks
        stock.chicken_log.append(len(stock.chickens))
        rc = costs.running_costs()
        costssold = costs.cogs()
        costs.running_costs_log.append(rc)
        costs.cogs_log.append(costssold)
        eggrev = revenue.egg_revenue()
        chirev = revenue.chick_revenue()
        revenue.egg_revenue_log.append(eggrev)
        revenue.chick_revenue_log.append(chirev)
        revenue.total_revenue_log.append(eggrev + chirev)
        revenue.total_profit_log.append(eggrev + chirev - rc - costssold - conditions.repayment)
        total_costs_log.append(- rc - costssold - conditions.repayment)
        if (revenue.total_profit_log[-1]) > 0:
            loan.debt_log.append(
                loan.debt_log[-1] - conditions.repayment)  # if there was profit, the farmer repays the set amount
        else:
            loan.debt_log.append(loan.debt_log[
                                     -1] + revenue.total_revenue() - rc - costssold - conditions.repayment)  # if no profit, the farmer repays but there is accumulated debt
        time.update_month()
        stock.increase_age(1)
        balance.append(balance[-1] + revenue.total_profit_log[-1])
    plt.plot(costs.running_costs_log, label="running costs")
    plt.plot(costs.cogs_log, label='COGS')
    plt.plot([0] * len(loan.debt_log), 'black')
    plt.xticks(np.arange(0, len(loan.debt_log), 2))
    plt.legend(bbox_to_anchor=(0., 0.99, 1., .102), loc='lower left',
               ncol=2, mode="expand", borderaxespad=0.)
    plt.show()


def debt(entries):
    c = Initialize2(entries)
    loan = c[0]
    stock = c[1]
    stock.reset_stock()  # resets and puts all initial 50 chickens
    costs = c[2]
    revenue = c[3]
    balance = [0, 0]
    stock.chicken_log = [50]
    stock.added_chickens_log = [50]
    costs.running_costs_log = [0]
    costs.cogs_log = [0]
    total_costs_log = [-100]
    monthly_repayments = [0]
    revenue.egg_revenue_log = [0]
    revenue.chick_revenue_log = [0]
    revenue.total_revenue_log = [0]
    revenue.total_profit_log = [0]
    loan.debt_log = [loan.loan_value * (1 + loan.interest)]
    grown_chick_revenue_log = [0]  # !!!!!!NEW!!!!!!!!

    for x in range(int(loan.months)):
        newc = round(stock.new_chicks())
        stock.add_chickens(newc, 0)
        stock.added_chickens_log.append(newc)  # this valus is before selling chicks
        stock.chicken_log.append(len(stock.chickens))
        rc = costs.running_costs()
        costssold = costs.cogs()
        costs.running_costs_log.append(rc)
        costs.cogs_log.append(costssold)
        eggrev = revenue.egg_revenue()
        chirev = revenue.chick_revenue()
        revenue.egg_revenue_log.append(eggrev)
        revenue.chick_revenue_log.append(chirev)
        revenue.total_revenue_log.append(eggrev + chirev)
        revenue.total_profit_log.append(eggrev + chirev - rc - costssold - conditions.repayment)
        total_costs_log.append(- rc - costssold - conditions.repayment)
        if (revenue.total_profit_log[-1]) > 0:
            loan.debt_log.append(
                loan.debt_log[-1] - conditions.repayment)  # if there was profit, the farmer repays the set amount
        else:
            loan.debt_log.append(loan.debt_log[
                                     -1] + revenue.total_revenue() - rc - costssold - conditions.repayment)  # if no profit, the farmer repays but there is accumulated debt
        time.update_month()
        stock.increase_age(1)
        balance.append(balance[-1] + revenue.total_profit_log[-1])
        # a = float(entries['Initial Loan (USD)'].get())
        b = float(entries['Interest Rate (%)'].get())
        c = float(entries['Simulation Months'].get())
    plt.plot(loan.debt_log, label=f"Debt Repayment - Interest:{b}% ; Monthly Payback:{conditions.repayment}USD")
    f"Montly Profits {incubator.hatch_rate * 100}%"
    plt.plot([0] * len(loan.debt_log), 'black')
    plt.xticks(np.arange(0, len(loan.debt_log), 2))
    plt.legend(bbox_to_anchor=(0., 0.99, 1., .102), loc='lower left',
               ncol=2, mode="expand", borderaxespad=0.)

    plt.show()


i = 0


def payback(entries):
    entries['Payback time (months)'].delete(0, tk.END)
    c = Initialize2(entries)
    loan = c[0]
    stock = c[1]
    stock.reset_stock()  # resets and puts all initial 50 chickens
    costs = c[2]
    revenue = c[3]
    balance = [0, 0]
    stock.chicken_log = [50]
    stock.added_chickens_log = [50]
    costs.running_costs_log = [0]
    costs.cogs_log = [0]
    total_costs_log = [-100]
    monthly_repayments = [0]
    revenue.egg_revenue_log = [0]
    revenue.chick_revenue_log = [0]
    revenue.total_revenue_log = [0]
    revenue.total_profit_log = [0]
    loan.debt_log = [loan.loan_value * (1 + loan.interest)]
    grown_chick_revenue_log = [0]  # !!!!!!NEW!!!!!!!!

    # for x in range(int(loan.months)):
    while loan.debt_log[-1] > 0:
        newc = round(stock.new_chicks())
        stock.add_chickens(newc, 0)
        stock.added_chickens_log.append(newc)  # this valus is before selling chicks
        stock.chicken_log.append(len(stock.chickens))
        rc = costs.running_costs()
        costssold = costs.cogs()
        costs.running_costs_log.append(rc)
        costs.cogs_log.append(costssold)
        eggrev = revenue.egg_revenue()
        chirev = revenue.chick_revenue()
        revenue.egg_revenue_log.append(eggrev)
        revenue.chick_revenue_log.append(chirev)
        revenue.total_revenue_log.append(eggrev + chirev)
        revenue.total_profit_log.append(eggrev + chirev - rc - costssold - conditions.repayment)
        total_costs_log.append(- rc - costssold - conditions.repayment)
        if (revenue.total_profit_log[-1]) > 0:
            loan.debt_log.append(
                loan.debt_log[-1] - conditions.repayment)  # if there was profit, the farmer repays the set amount
        else:
            loan.debt_log.append(loan.debt_log[
                                     -1] + revenue.total_revenue() - rc - costssold - conditions.repayment)  # if no profit, the farmer repays but there is accumulated debt
        time.update_month()
        stock.increase_age(1)
        balance.append(balance[-1] + revenue.total_profit_log[-1])
        i = +1
        print(loan.debt_log[-1])
        if len(loan.debt_log) > 72:
            print('No repayment after 72 months, stopped computing')
            break
    print('repayment time is: ', len(loan.debt_log))
    if len(loan.debt_log) > 72:
        entries['Payback time (months)'].insert(0, 'Very risky, did not payback under 6 years')
    else:
        entries['Payback time (months)'].insert(0, len(loan.debt_log) - 1)


import tkinter as tk
from tkinter import ttk

root = tk.Tk()
fields = (
    'Incubator Cost', 'Training Cost', 'Transport Cost', 'Aditional Costs', 'Interest Rate (%)', 'Simulation Months',
    "% of chicks kept each month", 'Laying Rate (eggs/chicken/month)', 'Hatch Rate (%) ', 'Incubator Capacity',
    'Price per Kg Feed (USD)',
    'Price per Chick sold (USD)', 'Price per Grown Chicken Sold (USD)', 'Poultry Pen Capacity',
    'Selling Age Grown Chicken(months)', 'Price per tray of Eggs sold (30)(USD)',
    'Feeders and drinkers Cost (USD)', 'Vaccination per chicken costs (USD)', 'Monthly Repayment (USD)',
    'Poultry Pen Price (USD)', 'Payback time (months)', 'Excel Filename')


def makeform(root, fields):
    entries = {}
    i = 0
    for field in fields:
        r = [2500, 200, 200, 100, 20, 36, 1, 8, 75, 176, 0.4, 1, 5, 60, 12, 4, 40, 0.5, 100, 120,
             "Press 'Payback Time (months)' to Compute", 'Cash Flow X']
        row = tk.Frame(root)
        lab = ttk.Label(row, width=35, text=field + ": ", anchor='w')
        ent = tk.Entry(row)

        ent.insert(0, f"{r[i]}")
        row.pack(side=tk.TOP,
                 fill=tk.X,
                 padx=4,
                 pady=4)
        lab.pack(side=tk.LEFT)
        ent.pack(side=tk.RIGHT,
                 expand=tk.YES,
                 fill=tk.X)
        entries[field] = ent
        i += 1

    return entries


from tkinter import *

if __name__ == '__main__':
    ents = makeform(root, fields)
    b1 = tk.Button(root, text='Revenue and Profits Graph',
                   command=(lambda e=ents: revenues(e)))
    b1.pack(side=tk.LEFT, padx=5, pady=5)

    b2 = tk.Button(root, text='Cogs and Running Costs Graph',
                   command=(lambda e=ents: costs(e)))
    b2.pack(side=tk.LEFT, padx=5, pady=5)

    b4 = tk.Button(root, text='Debt Evolution',
                   command=(lambda e=ents: debt(e)))
    b4.pack(side=tk.LEFT, padx=5, pady=5)

    b5 = tk.Button(root, text='Start/Restart',
                   command=(lambda e=ents: Initialize2(e)))
    b5.pack(side=tk.LEFT, padx=5, pady=5)

    b6 = tk.Button(root, text='Payback time (months)',
                   command=(lambda e=ents: payback(e)))
    b6.pack(side=tk.LEFT, padx=5, pady=5)

    b7 = tk.Button(root, text='All',
                   command=(lambda e=ents: cycles(e)))
    b7.pack(side=tk.LEFT, padx=5, pady=5)

    b8 = tk.Button(root, text='Build Excell Datasheet',
                   command=(lambda e=ents: excel(e)))
    b8.pack(side=tk.LEFT, padx=5, pady=5)

    b9 = tk.Button(root, text='Quit', command=root.quit)
    b9.pack(side=tk.LEFT, padx=5, pady=5)

    root.mainloop()
