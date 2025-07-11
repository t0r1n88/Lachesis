# -*- coding: UTF-8 -*-
"""
Графический интерфейс программы
"""
from create_result_docs import generate_result_docs # импортируем функцию по созданию документов по профориентации
from create_other_docs import generate_other_docs_from_template # импортируем функцию для создания остальных документов
from processing_complex import generate_result_all_age # функция для обработки тестов

import pandas as pd
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
pd.options.mode.chained_assignment = None
import sys
import logging
logging.basicConfig(
    level=logging.WARNING,
    filename="error.log",
    filemode='w',
    # чтобы файл лога перезаписывался  при каждом запуске.Чтобы избежать больших простыней. По умолчанию идет 'a'
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)






# # Классы для исключений

class WrongNumberColumn(Exception):
    """
    Класс для исключения проверяющего количество колонок в в таблице
    """
    pass


class CheckBoxException(Exception):
    """
    Класс для вызовы исключения в случае если неправильно выставлены чекбоксы
    """
    pass


class NotFoundValue(Exception):
    """
    Класс для обозначения того что значение не найдено
    """
    pass


def select_file_template_doc():
    """
    Функция для выбора файла шаблона
    :return: Путь к файлу шаблона
    """
    global name_file_template_doc
    name_file_template_doc = filedialog.askopenfilename(
        filetypes=(('Word files', '*.docx'), ('all files', '*.*')))


def select_file_data_doc():
    """
    Функция для выбора файла с данными на основе которых будет генерироваться документ
    :return: Путь к файлу с данными
    """
    global name_file_data_doc
    # Получаем путь к файлу
    name_file_data_doc = filedialog.askopenfilename(filetypes=(('Excel files', '*.xlsx'), ('all files', '*.*')))


def select_end_folder_doc():
    """
    Функция для выбора папки куда будут генерироваться файлы
    :return:
    """
    global path_to_end_folder_doc
    path_to_end_folder_doc = filedialog.askdirectory()


def processing_generate_docs():
    """
    Функция для создания документов из произвольных таблиц
    :return:
    """
    try:
        folder_structure = entry_folder_structure.get() # получаем по каким колонкам будет формироваться структура папок
        name_file = entry_name_file.get() # получаем по каким колонкам будет формироваться название файла
        name_type_file = entry_type_file.get() # получаем тип документа который будет создаваться

        # получаем состояние переключателя режима
        mode_full = mode_full_type.get()
        # получаем состояние чекбокса создания pdf
        mode_pdf = mode_pdf_value.get() # чекбокс нужно ли создавать пдф версии

        generate_result_docs(name_file_data_doc,name_file_template_doc,path_to_end_folder_doc,folder_structure,
                             name_file,name_type_file,mode_pdf,mode_full)

    except NameError as e:
        messagebox.showerror('Лахеcис Обработка результатов профориентационных тестов',
                             f'Выберите шаблон,файл с данными и папку куда будут генерироваться файлы')



"""
Функции для обработки тестов
"""

def select_file_params_all_age():
    """
    Функция для выбора файла с данными на основе которых будет генерироваться документ
    :return: Путь к файлу с данными
    """
    global file_params_all_age
    # Получаем путь к файлу
    file_params_all_age = filedialog.askopenfilename(filetypes=(('Excel files', '*.xlsx'), ('all files', '*.*')))

def select_file_data_xlsx_all_age():
    """
    Функция для выбора файла с данными на основе которых будет генерироваться документ
    :return: Путь к файлу с данными
    """
    global file_data_xlsx_all_age
    # Получаем путь к файлу
    file_data_xlsx_all_age = filedialog.askopenfilename(filetypes=(('Excel files', '*.xlsx'), ('all files', '*.*')))

def select_end_folder_all_age():
    """
    Функция для выбора конечной папки куда будут складываться итоговые файлы
    :return:
    """
    global path_to_end_folder_all_age
    path_to_end_folder_all_age = filedialog.askdirectory()


def processing_all_age():
    """
    Функция для генерации результатов комплексного тестирования на тревожность школьников
    """
    try:
        start_threshold = var_entry_threshold_all_age.get() # получаем количество колонок
        start_threshold = int(start_threshold)


        svod_cols = var_entry_svod_all_age.get() # получаем строку

        generate_result_all_age(file_params_all_age, file_data_xlsx_all_age, path_to_end_folder_all_age, start_threshold, svod_cols)
    except ValueError:
        messagebox.showerror('Лахеcис',
                             f'Введите целое число начиная с 1 !!!')
    except NameError:
        messagebox.showerror('Лахеcис',
                             f'Выберите файлы с данными и папку куда будет генерироваться файл')



"""
Функции для создания остальных документов 
"""
def select_file_template_other_doc():
    """
    Функция для выбора файла шаблона
    :return: Путь к файлу шаблона
    """
    global name_file_template_other_doc
    name_file_template_other_doc = filedialog.askopenfilename(
        filetypes=(('Word files', '*.docx'), ('all files', '*.*')))


def select_file_data_other_doc():
    """
    Функция для выбора файла с данными на основе которых будет генерироваться документ
    :return: Путь к файлу с данными
    """
    global name_file_data_other_doc
    # Получаем путь к файлу
    name_file_data_other_doc = filedialog.askopenfilename(filetypes=(('Excel files', '*.xlsx'), ('all files', '*.*')))


def select_end_folder_other_doc():
    """
    Функция для выбора папки куда будут генерироваться файлы
    :return:
    """
    global path_to_end_folder_other_doc
    path_to_end_folder_other_doc = filedialog.askdirectory()


def generate_other_docs():
    """
    Функция для создания документов из произвольных таблиц
    :return:
    """
    try:
        name_column = entry_name_column_data_other_doc.get() # название колонки по которой будут создаваться имена файлов
        name_type_file = entry_type_file_other_doc.get() # название создаваемого документа
        name_value_column = entry_value_column_single_other_doc.get() # значение для генерации одиночного файла
        number_structure_folder = entry_structure_folder_value_other_doc.get() # получаем список номеров колонок для структуры папок

        # получаем состояние чекбокса создания только pdf версий файлов
        mode_full = mode_full_value_other_doc.get()
        # получаем состояние чекбокса создания pdf
        mode_pdf = mode_pdf_value_other_doc.get()
        # Получаем состояние  чекбокса объединения файлов в один
        mode_combine = mode_combine_value_other_doc.get()
        # Получаем состояние чекбокса создания индвидуального файла
        mode_group = mode_group_doc_value_other_doc.get()
        # получаем состояние чекбокса создания структуры папок
        mode_structure_folder = mode_structure_folder_value_other_doc.get()

        generate_other_docs_from_template(name_file_template_other_doc,name_file_data_other_doc,name_column, name_type_file, path_to_end_folder_other_doc, name_value_column, mode_pdf,
                                    mode_combine, mode_group,mode_structure_folder,number_structure_folder,mode_full)

    except NameError as e:
        messagebox.showerror('Лахесис',
                             f'Выберите шаблон,файл с данными и папку куда будут генерироваться файлы')
        logging.exception('AN ERROR HAS OCCURRED')


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller
    Функция чтобы логотип отображался"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

"""
Функции для создания контекстного меню(Копировать,вставить,вырезать)
"""


def make_textmenu(root):
    """
    Функции для контекстного меню( вырезать,копировать,вставить)
    взято отсюда https://gist.github.com/angeloped/91fb1bb00f1d9e0cd7a55307a801995f
    """
    # эта штука делает меню
    global the_menu
    the_menu = Menu(root, tearoff=0)
    the_menu.add_command(label="Вырезать")
    the_menu.add_command(label="Копировать")
    the_menu.add_command(label="Вставить")
    the_menu.add_separator()
    the_menu.add_command(label="Выбрать все")


def callback_select_all(event):
    """
    Функции для контекстного меню( вырезать,копировать,вставить)
    взято отсюда https://gist.github.com/angeloped/91fb1bb00f1d9e0cd7a55307a801995f
    """
    # select text after 50ms
    window.after(50, lambda: event.widget.select_range(0, 'end'))


def show_textmenu(event):
    """
    Функции для контекстного меню( вырезать,копировать,вставить)
    взято отсюда https://gist.github.com/angeloped/91fb1bb00f1d9e0cd7a55307a801995f
    """
    e_widget = event.widget
    the_menu.entryconfigure("Вырезать", command=lambda: e_widget.event_generate("<<Cut>>"))
    the_menu.entryconfigure("Копировать", command=lambda: e_widget.event_generate("<<Copy>>"))
    the_menu.entryconfigure("Вставить", command=lambda: e_widget.event_generate("<<Paste>>"))
    the_menu.entryconfigure("Выбрать все", command=lambda: e_widget.select_range(0, 'end'))
    the_menu.tk.call("tk_popup", the_menu, event.x_root, event.y_root)


def on_scroll(*args):
    canvas.yview(*args)

def set_window_size(window):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()

    # Устанавливаем размер окна в 80% от ширины и высоты экрана
    if screen_width >= 3840:
        width = int(screen_width * 0.2)
    elif screen_width >= 2560:
        width = int(screen_width * 0.31)
    elif screen_width >= 1920:
        width = int(screen_width * 0.41)
    elif screen_width >= 1600:
        width = int(screen_width * 0.5)
    elif screen_width >= 1280:
        width = int(screen_width * 0.62)
    elif screen_width >= 1024:
        width = int(screen_width * 0.77)
    else:
        width = int(screen_width * 1)

    height = int(screen_height * 0.8)

    # Рассчитываем координаты для центрирования окна
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2

    # Устанавливаем размер и положение окна
    window.geometry(f"{width}x{height}+{x}+{y}")


"""
Создание нового окна
"""
def open_list_changes():
    # Создание нового окна
    new_window = Toplevel(window)

    # Настройка нового окна
    new_window.title("Список изменений")
    text_area = Text(new_window, width=200, height=100)

    with open(list_changes_path, 'r', encoding='utf-8') as file:
        text = file.read()
        text_area.insert(END, text)
    text_area.configure(state='normal')
    text_area.pack(side=LEFT)

    scroll = Scrollbar(new_window, command=text_area.yview)
    scroll.pack(side=LEFT, fill=Y)

    text_area.config(yscrollcommand=scroll.set)

def open_license():
    # Создание нового окна
    new_window = Toplevel(window)

    # Настройка нового окна
    new_window.title("Лицензия")
    text_area = Text(new_window, width=200, height=100)

    with open(license_path, 'r', encoding='utf-8') as file:
        text = file.read()
        text_area.insert(END, text)
    text_area.configure(state='normal')
    text_area.pack(side=LEFT)

    scroll = Scrollbar(new_window, command=text_area.yview)
    scroll.pack(side=LEFT, fill=Y)

    text_area.config(yscrollcommand=scroll.set)


def open_libraries():
    # Создание нового окна
    new_window = Toplevel(window)

    # Настройка нового окна
    new_window.title("Дополнительные библиотеки Python")
    text_area = Text(new_window, width=200, height=100)

    with open(license_library, 'r', encoding='utf-8') as file:
        text = file.read()
        text_area.insert(END, text)
    text_area.configure(state='normal')
    text_area.pack(side=LEFT)

    scroll = Scrollbar(new_window, command=text_area.yview)
    scroll.pack(side=LEFT, fill=Y)

    text_area.config(yscrollcommand=scroll.set)


def open_list_pioneers():
    """
    Функция для демонстрации списка людей, что участвовали во внедрении
    :return:
    """
    # Создание нового окна
    new_window = Toplevel(window)
    # Устанавливаем размер окна на весь экран
    screen_width = new_window.winfo_screenwidth()
    screen_height = new_window.winfo_screenheight()
    new_window.geometry(f"{screen_width}x{screen_height}+0+0")


    # Настройка нового окна
    new_window.title("Пионеры проекта")

    text_widget = Text(new_window, wrap=WORD, font=("Arial", 12), bg="white", fg="black")
    text_widget.pack(padx=10, pady=10, fill=BOTH, expand=True)

    # Настройка тегов для форматирования
    text_widget.tag_config("header", font=("Arial", 16, "bold"), foreground="blue")
    text_widget.tag_config("person", font=("Arial", 14))

    # Заголовок
    text_widget.insert(END, "Организаторы\n\n", "header")

    # Список людей
    orgs = [
        "Белькова Мария Родионовна - Республика Бурятия",
        "Бояркина Анна Витальевна - Красноярский край",
    ]

    # Добавляем организаторов в текстовый виджет
    for person in orgs:
        text_widget.insert(END, f"- {person}\n", "person")


    workers = [
        'Демина Татьяна Николаевна - Красноярский край',
        'Казарина Мария Александровна - Красноярский край',
    ]
    text_widget.insert(END,"\n\nПедагоги-психологи внесшие особый вклад\n\n", "header")
    # Добавляем учителей в текстовый виджет
    for worker in workers:
        text_widget.insert(END, f"- {worker}\n", "person")


    text_widget.insert(END,"\n\nПедагоги-психологи участники пилотного внедрения\n\n", "header")



    # Добавляем участников
    teachers  = [
        'Багмет Ольга Евгеньевна - Республика Бурятия',
        'Клыпина Юлия Александровна - Республика Бурятия',
        'Матис Ирина Николаевна - Республика Бурятия',
        'Монгуш Чинчи Орлановна - Республика Бурятия',
        'Попова Ольга Алексеевна - Республика Бурятия',
        'Чимитова Сэсэгма Дашинимаевна - Республика Бурятия',
        'Абрамов Константин Александрович - Республика Бурятия',


    ]
    # Добавляем учителей в текстовый виджет
    for teach in teachers:
        text_widget.insert(END, f"- {teach}\n", "person")



    # Отключаем редактирование текста
    text_widget.config(state=DISABLED)



if __name__ == '__main__':
    window = Tk()
    window.title('Лахеcис Обработка результатов психологических тестов ver 3.0')

    # Устанавливаем размер и положение окна
    set_window_size(window)

    window.resizable(True, True)
    # Добавляем контекстное меню в поля ввода
    make_textmenu(window)

    # Создаем вертикальный скроллбар
    scrollbar = Scrollbar(window, orient="vertical")

    # Создаем холст
    canvas = Canvas(window, yscrollcommand=scrollbar.set)
    canvas.pack(side="left", fill="both", expand=True)

    # Привязываем скроллбар к холсту
    scrollbar.config(command=canvas.yview)

    # Создаем ноутбук (вкладки)
    tab_control = ttk.Notebook(canvas)

    """
    Обработка результатов тестов
    """
    # Создаем вкладку обработки данных
    tab_report_all_age = ttk.Frame(tab_control)
    tab_control.add(tab_report_all_age, text='Обработка результатов\nтестов')
    tab_control.pack(expand=1, fill='both')
    # Добавляем виджеты на вкладку
    # Создаем метку для описания назначения программы
    lbl_hello_all_age = Label(tab_report_all_age,
                             text='Центр опережающей профессиональной подготовки Республики Бурятия\nОбработка результатов комплексных психологических и профориентационных тестов \n'
                             )
    lbl_hello_all_age.grid(column=0, row=0, padx=10, pady=25)

    # Картинка
    path_to_img_all_age = resource_path('logo.png')

    img_all_age = PhotoImage(file=path_to_img_all_age)
    Label(tab_report_all_age,
          image=img_all_age
          ).grid(column=1, row=0, padx=10, pady=25)

    # Создаем кнопку Выбрать файл с параметрами
    btn_choose_data_all_age = Button(tab_report_all_age, text='1) Выберите файл с параметрами',
                                    font=('Arial Bold', 14),
                                    command=select_file_params_all_age
                                    )
    btn_choose_data_all_age.grid(column=0, row=2, padx=10, pady=10)

    # Создаем кнопку Выбрать файл с данными
    btn_choose_data_all_age = Button(tab_report_all_age, text='2) Выберите файл с результатами',
                                    font=('Arial Bold', 14),
                                    command=select_file_data_xlsx_all_age
                                    )
    btn_choose_data_all_age.grid(column=0, row=3, padx=10, pady=10)

    # Создаем кнопку для выбора папки куда будут генерироваться файлы

    btn_choose_end_folder_all_age = Button(tab_report_all_age, text='3) Выберите конечную папку',
                                          font=('Arial Bold', 14),
                                          command=select_end_folder_all_age
                                          )
    btn_choose_end_folder_all_age.grid(column=0, row=4, padx=10, pady=10)

    # Создаем поле для ввода количества колонок без вопросов(анкетные данные)
    # Определяем переменную
    var_entry_threshold_all_age = StringVar()
    # Описание поля
    label_name_threshold_all_age = Label(tab_report_all_age,
                                        text='4) Введите количество колонок в начале таблицы\n не относящихся к вопросам тестов\nНапример 2')
    label_name_threshold_all_age.grid(column=0, row=5, padx=10, pady=5)
    # поле ввода
    entry_threshold_all_age = Entry(tab_report_all_age, textvariable=var_entry_threshold_all_age,
                                   width=30)
    entry_threshold_all_age.grid(column=0, row=6, padx=5, pady=5, ipadx=30, ipady=4)


    # Создаем поле для ввода количества колонок по которым нужно сделать свод
    # Определяем переменную
    var_entry_svod_all_age = StringVar()
    # Описание поля
    label_name_svod_all_age = Label(tab_report_all_age,
                                        text='5) Введите через запятую порядковые номера колонок по которым нужно сделать свод.\n'
                                             'Например 1,2 или 2 или 3,1,2\n'
                                             'или оставьте это поле пустым\n'
                                             ' если вам не надо делать своды по организациям, категориям и т.п.\n'
                                             'Можно ввести не более 3 целых цифр разделенных запятой')
    label_name_svod_all_age.grid(column=0, row=7, padx=10, pady=5)
    # поле ввода
    entry_svod_all_age = Entry(tab_report_all_age, textvariable=var_entry_svod_all_age,
                                   width=30)
    entry_svod_all_age.grid(column=0, row=8, padx=5, pady=5, ipadx=30, ipady=4)




    # Создаем кнопку обработки данных

    btn_proccessing_data_all_age = Button(tab_report_all_age, text='6) Обработать данные',
                                         font=('Arial Bold', 14),
                                         command=processing_all_age
                                         )
    btn_proccessing_data_all_age.grid(column=0, row=9, padx=10, pady=10)






    """
    Создание отчетов
    """

    tab_create_doc = ttk.Frame(tab_control)
    tab_control.add(tab_create_doc, text='Генерация документов\nпо результатам тестирования')
    tab_control.pack(expand=1, fill='both')

    # Добавляем виджеты на вкладку Создание документов
    # Создаем метку для описания назначения программы
    lbl_hello = Label(tab_create_doc,
                      text='Центр опережающей профессиональной подготовки Республики Бурятия\nГенерация результатов тестирования'
                           '')
    lbl_hello.grid(column=0, row=0, padx=10, pady=25)

    # Картинка
    path_to_img = resource_path('logo.png')
    img = PhotoImage(file=path_to_img)
    Label(tab_create_doc,
          image=img
          ).grid(column=1, row=0, padx=10, pady=25)

    # Создаем область для того чтобы поместить туда подготовительные кнопки(выбрать файл,выбрать папку и т.п.)
    frame_data_for_doc = LabelFrame(tab_create_doc, text='Подготовка')
    frame_data_for_doc.grid(column=0, row=2, padx=10)

    # Создаем кнопку Выбрать шаблон
    btn_template_doc = Button(frame_data_for_doc, text='1) Выберите шаблон документа', font=('Arial Bold', 14),
                              command=select_file_template_doc
                              )
    btn_template_doc.grid(column=0, row=3, padx=10, pady=10)
    #
    # Создаем кнопку Выбрать файл с данными
    btn_data_doc = Button(frame_data_for_doc, text='2) Выберите файл с данными', font=('Arial Bold', 14),
                          command=select_file_data_doc
                          )
    btn_data_doc.grid(column=0, row=4, padx=10, pady=10)
    #
    # Создаем кнопку для выбора папки куда будут генерироваться файлы

    # Определяем текстовую переменную
    entry_folder_structure = StringVar()
    # Описание поля
    label_folder_structure = Label(frame_data_for_doc,
                                   text='3) Введите через запятую порядковые номера колонок таблице\n по которым будет создаваться структура папок в которых будут файлы.\n'
                                        'Например 3,4,5 или 2,3. Может быть указано не более 4 колонок.\n МОЖНО НИЧЕГО НЕ УКАЗЫВАТЬ\n если вам не надо чтобы файлы были разложены по папкам (групп,классов и т.п.)')
    label_folder_structure.grid(column=0, row=5, padx=10, pady=5)
    # поле ввода
    entry_folder_structure = Entry(frame_data_for_doc, textvariable=entry_folder_structure, width=30)
    entry_folder_structure.grid(column=0, row=6, padx=5, pady=5, ipadx=30, ipady=4)

    # Поле для ввода названия генериуемых документов
    # Определяем текстовую переменную
    entry_name_file = StringVar()
    # Описание поля
    label_name_file = Label(frame_data_for_doc,
                                   text='4) Введите через запятую порядковые номера колонок в таблице\n по которым файлы будут называться.\n'
                                        'Например 6,7 или 3,4. Может быть указано не более 2 колонок')
    label_name_file.grid(column=0, row=7, padx=10, pady=5)
    # поле ввода
    entry_name_file = Entry(frame_data_for_doc, textvariable=entry_name_file, width=30)
    entry_name_file.grid(column=0, row=8, padx=5, pady=5, ipadx=30, ipady=4)


    entry_type_file = StringVar()
    # Описание поля
    label_name_column_type_file = Label(frame_data_for_doc, text='5) Введите что вы создаете.\n Например Результат тестирования или просто Результат')
    label_name_column_type_file.grid(column=0, row=9, padx=10, pady=5)
    # поле ввода
    type_file_column_entry = Entry(frame_data_for_doc, textvariable=entry_type_file, width=30)
    type_file_column_entry.grid(column=0, row=10, padx=5, pady=5, ipadx=30, ipady=4)

    btn_choose_end_folder_doc = Button(frame_data_for_doc, text='6) Выберите конечную папку', font=('Arial Bold', 14),
                                       command=select_end_folder_doc
                                       )
    btn_choose_end_folder_doc.grid(column=0, row=11, padx=10, pady=10)

    # Создаем переключатель для вариантов короткого или полного
    mode_full_type = StringVar()
    mode_full_type.set('No')
    # Создаем чекбокс для выбора режима создания документов
    chbox_full_type = Checkbutton(frame_data_for_doc,
                                 text='Поставьте галочку, если вам нужно  \n'
                                      'включить краткий режим при нем будут создаваться только pdf.\n'
                                      'В полном режиме создаются docx, объединенный файл, файл с архивом ',
                                 variable=mode_full_type,
                                 offvalue='No',
                                 onvalue='Yes')
    chbox_full_type.grid(column=0, row=12, padx=1, pady=1)


    # Создаем чекбокс для режима создания pdf
    # Создаем переменную для хранения результа переключения чекбокса
    mode_pdf_value = StringVar()

    # Устанавливаем значение по умолчанию для этой переменной. По умолчанию PDF варианты создаваться не будут
    mode_pdf_value.set('No')

    # Создаем чекбокс для выбора режима подсчета

    chbox_mode_pdf = Checkbutton(frame_data_for_doc,
                                 text='Поставьте галочку, если вам нужно чтобы \n'
                                      'в полном режиме дополнительно создавались pdf версии документов',
                                 variable=mode_pdf_value,
                                 offvalue='No',
                                 onvalue='Yes')
    chbox_mode_pdf.grid(column=0, row=13, padx=1, pady=1)


    # Создаем кнопку для создания документов из таблиц с произвольной структурой
    btn_create_files_other = Button(tab_create_doc, text='7) Получить результаты',
                                    font=('Arial Bold', 14),
                                    command=processing_generate_docs
                                    )
    btn_create_files_other.grid(column=0, row=14, padx=10, pady=10)

    """
      Создаем вкладку создания документов
      """
    tab_create_other_doc = Frame(tab_control)
    tab_control.add(tab_create_other_doc, text='Создание\nдокументов')

    create_other_doc_frame_description = LabelFrame(tab_create_other_doc)
    create_other_doc_frame_description.pack()

    lbl_hello = Label(create_other_doc_frame_description,
                      text='Генерация документов по шаблону\n'
                           'ПРИМЕЧАНИЯ\n'
                           'Данные обрабатываются С ПЕРВОГО ЛИСТА В ФАЙЛЕ !!!\n'
                           'Заголовок таблицы должен занимать только первую строку!\n'
                           'Для корректной работы программы уберите из таблицы\nобъединенные ячейки'
                      , width=60)
    lbl_hello.pack(side=LEFT, anchor=N, ipadx=25, ipady=10)
    # #
    # #
    # Картинка
    path_to_img_other_doc = resource_path('logo.png')
    img_other_doc = PhotoImage(file=path_to_img_other_doc)
    Label(create_other_doc_frame_description,
          image=img_other_doc, padx=10, pady=10
          ).pack(side=LEFT, anchor=E, ipadx=5, ipady=5)

    # Создаем фрейм для действий
    create_other_doc_frame_action = LabelFrame(tab_create_other_doc, text='Подготовка')
    create_other_doc_frame_action.pack()

    # Создаем кнопку Выбрать шаблон
    btn_template_other_doc = Button(create_other_doc_frame_action, text='1) Выберите шаблон документа',
                                    font=('Arial Bold', 14),
                                    command=select_file_template_other_doc
                                    )
    btn_template_other_doc.pack(padx=10, pady=10)

    btn_data_other_doc = Button(create_other_doc_frame_action, text='2) Выберите файл с данными',
                                font=('Arial Bold', 14),
                                command=select_file_data_other_doc
                                )
    btn_data_other_doc.pack(padx=10, pady=10)
    #
    # Создаем кнопку для выбора папки куда будут генерироваться файлы

    # Определяем текстовую переменную
    entry_name_column_data_other_doc = StringVar()
    # Описание поля
    label_name_column_data_other_doc = Label(create_other_doc_frame_action,
                                             text='3) Введите название колонки в таблице\n по которой будут создаваться имена файлов')
    label_name_column_data_other_doc.pack(padx=10, pady=10)
    # поле ввода
    data_column_entry_other_doc = Entry(create_other_doc_frame_action, textvariable=entry_name_column_data_other_doc,
                                        width=30)
    data_column_entry_other_doc.pack(ipady=5)

    # Поле для ввода названия генериуемых документов
    # Определяем текстовую переменную
    entry_type_file_other_doc = StringVar()
    # Описание поля
    label_name_column_type_file_other_doc = Label(create_other_doc_frame_action,
                                                  text='4) Введите название создаваемых документов')
    label_name_column_type_file_other_doc.pack(padx=10, pady=10)
    # поле ввода
    type_file_column_entry_other_doc = Entry(create_other_doc_frame_action, textvariable=entry_type_file_other_doc,
                                             width=30)
    type_file_column_entry_other_doc.pack(ipady=5)

    btn_choose_end_folder_other_doc = Button(create_other_doc_frame_action, text='5) Выберите конечную папку',
                                             font=('Arial Bold', 14),
                                             command=select_end_folder_other_doc
                                             )
    btn_choose_end_folder_other_doc.pack(padx=10, pady=10)

    # Создаем область для того чтобы поместить туда опции
    frame_data_for_options_other_doc = LabelFrame(tab_create_other_doc, text='Дополнительные опции')
    frame_data_for_options_other_doc.pack(padx=10, pady=10)

    # Создаем переменную для хранения переключателя сложного сохранения
    mode_structure_folder_value_other_doc = StringVar()
    mode_structure_folder_value_other_doc.set('No')  # по умолчанию сложная структура создаваться не будет
    chbox_mode_structure_folder_other_doc = Checkbutton(frame_data_for_options_other_doc,
                                                        text='Поставьте галочку, если вам нужно чтобы файлы были сохранены по дополнительным папкам',
                                                        variable=mode_structure_folder_value_other_doc,
                                                        offvalue='No',
                                                        onvalue='Yes')
    chbox_mode_structure_folder_other_doc.pack()
    # Создаем поле для ввода
    # Определяем текстовую переменную
    entry_structure_folder_value_other_doc = StringVar()
    # Описание поля
    label_number_column_other_doc = Label(frame_data_for_options_other_doc,
                                          text='Введите через запятую не более 3 порядковых номеров колонок по которым будет создаваться структура папок.\n'
                                               'Например: 4,15,8')
    label_number_column_other_doc.pack()
    # поле ввода
    entry_value_number_column_other_doc = Entry(frame_data_for_options_other_doc,
                                                textvariable=entry_structure_folder_value_other_doc, width=30)
    entry_value_number_column_other_doc.pack(ipady=5)

    # Переключатель краткой версии или полной версии
    mode_full_value_other_doc = StringVar()

    # Устанавливаем значение по умолчанию для этой переменной. По умолчанию будет вестись подсчет числовых данных
    mode_full_value_other_doc.set('No')
    # Создаем чекбокс для выбора режима подсчета

    chbox_mode_full_other_doc = Checkbutton(frame_data_for_options_other_doc,
                                            text='Поставьте галочку, если вам нужно чтобы создавались ТОЛЬКО pdf файлы. Работает только в Windows!',
                                            variable=mode_full_value_other_doc,
                                            offvalue='No',
                                            onvalue='Yes')
    chbox_mode_full_other_doc.pack()

    # Создаем переменную для хранения результа переключения чекбокса
    mode_combine_value_other_doc = StringVar()

    # Устанавливаем значение по умолчанию для этой переменной. По умолчанию будет вестись подсчет числовых данных
    mode_combine_value_other_doc.set('No')
    # Создаем чекбокс для выбора режима подсчета

    chbox_mode_calculate_other_doc = Checkbutton(frame_data_for_options_other_doc,
                                                 text='Поставьте галочку, если вам нужно чтобы все файлы были объединены в один',
                                                 variable=mode_combine_value_other_doc,
                                                 offvalue='No',
                                                 onvalue='Yes')
    chbox_mode_calculate_other_doc.pack()

    # Создаем чекбокс для режима создания pdf
    # Создаем переменную для хранения результа переключения чекбокса
    mode_pdf_value_other_doc = StringVar()

    # Устанавливаем значение по умолчанию для этой переменной. По умолчанию будет вестись подсчет числовых данных
    mode_pdf_value_other_doc.set('No')
    # Создаем чекбокс для выбора режима подсчета

    chbox_mode_pdf_other_doc = Checkbutton(frame_data_for_options_other_doc,
                                           text='Поставьте галочку, если вам нужно чтобы \n'
                                                'дополнительно создавались pdf версии документов',
                                           variable=mode_pdf_value_other_doc,
                                           offvalue='No',
                                           onvalue='Yes')
    chbox_mode_pdf_other_doc.pack()

    # создаем чекбокс для единичного документа

    # Создаем переменную для хранения результа переключения чекбокса
    mode_group_doc_value_other_doc = StringVar()

    # Устанавливаем значение по умолчанию для этой переменной. По умолчанию будет вестись подсчет числовых данных
    mode_group_doc_value_other_doc.set('No')
    # Создаем чекбокс для выбора режима подсчета
    chbox_mode_group_other_doc = Checkbutton(frame_data_for_options_other_doc,
                                             text='Поставьте галочку, если вам нужно создать один документ\nдля конкретного значения (например для определенного ФИО)',
                                             variable=mode_group_doc_value_other_doc,
                                             offvalue='No',
                                             onvalue='Yes')
    chbox_mode_group_other_doc.pack(padx=10, pady=10)
    # Создаем поле для ввода значения по которому будет создаваться единичный документ
    # Определяем текстовую переменную
    entry_value_column_single_other_doc = StringVar()
    # Описание поля
    label_name_column_group_other_doc = Label(frame_data_for_options_other_doc,
                                              text='Введите значение из колонки\nуказанной на шаге 3 для которого нужно создать один документ,\nнапример конкретное ФИО')
    label_name_column_group_other_doc.pack()
    # поле ввода
    type_file_group_entry_other_doc = Entry(frame_data_for_options_other_doc,
                                            textvariable=entry_value_column_single_other_doc, width=30)
    type_file_group_entry_other_doc.pack(ipady=5)

    # Создаем кнопку для создания документов из таблиц с произвольной структурой
    btn_create_files_other_doc = Button(tab_create_other_doc, text='6) Создать документ(ы)',
                                        font=('Arial Bold', 20),
                                        command=generate_other_docs
                                        )
    btn_create_files_other_doc.pack(padx=10, pady=10)

    """
       Создаем вкладку для размещения описания программы, руководства пользователя,лицензии.
       """

    tab_about = ttk.Frame(tab_control)
    tab_control.add(tab_about, text='О ПРОГРАММЕ')

    about_frame_description = LabelFrame(tab_about, text='О программе')
    about_frame_description.pack()

    lbl_about = Label(about_frame_description,
                      text="""Лахесис Обработка результатов психологических тестов.
                              Версия 3.0
                              Язык программирования - Python 3\n
                              Используемая лицензия BSD-2-Clause\n
                              Copyright (c) <2025> <Будаев Олег Тимурович>\n
                              Организатор <Белькова Мария Родионовна>\n
                              Адрес сайта программы: https://itdarhan.ru/laсhesis.html\n
                              Свидетельство о государственной регистрации № 2025616743\n
                              Реестровая запись №27936 от 06.05.2025 в реестре 
                              Российского программного обеспечения.
                              
                              Чтобы скопировать ссылку или текст переключитесь на \n
                              английскую раскладку.
                              """, width=60)

    lbl_about.pack(side=LEFT, anchor=N, ipadx=25, ipady=10)
    # Картинка
    path_to_img_about = resource_path('logo.png')
    img_about = PhotoImage(file=path_to_img_about)
    Label(about_frame_description,
          image=img_about, padx=10, pady=10
          ).pack(side=LEFT, anchor=E, ipadx=5, ipady=5)

    # Создаем поле для лицензий библиотек
    guide_frame_description = LabelFrame(tab_about, text='Ссылки для скачивания и обучающие материалы')
    guide_frame_description.pack()

    text_area_url = Text(guide_frame_description, width=84, height=20)
    list_url_path = resource_path('Ссылки.txt')  # путь к файлу лицензии
    with open(list_url_path, 'r', encoding='utf-8') as file:
        text = file.read()
        text_area_url.insert(END, text)
    text_area_url.configure(state='normal')
    text_area_url.pack(side=LEFT)

    scroll = Scrollbar(guide_frame_description, command=text_area_url.yview)
    scroll.pack(side=LEFT, fill=Y)

    text_area_url.config(yscrollcommand=scroll.set)

    text_area_url.configure(state='normal')
    text_area_url.pack(side=LEFT)

    # Кнопка для демонстрации ФИО первопроходцев
    button_pioneers = Button(tab_about, text="Пионеры", command=open_list_pioneers)
    button_pioneers.pack(padx=10, pady=10)


    # Кнопка, для демонстрации в отдельном окне списка изменений
    list_changes_path = resource_path('Список изменений.txt')  # путь к файлу лицензии
    button_list_changes = Button(tab_about, text="Список изменений", command=open_list_changes)
    button_list_changes.pack(padx=10, pady=10)

    # Кнопка, для демонстрации в отдельном окне лицензии
    license_path = resource_path('License.txt')  # путь к файлу лицензии
    button_lic = Button(tab_about, text="Лицензия", command=open_license)
    button_lic.pack(padx=10, pady=10)

    # Кнопка, для демонстрации в отдельном окне используемых библиотек
    license_library = resource_path('LibraryLicense.txt')  # путь к файлу с библиотеками
    button_lib = Button(tab_about, text="Дополнительные библиотеки Python", command=open_libraries)
    button_lib.pack(padx=10, pady=10)





    # Создаем виджет для управления полосой прокрутки
    canvas.create_window((0, 0), window=tab_control, anchor="nw")

    # Конфигурируем холст для обработки скроллинга
    canvas.config(yscrollcommand=scrollbar.set, scrollregion=canvas.bbox("all"))
    scrollbar.pack(side="right", fill="y")

    # Вешаем событие скроллинга
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    window.bind_class("Entry", "<Button-3><ButtonRelease-3>", show_textmenu)
    window.bind_class("Entry", "<Control-a>", callback_select_all)
    window.mainloop()
