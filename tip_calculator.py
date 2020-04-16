# Get the percent of tip the table wants to add.
# For each person: make him enter his name and the cost of each thing he ordered. 40, 30, 10
# At the end, print a summary of what each person has to pay.

import sys


def calculate_personal_meal_cost(order_costs, tip_percentage):
    sum_of_order = sum(order_costs)
    return sum_of_order * ((tip_percentage + 100) / 100)


def print_people_and_costs(person_and_cost):
    for person, cost in person_and_cost.items():
        print(person + " has to pay: " + str(cost))


def main():
    person_and_cost = {}
    tip_percentage = int(input("How much tip does your table want to add? \n"))
    if tip_percentage < 0:
        print("BAD! STOP THAT!")
        sys.exit(1)
    amount_of_people = int(input("How many are you? \n"))
    for person in range(amount_of_people):
        name = input("Whats your name? \n")
        order = input("What are the prices of what you got? Enter them between ','s. \n")
        order_costs = order.split(',')
        order_costs = [int(item) for item in order_costs]
        personal_meal_cost = calculate_personal_meal_cost(order_costs, tip_percentage)
        person_and_cost[name] = personal_meal_cost

    print_people_and_costs(person_and_cost)


if __name__ == '__main__':
    main()
