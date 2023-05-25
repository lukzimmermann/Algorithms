import AStar
from termcolor import colored
import time

astar = AStar.AStar('pic10.png')
astar.setStartByColor(0, 255, 0)
astar.setEndByColor(255, 0, 0)
#astar.setEndByCoordinate(0, 0)

try:
    #iteration = astar.compute(True, './Record')
    start = time.time()
    iteration = astar.compute()
    path = astar.getPath(drawPath=True)
    
    for item in path:
        print(item)

except Exception as e:
    print(colored(f'Error: {e}', 'red'))