from kivy.graphics import Ellipse, Line
from kivy.vector import Vector


class LinePreview:

    def __init__(self, canvas):
        self.canvas = canvas

    def start(self, x, y):
        self.start_coords = (x, y)

        with self.canvas:
            self.line = Line(points=(x, y))

    def move(self, x, y):
        self.line.points = self.start_coords + (x, y)

    def stop(self, x, y):
        self.end_coords = (x, y)
        self.canvas.remove(self.line)
        self.line = None

    @property
    def command(self):
        return LineCommand(self.canvas, self.start_coords, self.end_coords)


class CirclePreview:

    def __init__(self, canvas):
        self.canvas = canvas

    def start(self, x, y):
        self.center = (x, y)

        with self.canvas:
            self.circle = Ellipse(pos=self.center, size=(0, 0))

    def move(self, x, y):
        radius = Vector(self.center).distance((x, y))
        self.circle.pos = (self.center[0] - radius, self.center[1] - radius)
        self.circle.size = (radius * 2, radius * 2)

    def stop(self, x, y):
        self.radius = Vector(self.center).distance((x, y))
        self.canvas.remove(self.circle)
        self.circle = None

    @property
    def command(self):
        return CircleCommand(self.canvas, self.center, self.radius)


# Note that the canvas is the receiver in this scenario
class LineCommand:

    def __init__(self, canvas, start, end):
        self.canvas = canvas
        self.start = start
        self.end = end

    def execute(self):
        with self.canvas:
            self.line = Line(points=self.start + self.end)

    def undo(self):
        self.canvas.remove(self.line)

    def __str__(self):
        points = [int(point) for point in (self.start + self.end)]
        return 'Line:  ({}, {}) -> ({}, {})'.format(*points)

class CircleCommand:

    def __init__(self, canvas, center, radius):
        self.canvas = canvas
        self.center = center
        self.radius = radius

    def execute(self):
        with self.canvas:
            self.circle = Ellipse(
                pos=(self.center[0] - self.radius, self.center[1] - self.radius),
                size=(self.radius * 2, self.radius * 2)
            )

    def undo(self):
        self.canvas.remove(self.circle)

    def __str__(self):
        return 'Circle:  ({}, {})  r: {}'.format(int(self.center[0]), int(self.center[1]), self.radius)

