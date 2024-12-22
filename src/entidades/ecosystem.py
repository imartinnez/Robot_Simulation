# @author: Íñigo Martínez Jiménez
class Ecosystem:
    def __init__(self, name: str, minerals: int, water: int, dificulty: int) -> None:
        """ Constructor

        Attributes:
            name (str):  Ecosystem name.
            minerals (int): Amount of minerals that are in the ecosystem.
            water (int): Amount of water that are in the ecosystem.
            dificulty (int): Dificulty by exploring the ecosystem.
            reserved (bool): Indicates if the ecosystem is reserved for extraction.
        """
        self._name = name
        self._minerals = minerals
        self._water = water
        self._dificulty = dificulty
        self._reserved = False

    @property
    def name(self) -> str:
        """Name getter

        Returns:
            str: Name attribute
        """
        return self._name

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
    def water(self, value: int) -> None:
        """Water setter

        Args:
            value (int): Updated water value
        """
        self._water = value

    @property
    def dificulty(self) -> int:
        """Dificulty getter

        Returns:
            int: Dificulty attribute
        """
        return self._dificulty

    # @author: Íñigo Martínez Jiménez
    def extract_materials(self, robot: object) -> tuple[int, int]:
        """ Extracts minerals and water from the ecosystem.

        Args:
            robot (object): A recollector robot that extract the resources.

        Returns:
            tuple[int, int]: The extracted minerals and water as a tuple.
        """
        # We set the avaible capacity for each resource, being equally for the two of them
        minerals_cuantity = robot.capacity // 2
        water_cuantity = robot.capacity // 2

        # We set the resources that the robot recollect, contrainted by the resources he alredy has
        extracted_minerals = min(self._minerals, minerals_cuantity - robot.minerals)
        extracted_water = min(self._water, water_cuantity - robot.water)
        
        # Update the ecosystem´s resources
        self._minerals -= extracted_minerals
        self._water -= extracted_water
        
        return extracted_minerals, extracted_water

    # @author: Íñigo Martínez Jiménez
    def not_empty(self) -> bool:
        """ Confirm if the ecosystem is empty

        Returns:
            bool: True if the ecosystem has resources, False if it is not.
        """
        if self._minerals == 0 and self._water == 0:
            return False
        else:
            return True

    # @author: Íñigo Martínez Jiménez
    def __str__(self) -> str:
        """ Representation of the Ecosystem with words.

        Returns:
            str: Ecosystem details in a string.
        """
        return f"Ecosystem {self._name} (Minerals: {self._minerals}, \
Water: {self._water}, Difficulty: {self._dificulty})"