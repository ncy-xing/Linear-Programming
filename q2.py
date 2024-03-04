"""
TODO
Grid size at top of file relevant? 
Assume int distances? 
"""
from pulp import * 
import sys

class Entity:
    """ Represents an entity at position (x, y). """

    def __init__(self, type : str="Entity", id : str="#", x : int=0, y : int=0) -> None:
        """ Initialize cordinates. """
        self.type = type
        self.id = id
        self.x = x
        self.y = y
    
    def distance_from(self, x : int | float, y : int | float) -> int | float:
        """ Computes the Manhattan distance between self and given coordinates. """
        return abs(self.x - x) + abs(self.y - y)

    def __str__(self) -> str:
        """ Returns serialized version of entity. """
        return f"{self.type} {self.id} at ({self.x}, {self.y})"


def match_drivers(drivers : List[Entity], riders: List[Entity]) -> List[tuple[Entity]]:
    """
    Attempts to match all drivers to customers, minimizing the total distance traveled. 
    One driver will be matched to one rider. 
    TODO If drivers < riders, some riders will not be matched. 
    TODO If riders > drivers, some drivers will not be matched.  

    drivers -- List of drivers to be matched
    riders -- List of riders to be matched
    """
    objective = []
    num_matches = min(len(drivers), len(riders))
    driver_constraints = [] # Each item is all the variables associated with one driver 
    rider_constraints = [] # Each item is all the variables associated with one rider 
    match_constraints = []
    lp = LpProblem("Match_Drivers", LpMinimize)
    
    # Driver constraints
    for i in range(len(drivers)):
        d_constraints = []
        driver = drivers[i]
        for j in range(len(riders)): 
            rider = riders[j]
            x = LpVariable(name=f"x_{i}{j}", lowBound=0, cat="Integer")
            d_constraints.append((x, f"x_{i}{j}"))
            match_constraints.append((x, f"x_{i}{j}")) # Only in one itreration
            distance = driver.distance_from(rider.x, rider.y)
            objective.append((x, distance))
        driver_constraints.append(d_constraints)
    
    # Rider constraints
    for i in range(len(riders)):
        rider = riders[i]
        r_constraints = []
        for j in range(len(drivers)):
            driver = drivers[j]
            x = LpVariable(name=f"x_{j}{i}", lowBound=0, cat="Integer")
            distance = driver.distance_from(rider.x, rider.y)
            r_constraints.append((x, f"x_{j}{i}"))
            objective.append((x, distance))
        rider_constraints.append(r_constraints)
    
    print(f"driver_constraints: {[d for d in driver_constraints]}")
    print(f"rider_constraints: {[r for r in rider_constraints]}")
    print(f"objective: {objective}")
    print(f"match constraints: {match_constraints}")

    # Plug into LP solver
    # TODO add constraint: every item in drivers and riders should add to # of drivers/riders 
    # TODO add constraint: sum of every variable should == num matches 
    
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
        drivers.append(Entity("driver", f"0{i}", int(coords[0]), int(coords[1])))
    for i in range(num_riders):
        coords = data.pop(0).split()
        riders.append(Entity("driver", f"0{i}", int(coords[0]), int(coords[1])))
    # for i in drivers:
    #     print(i)
        
    # Solve LP
    solution = match_drivers(drivers, riders)
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
