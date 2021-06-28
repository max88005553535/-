from kivy.app import App
from kivy.graphics import Color, Rectangle
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView

from instructions import txt_instruction, txt_test1, txt_test2, txt_test3, txt_sits
from scrollLabel import ScrollLabel
from ruffier import test
from color import ColoredLayout

from seconds import Seconds
from sits import Sits
from runner import Runner

Window.clearcolor = (0.8, 1, 1, 1)
btn_color = (0, 1, 0, 1)

age = 7
name = ""
p1, p2, p3 = 0, 0, 0

def check_int(str_num):
    try:
        return int(str_num)
    except:
        return False

def get_result():
    res = test(p1, p2, p3, age)
    return name + '\n' + res[0] + '\n' + res[1]

class MainSrc(Screen):
    def __init__(self, name='instruction'):
        super().__init__(name = name)

        instr = ScrollLabel(txt_instruction)

        self.popup = Popup(title='Oшибка',
                      content = Label(text='Возраст должен быть старше или равен 7 лет'),
                      size_hint =(0.5, 0.5), 
                      size = (200, 200), 
                      pos_hint={'center_x': 0.5, 'center_y': 0.5}
                      )

        self.popup2 = Popup(title='Ошибка',
                      content = Label(text='Введите имя'),
                      size_hint=(0.5, 0.5),
                      size = (200, 200),
                      pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        txt = Label(text= 'Инструкция!',height='30px', size_hint=(1, 0.3), pos_hint={'center_x': 0.5}, font_size='35px')
        l1 = Label(text='Введите имя:', halign='right', font_size='20px')
        l2 = Label(text='Введите возраст:', halign='right', font_size='20px')
        
        txt.color = '#FF0000'
        l1.color = '#0000FF'
        l2.color = '#0000FF'
        
        self.btn = Button(text='Начать', size_hint=(0.3, 0.2), pos_hint={'center_x': 0.5}, font_size='20px')
        self.btn.background_color = btn_color
        self.btn.color = (0.8, 1, 1, 1)
        self.btn.on_press = self.next
        self.in_name = TextInput(multiline=False) 
        self.in_age = TextInput(text='7', multiline=False)

        line1 = BoxLayout(size_hint=(0.8, None), height='30sp')
        line2 = BoxLayout(size_hint=(0.8, None), height='30sp')
        line1.add_widget(l1)
        line1.add_widget(self.in_name)
        line2.add_widget(l2)
        line2.add_widget(self.in_age)

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer.add_widget(txt)
        outer.add_widget(instr)
        outer.add_widget(line1)
        outer.add_widget(line2)
        outer.add_widget(self.btn)

        self.add_widget(outer)
    
    def next(self, direction='right'):
        self.manager.transition.direction = 'left'
        global age, name
        name = self.in_name.text
        age = check_int(self.in_age.text)
        if age == False or age < 7:
            age = 7
            self.in_age.text = str(age)
            self.popup.open()
        elif (name == "") or (name == None):
            self.in_name.text = str(name)
            self.popup2.open()
        else:
            self.manager.current = 'first'

class FirstSrc(Screen):
    def __init__(self, name='first'):
        super().__init__(name = name)
        self.next_screen = False

        self.popup = Popup(title='Oшибка',
                      content = Label(text='Введите ваш результат в поле пожалуйста'),
                      size_hint=(0.5, 0.5), 
                      size = (200, 200), 
                      pos_hint={'center_x': 0.5, 'center_y': 0.5},
                      auto_dismiss = True)
        
        instr = ScrollLabel(txt_test1)
        l1 = ScrollLabel('Внимание идёт счёт пульса!', textcolor = '#FF0000', pos_hint={'center_x': 0.7})
        self.sec = Seconds(15, textcolor = '#FF0000', pos_hint={'center_x': 0.8})
        self.sec.bind(done=self.sec_finished)

        line1 = ColoredLayout(lcolor = (0, 1, 0, 1))
        vlay = ColoredLayout(orientation='vertical', lcolor = (0.8, 1, 1, 1))
        vlay.add_widget(l1)
        vlay.add_widget(self.sec)
        line1.add_widget(instr)
        line1.add_widget(vlay)

        line2 = BoxLayout(size_hint=(0.8, None), height='30sp')
        result = Label(text='Введите результат:', halign='right', font_size='20px')
        result.color = '#0000FF'
        self.in_result = TextInput(text='0', multiline=False)
        self.in_result.set_disabled(True)
        
        line2.add_widget(result)
        line2.add_widget(self.in_result)

        self.btn = Button(text='Запустить таймер', size_hint=(1, 0.25), font_size='20px')
        self.btn.background_color = btn_color
        self.btn.on_press = self.next
        self.btn_back = Button(text='Инструкция!', size_hint=(1, 0.25), font_size='20px')
        self.btn_back.background_color = btn_color
        self.btn_back.on_press = self.back

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer2 = BoxLayout(orientation='horizontal', size_hint=(0.8, .9), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        outer.add_widget(line1)
        outer.add_widget(line2)
        outer2.add_widget(self.btn_back)
        outer2.add_widget(self.btn)
        outer.add_widget(outer2)
        self.add_widget(outer)
        
    def sec_finished(self, *args):
        self.in_result.set_disabled(False)
        self.btn.set_disabled(False)
        self.btn.text = 'Продолжить'
        self.next_screen = True

    def next(self):
        self.manager.transition.direction = 'left'
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.sec.start()
        else:
            global p1
            p1 = check_int(self.in_result.text)
            if p1 == False or p1 <= 0:
                p1 = 0
                self.in_result.text = str(p1)
                self.popup.open()
            else:
                self.manager.current = 'second'
    
    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'instruction'

class SecondSrc(Screen):
    def __init__(self, name='second'):
        super().__init__(name = name)
        self.next_screen = False

        instr = ScrollLabel(txt_test2)
        l1 = ScrollLabel('Сделайте 30 приседаний', textcolor = '#FF0000')
        self.sits = Sits(30, textcolor = '#FF0000')
        self.run = Runner(total=30, steptime=1.5, lcolor = (0.8, 1, 1, 1))
        self.run.bind(finished=self.run_finished)

        line = ColoredLayout(lcolor = (0, 1, 0, 1))
        vlay = BoxLayout(orientation='vertical')
        vlay.add_widget(instr)
        vlay.add_widget(l1)
        vlay.add_widget(self.sits)
        line.add_widget(vlay)
        line.add_widget(self.run)

        self.btn = Button(text='Начать', font_size='20px')
        self.btn.background_color = btn_color
        self.btn.on_press = self.next
        self.btn1 = Button(text='Назад', font_size='20px')
        self.btn1.background_color = btn_color
        self.btn1.on_press = self.back

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer2 = BoxLayout(orientation='horizontal', size_hint=(0.8, 0.125), pos_hint={'center_x': 0.5})
        outer.add_widget(line)
        outer2.add_widget(self.btn1)
        outer2.add_widget(self.btn)
        outer.add_widget(outer2)

        self.add_widget(outer)

    def run_finished(self, instance, value):
        self.btn.set_disabled(False)
        self.btn.text = 'Продолжить'
        self.next_screen = True

    def next(self):
        self.manager.transition.direction = 'left'
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.run.start()
            self.run.bind(value=self.sits.next)
        else:
            self.manager.current = 'third'

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'first'

class ThirdSrc(Screen):
    def __init__(self, name='third'):
        super().__init__(name = name)
        self.next_screen = False

        self.popup = Popup(title='Oшибка',
                      content = Label(text='Введите ваш результат в поле пожалуйста'),
                      size_hint=(0.5, 0.5), 
                      size = (200, 200), 
                      pos_hint={'center_x': 0.5, 'center_y': 0.5})

        self.stage = 0
        instr = ScrollLabel(txt_test3)

        self.l1 = ScrollLabel('Считайте пульс', textcolor = '#FF0000')
        self.sec = Seconds(15, textcolor = '#FF0000')
        self.sec.bind(done=self.sec_finished)

        line0 = ColoredLayout(lcolor = (0, 1, 0, 1))
        vlay = ColoredLayout(orientation='vertical', lcolor =(0.8, 1, 1, 1))
        vlay.add_widget(self.l1)
        vlay.add_widget(self.sec)
        line0.add_widget(instr)
        line0.add_widget(vlay)

        line1 = BoxLayout(size_hint=(0.8, None), height='30sp')
        result1 = Label(text='Результат:', halign='right', font_size = '20px')
        result1.color = '#0000FF'
        self.in_result1 = TextInput(text='0', multiline=False)
        self.in_result1.set_disabled(True)

        line1.add_widget(result1)
        line1.add_widget(self.in_result1)

        line2 = BoxLayout(size_hint=(0.8, None), height='30sp')
        result2 = Label(text='Результат после отдыха:', halign='right', font_size = '20px')
        result2.color = '#0000FF'
        self.in_result2 = TextInput(text='0', multiline=False)
        self.in_result2.set_disabled(True)

        line2.add_widget(result2)
        line2.add_widget(self.in_result2)

        self.btn = Button(text='Начать', size_hint=(1, 0.25), font_size='20px')
        self.btn.background_color = btn_color
        self.btn.on_press = self.next
        self.btn1 = Button(text='Назад', size_hint=(1, 0.25), font_size='20px')
        self.btn1.background_color = btn_color
        self.btn1.on_press = self.back

        outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        outer2 = BoxLayout(orientation='horizontal', size_hint=(0.8, .9), pos_hint={'center_x': 0.5, 'center_y': 0.5})

        outer.add_widget(line0)
        outer.add_widget(line1)
        outer.add_widget(line2)
        outer2.add_widget(self.btn1)
        outer2.add_widget(self.btn)
        outer.add_widget(outer2)

        self.add_widget(outer)

    def sec_finished(self, instance, value):
        if value:
            if self.stage == 0:
                # закончили первый подсчет, отдыхаем
                self.stage = 1
                self.l1.set_text('Отдыхайте')
                self.sec.restart(30)
                self.in_result1.set_disabled(False)
            elif self.stage == 1:
                # закончили отдых, считаем
                self.stage = 2
                self.l1.set_text('Считайте пульс')
                self.sec.restart(15)
            elif self.stage == 2:
                self.in_result2.set_disabled(False)
                self.btn.set_disabled(False)
                self.btn.text = 'Завершить'
                self.next_screen = True

    def next(self):
        if not self.next_screen:
            self.btn.set_disabled(True)
            self.sec.start()
        else:
            global p2, p3
            p2 = check_int(self.in_result1.text)
            p3 = check_int(self.in_result2.text)
            if p2 == False and p3 == False:
                p2 = 0
                self.in_result1.text = str(p2)
                p3 = 0
                self.in_result2.text = str(p3)
                self.popup.open()
            elif p2 == False:
                p2 = 0
                self.in_result1.text = str(p2)
                self.popup.open()
            elif p3 == False:
                p3 = 0
                self.in_result2.text = str(p3)
                self.popup.open()
            else:
                self.manager.current = 'result'

    def back(self):
        self.manager.transition.direction = 'right'
        self.manager.current = 'second'

class ResultSrc(Screen):
    def __init__(self, name='result'):
        super().__init__(name = name)

        self.outer = BoxLayout(orientation='vertical', padding=8, spacing=8)
        self.instr = ScrollLabel('')
        self.outer.add_widget(self.instr)

        self.add_widget(self.outer)
        self.on_enter = self.before
    
    def before(self):
        self.instr.set_text(get_result())

class MyApp(App):
    def build(self):
        '''line = ColoredLayout(lcolor = (1, 0.6, 0, 1))'''
        c = ScreenManager()
        c.add_widget(MainSrc())
        c.add_widget(FirstSrc())
        c.add_widget(SecondSrc())
        c.add_widget(ThirdSrc())
        c.add_widget(ResultSrc())
        '''line.add_widget(c)'''
        
        '''return line'''
        return c
        
MyApp().run()
