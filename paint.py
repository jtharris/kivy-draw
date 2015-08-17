from kivy.app import App
from kivy.clock import Clock
from kivy.uix.widget import Widget
from kivy.uix.listview import ListView
from kivy.properties import ObjectProperty
from commands import LinePreview


class PaintHistory(ListView):

    def __init__(self, *args, **kwargs):
        super(PaintHistory, self).__init__(*args, **kwargs)

        self.commands = []

    def add(self, command):
        self.commands.append(command)
        command.execute()

        self.refresh()

    def clear(self):
        self.commands = []
        self.refresh()

    def refresh(self):
        self.item_strings = [str(command) for command in self.commands]

    def redraw(self):
        for i, command in enumerate(self.commands):
            # Just for visual effect
            Clock.schedule_once(lambda dt, c=command: c.execute(), i * 0.5)

    def undo_last(self):
        try:
            self.commands.pop().undo()
        except IndexError:
            pass

        self.refresh()


class PaintCanvas(Widget):

    paint_history = ObjectProperty(None)

    def __init__(self, *args, **kwargs):
        super(PaintCanvas, self).__init__(*args, **kwargs)

        self.preview = None

    def clear(self):
        self.canvas.clear()

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.preview = LinePreview(self.canvas)
            self.preview.start(touch.x, touch.y)

    def on_touch_move(self, touch):
        if self.preview and self.collide_point(touch.x, touch.y):
            self.preview.move(touch.x, touch.y)

    def on_touch_up(self, touch):
        if self.preview and self.collide_point(touch.x, touch.y):
            self.preview.stop(touch.x, touch.y)
            self.paint_history.add(self.preview.command)

            self.preview = None


class PaintApp(App):
    pass

PaintApp().run()
