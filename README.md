# Planetary Exploration and Collection Simulation with Robots

This project implements a simulation focused on planetary exploration and resource collection using autonomous robots. The main goal is to optimize the construction of a planetary base by minimizing the required time while efficiently managing energy and robot activities.

## Main Features
### 1. Main Components

Explorer Robots: Locate ecosystems within the planet.

Collector Robots: Collect resources and manage their energy capacity.

Base: Manages collected materials and provides charging stations.

Planet: Represented as a 2D grid with randomly generated ecosystems.

Ecosystems: Contain resources (water and minerals) and have a difficulty level that affects the robots' energy consumption.
### 2. Processes

Weather: Modeled using a Markov model to simulate changing conditions every 20 seconds.

Exploration: Explorer robots move randomly searching for ecosystems.

Collection: Collector robots collect resources and report back to the base.
### 3. Intelligent Decisions

Fuzzy Logic: Implemented to determine whether robots should return to the base to recharge.

Markov Model: Predicts the weather, affecting performance and energy consumption.
### 4. Optimization with PSO

A Particle Swarm Optimization (PSO) algorithm is used to optimize the base construction time, evaluating parameter combinations such as the number of robots and costs.

## Project Structure

The project is organized into several modules:

ANALYSIS: Contains code for analyzing parameter combinations of the PSO.

ENTITIES: Includes classes representing system elements such as planets, ecosystems, and robots.

EVENTS: Defines and manages events occurring during the simulation.

OP FUZZY MARKOV: Implements fuzzy logic and the Markov model.

PROCESSES: Defines the exploration and collection processes.

VIRT_ENV: Virtual environment for managing dependencies.

The main file is app.py, which runs the simulation.

## Requirements

Python 3.8 or higher.

Libraries specified in requirements.txt.

## Execution Instructions

Clone this repository:

git clone [https://github.com/imartinnez/Robots_Simulation]
cd your-repository

Create and activate a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Run the simulation:

python app.py

## Code Structure

    CODIGO/analysis.ipynb: Contains the analysis of PSO parameters.
    CODIGO/pso.py: Implements the PSO algorithm.
    CODIGO/entities/: Classes for entities like robots and ecosystems.
    CODIGO/events/: Event management system.
    CODIGO/fuzzy_markov/: Implementation of fuzzy logic and Markov model.

## Simulation Output

The simulation generates a detailed log with:

    Time in days for each action.
    Robots' energy status.
    Collected resources and events that occurred.

## Credits

Developed by Iñigo Martínez as part of an AI project.
