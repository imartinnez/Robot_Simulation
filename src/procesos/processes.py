import simpy

import op_fuzzy_markov.operations as o
import op_fuzzy_markov.fuzzy as f
import op_fuzzy_markov.weather_markov as w

# @author: Íñigo Martínez Jiménez
def weather(env: simpy.Environment, planet: object):
    """ It is the process in charge of directing the behavior of the weather of the planet.
        It will be changing every 20 units of time in the simulation

    Args:
        env (simpy.Environment): Simulation environment.
        planet (object): The planet being explored.

    Yields:
        simpy.timeout: Represents the time the weather changes in the simulation
    """
    # The planet is going to be active until the simulation is finished
    while env.simulation:
            # The planet change it´s weather every 20 units of time
            yield env.timeout(20)

            # With a Markov Model, we calculate the next weather state
            new_weather = w.planet_weather(planet.weather, planet.weather_states)
            
            # If the weather is different from the past weather state, it will make an advise and update it
            if new_weather != planet.weather:
                print(f"{env.now:5}) | **The weather in the planet has changed to {planet.weather}")
                planet.weather = new_weather

# @author: Íñigo Martínez Jiménez
def explore(env: simpy.Environment, planet: object, robot: object):
    """ It is the process in charge of directing all the behavior
        of the robot explorer. It allows the robot to move and explore new ecosystems.

    Args:
        env (simpy.Environment): Simulation environment.
        planet (object): The planet being explored.
        robot (object): The explorer robot object.
        rec_robot (object): The recollector robot associated with the explorer.
        base (object): The base object.

    Yields:
        simpy.timeout: Represents each unit of time that the robot waits during movement.
    """
    # It is going to be exploring until the simulation is finished
    while env.simulation:
        # We check if the recollector robot is not working and explorer has energy
        if not robot.rec_ocupied and robot.energy > 0:
            # It tooks one unit of time to the robot to do a movement
            yield env.timeout(1) 
            
            # We call the explore method from the robot class
            explore = robot.explore(env, planet)
            
            # If an ecosystem has been found, the explorer nreports the recollector robot about the found ecosystem
            # and waits until he has finished his job
            if explore:
                # We mark the recollector robot as occupied
                robot.rec_ocupied = True  
        else:
            # Explorer robots waits until the recollector robot completes its job
            yield env.timeout(1)


# @author: Íñigo Martínez Jiménez
def recollection(env: simpy.Environment, robot: object, exp_robot: object, planet: object, base: object):
    """ It is the process in charge of directing all the behavior of the harvesting robot. It allows to give it the ability
        to collect an ecosystem as well as to check if there are enough resources to build the base or if it is already built. 
        It also allows to give it the ability on it and the explorer robots to return to the base based on fuzzy rules.

    Args:
        env (simpy.Environment): Simulation environment.
        robot (object): The recollector robot object.
        exp_robot (object): The explorer robot associated with the recollector.
        planet (object): The planet that is being explored.
        base (object): The base to which resources are delivered.

    Raises:
        simpy.Interrupt: Raised when all ecosystems have been visited

    Yields:
        simpy.timeout: Represents the time spent during traveling to ecosystems, collecting resources, or waiting.
    """
    # It is going to be exploring until the simulation is finished
    while env.simulation:
        
        # We check with the fuzzy logic if the explorer or recollector robot must come back to the base to recharge 
        if f.decide(o.normalize(exp_robot.energy, 0, robot.max_energy), exp_robot.position, planet,  robot.base) >= 5 or \
robot.energy < 1:
            print(f"{env.now:5}) {robot.name} and {exp_robot.name} have not enough energy to recollect more resources and explore. Returning to base to charge.")

            # We set the robot to occupied because the are going to be recharging their energy
            exp_robot.rec_ocupied = True

            # It request  the access to the shared base charge station
            with base.charge_st.request() as req:
                # They wait until the resource is available
                yield req 
                
                # Once is avaliable, we call the base's recharge function to recharge both robots
                yield from base.recharge(exp_robot, robot)
            
            # We update both robots' positions to the base after recharging
            robot.position = robot.base
            exp_robot.position = robot.base

            # Then, we let the recollector robot free
            exp_robot.rec_ocupied = False


        # We check the list to see if there are ecosystems to recollect
        if exp_robot.ecos_to_recollect:
            # Takes the position of the last ecosystem that has been reported
            ecosystem_position = exp_robot.ecos_to_recollect.pop(0)

            # This loop allows the robot to recollect resources as long as they remain in the ecosystem
            while True:
                # The recollector robot moves to the ecosystem
                print(f"{env.now:5}) | {robot.energy:>8}% REC_ENERGY - {robot.name} is moving to the ecosystem in {ecosystem_position}.")
                # We update the energy's robot based on the distance of the trip
                robot.energy -= o.manhattan_distance(*ecosystem_position, *robot.position)
                yield env.timeout(o.time_distance(ecosystem_position, robot.position))  # Simulate the time taken for recollection
                robot.position = ecosystem_position

                # We get the ecosystem object of the position and call the recolect method to extract the resources
                ecosystem = planet.box_content(*ecosystem_position)
                recolect = robot.recolect(env, robot, base, ecosystem, planet)

                # This conditional allows the robot to return to the base if mineral capacity is full, if water capacity is full or robot is out of energy
                if (robot.minerals >= robot.capacity // 2 or robot.water >= robot.capacity // 2 or \
robot.energy <= 0 or recolect):

                    # We call the method, so the robot can return to the base
                    yield from robot.back_to_base(env, base)

                # We check if all ecosystems have been visited and  the ecosystem the robot had just recolected is empty
                # if it is, it raise the interrupt exception
                if len(list(set(planet.eco_visited))) == planet.ecosystem_num and not ecosystem.not_empty():
                    env.simulation = False
                    raise simpy.Interrupt(f"  TIME:{env.now} | $$**$$**All ecosystems on the planet have been visited. The base cannot be built.$$**$$**")
                
                # If the ecosystem still has resources, it will continue recollecting, otherwise
                # if the are no more ecosystems, it let the explorer robot free and exit the recollection loop
                if ecosystem.not_empty() and robot.energy > 0:
                    robot.energy -= 10
                    continue
                else:
                    exp_robot.rec_ocupied = False
                    break
        else:
            # The recollector robot waits until new ecosystems are reported
            yield env.timeout(1)