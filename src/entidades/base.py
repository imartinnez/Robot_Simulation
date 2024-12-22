import simpy

import op_fuzzy_markov.operations as o

# @author: Íñigo Martínez Jiménez
class Base:
    def __init__(self, minerals: int, water: int, env: simpy.Environment, charge_st: simpy.Resource) -> None:
        """ Constructor

        Attributes:
            env (simpy.Environment):  Simulation environment.
            charge_st (simpy.Resource): A SimPy resource to synchronize the recharge of the robots,
            with the 20% capacity of the amount of robots.
            resources (dict): A dictionary to put the accumulated resources,
            minerals/water (initialized to 0)
            resources_obj (dict): dictionary for the required resources to build the base.
            constructed (bool): A boolean that indicates if the base is been constructed
        """
        self.env = env
        self.charge_st = charge_st  
        self._resources = {"minerals": 0, "water": 0}
        self._resources_obj = {"minerals": minerals, "water": water}
        self._constructed = False
    

    @property
    def tot_minerals(self) -> int:
        """Tot_minerals getter

        Returns:
            int: Minerals value
        """
        return self._resources["minerals"]

    @tot_minerals.setter
    def tot_minerals(self, value: int) -> None:
        """Tot_minerals setter

        Args:
            value (int): Updated minerals value
        """
        self._resources["minerals"] = value


    @property
    def tot_water(self) -> int:
        """Tot_water getter

        Returns:
            int: Water value
        """
        return self._resources["water"]

    @tot_water.setter
    def tot_water(self, value: int) -> None:
        """Tot_water setter

        Args:
            value (int): Updated water value
        """
        self._resources["water"] = value


    @property
    def constructed(self) -> bool:
        """Constructed getter

        Returns:
            bool: Constructed attribute
        """
        return self._constructed
    

    # @author: Íñigo Martínez Jiménez
    def verify_construction(self , env: simpy.Environment, rec_robot: object):
        """ Methot that check if the base has the resources for being built.

        Args:
            env (simpy.Environment): Simulation environment
            rec_robot (object):recollector robot (recolect the ecosystems)

        Returns:
            bool: True if the base can be built, false if not.
        """
        if (self.tot_minerals + rec_robot.minerals >= self._resources_obj["minerals"] and \
self.tot_water + rec_robot.water >= self._resources_obj["water"]):
                    
                    # If a robot verify that the base can be built, it warns that the resources are available for building it.
                    if not self._constructed:
                        print(f"{env.now:5}) | **ALL RESOURCES ARE READY TO BUILD THE BASE!!!")

                    self._constructed = True 

                    # We change the state of the simulation flag to stop the running processes.
                    env.simulation = False 
                    return True
    
    
    # @author: Íñigo Martínez Jiménez
    def recharge(self, exp_robot, rec_robot):
        """ Recharge method of the robot explorer and recollector in the base.

        Args:
            ex_robot (_type_): Explorer robot that has to be recharged.
            rec_robot (_type_): Recollector robot that has to be recharged.

        Yields:
            simpy.timeout: Time for the recharged process.
        """
        yield self.env.timeout(o.time_distance(exp_robot.position, exp_robot.base))
        
        print(f"{self.env.now:5}) {exp_robot.name} and {rec_robot.name} are starting to recharge at the base.")

        #  It calculates the recharge time based on robot's maximum energy
        recharge_time = exp_robot.max_energy // 10
        # The robots wait until they are charged
        yield self.env.timeout(recharge_time)

        # We update the robots energy to their maximum capacity
        exp_robot.energy = exp_robot.max_energy
        rec_robot.energy = rec_robot.max_energy

        print(f"{self.env.now:5}) {exp_robot.name} and {rec_robot.name} have finished recharging.")