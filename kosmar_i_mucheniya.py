# -*- coding: cp1251 -*-

import kivy 
from kivy.config import Config
from kivy.graphics import Color
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.app import App
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from datetime import date, datetime, timedelta



class ITextInput(TextInput):
    def on_text_validate(self):
        self.search(self.text)

    def search(self, input_text):
        file_name = input_text + '.txt'
        try:
            f = open(file_name, 'r')
            data = []
            data = f.read()
            Message = Popup(title='Message', content=Label(text=data), size_hint=(None, None), size=(200, 200))
            Message.open()
        except FileNotFoundError:
            Message = Popup(title='Error', content=Label(text='File not found'), size_hint=(None, None), size=(200, 200))
            Message.open()


class SearchScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # создаем вертикальный BoxLayout
        layout = BoxLayout(orientation='vertical')

        # добавляем название приложения и кнопку фильтра в верхнюю часть
        header_layout = BoxLayout(size_hint=(1, 0.1))
        header_layout.add_widget(Label(text='To Do Look', size_hint=(0.6, 1), halign='center'))
        layout.add_widget(header_layout)

        # добавляем поле для ввода
        input_text = ITextInput(background_color=(255/256, 87/256, 34/256, 1), hint_text='Ввести', multiline=False, size_hint=(1, 0.1))
        layout.add_widget(input_text)

        # добавляем кнопку "Вернуться назад"
        back_button = Button(background_color=(229/256, 115/256, 115/256, 1), text='Вернуться назад', on_press=self.goto_main_screen, size_hint=(1, 0.1))
        layout.add_widget(back_button)

        self.add_widget(layout)

    def goto_main_screen(self, instance):
        self.manager.current = 'main'





class ReminderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        layout = BoxLayout(orientation='vertical')
        
        # Верхняя часть
        title = Label(color=(0, 1, 1, 1), text='To Do Look')
        layout.add_widget(title)
        
        # Средняя часть
        create_note = Button(text='Создать заметку', on_press=self.goto_CreateNote_screen)
        create_reminder = Button(text='Создать напоминание', on_press=self.goto_CreateReminder_screen)
        cancel = Button(background_color=(1, 8/255, 0, 1), text='Отмена', on_press=self.goto_main_screen)
        layout.add_widget(create_note)
        layout.add_widget(create_reminder)
        layout.add_widget(cancel)
        
        # Нижняя часть
        add = Button(text='+', size_hint=(None, None), size=(50, 50), pos_hint={'right': 1, 'bottom': 1})
        layout.add_widget(add)
        
        self.add_widget(layout)

    def goto_main_screen(self, instance):
        self.manager.current = 'main'

    def goto_CreateReminder_screen(self, instance):
        self.manager.current = 'create_reminder'
    
    def goto_CreateNote_screen(self, instance):
        self.manager.current = 'create_note'



class DateTextInput(TextInput):
    def insert_text(self, substring, from_undo=False):
        if len(self.text) >= 10:
            return
        if not substring.isdigit():
            return
        if len(self.text) == 2 or len(self.text) == 5:
            self.text += "/"
        super(DateTextInput, self).insert_text(substring, from_undo=from_undo)



class Create_reminderScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # создаем вертикальный BoxLayout
        layout = BoxLayout(orientation='vertical')

        # добавляем название приложения и кнопки "Сохранить" и "Отмена" в верхнюю часть
        header_layout = BoxLayout(size_hint=(1, 0.1))
        header_layout.add_widget(Button(background_color=(255/256, 8/256, 0, 1), text='Отмена', color=(0, 0, 0, 1), on_press=self.goto_main_screen,size_hint=(0.1, 1)))
        header_layout.add_widget(Label(text='To Do Look', size_hint=(0.8, 1), halign='center'))
        header_layout.add_widget(Button(background_color=(0, 1, 0, 1), text='Сохранить', color=(0, 0, 0, 1), on_press=lambda instance:self.writing_to_a_file(title_input.text, category_input.text, text_input.text, date_input.text),size_hint=(0.1, 1)))
        layout.add_widget(header_layout)

        # добавляем поле для ввода категории
        category_input = TextInput(background_color=(158/256, 158/256, 158/256, 1), hint_text='Категория', size_hint=(1, 0.1))
        layout.add_widget(category_input)

        # добавляем поле для ввода заголовка
        title_input = TextInput(background_color=(189/256, 189/256, 189/256, 1), hint_text='Заголовок', size_hint=(1, 0.1))
        layout.add_widget(title_input)

        # добавляем поле для ввода текста
        text_input = TextInput(background_color=(238/256, 238/256, 238/256, 1), hint_text='Введите текст', size_hint=(1, 0.6))
        layout.add_widget(text_input)

        date_input = DateTextInput(multiline=False, size_hint=(1, 0.1))
        layout.add_widget(date_input)
        # добавляем поле для ввода времени
    
        self.add_widget(layout)

    def goto_main_screen(self, instance):
        self.manager.current = 'main'

    def on_datedate_input(self, instance, value):
        # Форматируем введенную дату и время
        if len(value) == 2 and value[1] != '/':
            self.datedate_input.text = value[0] + '/'
        elif len(value) == 5 and value[4] != '/':
            self.datedate_input.text = value[:3] + '/' + value[3]
        elif len(value) == 10 and value[9] != ' ':
            self.datedate_input.text = value[:9] + ' ' + value[9]
        elif len(value) == 13 and value[12] != ':':
            self.datedate_input.text = value[:12] + ':' + value[12:]
        elif len(value) > 16:
            self.datedate_input.text = value[:16]


    def writing_to_a_file(self, title_input, category_input, text_input, date_input):
        if (title_input != '') or (text_input != '') or (date_input != ''):
            file_name = title_input + '.txt'
            f = open(file_name, 'w')
            file_with_name = open('file_with_name.txt', 'w+')
            file_with_name.write(title_input)
            file_with_name.write('\n')
            file_with_name.close()
            f.write(category_input)
            f.write('\n')
            f.write(text_input)
            f.write('\n')
            f.write(date_input)
            f.close()
            self.manager.current = 'main'
            title_input = ''
            text_input = ''
            date_input = ''
            category_input = ''
        else:
            Message = Popup(title='Message', content=Label(text='Введите, пожалуйста, ещё немного данных, чтобы были заняты все ячейки!'), size_hint=(None, None), size=(200, 200))
            Message.open()



class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # создаем вертикальный BoxLayout
        layout = BoxLayout(orientation='vertical')
        
        # Добавляем название программы и кнопку настроек
        header_layout = BoxLayout(size_hint=(1, 0.1))
        header_layout.add_widget(Label(text='To Do Look', size_hint=(0.8, 1), halign='center'))
        layout.add_widget(header_layout)

        # Добавляем кнопку "Поиск"
        layout.add_widget(Button(text='Поиск', on_press=self.goto_search_screen, size_hint=(1, None), height=100))
        
        # Добавляем кнопку "Показать" и комбобокс для выбора даты
        inner_layout = BoxLayout(size_hint=(1, 0.6), height=100)
        inner_layout.add_widget(Button(text='Показать', on_press=self.goto_show_screen, size_hint=(0.3, 1), height=100))
        spinner_values = ['Сегодня', 'Завтра', 'Послезавтра']
        spin = Spinner(text=spinner_values[0], values=spinner_values, size_hint=(0.7, 1), height=100)
        inner_layout.add_widget(spin)
        layout.add_widget(inner_layout)
        
        # добавляем кнопку "+" в правый нижний угол
        add_button = Button(background_color=(1, 0, 0, 1), text='+', color=(0, 0, 0, 1), on_press=self.goto_reminder_screen,size=(50, 50), size_hint=(None, None), pos_hint={'x': 0.9, 'y': 0})
        layout.add_widget(add_button)
        
        self.add_widget(layout)

    def goto_search_screen(self, instance):
        self.manager.current = 'search'


    def goto_show_screen(self, instance):
# изменяем аргумент функции spin на instance, т.к. это экземпляр класса Spinner
        with open('file_with_name.txt', 'r') as file:
# Считываем все строки из файла и сохраняем их в массиве
            lines_array = file.readlines()
            today = date.today()
            today_string = today.strftime('%d/%m/%Y')
            val = instance.text # обратимся к атрибуту text, чтобы получить выбранное значение
            if val[0]:
                data = "Ничего не найдено"
                for line in range(len(lines_array)):
                    file_name = lines_array[line].strip() + '.txt'
                    f = open(file_name, 'r')
                    strings = f.readline()
                    last_string = strings[-1].strip()
                    if last_string == today_string:
                        data = f.read() 
                        f.close()
                    Message = Popup(title='Message', content=Label(text=data), size_hint=(None, None), size=(200, 200))
                    Message.open()
            else:
                tomorrow = datetime.today() + timedelta(days=1)
                tomorrow_string = tomorrow.strftime('%d/%m/%Y')
                val = instance.text # обратимся к атрибуту text, чтобы получить выбранное значение
                if val[1]:
                    data = "Ничего не найдено"
                    for line in range(len(lines_array)):
                        file_name = lines_array[line].strip() + '.txt'
                        f = open(file_name, 'r')
                        strings = f.readline()
                        last_string = strings[-1].strip()
                        if last_string == today_string:
                            data = f.read() 
                            f.close()
                        Message = Popup(title='Message', content=Label(text=data), size_hint=(None, None), size=(200, 200))
                        Message.open()

                else:
                    tomorrow = datetime.today() + timedelta(days=1) + timedelta(days=1)
                    tomorrow_string = tomorrow.strftime('%d/%m/%Y')
                    val = instance.text # обратимся к атрибуту text, чтобы получить выбранное значение
                    if val[2]:
                        data = "Ничего не найдено"
                        for line in range(len(lines_array)):
                            file_name = lines_array[line].strip() + '.txt'
                            f = open(file_name, 'r')
                            strings = f.readline()
                            last_string = strings[-1].strip()
                            if last_string == today_string:
                                data = f.read() 
                                f.close()
                            Message = Popup(title='Message', content=Label(text=data), size_hint=(None, None), size=(200, 200))
                            Message.open()



    def goto_reminder_screen(self, instance):
        self.manager.current = 'reminder'



class Create_noteScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # создаем вертикальный BoxLayout
        layout = BoxLayout(orientation='vertical')

        # добавляем название приложения и кнопки "Сохранить" и "Отмена" в верхнюю часть
        header_layout = BoxLayout(size_hint=(1, 0.1))
        header_layout.add_widget(Button(background_color=(255/256, 8/256, 0, 1), text='Отмена', color=(0, 0, 0, 1), on_press=self.goto_main_screen, size_hint=(0.1, 1)))
        header_layout.add_widget(Label(text='To Do Look', size_hint=(0.8, 1), halign='center'))
        header_layout.add_widget(Button(background_color=(0, 1, 0, 1), text='Сохранить', color=(0, 0, 0, 1), on_press=lambda instance:self.writing_to_a_file(self.title_input.text, self.category_input.text, self.text_input.text), size_hint=(0.1, 1)))
        layout.add_widget(header_layout)

        # добавляем поле для ввода категории
        self.category_input = TextInput(background_color=(158/256, 158/256, 158/256, 1), hint_text='Категория', size_hint=(1, 0.1))
        layout.add_widget(self.category_input)

        # добавляем поле для ввода заголовка
        self.title_input = TextInput(background_color=(189/256, 189/256, 189/256, 1), hint_text='Заголовок', size_hint=(1, 0.1))
        layout.add_widget(self.title_input)

        # добавляем поле для ввода текста
        self.text_input = TextInput(background_color=(238/256, 238/256, 238/256, 1), hint_text='Введите текст', size_hint=(1, 0.7))
        layout.add_widget(self.text_input)

        self.add_widget(layout)

    def goto_main_screen(self, instance):
        self.manager.current = 'main'

    def writing_to_a_file(self, title_input, category_input, text_input):
        if (title_input != '') and (text_input != ''):
            file_name = title_input + '.txt'
            f = open(file_name, 'w')
            f.write(category_input)
            f.write('\n')
            f.write(text_input)
            self.manager.current = 'main'
        else:
            Message = Popup(title='Message', content=Label(text='Введите, пожалуйста, ещё немного данных, чтобы были заняты все ячейки!'), size_hint=(None, None), size=(200, 200))
            Message.open()





class MyScreenManager(ScreenManager):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # добавляем экраны
        self.add_widget(MainScreen(name='main'))
        self.add_widget(SearchScreen(name='search'))
        self.add_widget(ReminderScreen(name='reminder'))
        self.add_widget(Create_reminderScreen(name='create_reminder'))
        self.add_widget(Create_noteScreen(name='create_note'))

# создаем приложение
class MyApp(App):
    def build(self):
        return MyScreenManager()

if __name__ == '__main__':
    MyApp().run()