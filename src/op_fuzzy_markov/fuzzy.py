import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

import op_fuzzy_markov.operations as o

# @author: Íñigo Martínez Jiménez

# We create the fuzzy variables by defining the ranges of each one of them
energy = ctrl.Antecedent(np.arange(0, 11, 1), 'energy')
distance = ctrl.Antecedent(np.arange(0, 11, 1), 'distance')
decision = ctrl.Consequent(np.arange(0, 11, 1), 'decision') 

# We create the membership functions of energy
energy['very_low'] = fuzz.trimf(energy.universe, [0, 0, 3])  
energy['low'] = fuzz.trimf(energy.universe, [2, 5, 7])      
energy['high'] = fuzz.trimf(energy.universe, [6, 10, 10])   

# We create the membership functions of distance
distance['close'] = fuzz.trimf(distance.universe, [0, 0, 4]) 
distance['far'] = fuzz.trimf(distance.universe, [3, 10, 10])  

# We create the membership functions of decisison
decision['continue'] = fuzz.trimf(decision.universe, [0, 2, 5])  
decision['return'] = fuzz.trimf(decision.universe, [5, 8, 10])   

# We create our fuzzy relationships between each variable from the rules that define the logic we want to implement
rule1 = ctrl.Rule(energy['very_low'] & distance['close'], decision['return'])
rule2 = ctrl.Rule(energy['very_low'] & distance['far'], decision['return'])
rule3 = ctrl.Rule(energy['low'] & distance['close'], decision['continue'])  
rule4 = ctrl.Rule(energy['low'] & distance['far'], decision['return'])
rule5 = ctrl.Rule(energy['high'] & distance['close'], decision['continue'])  
rule6 = ctrl.Rule(energy['high'] & distance['far'], decision['continue'])

# We create and simulate de control system
decision_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6])
decision = ctrl.ControlSystemSimulation(decision_ctrl)


# @author: Íñigo Martínez Jiménez
def decide(energy: float, position: int, planet: object, base: tuple[int, int]) -> float:
    """ Method that calculates the number that represents the decision that the robot
        is going to make

    Args:
        energy (float): energy of the robot
        position (int): position of the robot
        planet (object): planet object
        base (tuple[int, int]): the base object of the planet

    Returns:
        float: The number that represents the decision
    """
    # We calculate the manhattan distance between the robot position and the base, 
    # then we normalize this distance.
    distance = o.normalize(o.manhattan_distance(*position, *base), 0 , planet.size)

    # We pass the input of the variables to the ControlSystem using labels 
    decision.input['energy'] = energy
    decision.input['distance'] = distance

    # It computes the calculations
    decision.compute()

    return decision.output['decision']