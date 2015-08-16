from kivy.app import App
from kivy.uix.widget import Widget
from kivy.uix.treeview import TreeView, TreeViewLabel
from kivy.properties import ObjectProperty
from commands import LinePreview


class PaintHistory(TreeView):

    def add(self, command):
        if not hasattr(self, 'commands'):
            self.commands = []

        self.commands.append(command)
        command.execute()

        self.refresh()

    def clear(self):
        for node in self.iterate_all_nodes():
            self.remove_node(node)

    def refresh(self):
        self.clear()

        for command in self.commands:
            self.add_node(TreeViewLabel(text=str(command)))


class PaintCanvas(Widget):

    paint_history = ObjectProperty(None)

    def on_touch_down(self, touch):
        self.preview = LinePreview(self.canvas)
        self.preview.start(touch.x, touch.y)

    def on_touch_move(self, touch):
        self.preview.move(touch.x, touch.y)

    def on_touch_up(self, touch):
        self.preview.stop(touch.x, touch.y)
        self.paint_history.add(self.preview.command)

class PaintApp(App):
    pass

PaintApp().run()
