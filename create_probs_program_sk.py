# -*- coding: UTF-8 -*-
import pandas as pd
import numpy as np
import openpyxl
from openpyxl import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import Font
from openpyxl.styles import Alignment
import time
import re

from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document
from docx2pdf import convert

df = pd.read_excel('data/probs.xlsx',dtype=str)
name_file_template_doc = 'data/Шаблон профессиональной пробы.docx'

lst_name_columns = ['ID','Время_создания','Профессиональная_проба','Наименование_профессионального_направления','Автор_программы','Контакты_автора',
                    'Уровень_сложности','Формат_проведения','Время_проведения','Возрастная_категория','Допустимые_нозологии',
                    'Спец_условия','Возможность_проведения','Краткое_описание','Перспективы','Навыки_знания','Интересные_факты',
                    'Связь_пробы','Постановка_цели','Демонстрация','Инструкция','Рекомендации_организация','Критерии','Рекомендации_контроль',
                    'Рефлексия','Инфраструктурный_лист','Доп_источники','Доп_файлы']

df.columns = lst_name_columns

 # Заполняем Nan
df.fillna(' ', inplace=True)

df = df.applymap(lambda x:x.replace("\u00A0", " ")) # удаляем символ неразрывного пробела

 # Конвертируем датафрейм в список словарей
data = df.to_dict('records')

for idx,row in enumerate(data):
    name_author = row['Автор_программы'].split(',')[0]
    name_prob = row['Наименование_профессионального_направления']
    inf_lst = row['Инфраструктурный_лист'].split('*')
    inf_lst = list(map(str.strip, inf_lst)) # очищаем от пробельных символов
    inf_lst = [value for value in inf_lst if value] # очищаем от пустого пробела в конце списка
    split_data = [item.split(';') for item in inf_lst] # создаем список списков
    # создаем датафрейм для хранения инфраструктурника
    inf_df = pd.DataFrame(split_data, columns=['Наименование', 'Характеристика', 'Количество', 'Распределение'])
    # Обрабатываем дополнительные ссылки
    url_lst = row['Доп_источники'].split(';')
    url_lst = list(map(str.strip, url_lst)) # очищаем от пробельных символов
    url_lst = list(map(lambda x:x.replace('•\t',''), url_lst)) # очищаем от пробельных символов

    url_lst = [value for value in url_lst if value] # очищаем от пустого пробела в конце списка
    print(url_lst)


    doc = DocxTemplate(name_file_template_doc)
    context = row
    context['inf_lst'] = inf_df.to_dict('records')
    context['url_lst'] = url_lst

    doc.render(context)
    doc.save(f'data/{name_prob} {name_author}.docx')