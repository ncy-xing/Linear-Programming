from pulp import * 
import sys

def main():
    # Primal 
    lp = LpProblem("Bakery_Problem", LpMaximize)

    #Define variables
    x1 = LpVariable(name="Bowdoin_log", lowBound=0, cat="Integer")
    x2 = LpVariable(name="Chocolate_cake", lowBound=0, cat="Integer")

    #Add the objective function
    lp += 10 * x1 + 5 * x2
    # print(lp.objective)

    # Add the constraints
    lp += (5 * x1 + x2 <= 90, "oven_constraint")
    lp += (x1 + 10 * x2 <= 300, "food_processor_constraint")
    lp += (4 * x1 + 6 * x2 <= 125, "boiler_constraint")
    # print(lp.constraints)

    # Solve the LP
    status = lp.solve(PULP_CBC_CMD(msg=0))
    # print("Status:", status) #1:optimal, 2:not solved, 3:infeasible, 4:unbounded, 5:undef
    
    #Print solution
    # for var in lp.variables():
    #     print(var, "=", value(var))
    print("Primal OPT =", value(lp.objective))

    # Dual solution
    dual_lp = LpProblem("Bakery_Problem_Dual", LpMinimize)
    y1 = LpVariable(name="Oven", lowBound=0, cat="Integer")
    y2 = LpVariable(name="Food_Processer", lowBound=0, cat="Integer")
    y3 = LpVariable(name="Boiler", lowBound=0, cat="Integer")
    
    # Objective function
    dual_lp += 90 * y1 + 300 * y2 + 125 * y3

    # Constraints 
    lp += (5 * y1 + y2 + 4 * y3 >= 10, "log_constraint")
    lp += (y1 + 10 * y2 + 6 * y3 >= 5, "cake_constraint")

    # Solve
    dual_status = dual_lp.solve(PULP_CBC_CMD(msg=0))
    # print("Status:", dual_status) #1:optimal, 2:not solved, 3:infeasible, 4:unbounded, 5:undef

    #Print solution
    # for var in dual_lp.variables():
    #     print(var, "=", value(var))
    print("Dual OPT =", value(lp.objective))


if __name__ == "__main__":
    main()