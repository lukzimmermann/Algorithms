class Point:
    def __init__(self, x, y, g_cost=float('inf'), h_cost=float('inf')):
        self.x = x
        self.y = y
        self.f_cost = g_cost + h_cost
        self.g_cost = g_cost
        self.h_cost = h_cost
        self.parentPoint:Point = None

    def __repr__(self) -> str:
        return f'{self.x},{self.y}:\tf{round(self.f_cost,2):4}\tg{round(self.g_cost,2):4}\th{round(self.h_cost,2):4}'
    
    def __eq__(self, point: object) -> bool:
        if self.x == point.x and self.y == point.y:
            return True
        else:
            return False

    def updateCost(self, g_cost, h_cost) -> None:
        self.f_cost = g_cost + h_cost
        self.g_cost = g_cost
        self.h_cost = h_cost