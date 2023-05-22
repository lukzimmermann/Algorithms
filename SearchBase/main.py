import AStar
from termcolor import colored

astar = AStar.AStar('pic5.png')
astar.setStartByColor(0, 255, 0)
astar.setEndByColor(255, 0, 0)

try:
    #iteration = astar.compute(True, './Record')
    iteration = astar.compute(True)
    print(f'Iteration: {iteration}')
except Exception as e:
    print(colored(f'Error: {e}', 'red'))