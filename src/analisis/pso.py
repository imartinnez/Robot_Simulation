import numpy as np
import pandas as pd
from pyswarm import pso
from itertools import product
import sys

sys.path.append("./")

import app as s

# @author: Íñigo Martínez Jiménez
def fitness(x: np.array) -> float:
    """Fitness function for optimize the time of construction of the base.

    Args:
        x (np.array): N-dimensional candidate solution to evaluate.

    Returns:
        float: Fitness value
    """
    # We unpuck the limits that have been chosen
    num_robots, planet_size = x

    max_num_robots = 20
    penalty = 0

    # Here we run the simulation to get the outputs that we are going to analize
    time, b_constructed = s.run_simulation(int(num_robots), int(planet_size))

    # If the base has not been constructed, we add a penalty to the function
    if not b_constructed:
        penalty = 10000000

    # We calculate the cost and the maximum cost of the robots
    cost = num_robots * 8
    max_cost = max_num_robots * 8

    # Fitness function
    return (time + ((max_cost / cost) * 2) + num_robots * 0.3 + penalty)


# @author: Íñigo Martínez Jiménez
def pso_opt(fitness: float, swarmsize: np.array, omega: np.array, phip: np.array, phig: np.array, max_iter: np.array) -> pd.DataFrame:
    """PSO analysis with Cartesian product 

    Args:
        fitness (np.array): Objective function
        swarmsize (np.array): Number of particles
        omega (np.array): Inertia coeficient
        phip (np.array): Cognitive aceleration coeficient
        phig (np.array): Social aceleration coeficient
        max_iter (np.array): Maximun number of PSO generations

    Returns:
        pd.DataFrame: Results of the cartesian product
    """
    
    dataframe = pd.DataFrame()
        
    # Iterations counter
    i = 1 
    
    # We use the itertools library to do the cartesian product of the PSO algorithm
    for c in product(swarmsize, omega, phip, phig, max_iter):
        
        # We unpack the different combinations
        swarmsize, omega, phip, phig, max_iter = c
        
        
        # The number of robots and the size of the planet that 
        # are the lower and upper bounds
        lb = [2, 15]   
        ub = [20, 40]  
        
        # This will return a tuple with to values, xopt that is the optimal input values,
        # and fopt, that is the objective function value, in other words, the fitness value
        xopt, fopt = pso(fitness, lb, ub, swarmsize=swarmsize, omega=omega, phip=phip, phig=phig, maxiter=max_iter)
        
        print(f'[iteration {i}] Parameters: particles {swarmsize} | omega {omega} \
phip {phip} | phig {phig} | max_iter: {max_iter} | fopt {fopt}')
        
        # We generate the dataframe putting the parameters and the result of this iteration
        data = pd.DataFrame.from_dict({
            'particles': [swarmsize], 
            'omega': [omega],
            'phip': [phip], 
            'phig': [phig], 
            'max_iter': [max_iter],
            'Best solution': [xopt],
            'Fitness value': [fopt]
        })
        
        # Then, we concat the dataFrame to all the results 
        dataframe = pd.concat([dataframe, data])
        i += 1

    return dataframe

if __name__=="__main__":

    # We set the range of the PSO parameters
    swarmsize = [15, 25]
    omega = [0.45, 0.75]
    phip = [1.5, 1.75, 2]
    phig = [1.5,1.75, 2]  
    max_iter = [5, 10]
    
    # We calculate de cartesian product of the PSO algorithm
    dataframe = pso_opt(fitness, swarmsize, omega, phip, phig, max_iter)

    # Finally, we save the results in a .csv
    dataframe.to_csv('./analisis/dataframe.csv', index=False)