import Point
import AStar
from termcolor import colored
from operator import attrgetter



points = [
    Point.Point(4, 9, 10, 20),
    Point.Point(44, 54, 20, 20),
    Point.Point(4, 9, 5, 10),
    Point.Point(43, 12, 25, 5),
]

points = sorted(points, key=attrgetter('f_cost', 'g_cost'))



astar = AStar.AStar('pic5.png')
astar.setStartByColor(0, 255, 0)
astar.setEndByColor(255, 0, 0)


try:
    iteration = astar.compute(True, './Record')
    print(f'Iteration: {iteration}')
except Exception as e:
    print(colored(f'Error: {e}', 'red'))

