"""
A script that matches driver and rider coordinates given in a text file
such that all drivers are matched and the total pickup time 
(ie, Manhattan distance) is minimized. 


LP Formulation:

Let there be n > 0 drivers and m > 0 riders placed on a 2-D grid. 

MINIMIZE 
For all i in range (1...n) and j in range (1...m)
x_ij * (distance_ij) 
SUCH THAT
x_i1 + x_i2 + x_i3 + ... = 1, 
x_1j + x_2j + x_3j + ... = 1, 
x_11 + x_12 + ... + x_ij = min(n, m)

Where distance_ij is the Manhattan distance between driver i and rider j,
(|x_driver - x_rider| + |y_driver - y_rider|)
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


def match_drivers(drivers : List[Entity], riders: List[Entity]) -> None:
    """
    Attempts to match all drivers to customers, minimizing the total distance traveled. 
    One driver will be matched to one rider. Prints matches. 

    drivers -- List of drivers to be matched
    riders -- List of riders to be matched
    """
    objective = []
    num_matches = min(len(drivers), len(riders))
    vars = []
    driver_constraints = [] # Each item is all the variables associated with one driver 
    rider_constraints = [] # Each item is all the variables associated with one rider 
    match_constraint_vars = [] # Contains every variable
    
    # Populate matrix of variables
    for i in range(len(drivers)):
        row = []
        for j in range(len(riders)): 
            row.append(LpVariable(name=f"0{i}_0{j}", lowBound=0, cat="Integer"))
        vars.append(row)

    # Driver constraints
    for i in range(len(drivers)):
        d_constraints = []
        driver = drivers[i]
        for j in range(len(riders)): 
            rider = riders[j]
            x = vars[i][j]
            d_constraints.append(x)
            match_constraint_vars.append(x) 
            distance = driver.distance_from(rider.x, rider.y)
            objective.append((x, distance))
        driver_constraints.append(d_constraints)
    
    # Rider constraints
    for i in range(len(riders)):
        rider = riders[i]
        r_constraints = []
        for j in range(len(drivers)):
            driver = drivers[j]
            x = vars[j][i]
            distance = driver.distance_from(rider.x, rider.y)
            r_constraints.append(x)
            objective.append((x, distance))
        rider_constraints.append(r_constraints)

    # Plug into LP solver
    lp = LpProblem("Match_Drivers", LpMinimize)
    lp += lpSum([i[0] * i[1] for i in objective]) 

    # Add constraint: each driver or rider is only matched once
    for i in range(len(driver_constraints)):
        driver = driver_constraints[i]
        constraint = lpSum([d for d in driver]) 
        lp += (constraint <= 1, f"driver_constraint_{i}")
    for i in range(len(rider_constraints)):
        rider = rider_constraints[i]
        constraint = lpSum([r for r in rider])
        lp += (constraint <= 1, f"rider_constraint_{i}")
        
    # Add constraint: Total number of matches 
    match_constraint = lpSum([i for i in match_constraint_vars]) 
    lp += (match_constraint >= num_matches, "num_total_matches")
    
    # Solve
    print("\nMatches (driver_rider): ")
    for var in lp.variables():
        if value(var) == 1.0:
            print(var)
    print(f"Total pick-up time: {value(lp.objective)}")


def main(input_file_name : str) -> None:
    # Parse file data 
    with open(input_file_name, "r") as file:
        data = file.readlines()
        num_drivers = int(data.pop(0))
        num_riders = int(data.pop(0))
    drivers = []
    riders = []
    for i in range(num_drivers):
        coords = data.pop(0).split()
        drivers.append(Entity("driver", f"0{i}", int(coords[0]), int(coords[1])))
    for i in range(num_riders):
        coords = data.pop(0).split()
        riders.append(Entity("driver", f"0{i}", int(coords[0]), int(coords[1])))

    # Solve    
    match_drivers(drivers, riders)


if __name__ == "__main__":
    main(sys.argv[1])
