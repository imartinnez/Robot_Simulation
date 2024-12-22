import simpy

# @author: Íñigo Martínez Jiménez
def find_event(robot: object, ecosystem: object, env: simpy.Environment) -> None:
    """Event that occurs when a robot find a new ecosystem.

    Args:
        robot (object): Robot that finds the ecosystem
        ecosystem (object): The ecosystem object being found
        env (simpy.Environment): Simulation environment.
    """
    print(f"{env.now:5}) | {robot.energy:>8}% EXP_ENERGY - {robot.name} has found an ecosystem in {robot.position}: {ecosystem}")
    
    # Change the robot's energy depending on the dificulty of each ecosystem
    # considering that energy cannot go below 0
    if (robot.energy - ecosystem.dificulty) < 0:
        robot.energy = 0
    else: 
        robot.energy -= ecosystem.dificulty

# @author: Íñigo Martínez Jiménez
def recolect_event(robot: object, ecosystem: object, planet: object, env: simpy.Environment) -> None:
    """Event that occurs when a recollector robot recollect resources from the discovered ecosystem.

    Args:
        robot (object): The recollector robot that is going to extract the resources.
        ecosystem (object): The ecosystem that is going to be recollected.
        planet (object): The planet object.
        env (simpy.Environment): Simulation environment.
    """
    # We call the ecosystem method to extract from it their resources
    minerals, water = ecosystem.extract_materials(robot)

    # We update the robot's inventory
    robot.minerals += minerals
    robot.water += water

    print(f"{env.now:5}) | {robot.energy:>8}% REC_ENERGY - {robot.name} recolected {minerals} minerals and {water} of water.")

    # Change the robot's energy depending on the dificulty of each ecosystem and
    # also depending on the weather of the planet, the robot will decrements it´s
    # energy more or less considering that energy cannot go below 0 
    if (robot.energy - ecosystem.dificulty*8) < 0:
        robot.energy = 0
    else:
        robot.energy -=  1 * (planet.weather_states.index(planet.weather) + 1)
        robot.energy -= ecosystem.dificulty*8