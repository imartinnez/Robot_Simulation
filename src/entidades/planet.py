import simpy
import random
import math
import numpy

import entidades.ecosystem as e
import op_fuzzy_markov.weather_markov as m

# @author: Íñigo Martínez Jiménez
class Planet:
    def __init__(self, name: str, size: int) -> None:
        """ Constructor

        Attributes:
            name (str): The identity of the planet.
            size (int): Attribute that contains the size.
            map (list): A 2D list representing the grid of the planet, 
            where each cell contains a base object, an ecosystem object or an empty space (“*”).
            eco_visited (list): A list of tuples that represent the positions of the ecosystems that are visited.
            ecosystem_num (int): Attribute that contains the number of ecosystems on the planet.
        """
        self._name = name   
        self._size = size
        self.map = [[["*"] for col in range(size)] for row in range(size)]
        self._eco_visited = [] 
        # 20% of the total grid cells are used to calculate the numer of ecosystem
        self._ecosystem_num = math.trunc((size * size)* 0.2)
        self._weather_states = ["clear", "stormy", "tornado"]
        self._weather = random.choice(self.weather_states)


    @property
    def name(self) -> str:
        """Name getter

        Returns:
            str: Name attribute
        """
        return self._name

    @property
    def size(self) -> int:
        """Size getter

        Returns:
            int: Size attribute
        """
        return self._size
    
    @property
    def eco_visited(self) -> str:
        """Eco_visited getter

        Returns:
            list: Eco_visited attribute
        """
        return self._eco_visited
    
    @property
    def ecosystem_num(self) -> str:
        """Ecosystem_num getter

        Returns:
            list: Ecosystem_num attribute
        """
        return self._ecosystem_num
    
    @property
    def weather(self) -> str:
        """Weather getter

        Returns:
            string: Weather attribute
        """
        return self._weather
    
    @weather.setter
    def weather(self, value: str) -> None:
        """Energy setter

        Args:
            value (str): Updated weather value
        """
        self._weather = value

    @property
    def weather_states(self) -> str:
        """Weather getter

        Returns:
            string: Weather attribute
        """
        return self._weather_states


    # @author: Íñigo Martínez Jiménez
    def generate_map(self) -> None:
        """ Method that generates the matrix that acts as a map and placing ecosystems
           randomly on the matrix with randomly properties.
        """
        for i in range(self._ecosystem_num):
            # Generate random atributes for the ecosystem with certain levels
            minerals = random.randint(0, 40)
            water = random.randint(0, 120)
            dificulty = random.randint(1, 5)

            # Initializes each ecosystem with its corresponding attributes
            ecosystem = e.Ecosystem(f" {i+1}", minerals, water, dificulty)

            # Place the ecosystem in a random selected empty cell cheking if the cell is empty (Line 65)
            while True:
                x = random.randint(0, self.size - 1)
                y = random.randint(0, self.size - 1)
                if (self.map[x][y] == ["*"]):
                    self.map[x][y] = ecosystem
                    break
    
    # @author: Íñigo Martínez Jiménez
    def place_base(self, base: object) -> None:
        """ Initialize the base of the planet

        Args:
            base (object): Base of the planet
        """
        # Place the base at the center of the map
        self.map[self.size // 2][self.size // 2] = base

        return base

    # @author: Íñigo Martínez Jiménez
    def register_ecosystem(self, position: tuple[int, int]) -> None:
        """ Method that ads an ecosystem to the global list when the ecosystem is visited

        Args:
            position (tuple[int, int]): The (x, y) position of the ecosystem.
        """
        self._eco_visited.append(position)
        
    # @author: Íñigo Martínez Jiménez
    def box_content(self, x: int, y: int) -> object:
        """ Returns the content of a given cell of the planet

        Args:
            x (int): The row index of the cell.
            y (int): The column index of the cell.

        Returns:
            object: The content of the cell (Base, Ecosystem, or "*").
        """
        return self.map[x][y]