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
import os

from docxtpl import DocxTemplate
from docxcompose.composer import Composer
from docx import Document
from docx2pdf import convert

df = pd.read_excel('data/probs.xlsx',dtype=str)
name_file_template_doc = 'data/Шаблон профессиональной пробы.docx'
path_to_end_folder_doc = 'data'
mode_pdf = 'Yes'


lst_name_columns = ['ID','Время_создания','Профессиональная_проба','Наименование_профессионального_направления','Автор_программы','Контакты_автора',
                    'Уровень_сложности','Формат_проведения','Время_проведения','Возрастная_категория','Допустимые_нозологии',
                    'Спец_условия','Возможность_проведения','Краткое_описание','Перспективы','Навыки_знания','Интересные_факты',
                    'Связь_пробы','Постановка_цели','Демонстрация','Инструкция','Рекомендации_организация','Критерии','Рекомендации_контроль',
                    'Рефлексия','Инфраструктурный_лист','Доп_источники','Доп_файлы']

df.columns = lst_name_columns

 # Заполняем Nan
df.fillna(' ', inplace=True)

df = df.applymap(lambda x:x.replace("\u00A0", " ")) # удаляем символ неразрывного пробела
df = df.applymap(lambda x:x.replace("_x000D_", "")) # удаляем

 # Конвертируем датафрейм в список словарей
data = df.to_dict('records')
error_df = pd.DataFrame(columns=['Автор','Наименование','Ошибка'])

for idx,row in enumerate(data):
    name_author = row['Автор_программы'].split(',')[0]
    name_prob = row['Наименование_профессионального_направления']
    inf_lst = row['Инфраструктурный_лист'].split('*')

    inf_lst = list(map(str.strip, inf_lst)) # очищаем от пробельных символов
    inf_lst = [value for value in inf_lst if value] # очищаем от пустого пробела в конце списка
    for value in inf_lst:
        tmp_lst = value.split(';')
        tmp_lst =[val for val in tmp_lst if val]
        if len(tmp_lst) != 4:
            error_df.loc[len(error_df.index)] = [name_author,name_prob,'Ошибка в инфраструктурном листе. Не хватает значений. Проверьте вручную.']
    split_data = [item.split(';') for item in inf_lst] # создаем список списков
    # создаем датафрейм для хранения инфраструктурника
    inf_df = pd.DataFrame(split_data, columns=['Наименование', 'Характеристика', 'Количество', 'Распределение'])
    # Обрабатываем дополнительные ссылки
    url_lst = row['Доп_источники'].split(';')
    url_lst = list(map(str.strip, url_lst)) # очищаем от пробельных символов
    url_lst = list(map(lambda x:x.replace('•\t',''), url_lst)) # очищаем от пробельных символов

    url_lst = [value for value in url_lst if value] # очищаем от пустого пробела в конце списка


    doc = DocxTemplate(name_file_template_doc)
    context = row
    context['inf_lst'] = inf_df.to_dict('records')
    context['url_lst'] = url_lst

    doc.render(context)
    name_file = f'{name_prob} {name_author}'
    name_file = re.sub(r'[<> :"?*|\\/]', ' ', name_file)
    # проверяем файл на наличие, если файл с таким названием уже существует то добавляем окончание
    if os.path.exists(f'{path_to_end_folder_doc}/{name_file}.docx'):
        doc.save(f'{path_to_end_folder_doc}/{name_file}_{idx}.docx')
    doc.save(f'{path_to_end_folder_doc}/{name_file}.docx')
    # создаем pdf
    if mode_pdf == 'Yes':
        convert(f'{path_to_end_folder_doc}/{name_file}.docx', f'{path_to_end_folder_doc}/{name_file}.pdf',
                keep_active=True)

error_df.to_excel(f'{path_to_end_folder_doc}/Файлы в которых есть ошибки.xlsx',index=False)