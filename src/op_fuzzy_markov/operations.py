# @author: Íñigo Martínez Jiménez
def normalize(x: int, x_min: int, x_max: int) -> float:
    """ This method allows us to normalize a number

    Args:
        x (int): value we want to normalize
        x_min (int): minimum limit
        x_max (int): maximum limit

    Returns:
        float: The number normalized
    """
    return ((x - x_min) / (x_max - x_min)) * 10

# @author: Íñigo Martínez Jiménez
def manhattan_distance(x1: int, y1: int, x2: int, y2: int) -> int:
    """This method allows us to calculate the manhattan distance between two points

    Args:
        x1 (int): x coordenate for the first point
        y1 (int): y coordenate for the first point
        x2 (int): x coordenate for the second point
        y2 (int): y coordenate for the second point

    Returns:
        int: The manhattan distance
    """
    return (abs(x1 - x2) + abs(y1 - y2))

# @author: Íñigo Martínez Jiménez
def time_distance(d1: tuple[int, int], d2: tuple[int, int]):
    """ This method allows us to calculate the time it takes to travel
        between two points 

    Args:
        d1 (tuple[int, int]): The first point
        d2 (tuple[int, int]): The second point

    Returns:
        int: The units of time that takes to travel between two points
    """
    return manhattan_distance(*d1, *d2)