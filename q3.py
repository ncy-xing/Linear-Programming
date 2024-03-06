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
    # Primal LP
    # TODO Create vars for each row action and one var for objective 
    # TODO Add constraint: All action variables are a probability distribution
    # TODO add constraint: for each column action, sum of each action variable * coefficient >= objective var
    # TODO Solve  

    # Dual LP 
    # TODO Create vars for each col action and one var for objective 
    # TODO Add constraint: All action variables are a probability distribution
    # TODO add constraint: for each row action, sum of each action variable * coefficient >= objective var
    # TODO Solve  

    # TODO Print clean results 

def main(input_file_name : str) -> None:
    # Parse file data 
    with open(input_file_name, "r") as file:
        data = file.readlines()
        num_row_actions = int(data.pop(0))
        num_col_actions = int(data.pop(0))
    payoffs = [[0] * num_col_actions] * num_row_actions
    for i in range(num_row_actions):
        col_actions = data.pop(0).split()
        for j in range(num_col_actions):
            payoffs[i][j] = int(col_actions[j])


if __name__ == "__main__":
    main("q3 tests/1.txt")
    # main(sys.argv[1])
