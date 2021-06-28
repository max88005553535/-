# Модуль с классом-наследником ScrollView для создания инструкции, у которой при необходимости включается полоса прокрутки
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label

class ScrollLabel(ScrollView):
    def __init__(self, ltext, textcolor = '#0000FF', **kwargs):
        super().__init__(**kwargs)

        self.textcolor = textcolor
        ftext = '[color=' + self.textcolor + ']' + ltext + '[/color]'

        self.label = Label(text=ftext, markup=True, size_hint_y=None, font_size='20px', halign='left', valign='top')
        self.label.bind(size=self.resize)
        self.add_widget(self.label)

    def resize(self, *args):
        self.label.text_size = (self.label.width, None)
        self.label.texture_update()
        self.label.height = self.label.texture_size[1]

    def set_text(self, ltext):
        ftext = '[color=' + self.textcolor + ']' + ltext + '[/color]'
        self.label.text = ftext
        self.resize()
# Здесь должен быть твой код