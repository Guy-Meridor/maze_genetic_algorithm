import matplotlib.pyplot as plt

DIRECTIONS_SIGNS = ["D", "U", "L", "R"]

DIRECTIONS_TUPLES = {
    "D": (1, 0),
    "U": (-1, 0),
    "L": (0, -1),
    "R": (0, 1),
}


class RouteStats:
    def __init__(self):
        self.steps = 0
        self.repeats = 0
        self.disFromDest = float('inf')


class Maze:
    def __init__(self, size, start, destination, obstacles=[]):
        self.size = size
        self.obstacles = obstacles
        self.startPoint = start
        self.destinationPoint = destination

    def walk_maze(self, directions):
        currPoint = self.startPoint
        pointsVisited = [self.startPoint]
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
                    pointsVisited.append(currPoint)

                if currPoint == self.destinationPoint:
                    stats.disFromDest = 0
                    return stats, pointsVisited
                else:
                    pointsVisited.append(currPoint)

        stats.disFromDest = distance(currPoint, self.destinationPoint)
        return stats, pointsVisited

    def isLegalPoint(self, point):
        return (0 <= point[0] < self.size and
                0 <= point[1] < self.size
                and point not in self.obstacles)

    def drawPath(self, directions):
        stats, visited_points = self.walk_maze(directions)
        path_x, path_y = get_cords_in_lists(visited_points)
        obstacles_x, obstacles_y = get_cords_in_lists(self.obstacles)
        destination_x, destination_y = self.destinationPoint
        start_x, start_y = self.startPoint

        plt.plot(path_x, path_y, label="path")
        plt.plot(obstacles_x, obstacles_y, 'ks', label="obstacles", lineWidth=1)
        plt.plot(start_x, start_y, 'ro', label="start")
        plt.plot(destination_x, destination_y, 'go', label="destination")

        plt.xlabel('x')
        plt.ylabel('y')
        plt.title("result path")
        plt.legend()
        plt.show()


addDirection = lambda pt, direction: (pt[0] + direction[0], pt[1] + direction[1])

distance = lambda pt1, pt2: abs(pt1[0] - pt2[0]) + abs(pt1[1] - pt2[1])


def get_cords_in_lists(points):
    return [pt[0] for pt in points], \
           [pt[1] for pt in points]
