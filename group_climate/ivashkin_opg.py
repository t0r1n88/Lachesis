"""
Скрипт для обработки результатов Определение привлекательности для школьника группы одноклассников Ивашкин
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod,create_list_on_level

class BadOrderOPSGOI(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOPSGOI(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOPSGOI(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 5
    """
    pass

def calc_value(row):
    """
    Функция для подсчета значения шкалы Самочувствие
    :param row: строка с ответами
    :return: число
    """
    value_pos = 0
    # 1
    if row[0] == 'Считаю себя активным, полноправным членом класса':
        value_pos += 5
    elif row[0] == 'Участвую в большинстве дел класса, но часть одноклассников делают это активнее меня':
        value_pos += 4
    elif row[0] == 'Участвую примерно в половине дел класса':
        value_pos += 3
    elif row[0] == 'Не чувствую привязанности к классу и в его делах участвую редко':
        value_pos += 2
    elif row[0] == 'Делами класса не интересуюсь и участвовать в них не желаю':
        value_pos += 1

    # 2
    if row[1] == 'Очень хотел бы':
        value_pos += 1
    elif row[1] == 'Скорее всего перешел бы, чем остался':
        value_pos += 2
    elif row[1] == 'Не вижу никакой разницы':
        value_pos += 3
    elif row[1] == 'Скорее всего остался бы в своем классе':
        value_pos += 4
    elif row[1] == 'Очень хотел бы остаться в своем классе':
        value_pos += 5
    # 3
    if row[2] == 'Лучше, чем в других классах':
        value_pos += 3
    elif row[2] == 'Такие же, как в других классах':
        value_pos += 2
    elif row[2] == 'Хуже, чем в других классах':
        value_pos += 1

    # 4
    if row[3] == 'Лучше, чем в других классах':
        value_pos += 3
    elif row[3] == 'Такие же, как в других классах':
        value_pos += 2
    elif row[3] == 'Хуже, чем в других классах':
        value_pos += 1

    # 5
    if row[4] == 'Лучше, чем в других классах':
        value_pos += 3
    elif row[4] == 'Такое же, как в других классах':
        value_pos += 2
    elif row[4] == 'Хуже, чем в других классах':
        value_pos += 1



    return value_pos


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if  5 <=value <= 8:
        return f'от 5 до 8'
    elif 9 <= value <= 12:
        return f'от 9 до 12'
    elif 13 <= value <= 16:
        return f'от 13 до 16'
    else:
        return f'от 17 до 18'


def calc_level_all(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 5 <= value < 8:
        return f'5-7.99'
    elif 8 <= value < 12:
        return f'8-11.99'
    elif 12 <= value < 16:
        return f'12-15.99'
    else:
        return f'16-18'





def processing_opsgo_ivashkin(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """

    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 5:  # проверяем количество колонок с вопросами
        raise BadCountColumnsOPSGOI

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst
    lst_check_cols = ['Как бы вы оценили свою принадлежность к группе?',
                      'Перешли бы вы в другую группу, если бы представилась такая возможность (без изменения прочих условий)?',
                      'Каковы взаимоотношения между членами вашей группы?',
                      'Каковы у вас взаимоотношения с руководством?',
                      'Каково отношение к делу (учебе и т. п.) в вашем коллективе?'
                      ]

    # Проверяем порядок колонок
    order_main_columns = lst_check_cols  # порядок колонок и названий как должно быть
    order_temp_df_columns = list(answers_df.columns)  # порядок колонок проверяемого файла
    error_order_lst = []  # список для несовпадающих пар
    # Сравниваем попарно колонки
    for main, temp in zip(order_main_columns, order_temp_df_columns):
        if main != temp:
            error_order_lst.append(f'На месте колонки {main} находится колонка {temp}')
            error_order_message = ';'.join(error_order_lst)
    if len(error_order_lst) != 0:
        raise BadOrderIGSSH

    valid_values = [['Чувствую себя ее членом, частью коллектива','Участвую в большинстве видов деятельности','Участвую в одних видах деятельности и не участвую в других',
                     'Не чувствую, что являюсь членом группы','Живу и существую отдельно от нее','Не знаю, затрудняюсь ответить'],
                    ['Да, очень хотел бы перейти','Скорее перешел бы, чем остался','Не вижу никакой разницы',
                     'Скорее всего остался бы в своей группе','Очень хотел бы остаться в своей группе','Не знаю, трудно сказать'],
                    ['Лучше, чем в большинстве коллективов','Примерно такие же, как и в большинстве коллективов','Хуже, чем в большинстве коллективов','Не знаю, трудно сказать'],
                    ['Лучше, чем в большинстве коллективов','Примерно такие же, как и в большинстве коллективов','Хуже, чем в большинстве коллективов','Не знаю'],
                    ['Лучше, чем в большинстве коллективов','Примерно такие же, как и в большинстве коллективов','Хуже, чем в большинстве коллективов','Не знаю']]

    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for idx, lst_values in enumerate(valid_values):
        mask = ~answers_df.iloc[:, idx].isin(lst_values)  # проверяем на допустимые значения
        # Получаем строки с отличающимися значениями
        result_check = answers_df.iloc[:, idx][mask]

        if len(result_check) != 0:
            error_row = list(map(lambda x: x + 2, result_check.index))
            error_row = list(map(str, error_row))
            error_row_lst = [f'В {idx + 1} вопросной колонке на строке {value}' for value in error_row]
            error_in_column = ','.join(error_row_lst)
            lst_error_answers.append(error_in_column)

    if len(lst_error_answers) != 0:
        error_message = ';'.join(lst_error_answers)
        raise BadValueIGSSH

    base_df['ИО_Значение'] = answers_df.apply(calc_value, axis=1)
    base_df['ИО_Диапазон'] = base_df['ИО_Значение'].apply(calc_level)

    if len(lst_svod_cols) == 0:
        base_df['ГО_Значение'] = round(base_df['ИО_Значение'].sum() / len(base_df), 1)
        base_df['ГО_Уровень'] = base_df['ГО_Значение'].apply(calc_level_all)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['МОУПККЛ_ИО_Значение'] = base_df['ИО_Значение']
        part_df['МОУПККЛ_ИО_Диапазон'] = base_df['ИО_Диапазон']
        part_df['МОУПККЛ_ГО_Значение'] = base_df['ГО_Значение']
        part_df['МОУПККЛ_ГО_Уровень'] = base_df['ГО_Уровень']





    base_df.to_excel('data/res.xlsx')





