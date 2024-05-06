# -*- coding: UTF-8 -*-
"""
Скрипт для генерации документов по результатам тестирования
"""
import pandas as pd
import os
import re
from docxcompose.composer import Composer
from docx import Document
from docxtpl import DocxTemplate
from docx2pdf import convert

class NotNumberColumn(Exception):
    """
    Исключение для обработки варианта когда в таблице нет колонки с таким порядковым номером
    """
    pass

class NoMoreNumberColumn(Exception):
    """
    Исключение для обработки варианта когда в таблице нет колонки с таким порядковым номером
    """
    pass

def prepare_entry_str(raw_str:str,pattern:str,repl_str:str,sep_lst:str)->list:
    """
    Функция для очистки строки от лишних символов и уменьшения на единицу (для нумерации с нуля)
    :param raw_str: обрабатываемая строка
    :param pattern: паттерн для замены символов
    :param repl_str: строка на которую нужно заменять символы
    :param sep_lst: разделитель по которому будет делиться список
    :return: список
    """
    number_column_folder_structure = re.sub(pattern,repl_str,raw_str) # убираем из строки все лишние символы
    lst_number_column_folder_structure = number_column_folder_structure.split(sep_lst) # создаем список по запятой
    # отбрасываем возможные лишние элементы из за лишних запятых
    lst_number_column_folder_structure = [value for value in lst_number_column_folder_structure if value]
    # заменяем 0 на единицу
    lst_number_column_folder_structure = ['1' if x == '0' else x for x in lst_number_column_folder_structure]
    # Превращаем в числа и отнимаем 1 чтобы соответствовать индексам питона
    lst_number_column_folder_structure = list(map(lambda x:int(x)-1,lst_number_column_folder_structure))

    # очищаем от возможных дублей
    lst_number_column_folder_structure = list(set(lst_number_column_folder_structure))
    return lst_number_column_folder_structure





def generate_result_docs(name_file_data_doc:str,name_file_template_doc:str,path_to_end_folder_doc:str,
                         folder_structure:str,name_file:str,name_type_file:str,mode_pdf:str):
    """
    Функция для генерации документов по результатам тестирования с разбиением по папкам и определенным названиям
    :param name_file_data_doc: таблица с яндекс форм
    :param name_file_template_doc: файл шаблона
    :param path_to_end_folder_doc: куда сохранять результаты
    :param folder_structure:строка с порядковыми номерами колонок по которым будет создаваться структура папок - 3,4
    :param name_file: строка с порядковыми номерами колонок по которым будет создаваться имя файла - 5,6,7
    :param name_type_file: название создаваемых документов которое будет находится в начале имен создаваемых файлов - Справка, Результат
    :param mode_pdf: нужно ли создавать пдф версии создаваемых файлов
    :return:
    """

    # Считываем данные
    # Добавил параметр dtype =str чтобы данные не преобразовались а использовались так как в таблице
    df = pd.read_excel(name_file_data_doc, dtype=str)
    df.fillna('Не заполнено',inplace=True)
    # очищаем строку от лишних символов и превращаем в список номеров колонок
    lst_number_column_folder_structure = prepare_entry_str(folder_structure,r'[^\d,]','',',')

    # проверяем длину списка не более 3 и не равно 0
    if len(lst_number_column_folder_structure) == 0 or len(lst_number_column_folder_structure) > 3:
        raise NoMoreNumberColumn

    # проверяем чтобы номер колонки не превышал количество колонок в датафрейме
    for number_column in lst_number_column_folder_structure:
        if number_column > len(df):
            raise NotNumberColumn

    # обрабатываем колонки с именем с названием файла
    # очищаем строку от лишних символов и превращаем в список номеров колонок
    lst_number_column_name_file = prepare_entry_str(name_file,r'[^\d,]','',',')

    # проверяем длину списка не более 3 и не равно 0
    if len(lst_number_column_name_file) == 0 or len(lst_number_column_name_file) > 2:
        raise NoMoreNumberColumn

    # проверяем чтобы номер колонки не превышал количество колонок в датафрейме
    for number_column in lst_number_column_name_file:
        if number_column > len(df):
            raise NotNumberColumn

    print(lst_number_column_folder_structure)

    if len(lst_number_column_folder_structure) == 1:
        # Если нужно создавать одноуровневую структуру
        # получаем название колонки
        name_column = df.columns[lst_number_column_folder_structure[0]]
        lst_unique_value = df[name_column].unique() # получаем список уникальных значений
        for name_folder in lst_unique_value:
            temp_df = df[df[name_column] == name_folder] # фильтруем по названию
            # Конвертируем датафрейм в список словарей
            clean_name_folder = re.sub(r'[\r\b\n\t<>:"?*|\\/]', '_', name_folder)  # очищаем название от лишних символов
            finish_path = f'{path_to_end_folder_doc}/{clean_name_folder}'
            print(finish_path)
            if not os.path.exists(finish_path):
                os.makedirs(finish_path)
            data = temp_df.to_dict('records')

            # В зависимости от состояния чекбоксов обрабатываем файлы
            # Создаем в цикле документы
            if len(lst_number_column_name_file) == 1:
                # если указана только одна колонка
                name_column = temp_df.columns[lst_number_column_name_file[0]]
                for idx, row in enumerate(data):
                    doc = DocxTemplate(name_file_template_doc)
                    context = row
                    doc.render(context)
                    # Сохраняем файл
                    name_file = f'{name_type_file}_{row[name_column]}'
                    name_file = re.sub(r'[<> :"?*|\\/]', ' ', name_file)
                    threshold_name = 200 - (len(finish_path) + 10)
                    if threshold_name <= 0:  # если путь к папке слишком длинный вызываем исключение
                        raise OSError
                    name_file = name_file[:threshold_name]  # ограничиваем название файла
                    # проверяем файл на наличие, если файл с таким названием уже существует то добавляем окончание
                    if os.path.exists(f'{finish_path}/{name_file}.docx'):
                        doc.save(f'{finish_path}/{name_file}_{idx}.docx')
                        if mode_pdf == 'Yes':
                            convert(f'{finish_path}/{name_file}_{idx}.docx', f'{finish_path}/{name_file}_{idx}.pdf',
                                    keep_active=True)
                    else:
                        doc.save(f'{finish_path}/{name_file}.docx')
                        if mode_pdf == 'Yes':
                            convert(f'{finish_path}/{name_file}.docx', f'{finish_path}/{name_file}.pdf',
                                    keep_active=True)

            elif len(lst_number_column_name_file) == 2:
                name_main_column = temp_df.columns[lst_number_column_name_file[0]] # первая колонка
                name_second_column = temp_df.columns[lst_number_column_name_file[1]] # вторая колонка
                for idx, row in enumerate(data):
                    doc = DocxTemplate(name_file_template_doc)
                    context = row
                    doc.render(context)
                    # Сохраняем файл
                    name_file = f'{name_type_file}_{row[name_main_column]}_{row[name_second_column]}'
                    name_file = re.sub(r'[<> :"?*|\\/]', ' ', name_file)
                    threshold_name = 200 - (len(finish_path) + 10)
                    if threshold_name <= 0:  # если путь к папке слишком длинный вызываем исключение
                        raise OSError
                    name_file = name_file[:threshold_name]  # ограничиваем название файла
                    # проверяем файл на наличие, если файл с таким названием уже существует то добавляем окончание
                    if os.path.exists(f'{finish_path}/{name_file}.docx'):
                        doc.save(f'{finish_path}/{name_file}_{idx}.docx')
                        if mode_pdf == 'Yes':
                            convert(f'{finish_path}/{name_file}_{idx}.docx', f'{finish_path}/{name_file}_{idx}.pdf',
                                    keep_active=True)
                    else:
                        doc.save(f'{finish_path}/{name_file}.docx')
                        if mode_pdf == 'Yes':
                            convert(f'{finish_path}/{name_file}.docx', f'{finish_path}/{name_file}.pdf',
                                    keep_active=True)








    #
    # # Конвертируем датафрейм в список словарей
    # data = df.to_dict('records')
    #
    # # В зависимости от состояния чекбоксов обрабатываем файлы
    # # Создаем в цикле документы
    # for idx, row in enumerate(data):
    #     doc = DocxTemplate(name_file_template_doc)
    #     context = row
    #     # print(context)
    #     doc.render(context)
    #     # Сохраняенм файл0
    #     name_file = f'{name_type_file} {row[name_column]}'
    #     name_file = re.sub(r'[<> :"?*|\\/]', ' ', name_file)
    #     # проверяем файл на наличие, если файл с таким названием уже существует то добавляем окончание
    #     if os.path.exists(f'{path_to_end_folder_doc}/{name_file}.docx'):
    #         doc.save(f'{path_to_end_folder_doc}/{name_file}_{idx}.docx')
    #     doc.save(f'{path_to_end_folder_doc}/{name_file}.docx')
    #     # создаем pdf
    #     if mode_pdf == 'Yes':
    #         convert(f'{path_to_end_folder_doc}/{name_file}.docx', f'{path_to_end_folder_doc}/{name_file}.pdf',
    #                 keep_active=True)
    #
    #
    # # Список с созданными файлами
    # files_lst = []
    # # Создаем временную папку
    # with tempfile.TemporaryDirectory() as tmpdirname:
    #     print('created temporary directory', tmpdirname)
    #     # Создаем и сохраняем во временную папку созданные документы Word
    #     for row in data:
    #         doc = DocxTemplate(name_file_template_doc)
    #         context = row
    #         doc.render(context)
    #         # Сохраняем файл
    #         # очищаем от запрещенных символов
    #         name_file = f'{row[name_column]}'
    #         name_file = re.sub(r'[<> :"?*|\\/]', ' ', name_file)
    #
    #         doc.save(f'{tmpdirname}/{name_file}.docx')
    #         # Добавляем путь\ к файлу в список
    #         files_lst.append(f'{tmpdirname}/{name_file}.docx')
    #     # Получаем базовый файл
    #     main_doc = files_lst.pop(0)
    #     # Запускаем функцию
    #     combine_all_docx(main_doc, files_lst)

if __name__ == '__main__':
    main_name_file_data_doc = 'c:/Users/1/PycharmProjects/Lachesis/data/Таблица с обезличенными результатами.xlsx'
    main_name_file_template_doc = 'c:/Users/1/PycharmProjects/Lachesis/data/Шаблон Отчет о результатах комплексного профориентационного тестирования.docx'
    main_path_to_end_folder_doc = 'c:/Users/1/PycharmProjects/Lachesis/data/Результат'
    main_folder_structure = '3,4dfg, '
    main_folder_structure = '3'
    main_name_file = '5,6'
    main_name_type_file = 'Результат тестирования'
    main_mode_pdf = 'Yes'

    generate_result_docs(main_name_file_data_doc,main_name_file_template_doc,main_path_to_end_folder_doc,
                         main_folder_structure,main_name_file,main_name_type_file,main_mode_pdf)

    print('Lindy Booth')
