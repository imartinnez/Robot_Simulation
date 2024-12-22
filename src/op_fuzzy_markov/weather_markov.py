import numpy as np

# @author: Íñigo Martínez Jiménez
def planet_weather(weather: str, weather_states: list) -> str:
    """ This method implements a Markov model to predict the weather of the planet

    Args:
        weather (string): actual weather of the planet
        weather_states (list): differnt possibilities of weather

    Returns:
        string: The new weather of the planet
    """
    # Transition matrix, first row 'clear', second row 'stormy', third row 'tornado'
    matrix = np.array([[0.6, 0.3, 0.1], 
                       [0.65, 0.25, 0.1],
                       [0.7, 0.25, 0.05]])
    
    # We take the index of the actual weather state
    weather_index = weather_states.index(weather)

    # Based on the probabilities of the transition matrix, we calculate the new state
    new_weather = np.random.choice(len(weather_states), p = matrix[weather_index])
    
    return weather_states[new_weather]
