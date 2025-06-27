"""
Скрипт для обработки результатов теста Опросник психологического выгорания Рукавишников А.А
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,create_svod_sub




class BadOrderRPB(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueRPB(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsRPB(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 72
    """
    pass


def calc_sub_value_psych_attrition(row):
    """
    Функция для подсчета значения субшкалы Психоэмоциональное истощение
    :param row: строка с ответами
    :return: число
    """
    value_forward = 0
    lst_pr = [1,5,7,14,16,17,20,25,29,31,32,34,36,39,42,45,47,49,52,54,57,60,63,67,69]
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level_sub_psych_attrition(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 9:
        return 'очень низкий уровень'
    elif 10 <= value <= 20:
        return 'низкий уровень'
    elif 21 <= value <= 39:
        return 'средний уровень'
    elif 40 <= value <= 49:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'

def calc_sub_value_lo(row):
    """
    Функция для подсчета значения субшкалы Личностное отдаление
    :param row: строка с ответами
    :return: число
    """
    value_forward = 0
    lst_pr = [3,4,9,10,11,13,18,21,30,33,35,38,40,43,46,48,51,56,59,61,66,70,71,72]
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level_sub_lo(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 9:
        return 'очень низкий уровень'
    elif 10 <= value <= 16:
        return 'низкий уровень'
    elif 17 <= value <= 31:
        return 'средний уровень'
    elif 32 <= value <= 40:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'


def calc_sub_value_pm(row):
    """
    Функция для подсчета значения субшкалы Личностное отдаление
    :param row: строка с ответами
    :return: число
    """
    value_forward = 0
    lst_pr = [2,6,8,12,15,19,22,23,24,26,27,28,37,41,44,50,53,55,58,62,64,65,68]
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level_sub_pm(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 7:
        return 'очень низкий уровень'
    elif 8 <= value <= 12:
        return 'низкий уровень'
    elif 13 <= value <= 24:
        return 'средний уровень'
    elif 25 <= value <= 31:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'


def calc_level_index_psych_burnout(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 31:
        return 'очень низкий уровень'
    elif 32 <= value <= 51:
        return 'низкий уровень'
    elif 52 <= value <= 92:
        return 'средний уровень'
    elif 93 <= value <= 112:
        return 'высокий уровень'
    else:
        return 'очень высокий уровень'


def calc_count_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формироваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols: список с колонками
    :return:датафрейм
    """
    count_df = pd.pivot_table(df, index=lst_cat,
                                             columns=col_cat,
                                             values=val_cat,
                                             aggfunc='count', margins=True, margins_name='Итого')


    count_df.reset_index(inplace=True)
    count_df = count_df.reindex(columns=lst_cols)
    count_df['% очень низкий уровень от общего'] = round(
        count_df['очень низкий уровень'] / count_df['Итого'], 2) * 100
    count_df['% низкий уровень от общего'] = round(
        count_df['низкий уровень'] / count_df['Итого'], 2) * 100
    count_df['% средний уровень от общего'] = round(
        count_df['средний уровень'] / count_df['Итого'], 2) * 100
    count_df['% высокий уровень от общего'] = round(
        count_df['высокий уровень'] / count_df['Итого'], 2) * 100
    count_df['% очень высокий уровень от общего'] = round(
        count_df['очень высокий уровень'] / count_df['Итого'], 2) * 100

    return count_df





def create_result_rpb(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['очень низкий уровень', 'низкий уровень',
           'средний уровень', 'высокий уровень', 'очень высокий уровень', 'Итого'])

    # основная шкала
    svod_count_one_level_df = calc_count_level(base_df, lst_svod_cols, 'Значение_индекса_Психического_выгорания',
                                                    'Уровень_индекса_Психического_выгорания',
                                                    lst_reindex_one_level_cols)

    # Субшкалы
    svod_count_one_level_pai_df = calc_count_level(base_df, lst_svod_cols,
                                                           'Значение_субшкалы_Психоэмоциональное_истощение',
                                                           'Уровень_субшкалы_Психоэмоциональное_истощение',
                                                           lst_reindex_one_level_cols)

    svod_count_one_level_lo_df = calc_count_level(base_df, lst_svod_cols,
                                                               'Значение_субшкалы_Личностное_отдаление',
                                                               'Уровень_субшкалы_Личностное_отдаление',
                                                               lst_reindex_one_level_cols)

    svod_count_one_level_pm_df = calc_count_level(base_df, lst_svod_cols,
                                                              'Значение_субшкалы_Профессиональная_мотивация',
                                                              'Уровень_субшкалы_Профессиональная_мотивация',
                                                              lst_reindex_one_level_cols)

    svod_mean_one_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Значение_индекса_Психического_выгорания',
                                          'Значение_субшкалы_Психоэмоциональное_истощение',
                                          'Значение_субшкалы_Личностное_отдаление',
                                          'Значение_субшкалы_Профессиональная_мотивация',
                                          ],
                                  aggfunc=round_mean)

    svod_mean_one_df.reset_index(inplace=True)
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(['Значение_индекса_Психического_выгорания', 'Значение_субшкалы_Психоэмоциональное_истощение',
                           'Значение_субшкалы_Личностное_отдаление','Значение_субшкалы_Профессиональная_мотивация'])
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)
    dct_rename_cols_mean = {'Значение_индекса_Психического_выгорания': 'Ср. психического выгорания',
                            'Значение_субшкалы_Психоэмоциональное_истощение': 'Ср. психоэмоционального истошения',
                            'Значение_субшкалы_Личностное_отдаление': 'Ср. личностного отдаления',
                            'Значение_субшкалы_Профессиональная_мотивация': 'Ср. профессиональной мотивации'}

    svod_mean_one_df.rename(columns=dct_rename_cols_mean, inplace=True)

    # очищаем название колонки по которой делали свод
    out_name_lst = []
    for name_col in lst_svod_cols:
        name = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_col)
        if len(lst_svod_cols) == 1:
            out_name_lst.append(name[:14])
        elif len(lst_svod_cols) == 2:
            out_name_lst.append(name[:7])
        else:
            out_name_lst.append(name[:4])

    out_name = ' '.join(out_name_lst)
    if len(out_name) > 14:
        out_name = out_name[:14]

    out_dct.update({f'Свод {out_name}': svod_count_one_level_df,
                    f'Ср. {out_name}': svod_mean_one_df,
                    f'Свод ПЭИ {out_name}': svod_count_one_level_pai_df,
                    f'Свод ЛО {out_name}': svod_count_one_level_lo_df,
                    f'Свод ПМ {out_name}': svod_count_one_level_pm_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_main_level_cols = [lst_svod_cols[idx], 'очень низкий уровень', 'низкий уровень',
           'средний уровень', 'высокий уровень', 'очень высокий уровень', 'Итого']  # Основная шкала

            # основная шкала
            svod_count_column_level_df = calc_count_level(base_df, [lst_svod_cols[idx]],
                                                          'Значение_индекса_Психического_выгорания',
                                                          'Уровень_индекса_Психического_выгорания',
                                                          lst_reindex_column_main_level_cols)

            # Субшкалы
            svod_count_column_level_pai_df = calc_count_level(base_df, [lst_svod_cols[idx]],
                                                              'Значение_субшкалы_Психоэмоциональное_истощение',
                                                              'Уровень_субшкалы_Психоэмоциональное_истощение',
                                                              lst_reindex_column_main_level_cols)

            svod_count_column_level_lo_df = calc_count_level(base_df, [lst_svod_cols[idx]],
                                                             'Значение_субшкалы_Личностное_отдаление',
                                                             'Уровень_субшкалы_Личностное_отдаление',
                                                             lst_reindex_column_main_level_cols)

            svod_count_column_level_pm_df = calc_count_level(base_df, [lst_svod_cols[idx]],
                                                             'Значение_субшкалы_Профессиональная_мотивация',
                                                             'Уровень_субшкалы_Профессиональная_мотивация',
                                                             lst_reindex_column_main_level_cols)

            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Значение_индекса_Психического_выгорания',
                                                         'Значение_субшкалы_Психоэмоциональное_истощение',
                                                         'Значение_субшкалы_Личностное_отдаление',
                                                         'Значение_субшкалы_Профессиональная_мотивация',
                                                         ],
                                                 aggfunc=round_mean)

            svod_mean_column_df.reset_index(inplace=True)
            new_order_cols = [lst_svod_cols[idx]].copy()

            new_order_cols.extend(
                ['Значение_индекса_Психического_выгорания', 'Значение_субшкалы_Психоэмоциональное_истощение',
                 'Значение_субшкалы_Личностное_отдаление', 'Значение_субшкалы_Профессиональная_мотивация'])
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)
            dct_rename_cols_mean = {'Значение_индекса_Психического_выгорания': 'Ср. психического выгорания',
                                    'Значение_субшкалы_Психоэмоциональное_истощение': 'Ср. психоэмоционального истошения',
                                    'Значение_субшкалы_Личностное_отдаление': 'Ср. личностного отдаления',
                                    'Значение_субшкалы_Профессиональная_мотивация': 'Ср. профессиональной мотивации'}

            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
                            f'Ср. {name_column}': svod_mean_column_df,
                            f'Свод ПЭИ {name_column}': svod_count_column_level_pai_df,
                            f'Свод ЛО {name_column}': svod_count_column_level_lo_df,
                            f'Свод ПМ {name_column}': svod_count_column_level_pm_df,
                            })
        return out_dct









def processing_rukav_psych_burnout(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 72:  # проверяем количество колонок с вопросами
            raise BadCountColumnsRPB

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я легко раздражаюсь.','Думаю, что работаю лишь потому, что надо где-то работать.','Меня беспокоит, что думают коллеги о моей работе.',
                          'Я чувствую, что у меня нет никаких эмоциональных сил вникать в чужие проблемы.','Меня мучает бессонница.','Думаю, что, если бы представилась удачная возможность, я бы сменил(а) место работы.',
                          'Я работаю с большим напряжением.','Моя работа приносит мне удовлетворение.','Чувствую, что работа с людьми изматывает меня.',
                          'Думаю, что моя работа важна.','Я устаю от человеческих проблем, с решением которых сталкиваюсь на работе.','Я доволен(а) профессией, которую выбрал(а).',
                          'Непонятливость моих коллег или учеников раздражает меня.','Я эмоционально устаю на работе.','Думаю, что не ошибся(лась) в выборе своей профессии.',
                          'Я чувствую себя опустошенным(ой) и разбитым(ой) после рабочего дня.','Чувствую, что получаю мало удовлетворения от достигнутых успехов на работе.','Мне трудно устанавливать или поддерживать тесные контакты с коллегами по работе.',
                          'Для меня важно преуспеть на работе.','Идя утром на работу, я чувствую себя свежим(ей) и отдохнувшим(ей).','Мне кажется, что результаты моей работы не стоят затраченных мною усилий.',
                          'У меня не хватает времени на свою семью и личную жизнь.','Я полон(а) оптимизма по отношению к своей работе.','Мне нравится моя работа.',
                          'Я устал(а) всё время стараться.','Меня утомляет участие в дискуссиях на профессиональные темы.','Мне кажется, что я изолирован(а) от своих коллег по работе.',
                          'Я удовлетворен(а) своим профессиональным выбором.','Я чувствую физическое напряжение, усталость.','Постепенно я начинаю испытывать безразличие к своим ученикам.',
                          'Работа эмоционально выматывает меня.','Я использую лекарства для улучшения самочувствия.','Меня интересуют результаты работы моих коллег.',
                          'Утром мне трудно вставать и идти на работу.','На работе меня преследует мысль: поскорее бы рабочий день закончился.','Нагрузка на работе практически невыносима.',
                          'Я ощущаю радость, помогая окружающим меня людям.','Я чувствую, что стал(а) более безразличным к своей работе.','Случается, что у меня без особой причины начинает болеть голова или желудок.',
                          'Я прилагаю усилия, чтобы быть терпеливым с учениками.','Я люблю свою работу.','У меня возникает чувство, что глубоко внутри я эмоционально не защищен(а).',
                          'Меня раздражает поведение моих учеников.','Мне легко понять чувства окружающих по отношению ко мне.','Меня часто охватывает желание всё бросить и уйти со своего рабочего места.',
                          'Я замечаю, что становлюсь всё более черствым(ой) по отношению к людям.','Я чувствую эмоциональное напряжение.','Я совершенно не увлечен(а) и даже не интересуюсь своей работой.',
                          'Я чувствую себя измотанным(ой).','Я считаю, что своим трудом я приношу пользу людям.','Временами я сомневаюсь в своих способностях.',
                          'Я испытываю ко всему, что происходит вокруг, полную апатию.','Выполнение повседневных дел для меня – источник удовольствия и удовлетворения.','Я не вижу смысла в том, что делаю на работе.',
                          'Я чувствую удовлетворение от выбранной мной профессии.','Хочется плюнуть на всё.','Я жалуюсь на здоровье без четко определенных симптомов.',
                          'Я доволен(а) своим положением на работе и в обществе.','Мне понравилась бы работа, отнимающая мало времени и сил.','Я чувствую, что работа с людьми сказывается на моем физическом здоровье.',
                          'Я сомневаюсь в значимости моей работы.','Испытываю чувство энтузиазма по отношению к работе.','Я так устаю на работе, что не в состоянии выполнять свои повседневные обязанности.',
                          'Считаю, что вполне компетентен(а) в решении проблем, возникающих на работе.','Чувствую, что могу дать детям больше, чем даю.','Мне буквально приходится заставлять себя работать.',
                          'Присутствует ощущение, что я могу легко расстроиться, впасть в уныние.','Мне нравится отдавать все силы работе.','Я испытываю состояние внутреннего напряжения и раздражения.',
                          'Я стал(а) с меньшим энтузиазмом относиться к своей работе.','Верю, что способен(а) выполнить всё, что задумано.','У меня нет желания глубоко вникать в проблемы моих учеников.'
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
            raise BadOrderRPB

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 0,
                             'редко': 1,
                             'обычно': 2,
                             'часто': 3,
    }

        valid_values = [0, 1, 2, 3]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(72):
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
            raise BadValueRPB

        base_df = pd.DataFrame()
        base_df['Значение_индекса_Психического_выгорания'] = answers_df.sum(axis=1)
        base_df['Норма_индекса_Психического_выгорания'] = '0-92 баллов'
        base_df['Уровень_индекса_Психического_выгорания'] =  base_df['Значение_индекса_Психического_выгорания'].apply(calc_level_index_psych_burnout)

        # Психоэмоциональное истощение
        base_df['Значение_субшкалы_Психоэмоциональное_истощение'] = answers_df.apply(calc_sub_value_psych_attrition, axis=1)
        base_df['Норма_субшкалы_Психоэмоциональное_истощение'] = '0-39 баллов'
        base_df['Уровень_субшкалы_Психоэмоциональное_истощение'] = base_df['Значение_субшкалы_Психоэмоциональное_истощение'].apply(
            calc_level_sub_psych_attrition)

        # Личностное отдаление
        base_df['Значение_субшкалы_Личностное_отдаление'] = answers_df.apply(calc_sub_value_lo, axis=1)
        base_df['Норма_субшкалы_Личностное_отдаление'] = '0-31 балл'
        base_df['Уровень_субшкалы_Личностное_отдаление'] = base_df['Значение_субшкалы_Личностное_отдаление'].apply(
            calc_level_sub_lo)

        # Профессиональная мотивация
        base_df['Значение_субшкалы_Профессиональная_мотивация'] = answers_df.apply(calc_sub_value_pm, axis=1)
        base_df['Норма_субшкалы_Профессиональная_мотивация'] = '0-24 балл'
        base_df['Уровень_субшкалы_Профессиональная_мотивация'] = base_df['Значение_субшкалы_Профессиональная_мотивация'].apply(
            calc_level_sub_pm)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ПВР_Индекс_Психического_выгорания'] = base_df['Значение_индекса_Психического_выгорания']
        part_df['ПВР_Уровень_индекса_Психического_выгорания'] = base_df['Уровень_индекса_Психического_выгорания']

        part_df['ПВР_ПЭИ_Значение'] = base_df['Значение_субшкалы_Психоэмоциональное_истощение']
        part_df['ПВР_ПЭИ_Уровень'] = base_df['Уровень_субшкалы_Психоэмоциональное_истощение']

        part_df['ПВР_ЛО_Значение'] = base_df['Значение_субшкалы_Личностное_отдаление']
        part_df['ПВР_ЛО_Уровень'] = base_df['Уровень_субшкалы_Личностное_отдаление']

        part_df['ПВР_ПМ_Значение'] = base_df['Значение_субшкалы_Профессиональная_мотивация']
        part_df['ПВР_ПМ_Уровень'] = base_df['Уровень_субшкалы_Профессиональная_мотивация']

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)

        base_df.sort_values(by='Значение_индекса_Психического_выгорания', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['очень низкий уровень', 'низкий уровень',
                   'средний уровень','высокий уровень','очень высокий уровень'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень_индекса_Психического_выгорания',
                                       values='Значение_индекса_Психического_выгорания',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_индекса_Психического_выгорания'] / svod_level_df[
                'Значение_индекса_Психического_выгорания'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_индекса_Психического_выгорания': 'Количество'},
                                inplace=True)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['очень низкий уровень', 'низкий уровень',
                   'средний уровень','высокий уровень','очень высокий уровень']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_индекса_Психического_выгорания'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        # Свод по уровням субшкалы Психоэмоциональное истощение всего в процентном соотношении

        base_svod_pia_df = create_svod_sub(base_df, lst_level, 'Уровень_субшкалы_Психоэмоциональное_истощение',
                                           'Значение_субшкалы_Психоэмоциональное_истощение', 'count')

        # Свод по уровням субшкалы Личностное отдаление всего в процентном соотношении
        base_svod_lo_df = create_svod_sub(base_df, lst_level, 'Уровень_субшкалы_Личностное_отдаление',
                                              'Значение_субшкалы_Личностное_отдаление', 'count')

        # Свод по уровням субшкалы Профессиональная мотивация всего в процентном соотношении
        base_svod_pm_df = create_svod_sub(base_df, lst_level, 'Уровень_субшкалы_Профессиональная_мотивация',
                                             'Значение_субшкалы_Профессиональная_мотивация', 'count')

        # считаем среднее значение по субшкалам
        avg_all = round(base_df['Значение_индекса_Психического_выгорания'].mean(), 2)
        avg_pia = round(base_df['Значение_субшкалы_Психоэмоциональное_истощение'].mean(), 2)
        avg_lo = round(base_df['Значение_субшкалы_Личностное_отдаление'].mean(), 2)
        avg_pm = round(base_df['Значение_субшкалы_Профессиональная_мотивация'].mean(), 2)

        avg_dct = {'Среднее значение индекса Психического выгорания': avg_all,
                   'Среднее значение субшкалы Психоэмоциональное истощение': avg_pia,
                   'Среднее значение субшкалы Личностное отдаление': avg_lo,
                   'Среднее значение субшкалы Профессиональная мотивация': avg_pm,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод ПЭИ': base_svod_pia_df, 'Свод ЛО': base_svod_lo_df, 'Свод ПМ': base_svod_pm_df,
                        'Среднее по субшкалам': avg_df}
                       )

        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_rpb(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df
    except BadOrderRPB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник психологического выгорания Рукавишников обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueRPB:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник психологического выгорания Рукавишников обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsRPB:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник психологического выгорания Рукавишников\n'
                             f'Должно быть 72 колонки с ответами')




