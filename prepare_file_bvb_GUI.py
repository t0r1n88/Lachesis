import numpy as np
import os
import pandas as pd
from dateutil.parser import ParserError
from docxtpl import DocxTemplate
from docx2pdf import convert
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import tkinter
import openpyxl
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
from openpyxl.styles import Alignment
from openpyxl import load_workbook
import time
import datetime
import warnings
from collections import Counter
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')
pd.options.mode.chained_assignment = None
import sys
import locale
import logging
logging.basicConfig(
    level=logging.WARNING,
    filename="error.log",
    filemode='w',
    # чтобы файл лога перезаписывался  при каждом запуске.Чтобы избежать больших простыней. По умолчанию идет 'a'
    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
    datefmt='%H:%M:%S',
)

import re

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller
    Функция чтобы логотип отображался"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def select_folder():
    """
    Функция для выбора папки откуда будут браться файлы
    :return:
    """
    global path_to_dir
    path_to_dir = filedialog.askdirectory()



def select_end_folder():
    """
    Функция для выбора папки куда будут генерироваться файлы
    :return:
    """
    global path_to_end
    path_to_end = filedialog.askdirectory()

def select_file_mun():
    """
    Функция для выбора файла с данными муниципалитета
    :return: Путь к файлу с данными
    """
    global munic_file
    # Получаем путь к файлу
    munic_file = filedialog.askopenfilename(filetypes=(('Excel files', '*.xlsx'), ('all files', '*.*')))

def select_file_template():
    """
    Функция для выбора файла с данными муниципалитета
    :return: Путь к файлу с данными
    """
    global template_file
    # Получаем путь к файлу
    template_file = filedialog.askopenfilename(filetypes=(('Excel files', '*.xlsx'), ('all files', '*.*')))


def restore_inn_org(value):
    """
    проверка и восстановление ИНН
    """
    value = str(value)
    if len(value) == 9:
        return '0' + value
    elif len(value) == 10:
        return value
    else:
        return 'Неправильный ИНН'


def restore_mun(value):
    """
    Функция для восстановления правильного названия района
    """
    value = str(value)
    result = re.search(r'[А-Я][а-я]+[-]?', value)
    if result:
        mun_name = result.group()
        for title in lst_mun:
            if mun_name in title:
                return title
    else:
        return 'Не найдено'


def divide_str(value):
    """
    Функция для выделения первого слова в строке на случай если в ячейку было некорректно вставлено полное фио
    """
    value = str(value)
    return value.split(' ')[0]



def processing_data():
    """
    функция для восстановления длины ИНН, исправления муниципалитета, очистки от пробельных символов
    :return:
    """
    munic_df = pd.read_excel(munic_file)
    global lst_mun
    lst_mun = munic_df['Наименование'].to_list()


    try:
        for file in os.listdir(path_to_dir):
            print(file)
            df = pd.read_excel(f'{path_to_dir}/{file}',engine='openpyxl')
            df.fillna('', inplace=True)

            df['ИНН школы'] = df['ИНН школы'].apply(restore_inn_org)  # восстанавливаем ИНН
            df['Муниципалитет'] = df['Муниципалитет'].apply(restore_mun)  # правильный муниципалитет
            # очищаем от пробельных символов
            df['Роль'] = df['Роль'].apply(lambda x: x.strip())
            df.iloc[:, 4] = df.iloc[:, 4].apply(lambda x: x.strip())
            df['Фамилия'] = df['Фамилия'].apply(lambda x: x.strip())
            df['Фамилия'] = df['Фамилия'].apply(divide_str)
            df['Имя'] = df['Имя'].apply(lambda x: x.strip())
            df['Отчество'] = df['Отчество'].apply(lambda x: x.strip())

            wb = load_workbook(template_file)
            for r in dataframe_to_rows(df,index=False,header=False):
                wb['Списко пользователей'].append(r)

            wb.save(f'{path_to_end}/{file}')
            wb.close()



    except NameError as e:
        messagebox.showerror('Подготовка к импорту 1.0',
                             f'Выберите шаблон,файл с данными и папку куда будут генерироваться файлы')
    except KeyError as e:
        messagebox.showerror('Подготовка к импорту 1.0',
                             f'В таблице не найдена указанная колонка {e.args}')
    except PermissionError:
        messagebox.showerror('Подготовка к импорту 1.0',
                             f'Закройте все файлы созданные Минервой')
    except FileNotFoundError:
        messagebox.showerror('Подготовка к импорту 1.0',
                             f'Перенесите файлы которые вы хотите обработать в корень диска. Проблема может быть\n '
                             f'в слишком длинном пути к обрабатываемым файлам')
    else:
        messagebox.showinfo('Подготовка к импорту 1.0',
                            'Создание документов завершено!')


if __name__ == '__main__':
    window = Tk()
    window.title('Подготовка к импорту 1.0')
    window.geometry('450x560')
    window.resizable(False, False)

    tab_control = ttk.Notebook(window)
    """
    Создание программ профпроб
    """

    tab_create_program_prob = ttk.Frame(tab_control)
    tab_control.add(tab_create_program_prob, text='Очистка')
    tab_control.pack(expand=1, fill='both')
    # Создаем кнопку Выбрать файл с данными
    btn_data_template = Button(tab_create_program_prob, text='1) Выберите шаблон', font=('Arial Bold', 15),
                          command=select_file_template
                          )
    btn_data_template.grid(column=0, row=4, padx=10, pady=10)

    # Создаем кнопку Выбрать файл с данными
    btn_data_doc = Button(tab_create_program_prob, text='2) Выберите файл с данными', font=('Arial Bold', 15),
                          command=select_file_mun
                          )
    btn_data_doc.grid(column=0, row=5, padx=10, pady=10)
    #
    # Создаем кнопку для выбора папки куда будут генерироваться файлы

    btn_choose_folder = Button(tab_create_program_prob, text='3) Выберите папку с данными', font=('Arial Bold', 15),
                                       command=select_folder
                                       )
    btn_choose_folder.grid(column=0, row=6, padx=10, pady=10)

    btn_choose_folder_end = Button(tab_create_program_prob, text='4) Выберите конечную папку', font=('Arial Bold', 15),
                                       command=select_end_folder
                                       )
    btn_choose_folder_end.grid(column=0, row=7, padx=10, pady=10)

    # Создаем кнопку для создания документов из таблиц с произвольной структурой
    btn_processing = Button(tab_create_program_prob, text='5) Очистить',
                                    font=('Arial Bold', 15),
                                    command=processing_data
                                    )
    btn_processing.grid(column=0, row=8, padx=10, pady=10)

    window.mainloop()
