"""
Скрипт для обработки результатов теста Шкала нарушенных потребностей остракизм Бойкина
"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_union_svod,create_list_on_level

class BadOrderSHNPO(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSHNPO(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSHNPO(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass






def calc_sub_value_pr(row):
    """
    Функция для подсчета значения субшкалы Принадлежности
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1, 4, 6, 7, 13]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [1, 6, 13]  # список ответов которые нужно считать простым сложением
    lst_reverse = [4, 7] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_pr_pod(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 1.4:
        return 'низкий уровень социального остракизма'
    elif 1.5 <= value <= 2.4:
        return 'средний уровень социального остракизма'
    elif 2.5 <= value <= 5:
        return 'высокий уровень социального остракизма'

def calc_level_sub_pr_mol(value):
    """
    Функция для подсчета уровня субшкалы
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 3:
        return 'средний уровень социального остракизма'
    elif 3.1 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_sam(row):
    """
    Функция для подсчета значения субшкалы Самоуважение
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [5, 9, 11, 12, 15]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [5]  # список ответов которые нужно считать простым сложением
    lst_reverse = [9, 11, 12, 15] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_sam_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 2.8:
        return 'средний уровень социального остракизма'
    elif 2.9 <= value <= 5:
        return 'высокий уровень социального остракизма'

def calc_level_sub_sam_mol(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.8:
        return 'низкий уровень социального остракизма'
    elif 1.9 <= value <= 3.2:
        return 'средний уровень социального остракизма'
    elif 3.3 <= value <= 5:
        return 'высокий уровень социального остракизма'



def calc_sub_value_con(row):
    """
    Функция для подсчета значения субшкалы Контроль
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [3, 8, 10, 14, 20]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [3,8,14,20]  # список ответов которые нужно считать простым сложением
    lst_reverse = [10] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_con_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.2:
        return 'низкий уровень социального остракизма'
    elif 1.3 <= value <= 2.4:
        return 'средний уровень социального остракизма'
    elif 2.5 <= value <= 5:
        return 'высокий уровень социального остракизма'


def calc_level_sub_con_mol(value):
    """
    Функция для подсчета уровня субшкалы контроля
    :param value:
    :return:
    """
    if 1 <= value <= 1.6:
        return 'низкий уровень социального остракизма'
    elif 1.7 <= value <= 2.8:
        return 'средний уровень социального остракизма'
    elif 2.9 <= value <= 5:
        return 'высокий уровень социального остракизма'


def calc_sub_value_os(row):
    """
    Функция для подсчета значения субшкалы Осмысленное существование
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [2, 16, 17, 18, 19]

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_forward = [16,19]  # список ответов которые нужно считать простым сложением
    lst_reverse = [2, 17, 18] # обратный подсчет

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            if idx + 1 in lst_forward:
                # print(f'Прямой подсчет {idx +1}') # Для проверки корректности
                value_forward += value
            elif idx +1 in lst_reverse:
                # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
                if value == 5:
                    value_reverse += 1
                elif value == 4:
                    value_reverse += 2
                elif value == 3:
                    value_reverse += 3
                elif value == 2:
                    value_reverse += 4
                elif value == 1:
                    value_reverse += 5

    return round((value_forward + value_reverse) /5,1)

def calc_level_sub_os_pod(value):
    """
    Функция для подсчета уровня субшкалы самоуважения
    :param value:
    :return:
    """
    if 1 <= value <= 1.4:
        return 'низкий уровень социального остракизма'
    elif 1.5 <= value <= 2.6:
        return 'средний уровень социального остракизма'
    elif 2.7 <= value <= 5:
        return 'высокий уровень социального остракизма'

def calc_level_sub_os_mol(value):
    """
    Функция для подсчета уровня субшкалы осмысленного существования
    :param value:
    :return:
    """
    if 1 <= value <= 1.8:
        return 'низкий уровень социального остракизма'
    elif 1.9 <= value <= 3.2:
        return 'средний уровень социального остракизма'
    elif 3.3 <= value <= 5:
        return 'высокий уровень социального остракизма'










def processing_boykina_shnpo(result_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 20:  # проверяем количество колонок с вопросами
        raise BadCountColumnsSHNPO

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols = ['Я чувствую себя единым целым с другими людьми',
                      'Полагаю, что не вношу значимый вклад во что-либо',
                      'У меня есть уверенность, что я влияю на ход событий в моей жизни',
                      'Среди своего окружения я ощущаю себя лишним',
                      'Люди прислушиваются к моему мнению',
                      'В любой ситуации я чувствую поддержку хоть одного человека',
                      'Я ощущаю себя изгоем',
                      'Я совершенно точно управляю всем в своей жизни',
                      'Мне кажется, большинство из моего окружения невысокого обо мне мнения',
                      'Порой, кажется, что всё зависит от чьей-то чужой воли',
                      'Общаясь с людьми, я чувствую себя неуверенно',
                      'Такое ощущение, что общение с людьми – не моя сильная сторона',
                      'Думаю, что общество, в котором я живу, принимает меня',
                      'Я контролирую свою жизнь',
                      'Я переживаю, что люди плохо думают обо мне',
                      'Мне кажется, что моё участие в жизни окружающих очень важно',
                      'Порой я ощущаю себя невидимкой',
                      'Временами мне кажется, что от меня людям нет никакого толка',
                      'Думаю, мое участие в чем-либо всегда полезно',
                      'Такое ощущение, что у меня впереди еще много разных возможностей'
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
        raise BadOrderSHNPO

    # словарь для замены слов на числа
    dct_replace_value = {'не согласен': 5,
                         'редко': 4,
                         'иногда': 3,
                         'часто': 2,
                         'полностью согласен': 1}

    valid_values = [1, 2, 3, 4, 5]
    answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(20):
        mask = ~answers_df.iloc[:, i].isin(valid_values)  # проверяем на допустимые значения
        result_check = answers_df.iloc[:, i][mask]
        if len(result_check) != 0:
            error_row = list(map(lambda x: x + 2, result_check.index))
            error_row = list(map(str, error_row))
            error_row_lst = [f'В {i + 1} вопросной колонке на строке {value}' for value in error_row]
            error_in_column = ','.join(error_row_lst)
            lst_error_answers.append(error_in_column)

    if len(lst_error_answers) != 0:
        error_message = ';'.join(lst_error_answers)
        raise BadValueSHNPO

    base_df = pd.DataFrame()

    # Субшкала Принаддежность
    base_df['Значение_субшкалы_Принадлежность'] = answers_df.apply(calc_sub_value_pr, axis=1)
    base_df['Норма_Принадлежность_Подростки'] = '1,5-2,4 баллов'
    base_df['Уровень_субшкалы_Принадлежность_Подростки'] = base_df['Значение_субшкалы_Принадлежность'].apply(
        calc_level_sub_pr_pod)

    base_df['Норма_Принадлежность_Молодежь'] = '1,7-3 балла'
    base_df['Уровень_субшкалы_Принадлежность_Молодежь'] = base_df['Значение_субшкалы_Принадлежность'].apply(
        calc_level_sub_pr_mol)

    # Субшкала Самоуважение
    base_df['Значение_субшкалы_Самоуважение'] = answers_df.apply(calc_sub_value_sam, axis=1)
    base_df['Норма_Самоуважение_Подростки'] = '1,7-2,8 баллов'
    base_df['Уровень_субшкалы_Самоуважение_Подростки'] = base_df['Значение_субшкалы_Самоуважение'].apply(
        calc_level_sub_sam_pod)

    base_df['Норма_Самоуважение_Молодежь'] = '1,9-3,2 балла'
    base_df['Уровень_субшкалы_Самоуважение_Молодежь'] = base_df['Значение_субшкалы_Самоуважение'].apply(
        calc_level_sub_sam_mol)

    # Субшкала Контроль
    base_df['Значение_субшкалы_Контроль'] = answers_df.apply(calc_sub_value_con, axis=1)
    base_df['Норма_Контроль_Подростки'] = '1,3-2,4 баллов'
    base_df['Уровень_субшкалы_Контроль_Подростки'] = base_df['Значение_субшкалы_Контроль'].apply(
        calc_level_sub_con_pod)

    base_df['Норма_Контроль_Молодежь'] = '1,7-2,8 баллов'
    base_df['Уровень_субшкалы_Контроль_Молодежь'] = base_df['Значение_субшкалы_Контроль'].apply(
        calc_level_sub_con_mol)

    # Субшкала Осмысленное существование
    base_df['Значение_субшкалы_ОС'] = answers_df.apply(calc_sub_value_os, axis=1)
    base_df['Норма_ОС_Подростки'] = '1,5-2,6 баллов'
    base_df['Уровень_субшкалы_ОС_Подростки'] = base_df['Значение_субшкалы_ОС'].apply(
        calc_level_sub_os_pod)

    base_df['Норма_ОС_Молодежь'] = '1,9-3,2 балла'
    base_df['Уровень_субшкалы_ОС_Молодежь'] = base_df['Значение_субшкалы_ОС'].apply(
        calc_level_sub_os_mol)

    # Создаем датафрейм для создания части в общий датафрейм
    part_df = pd.DataFrame()

    part_df['ШНПО_П_Значение'] = base_df['Значение_субшкалы_Принадлежность']
    part_df['ШНПО_П_Под_Уровень'] = base_df['Уровень_субшкалы_Принадлежность_Подростки']
    part_df['ШНПО_П_Мол_Уровень'] = base_df['Уровень_субшкалы_Принадлежность_Молодежь']

    part_df['ШНПО_С_Значение'] = base_df['Значение_субшкалы_Самоуважение']
    part_df['ШНПО_С_Под_Уровень'] = base_df['Уровень_субшкалы_Самоуважение_Подростки']
    part_df['ШНПО_С_Мол_Уровень'] = base_df['Уровень_субшкалы_Самоуважение_Молодежь']

    part_df['ШНПО_К_Значение'] = base_df['Значение_субшкалы_Контроль']
    part_df['ШНПО_К_Под_Уровень'] = base_df['Уровень_субшкалы_Контроль_Подростки']
    part_df['ШНПО_К_Мол_Уровень'] = base_df['Уровень_субшкалы_Контроль_Молодежь']

    part_df['ШНПО_ОС_Значение'] = base_df['Значение_субшкалы_ОС']
    part_df['ШНПО_ОС_Под_Уровень'] = base_df['Уровень_субшкалы_ОС_Подростки']
    part_df['ШНПО_ОС_Мол_Уровень'] = base_df['Уровень_субшкалы_ОС_Молодежь']


    out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

    # Соединяем анкетную часть с результатной
    base_df = pd.concat([result_df, base_df], axis=1)
    base_df.sort_values(by='Значение_субшкалы_Принадлежность', ascending=False, inplace=True)  # сортируем

    # формируем основной словарь
    out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
               }


    # Создаем колонки для подсчета сводов
    base_df['Значение_субшкалы_Принадлежность_Подростки'] = base_df['Значение_субшкалы_Принадлежность']
    base_df['Значение_субшкалы_Принадлежность_Молодежь'] = base_df['Значение_субшкалы_Принадлежность']

    base_df['Значение_субшкалы_Самоуважение_Подростки'] = base_df['Значение_субшкалы_Самоуважение']
    base_df['Значение_субшкалы_Самоуважение_Молодежь'] = base_df['Значение_субшкалы_Самоуважение']

    base_df['Значение_субшкалы_Контроль_Подростки'] = base_df['Значение_субшкалы_Контроль']
    base_df['Значение_субшкалы_Контроль_Молодежь'] = base_df['Значение_субшкалы_Контроль']

    base_df['Значение_субшкалы_ОС_Подростки'] = base_df['Значение_субшкалы_ОС']
    base_df['Значение_субшкалы_ОС_Молодежь'] = base_df['Значение_субшкалы_ОС']


    # Делаем свод по интегральным показателям
    dct_svod_integral = {'Значение_субшкалы_Принадлежность_Подростки': 'Уровень_субшкалы_Принадлежность_Подростки',
                         'Значение_субшкалы_Принадлежность_Молодежь': 'Уровень_субшкалы_Принадлежность_Молодежь',

                         'Значение_субшкалы_Самоуважение_Подростки': 'Уровень_субшкалы_Самоуважение_Подростки',
                         'Значение_субшкалы_Самоуважение_Молодежь': 'Уровень_субшкалы_Самоуважение_Молодежь',

                         'Значение_субшкалы_Контроль_Подростки': 'Уровень_субшкалы_Контроль_Подростки',
                         'Значение_субшкалы_Контроль_Молодежь': 'Уровень_субшкалы_Контроль_Молодежь',

                         'Значение_субшкалы_ОС_Подростки': 'Уровень_субшкалы_ОС_Подростки',
                         'Значение_субшкалы_ОС_Молодежь': 'Уровень_субшкалы_ОС_Молодежь',
                         }

    dct_rename_svod_integral = {'Значение_субшкалы_Принадлежность_Подростки': 'П Под',
                                'Значение_субшкалы_Принадлежность_Молодежь': 'П Мол',

                                'Значение_субшкалы_Самоуважение_Подростки': 'С Под',
                                'Значение_субшкалы_Самоуважение_Молодежь': 'С Мол',

                                'Значение_субшкалы_Контроль_Подростки': 'К Под',
                                'Значение_субшкалы_Контроль_Молодежь': 'К Мол',

                                'Значение_субшкалы_ОС_Подростки': 'ОС Под',
                                'Значение_субшкалы_ОС_Молодежь': 'ОС Мол',
                                }

    lst_integral = ['низкий уровень социального остракизма', 'средний уровень социального остракизма', 'высокий уровень социального остракизма'
                   ]

    base_svod_integral_df = create_union_svod(base_df, dct_svod_integral, dct_rename_svod_integral, lst_integral)

    # считаем среднее
    avg_pr = round(base_df['Значение_общего_ЭИ'].mean(), 2)
    avg_mei = round(base_df['Значение_шкалы_МЭИ'].mean(), 2)
    avg_vei = round(base_df['Значение_шкалы_ВЭИ'].mean(), 2)
    avg_pa = round(base_df['Значение_шкалы_ПЭ'].mean(), 2)
    avg_ua = round(base_df['Значение_шкалы_УЭ'].mean(), 2)
    avg_mp = round(base_df['Значение_субшкалы_МП'].mean(), 2)
    avg_mu = round(base_df['Значение_субшкалы_МУ'].mean(), 2)
    avg_vp = round(base_df['Значение_субшкалы_ВП'].mean(), 2)
    avg_vu = round(base_df['Значение_субшкалы_ВУ'].mean(), 2)
    avg_va = round(base_df['Значение_субшкалы_ВЭ'].mean(), 2)

    avg_dct = {'Среднее значение Общий эмоциональный интеллект ': avg_ei,
               'Среднее значение шкалы Межличностный эмоциональный интеллект': avg_mei,
               'Среднее значение шкалы Внутриличностный эмоциональный интеллект': avg_vei,
               'Среднее значение шкалы Понимание эмоций': avg_pa,
               'Среднее значение шкалы Управление эмоциями': avg_ua,
               'Среднее значение субшкалы Понимание чужих эмоций': avg_mp,
               'Среднее значение субшкалы Управление чужими эмоциями': avg_mu,
               'Среднее значение субшкалы Понимание своих эмоций': avg_vp,
               'Среднее значение субшкалы Управление своими эмоциями': avg_vu,
               'Среднее значение субшкалы Контроль экспрессии': avg_va,

               }

    avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
    avg_df = avg_df.reset_index()
    avg_df.columns = ['Показатель', 'Среднее значение']

    out_dct.update({'Свод Субшкалы': base_svod_integral_df,
                    'Среднее': avg_df}
                   )








    # base_df.drop(columns=['Значение_субшкалы_Принадлежность_Подростки','Значение_субшкалы_Принадлежность_Молодежь',
    #                       'Значение_субшкалы_Самоуважение_Подростки','Значение_субшкалы_Самоуважение_Молодежь',
    #                       'Значение_субшкалы_Контроль_Подростки','Значение_субшкалы_Контроль_Молодежь',
    #                       'Значение_субшкалы_ОС_Подростки','Значение_субшкалы_ОС_Молодежь',
    #                       ],inplace=True)




















