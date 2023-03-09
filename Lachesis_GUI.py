import tkinter
import sys
import os
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
# pd.options.mode.chained_assignment = None  # default='warn'
import warnings
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
import pandas as pd
import numpy as np
import openpyxl
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
from openpyxl.styles import Alignment
import time

"""
Обработка результатов профориентационных тестов из яндекс форм
"""

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller
    Функция чтобы логотип отображался"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


def select_folder_data():
    """
    Функция для выбора папки c данными
    :return:
    """
    global path_folder_data
    path_folder_data = filedialog.askdirectory()

def select_end_folder():
    """
    Функция для выбора конечной папки куда будут складываться итоговые файлы
    :return:
    """
    global path_to_end_folder
    path_to_end_folder = filedialog.askdirectory()

def select_file_docx():
    """
    Функция для выбора файла Word
    :return: Путь к файлу шаблона
    """
    global file_docx
    file_docx = filedialog.askopenfilename(
        filetypes=(('Word files', '*.docx'), ('all files', '*.*')))

def select_file_data_xlsx():
    """
    Функция для выбора файла с данными на основе которых будет генерироваться документ
    :return: Путь к файлу с данными
    """
    global file_data_xlsx
    # Получаем путь к файлу
    file_data_xlsx = filedialog.askopenfilename(filetypes=(('Excel files', '*.xlsx'), ('all files', '*.*')))

def select_files_data_xlsx():
    """
    Функция для выбора нескоьких файлов с данными на основе которых будет генерироваться документ
    :return: Путь к файлу с данными
    """
    global files_data_xlsx
    # Получаем путь файлы
    files_data_xlsx = filedialog.askopenfilenames(filetypes=(('Excel files', '*.xlsx'), ('all files', '*.*')))

"""
Фунции ДДО
"""

def processing_ddo():
    """
    Фугкция для обработки данных ДДО
    :return:
    """
    try:
        # Создаем словари для создания текста письма
        global dct_prof
        dct_prof = {
            'Человек-природа': 'Тракторист, рыбовод, зоотехник, агроном, садовник, ветеринар, животновод, геолог, биолог, почвовед и т.д.',
            'Человек-техника': 'Водитель, токарь, инженер, слесарь, радиотехник, швея, электрик, механик, монтажник и т.п.',
            'Человек-человек': 'Продавец, медсестра, секретарь, бортпроводник, учитель, воспитатель, няня, преподаватель, врач, официант, администратор и т.п.',
            'Человек-знаковые системы': 'Наборщик, кассир, делопроизводитель, бухгалтер, программист, чертежник, корректор, экономист, радист, оператор ПЭВМ, машинистка, наборщик и т.п.',
            'Человек-художественный образ': 'Парикмахер, модельер, чеканщик, маляр, гравер, резчик по камню, фотограф, актер, художник, музыкант и т.п.'}

        global dct_desciprion
        dct_desciprion = {'Человек-природа':
"""Выявленный тип профессий - Человек-природа.\n
Представителей этих профессий объединяет одно очень важное качество — любовь к 
природе. Но любовь не созерцательная. Которой обладают практически все люди, 
считая природу наиболее благоприятной средой для отдыха, а деятельная связанная с
познанием ее законов и применением их. Одно дело — любить животных и растения,
играть с ними, радоваться им. И совсем другое — регулярно, день за днем ухаживать
за ними, наблюдать, лечить, выгуливать, не считаясь с личным временем и планами.
Специалист должен не просто все знать о живых организмах, но и прогнозировать
возможные изменения в них и принимать меры. От человека требуется инициатива и
самостоятельность в решении конкретных задач, заботливость, терпение и
дальновидность.\n 
Человек, работающий в сфере «человек-природа», должен быть спокойным и уравновешенным.""",
'Человек-техника': """Выявленный тип профессий - Человек-техника.\n
Особенность технических объектов в том, что они, как правило, могут быть точно
измерены по многим признакам. При их обработке, преобразовании, перемещении
или оценке от работника требуется точность, определенность действий. Техника как
предмет труда представляет широкие возможности для новаторства, выдумки,
творчества, поэтому важное значение приобретает такое качество, как практическое
мышление. Техническая фантазия, способность мысленно соединять и разъединять
технические объекты и их части — важные условия для успеха в данной области.
""", 'Человек-человек': """Выявленный тип профессий - Человек-человек.\n
Главное содержание труда в профессиях типа «человек-человек» сводится к
взаимодействию между людьми. Если не наладится это взаимодействие, значит, не
наладится и работа. Качества, необходимые для работы с людьми: устойчивое,
хорошее настроение в процессе работы с людьми, потребность в общении,
способность мысленно ставить себя на место другого человека, быстро понимать
намерения, помыслы, настроение людей, умение разбираться в человеческих
взаимоотношениях, хорошая память (умение держать в уме имена и особенности
многих людей), терпение.
""", 'Человек-знаковые системы': """Выявленный тип профессий - Человек-знаковая система.\n
Мы встречаемся со знаками значительно чаще, чем обычно представляем себе. Это
цифры. Коды, условные знаки, естественные или искусственные языки, чертежи,
таблицы формулы. В любом случае человек воспринимает знак как символ реального
объекта или явления. Поэтому специалисту, который работает со знаками, важно
уметь, с одной стороны, абстрагироваться от реальных физических, химически,
механических свойств предметов, а с другой —представлять и воспринимать
характеристики реальных явлений или объектов, стоящих за знаками. Чтобы успешно
работать в какой-нибудь профессии данного типа, необходимо уметь мысленно
погружаться в мир, казалось бы, сухих обозначений и сосредотачиваться на
сведениях, которые они несут в себе. Особые требования профессии этого типа
предъявляют к вниманию.
""", 'Человек-художественный образ': """Выявленный тип профессий - Человек-художественный образ.\n
Важнейшие требования, которые предъявляют профессии, связанные с изобразительной, музыкальной, литературно-художественной, актерско-сценической деятельностью человека это
наличие способности к искусствам, творческое воображение, образное мышление, талант, трудолюбие."""}

        df = pd.read_excel(file_data_xlsx)

        # переименовываем колонки
        df.columns = range(df.shape[1])
        df.rename(columns={0: 'ID', 1: 'Дата_создания', 2: 'Дата_изменения', 3: 'ФИО', 4: 'Населенный_пункт', 5: 'Школа',
                           6: 'Класс', 7: 'Электронная_почта'}, inplace=True)
        # делаем цифровые названия колонок строковыми
        df.columns = list(map(str, df.columns))

        df['Тип_профессии'] = df.apply(processing_result_ddo, axis=1)
        df['Тип_профессии'] =  df['Тип_профессии'].astype(str)

        df['Итог'] = df['Тип_профессии'].apply(create_out_str_ddo)

        df['Итог'] = df['ФИО'] + ' \nДифференциально-диагностический опросник\n ' + df['Итог']

        # генерируем текущее время
        t = time.localtime()
        current_time = time.strftime('%H_%M_%S', t)

        df.to_excel(f'{path_to_end_folder}/Полная таблица с результатами ДДО от {current_time}.xlsx', index=False)

        # Создаем сокращенный вариант
        send_df = df[
            ['Дата_изменения', 'ФИО', 'Населенный_пункт', 'Школа', 'Класс', 'Электронная_почта', 'Тип_профессии',
             'Итог']]

        wb = openpyxl.Workbook()

        for row in dataframe_to_rows(send_df, index=False, header=True):
            wb['Sheet'].append(row)

        wb['Sheet'].column_dimensions['A'].width = 15
        wb['Sheet'].column_dimensions['B'].width = 40
        wb['Sheet'].column_dimensions['C'].width = 30
        wb['Sheet'].column_dimensions['D'].width = 20
        wb['Sheet'].column_dimensions['E'].width = 10
        wb['Sheet'].column_dimensions['F'].width = 20
        wb['Sheet'].column_dimensions['G'].width = 20
        wb['Sheet'].column_dimensions['H'].width = 40

        wb.save(f'{path_to_end_folder}/Таблица для рассылки с результатами ДДО  от {current_time}.xlsx')
    except NameError:
        messagebox.showerror('Лахезис Обработка результатов профориентационных тестов ver 1.0',
                             f'Выберите файлы с данными и папку куда будет генерироваться файл')
    except KeyError as e:
        messagebox.showerror('Лахезис Обработка результатов профориентационных тестов ver 1.0',
                             f'В таблице не найдена указанная колонка {e.args}')
    except FileNotFoundError:
        messagebox.showerror('Лахезис Обработка результатов профориентационных тестов ver 1.0',
                             f'Перенесите файлы которые вы хотите обработать в корень диска. Проблема может быть\n '
                             f'в слишком длинном пути к обрабатываемым файлам')
    else:
        messagebox.showinfo('Лахезис Обработка результатов профориентационных тестов ver 1.0', 'Данные успешно обработаны')



def create_out_str_ddo(x):
    """
    Функция для создания выходной строки ДДО
    """
    return f'{dct_desciprion.get(x, "Проверьте результаты в колонке Тип_профессии")}\nРекомендуемые профессии:\n{dct_prof.get(x, "Проверьте результаты в колонке Тип_профессии")}'


def processing_result_ddo(row):
    """
    Обработка результатов тестирования
    """

    # Создаем словарь для хранения данных
    dct_type = {'Человек-природа': 0, 'Человек-техника': 0, 'Человек-человек': 0, 'Человек-знаковые системы': 0,
                'Человек-художественный образ': 0}
    dct_error = {}  # словарь для хранения ошибочных  значений, для того чтобы было легче находить ошибки при обновлении
    # 1
    if row[8] == 'Ухаживать за животными.':
        dct_type['Человек-природа'] += 1
    elif row[8] == 'Обслуживать машины, приборы (следить, регулировать).':
        dct_type['Человек-техника'] += 1
    else:
        dct_error[1] = row[8]

    # 2
    if row[9] == 'Помогать больным.':
        dct_type['Человек-человек'] += 1
    elif row[9] == 'Составлять таблицы, схемы, компьютерные программы.':
        dct_type['Человек-знаковые системы'] += 1
    else:
        dct_error[2] = row[9]

    # 3
    if row[10] == 'Следить за качеством книжных иллюстраций, плакатов, художественных открыток, музыкальных записей.':
        dct_type['Человек-художественный образ'] += 1
    elif row[10] == 'Следить за состоянием и развитием растений.':
        dct_type['Человек-природа'] += 1
    else:
        dct_error[3] = row[10]

    # 4
    if row[11] == 'Обрабатывать материалы (дерево, ткань, металл, пластмассу и т.п.).':
        dct_type['Человек-техника'] += 1
    elif row[11] == 'Доводить товары до потребителя, рекламировать, продавать.':
        dct_type['Человек-человек'] += 1
    else:
        dct_error[4] = row[11]

    # 5
    if row[12] == 'Обсуждать научно-популярные книги, статьи.':
        dct_type['Человек-знаковые системы'] += 1
    elif row[12] == 'Обсуждать художественные книги (или пьесы, концерты).':
        dct_type['Человек-художественный образ'] += 1
    else:
        dct_error[5] = row[12]

    # 6
    if row[13] == 'Выращивать молодняк (животных какой-либо породы).':
        dct_type['Человек-природа'] += 1
    elif row[
        13] == 'Тренировать товарищей (или младших) для выполнения и закрепления каких-либо навыков (трудовых, учебных, спортивных).':
        dct_type['Человек-человек'] += 1
    else:
        dct_error[6] = row[13]
    # 7
    if row[14] == 'Копировать рисунки, изображения (или настраивать музыкальные инструменты).':
        dct_type['Человек-художественный образ'] += 1
    elif row[
        14] == 'Управлять какой-либо машиной (грузовым, подъемным или транспортным средством) - подъемным краном, трактором, тепловозом и др.':
        dct_type['Человек-техника'] += 1
    else:
        dct_error[7] = row[14]

    # 8
    if row[15] == 'Сообщать, разъяснять людям нужные им сведения (в справочном бюро, на экскурсии и т.д.).':
        dct_type['Человек-человек'] += 1
    elif row[15] == 'Оформлять выставки, витрины (или участвовать в подготовке пьес, концертов).':
        dct_type['Человек-художественный образ'] += 1
    else:
        dct_error[8] = row[15]

    # 9
    if row[16] == 'Ремонтировать вещи, изделия (одежду, технику), жилище.':
        dct_type['Человек-техника'] += 1
    elif row[16] == 'Искать и исправлять ошибки в текстах, таблицах, рисунках.':
        dct_type['Человек-знаковые системы'] += 1
    else:
        dct_error[9] = row[16]

    # 10
    if row[17] == 'Лечить животных.':
        dct_type['Человек-природа'] += 1
    elif row[17] == 'Выполнять вычисления, расчёты.':
        dct_type['Человек-знаковые системы'] += 1
    else:
        dct_error[10] = row[17]

    # 11
    if row[18] == 'Выводить новые сорта растений.':
        dct_type['Человек-природа'] += 1
    elif row[18] == 'Конструировать, новые виды промышленных изделий (машины, одежду, дома, продукты питания и т.п.).':
        dct_type['Человек-техника'] += 1
    else:
        dct_error[11] = row[18]

    # 12
    if row[19] == 'Разбирать споры, ссоры между людьми, убеждать, разъяснять, наказывать, поощрять.':
        dct_type['Человек-человек'] += 1
    elif row[19] == 'Разбираться в чертежах, схемах, таблицах (проверять, уточнять, приводить в порядок).':
        dct_type['Человек-знаковые системы'] += 1
    else:
        dct_error[12] = row[19]

    # 13
    if row[20] == 'Наблюдать, изучать работу коллективов художественной самодеятельности.':
        dct_type['Человек-художественный образ'] += 1
    elif row[20] == 'Наблюдать, изучать жизнь микробов.':
        dct_type['Человек-природа'] += 1
    else:
        dct_error[13] = row[20]

    # 14
    if row[21] == 'Обслуживать, налаживать медицинские приборы, аппараты.':
        dct_type['Человек-техника'] += 1
    elif row[21] == 'Оказывать людям медицинскую помощь при ранениях, ушибах, ожогах и т.п.':
        dct_type['Человек-человек'] += 1
    else:
        dct_error[14] = row[21]

    # 15
    if row[22] == 'Художественно описывать, изображать события (наблюдаемые и представляемые).':
        dct_type['Человек-знаковые системы'] += 1
    elif row[22] == 'Составлять точные описания-отчеты о наблюдаемых явлениях, событиях, измеряемых объектах и др.':
        dct_type['Человек-художественный образ'] += 1
    else:
        dct_error[15] = row[22]

    # 16
    if row[23] == 'Делать лабораторные анализы в больнице.':
        dct_type['Человек-природа'] += 1
    elif row[23] == 'Принимать, осматривать больных, беседовать с ними, назначать лечение.':
        dct_type['Человек-человек'] += 1
    else:
        dct_error[16] = row[23]

    # 17
    if row[24] == 'Красить или расписывать стены помещений, поверхность изделий.':
        dct_type['Человек-техника'] += 1
    elif row[24] == 'Осуществлять монтаж или сборку машин, приборов.':
        dct_type['Человек-техника'] += 1
    else:
        dct_error[17] = row[24]

    # 18
    if row[25] == 'Организовывать культпоходы сверстников или младших в театры, музеи, экскурсии, туристические походы и т.п.':
        dct_type['Человек-человек'] += 1
    elif row[25] == 'Играть на сцене, принимать участие в концертах.':
        dct_type['Человек-художественный образ'] += 1
    else:
        dct_error[18] = row[25]

    # 19
    if row[26] == 'Изготовлять по чертежам детали, изделия (машины, одежду), строить здания.':
        dct_type['Человек-техника'] += 1
    elif row[26] == 'Заниматься черчением, копировать чертежи, карты.':
        dct_type['Человек-знаковые системы'] += 1
    else:
        dct_error[19] = row[26]

    # 20
    if row[27] == 'Вести борьбу с болезнями растений, с вредителями леса, сада.':
        dct_type['Человек-природа'] += 1
    elif row[27] == 'Работать на устройствах с клавиатурой, ноутбуке и др.).':
        dct_type['Человек-знаковые системы'] += 1

    if len(dct_error) > 0:
        return dct_error
    else:
        # возвращаем элемент с максимальным значением
        return max(dct_type, key=dct_type.get)


if __name__ == '__main__':
    window = Tk()
    window.title('Лахезис Обработка результатов профориентационных тестов ver 1.0')
    window.geometry('700x860')
    window.resizable(False, False)


    # Создаем объект вкладок

    tab_control = ttk.Notebook(window)

    # Создаем вкладку обработки данных ДДО
    tab_report_ddo = ttk.Frame(tab_control)
    tab_control.add(tab_report_ddo, text='ДДО')
    tab_control.pack(expand=1, fill='both')
    # Добавляем виджеты на вкладку ДДО
    # Создаем метку для описания назначения программы
    lbl_hello = Label(tab_report_ddo,
                      text='Центр опережающей профессиональной подготовки Республики Бурятия\nДифференциально-диагностический опросник ')
    lbl_hello.grid(column=0, row=0, padx=10, pady=25)

    # Картинка
    path_to_img_ddo = resource_path('logo.png')

    img_ddo = PhotoImage(file=path_to_img_ddo)
    Label(tab_report_ddo,
          image=img_ddo
          ).grid(column=1, row=0, padx=10, pady=25)

    # Создаем кнопку Выбрать файл с данными
    btn_choose_data = Button(tab_report_ddo, text='1) Выберите файл с результатами', font=('Arial Bold', 20),
                          command=select_file_data_xlsx
                          )
    btn_choose_data.grid(column=0, row=2, padx=10, pady=10)

    # Создаем кнопку для выбора папки куда будут генерироваться файлы

    btn_choose_end_folder = Button(tab_report_ddo, text='2) Выберите конечную папку', font=('Arial Bold', 20),
                                       command=select_end_folder
                                       )
    btn_choose_end_folder.grid(column=0, row=3, padx=10, pady=10)

    #Создаем кнопку обработки данных

    btn_proccessing_data = Button(tab_report_ddo, text='3) Обработать данные', font=('Arial Bold', 20),
                                       command=processing_ddo
                                       )
    btn_proccessing_data.grid(column=0, row=4, padx=10, pady=10)

    window.mainloop()