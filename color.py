from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle

class ColoredLayout(BoxLayout):
    def __init__(self, lcolor, **kwargs):
        super().__init__(**kwargs)
        self.padding = '10dp'

        with self.canvas.before:
            Color(*lcolor)  
            self.rect = Rectangle(size=self.size, pos=self.pos)

        self.bind(size=self._update_rect, pos=self._update_rect)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size