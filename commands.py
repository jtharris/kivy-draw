from kivy.graphics import Color, Ellipse, Line


# Note that the canvas is the receiver in this scenario
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


class LineCommand:

    def __init__(self, canvas, start, end):
        self.canvas = canvas
        self.start = start
        self.end = end

    def execute(self):
        with self.canvas:
            self.line = Line(points=self.start + self.end)

    def __str__(self):
        return 'Line:  {} -> {}'.format(self.start, self.end)

