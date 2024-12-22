import simpy
import random

import entidades.ecosystem as e
import eventos.events as events
import op_fuzzy_markov.operations as o


# @author: Íñigo Martínez Jiménez
class Robot:
    def __init__(self, planet: object, name: str, max_energy: int) -> None:
        """Constructor

        Attributes:
            planet (object): The planet where the robot works on.
            name (str): Robot name.
            max_energy (int): The robot's maximum energy .
            energy (int): The robot's energy level.
            base (tuple): Position of the base, that it is always at the centre of the map.
            position (tuple): The robot's position.
            capacity (int): The biggest capacity of the robot (1/2 for water & 1/2 for minerals).
            movements (int): The total of movements that are made by the robot in a try.
            visited_places (set): Visited positions for not explorating it twice.
        """
        self.planet = planet
        self._name = name
        self._max_energy = max_energy
        self._energy = max_energy
        self._base = (planet.size // 2, planet.size // 2)
        self._position =  self.base
        self._capacity = 200
        self.movements = 0


    @property
    def name(self) -> str:
        """Name getter

        Returns:
            str: Name attribute
        """
        return self._name

    @property
    def max_energy(self) -> int:
        """Max_energy getter

        Returns:
            int: Max_energy attribute
        """
        return self._max_energy

    @property
    def energy(self) -> int:
        """Energy getter

        Returns:
            int: Energy attribute
        """
        if self._energy < 0:
            return 0
        else:
            return self._energy
        

    @energy.setter
    def energy(self, value: int) -> None:
        """Energy setter

        Args:
            value (int): Updated energy value
        """
        if value < 0:
            self._energy = 0
        else:
            self._energy = value

    @property
    def base(self) -> int:
        """Base getter

        Returns:
            tuple[int, int]: Base attribute
        """
        return self._base

    @property
    def position(self) -> tuple[int, int]:
        """Positon getter

        Returns:
            tuple[int, int]: Position attribute
        """
        return self._position

    @position.setter
    def position(self, new_position: tuple[int, int]) -> None:
        """Position setter

        Args:
            new_position (tuple[int, int]): Updated position attribute
        """
        self._position = new_position

    @property
    def capacity(self) -> int:
        """Capacity getter

        Returns:
            int: Capacity attribute
        """
        return self._capacity

    # @author: Íñigo Martínez Jiménez
    def move(self, env: simpy.Environment) -> tuple[int, int]:
        """Moves the robot position.

        Args:
            env (simpy.Environment): Simulation enviroment.

        Returns:
            tuple[int, int]: The new position.
        """
        # Maximum movements attempts
        max_movements = 4 
        movements = 0
        
        # Possible movement directions
        directions = ["N", "S", "E", "W"]

        while movements < max_movements:
            
            x, y = self._position
            # We select a random direction
            direction = random.choice(directions) 
            # And remove the chosen direction to avoid repetition
            directions.remove(direction)
            

            # Update the position
            if direction == "N" and x > 0:
                x -= 1
            elif direction == "S" and x < self.planet.size - 1:
                x += 1
            elif direction == "E" and y < self.planet.size - 1:
                y += 1
            elif direction == "W" and y > 0:
                y -= 1
            else:
                # We increment the attempt variable for invalid moves
                movements += 1 
                # Retry
                continue
            
            # Define the new position
            new_position = (x, y)
                
            print(f"{env.now:5}) | {self._energy:>8}% EXP_ENERGY - {self._name} is moving from {self._position} to {new_position}.")
            self._position = new_position
            self.movements += 1
            # Depending on the weather of the planet, the robot will decrements it´s energy more or less
            self._energy -= 1 * (self.planet.weather_states.index(self.planet.weather) + 1)
                
            break
    
        return self._position

    # @author: Íñigo Martínez Jiménez
    def verify_energy(self) -> bool:
        """See if the robot can continue operating due to his batery.

        Returns:
            bool: False if energy is not greater than 0, True otherwise.
        """
        if (self._energy <= 0):
            return False
        return True


# @author: Íñigo Martínez Jiménez
class Explorer_Robot(Robot):

    def __init__(self, planet: object, name: str, max_energy: int) -> None:
        """ Constructor

        Attributes:
            ecos_to_recollect (list): Positions of ecosystems reported for resource recollection.
            rec_ocupied (bool): Indicates if a recollector robot is assigned to the robot's ecosystem.
        """
        super().__init__(planet, name, max_energy)
        self._ecos_to_recollect = []
        self.rec_ocupied = False

    @property
    def ecos_to_recollect(self) -> list[tuple[int, int]]:
        """ Ecos_to_recollect getter

        Returns:
            list[tuple[int, int]]: Ecos_to_recollect attribute
        """
        return self._ecos_to_recollect

    # @author: Íñigo Martínez Jiménez
    def explore(self, env: simpy.Environment, planet: object) -> bool:
        """ Explores the planet moving through it

        Args:
            env (simpy.Environment): Simulation environment.
            planet (object): The planet object.
            recollector_Robot (object): The associated recollector robot.

        Returns:
            bool: True if explorer has found an ecosystem successfully
        """
        if self.verify_energy():
            # The robot call the move() method to go to a new position
            new_position = self.move(env)
            
            if new_position != self.base:
                # We call the box_content() method that allows the robot to see if the cell is an ecosystem
                # To separate the coordinates of the position of the robot we put the * before the argument
                place = self.planet.box_content(*new_position)
                

                # It checks if the content is an ecosystem object
                if isinstance(place, e.Ecosystem):
                    # If it's in the global ecosystem list it has been visited
                    if new_position in planet.eco_visited:
                        print(f"{env.now:5}) | {self._energy:>8}% EXP_ENERGY - {self._name} is in an ecosystem in {new_position} but it has been already visited.")
                        return False
                    else:
                        # We call the find ecosystem event
                        events.find_event(self, place, env)
                        
                         # We register the ecosystem  in the globally list and in the recollection list
                        planet.register_ecosystem(new_position) # Register the ecosystem globally
                        self._ecos_to_recollect.append(new_position) # Mark for recollection
                            
                        
                        print(f"{env.now:5}) | {self._energy:>8}% EXP_ENERGY - {self._name} report ecosystem for recolect.")            
                        return True
                else:
                    # The content of the cell is empty
                    return False
            else:
                # The robot is in the base
                return False
        else:
            # The robot has no energy
            return False

# @author: Íñigo Martínez Jiménez
class Recollector_Robot(Robot):
    
    def __init__(self, planet: object, name: str, max_energy: int) -> None:
        """ Constructor

        Attributes:
            explorer_Robot (object): The associated explorer robot.
            water (int):  Amount of water that are recollected by the explorer.
            minerals (int):  Amount of minerals that are recollected by the explorer.
        """
        super().__init__(planet, name, max_energy)
        self._water = 0
        self._minerals = 0


    @property
    def minerals(self) -> int:
        """Minerals getter

        Returns:
            int: Minerals attribute
        """
        return self._minerals

    @minerals.setter
    def minerals(self, value: int) -> None:
        """Minerals setter

        Args:
            value (int): Updated minerals value
        """
        self._minerals = value

    @property
    def water(self) -> int:
        """Water getter

        Returns:
            int: Water attribute
        """
        return self._water

    @water.setter
    def water(self, value: int)-> None:
        """Water setter

        Args:
            value (int): Updated water value
        """
        self._water = value

    # @author: Íñigo Martínez Jiménez
    def recolect(self, env: simpy.Environment, robot: object, base: object, ecosystem: object, planet: object) -> bool:
        """ Method that allows the robot to recollect resources from an ecosystem and check if the base can be built.

        Args:
            env (simpy.Environment): Simulation environment.
            robot (object): The recollector robot.
            base (object): The base being constructed.
            ecosystem (object): The ecosystem being recollected.
            planet (object): The planet object.

        Returns:
            bool|None: Whether the base can be built or if collection stops.
        """
        # Stop collection if there is no energy
        if self.verify_energy():
            # We call recollection event
            events.recolect_event(robot, ecosystem, planet, env)

            # Check if the base can be built and return True if construction is successful
            if base.verify_construction(env, robot):
                return True
            else:
                return False
        else:   
            return False
        
    # @author: Íñigo Martínez Jiménez
    def back_to_base(self, env: simpy.Environment, base: object):
        """ Method to return to the base to unload collected resources from the ecosystem.

        Args:
            env (simpy.Environment): Simulation environment.
            base (object): The base object.

        Raises:
            simpy.Interrupt: Raised when the base can be constructed.

        Returns:
            None

        Yields:
            simpy.timeout: Is the time spent during the trip to the base.
        """
        print(f"{env.now:5}) | {self.energy:>8}% REC_ENERGY - {self.name} is returning to the base to unload resources.")
        # We simulate the time the robot that the robot needs to go back to the base
        # calculating the manhattan distance between them
        yield env.timeout(o.time_distance(self.position, self.base))

        # We deduct the energy of the robot depending as well on the manhattan distance
        # because we asummed that each unit of distance is a movement for the robot
        self.energy -= o.manhattan_distance(*self.position, *self.base)
        self.position = self.base

        # Unload the resources at the base
        base.tot_minerals += self.minerals
        base.tot_water += self.water
        print(f"{env.now:5}) | {self.energy:>8}% REC_ENERGY - {self.name} unloaded {self.minerals} minerals and {self.water} water at the base.")
        print(f"{env.now:5}) | **Accumulated resources in the base: Minerals: {base.tot_minerals}, Water: {base.tot_water}")
        
        # We update the actual resources of the robot       
        self.minerals = 0
        self.water = 0

        # We check if the base han been alredy constructed, if it is, it raise the interrupt exception
        if base.constructed and not env.simulation:
            raise simpy.Interrupt(f"  TIME:{env.now} | $$**$$**BASE SUCCESSFULLY BUILT.$$**$$**")
        else:
            return None