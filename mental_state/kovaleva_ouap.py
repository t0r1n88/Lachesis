"""
Скрипт для обработки результатов Опросник для учителя по адаптации первоклассников Ковалева Тарасенко
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderKTOUAP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueKTOUAP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsKTOUAP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 46
    """
    pass

def calc_value_kda(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [1,2,5,6,7,8,9,12,13,14,17,18,19,
               22,23,27,31,32,33,36,41,42]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        else:
            if value =='да':
                value_forward += 2

    return value_forward





def calc_level_scale(value,count):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    result = round((value / count) * 100)

    return f'{result}%'


def calc_level_procent(value:str):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    try:
        value = int(value.replace('%',''))
        if 0 <= value <= 25:
            return '0-25%'
        elif 26<= value <= 50:
            return '26-50%'
        elif 51 <= value <= 75:
            return '51-75%'
        else:
            return '76-100%'

    except:
        return 'ошибочное значение'


def calc_level(value:str):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    try:
        value = int(value.replace('%',''))
        if 0 <= value <= 14:
            return 'низкий уровень'
        elif 15<= value <= 30:
            return 'средний уровень'
        elif 31 <= value <= 40:
            return 'выше среднего'
        else:
            return 'высокий уровень'

    except:
        return 'ошибочное значение'



def calc_value_ro(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [1]
    lst_double = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward


def calc_value_ngsh(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [2]
    lst_double = [3,4]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_l(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [5,6]
    lst_double = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_ns(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [7,8,9]
    lst_double = [10,11]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward


def calc_value_i(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [12,13,14]
    lst_double = [15,16]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_gs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [17,18,19]
    lst_double = [20,21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_ins(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [22,23]
    lst_double = [24,25,26]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward


def calc_value_np(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [27]
    lst_double = [28,29,30]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward


def calc_value_nm(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [31,32,33]
    lst_double = [34,35]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_as(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [36]
    lst_double = [37,38,39,40]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward

def calc_value_nid(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_one = [41,42]
    lst_double = [43,44,45,46]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_one:
            if value == 'да':
                value_forward += 1
        elif idx in lst_double:
            if value =='да':
                value_forward += 2

    return value_forward





def processing_ouap_kov_tar(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 46:  # проверяем количество колонок с вопросами
        raise BadCountColumnsKTOUAP

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols = ['Родители совершенно устранились от воспитания, почти не бывают в школе',
                      'При поступлении в школу ребёнок не владел элементарными учебными навыками (не умел считать, не знал буквы и т. п.)',
                      'Не знает многое из того, что известно большинству детей его возраста (например, дни недели, времена года, сказки и т. п.)',
                      'Плохо развиты мелкие мышцы рук (трудности с письмом, неравномерные буквы, тремор и т. п.)',
                      'Пишет правой рукой, но со слов родителей является переученным левшой',
                      'Пишет левой рукой',
                      'Бесцельно двигает руками',
                      'Часто моргает',
                      'Сосёт палец или ручку',
                      'Иногда заикается',

                      'Грызёт ногти',
                      'У ребёнка хрупкое телосложение, маленький рост',
                      'Ребёнок явно «домашний», нуждается в доброжелательной атмосфере, любит, когда его гладят, обнимают',
                      'Очень любит играть, играет даже на уроках',
                      'Такое впечатление, что он младше других детей, хотя по возрасту им ровесник',
                      'Речь инфантильная, напоминает речь 4-5-летнего ребёнка',
                      'Чрезмерно беспокоен на уроках',
                      'Быстро примиряется с неудачами',
                      'Любит шумные, подвижные игры на переменах',
                      'Не может долго сосредоточиться на одном задании, всегда старается сделать побыстрее, не заботясь о качестве',

                      'После интересной игры, физкультурной паузы его невозможно настроить на серьёзную работу',
                      'Долго переживает неудачи',
                      'При неожиданном вопросе учителя часто теряется. Если дать время на обдумывание, может ответить хорошо',
                      'Очень долго выполняет любое задание',
                      'Домашние задания выполняет гораздо лучше классных (разница очень существенная, больше, чем у других детей)',
                      'Очень долго перестраивается с одной деятельности на другую',
                      'Часто не может повторить за учителем самый простой материал, при этом демонстрирует отличную память, когда речь идёт об интересующих его вещах (например, знает марки машин, но не может повторить самое простое правило)',
                      'Требует к себе постоянного внимания со стороны учителя. Почти всё делает только после персонального обращения: «Пиши!» и т. п.',
                      'Допускает много ошибок при списывании',
                      'Чтобы отвлечь его от задания, достаточно малейшей причины: скрипнула дверь, что-то упало и т. д.',

                      'Приносит в школу игрушки и играет на уроках',
                      'Никогда ничего не сделает сверх положенного минимума: не стремится узнать что-то, рассказать',
                      'Родители жалуются, что с трудом усаживают его за уроки',
                      'Такое впечатление, что на уроках ему плохо, оживает только на переменах',
                      'Не любит никаких усилий, если что-то не получается, бросает, ищет каких-то оправданий: рука болит и т. п.',
                      'Не совсем здоровый вид (бледный, худенький)',
                      'К концу урока работает хуже, часто отвлекается, сидит с отсутствующим видом',
                      'Если что-то не получается, раздражается, плачет',
                      'Плохо работает в условиях ограниченного времени. Если его торопить, может совсем «отключиться», бросить работу',
                      'Часто жалуется на усталость, головную боль',

                      'Почти никогда не отвечает правильно, если вопрос поставлен нестандартно, требует сообразительности',
                      'Ответы становятся лучше, если есть опора на какие-то внешние объекты (считает пальцы и т. п.)',
                      'После объяснения учителя не может выполнить аналогичное задание',
                      'Затрудняется применять ранее усвоенные понятия, навыки при объяснении учителем нового материала',
                      'Часто отвечает не по существу, не может выделить главное',
                      'Такое впечатление, что ему трудно понять объяснение, так как основные навыки, понятия у него не сформированы'
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
        raise BadOrderKTOUAP

    valid_values = ['да','нет']
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(46):
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
        raise BadValueKTOUAP

    base_df['КДА_Значение'] = answers_df.apply(calc_value_kda, axis=1)
    base_df['КДА_Процент'] = base_df['КДА_Значение'].apply(lambda x: calc_level_scale(x, 70))
    base_df['КДА_Уровень'] = base_df['КДА_Процент'].apply(calc_level)

    base_df['РО_Значение'] = answers_df.apply(calc_value_ro, axis=1)
    base_df['РО_Процент'] = base_df['РО_Значение'].apply(lambda x: calc_level_scale(x, 1))
    base_df['РО_Диапазон'] = base_df['РО_Процент'].apply(calc_level_procent)

    base_df['НГШ_Значение'] = answers_df.apply(calc_value_ngsh, axis=1)
    base_df['НГШ_Процент'] = base_df['НГШ_Значение'].apply(lambda x: calc_level_scale(x, 5))
    base_df['НГШ_Диапазон'] = base_df['НГШ_Процент'].apply(calc_level_procent)

    base_df['Л_Значение'] = answers_df.apply(calc_value_l, axis=1)
    base_df['Л_Процент'] = base_df['Л_Значение'].apply(lambda x: calc_level_scale(x, 2))
    base_df['Л_Диапазон'] = base_df['Л_Процент'].apply(calc_level_procent)

    base_df['НС_Значение'] = answers_df.apply(calc_value_ns, axis=1)
    base_df['НС_Процент'] = base_df['НС_Значение'].apply(lambda x: calc_level_scale(x, 7))
    base_df['НС_Диапазон'] = base_df['НС_Процент'].apply(calc_level_procent)

    base_df['И_Значение'] = answers_df.apply(calc_value_i, axis=1)
    base_df['И_Процент'] = base_df['И_Значение'].apply(lambda x: calc_level_scale(x, 7))
    base_df['И_Диапазон'] = base_df['И_Процент'].apply(calc_level_procent)

    base_df['ГС_Значение'] = answers_df.apply(calc_value_gs, axis=1)
    base_df['ГС_Процент'] = base_df['ГС_Значение'].apply(lambda x: calc_level_scale(x, 7))
    base_df['ГС_Диапазон'] = base_df['ГС_Процент'].apply(calc_level_procent)

    base_df['ИНС_Значение'] = answers_df.apply(calc_value_ins, axis=1)
    base_df['ИНС_Процент'] = base_df['ИНС_Значение'].apply(lambda x: calc_level_scale(x, 8))
    base_df['ИНС_Диапазон'] = base_df['ИНС_Процент'].apply(calc_level_procent)

    base_df['НП_Значение'] = answers_df.apply(calc_value_np, axis=1)
    base_df['НП_Процент'] = base_df['НП_Значение'].apply(lambda x: calc_level_scale(x, 7))
    base_df['НП_Диапазон'] = base_df['НП_Процент'].apply(calc_level_procent)

    base_df['НМ_Значение'] = answers_df.apply(calc_value_nm, axis=1)
    base_df['НМ_Процент'] = base_df['НМ_Значение'].apply(lambda x: calc_level_scale(x, 7))
    base_df['НМ_Диапазон'] = base_df['НМ_Процент'].apply(calc_level_procent)

    base_df['АС_Значение'] = answers_df.apply(calc_value_as, axis=1)
    base_df['АС_Процент'] = base_df['АС_Значение'].apply(lambda x: calc_level_scale(x, 9))
    base_df['АС_Диапазон'] = base_df['АС_Процент'].apply(calc_level_procent)

    base_df['НИД_Значение'] = answers_df.apply(calc_value_nid, axis=1)
    base_df['НИД_Процент'] = base_df['НИД_Значение'].apply(lambda x: calc_level_scale(x, 10))
    base_df['НИД_Диапазон'] = base_df['НИД_Процент'].apply(calc_level_procent)



    base_df.to_excel('data/res.xlsx',index=False)






