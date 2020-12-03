DIRECTIONS_SIGNS = ["D", "U", "L", "R"]

DIRECTIONS_TUPLES = {
    "D": (1, 0),
    "U": (-1, 0),
    "L": (0, -1),
    "R": (0, 1),
}

SAME_POINT_PENALTY = 3

FILE_NAME = "maze.txt"


class RouteStats:
    def __init__(self):
        self.solved = False
        self.steps = 0
        self.repeats = 0
        self.disFromDest = 0


class Maze:
    def __init__(self, size, start, destination):
        self.size = size
        self.maze = [[0 for r in range(0, size)] for c in range(0, size)]
        self.startPoint = start
        self.destinationPoint = destination

    def load_maze(self):
        return 0;

    def walk_maze(self, directions):
        currPoint = self.startPoint
        pointsVisited = []
        stats = RouteStats()

        for direction in directions:
            dirPoint = DIRECTIONS_TUPLES[direction]
            nextPoint = addDirection(currPoint, dirPoint)
            stats.steps += 1
            if self.isLegalPoint(nextPoint):
                currPoint = nextPoint
                if currPoint in pointsVisited:
                    stats.repeats += 1
                else:
                    if currPoint == self.destinationPoint:
                        stats.solved = True
                        stats.disFromDest = 0
                        return stats
                    else:
                        pointsVisited.append(currPoint)

        stats.disFromDest = distance(currPoint, self.destinationPoint)
        return stats

    def isLegalPoint(self, point):
        return (0 <= point[0] < self.size and
                0 <= point[1] < self.size)


addDirection = lambda pt, direction: (pt[0] + direction[0], pt[1] + direction[1])


distance = lambda pt1, pt2: abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])


MAZE_SIZE = 50
