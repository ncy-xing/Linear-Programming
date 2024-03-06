"""
A script that solves andy 2-player zero sum game
by implementing the primal and dual LPs for the players. 
"""
from pulp import * 
import sys

def solve(payoffs : List[List]) -> None:
    """
    Solves a 2-player zero sum game given the payoff matrix. Prints value of 
    the game and each player's probabilities. 
    """
    rows, cols = len(payoffs), len(payoffs[0])

    # Primal LP
    primal_lp = LpProblem("Row_LP", LpMaximize)
    primal_obj = LpVariable(name=f"v_r", lowBound=0, cat="Integer")
    primal_lp += primal_obj
    # Action variables 
    p_vars = []
    for i in range(rows):
        p_vars.append(LpVariable(name=f"x_{i}", lowBound=0))
    # Add constraint: probability distribution 
    primal_lp += (lpSum([p for p in p_vars]) == 1, "prob_dist") 
    # add constraints: column actions  
    for j in range(cols):
        constraint = [p_vars[i] * payoffs[i][j] for i in range(rows)]
        primal_lp += (lpSum(constraint) >= primal_obj, f"col_action_{j}")
    
    # Dual LP 
    dual_lp = LpProblem("Col_LP", LpMinimize)
    dual_obj = LpVariable(name=f"v_c", lowBound=0, cat="Integer")
    dual_lp += dual_obj
    q_vars = []
    for j in range(cols):
        q_vars.append(LpVariable(name=f"y_{j}", lowBound=0))
    dual_lp += (lpSum([q for q in q_vars]) == 1, "prob_dist")
    for i in range(rows):
        constraint = [q_vars[j] * payoffs[i][j] for j in range(cols)]
        dual_lp += (lpSum(constraint) <= dual_obj, f"row_action_{i}")

    # Solve
    primal_lp.solve(PULP_CBC_CMD(msg=0))
    dual_lp.solve(PULP_CBC_CMD(msg=0))
    print(value(primal_lp.objective))
    print(value(dual_lp.objective))
    row_dist = []
    col_dist = []
    for var in primal_lp.variables():
        if var.name != "v_r":
            row_dist.append(value(var))
    for var in dual_lp.variables():
        if var.name != "v_c":
            col_dist.append(value(var))
    print(row_dist)
    print(col_dist)


def main(input_file_name : str) -> None:
    # Parse file data 
    with open(input_file_name, "r") as file:
        data = file.readlines()
        num_row_actions = int(data.pop(0))
        num_col_actions = int(data.pop(0))
    payoffs = []
    for i in range(num_row_actions):
        col_actions = data.pop(0).split()
        payoffs.append([int(i) for i in col_actions])
    solve(payoffs)

if __name__ == "__main__":
    main(sys.argv[1])
