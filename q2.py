from pulp import * 
import sys

class Entity:
    """ Represents an entity at position (x, y). """

    def __init__(self, identifier : str="Entity", x : int=0, y : int=0) -> None:
        """ Initialize cordinates. """
        self.identifier = identifier
        self.x = x
        self.y = y
    
    def distance_from(self, x : int | float, y : int | float) -> int | float:
        """ Computes the Manhattan distance between self and given coordinates. """
        return abs(self.x - x) + abs(self.y - y)

    def __str__(self) -> str:
        """ Returns serialized version of entity. """
        return f"{self.identifier} at ({self.x}, {self.y})"


def match_drivers(drivers : List[Entity], riders: List[Entity]) -> List[tuple[Entity]]:
    """
    Attempts to match all drivers to customers, minimizing the total distance traveled. 
    One driver will be matched to one rider. 
    If drivers < riders, some riders will not be matched. TODO
    If riders > drivers, some drivers will not be matched. TODO 

    drivers -- List of drivers to be matched
    riders -- List of riders to be matched
    """
    pass 
        
        
def main(input_file_name):
    # Parse file data 
    with open(input_file_name, "r") as file:
        data = file.readlines()
        grid_size = int(data.pop(0))
        num_drivers = int(data.pop(0))
        num_riders = int(data.pop(0))
    print(f"Drivers: {num_drivers}\nRiders: {num_riders}")
    drivers = []
    riders = []
    for i in range(num_drivers):
        coords = data.pop(0).split()
        drivers.append(Entity(coords[0], coords[1], "driver"))
    for i in range(num_riders):
        coords = data.pop(0).split()
        riders.append(Entity(coords[0], coords[1], "rider"))

    # Primal 
    # lp = LpProblem("Bakery_Problem", LpMaximize)

    # #Define variables
    # x1 = LpVariable(name="Bowdoin_log", lowBound=0, cat="Integer")
    # x2 = LpVariable(name="Chocolate_cake", lowBound=0, cat="Integer")

    # #Add the objective function
    # lp += 10 * x1 + 5 * x2
    # # print(lp.objective)

    # # Add the constraints
    # lp += (5 * x1 + x2 <= 90, "oven_constraint")
    # lp += (x1 + 10 * x2 <= 300, "food_processor_constraint")
    # lp += (4 * x1 + 6 * x2 <= 125, "boiler_constraint")
    # # print(lp.constraints)

    # # Solve the LP
    # status = lp.solve(PULP_CBC_CMD(msg=0))
    # # print("Status:", status) #1:optimal, 2:not solved, 3:infeasible, 4:unbounded, 5:undef

    # #Print solution
    # # for var in lp.variables():
    # #     print(var, "=", value(var))
    # print("Primal OPT =", value(lp.objective))

if __name__ == "__main__":
    main("tests/1.txt")
    # main(sys.argv[1])
