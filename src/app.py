# SIMULACIÓN DE ROBOTS PLANETARIA
# Authors: Íñigo Martínez Jiménez

# Inteligencia Artificial
# Ingeniería Informática
# CUNEF Universidad

import simpy

import entidades.planet as p
import entidades.base as b
import entidades.robots as r
import procesos.processes as pR

# @author: Íñigo Martínez Jiménez
def run_simulation(num_robots: int, planet_size: int, max_energy: int = 100, obj_minerals: int = 500, obj_water: int = 1500) -> None:
    """ This method carries the entire simulation of the code. It initialises both the processes and the simulation environment.

    Args:
        num_robots (int): The number of pairs that will be exploring the planet.
        planet_size (int): The size of the planet.
        max_energy (int): The maximum energy capacity that the robots have.

    Returns:
        int: The unit of time when the simulation has stopped
        bool: True if the base has been constructed, False otherwise
        
    """
    # We create the simulation environment, the shared resource and the variable that is
    # going to help us to know if the simulation is still running
    env = simpy.Environment()
    charge_st = simpy.Resource(env, capacity = 10)
    env.simulation = True

    # We create a list to store the robot pairs
    r_pairs = []
    
    # We instantiate the planet, the base of the planet and we generate the map
    planet = p.Planet("Ubuntu Centauri", planet_size)
    base = planet.place_base(b.Base(obj_minerals, obj_water, env, charge_st))
    planet.generate_map()

    # We initialize each robot, giving to them an identification and nd associating
    # each one with his pair
    for x in range(1, num_robots + 1):
        explorer = r.Explorer_Robot(planet, f"Explorer {x}", max_energy)
        recollector = r.Recollector_Robot(planet, f"Recolector {x}", max_energy)

        r_pairs.append([explorer, recollector])

    # We launch the weather process
    env.process(pR.weather(env, planet))

    # We launch the robot's process taking into account each pair of robots
    for explorer, recollector in r_pairs:
        env.process(pR.explore(env, planet, explorer))
        env.process(pR.recollection(env, recollector, explorer, planet, base))
    

    # We run the simulation taking into account the exceptions we have 
    # instantiated throughout the code, in order to handle interrupts.
    try:
        env.run()
    except simpy.Interrupt as end:
        print(f"{end}")


    return env.now, base.constructed



if __name__ == "__main__":
    
    # Here we can try as many simulations as we want by varying the parameters.
    run_simulation(num_robots = 100, planet_size = 20)