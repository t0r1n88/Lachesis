"""
Скрипт для обработки результатов теста Методика измерения подростковой тревожности Хван Зайцев

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderMIPTHZ(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueMIPTHZ(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsMIPTHZ(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 30
    """
    pass


def calc_value_s(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,9,11,15,20,23,24,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_s_sten(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value == 0:
        return 1
    elif  value ==1 :
        return 2
    elif 2<= value <=3 :
        return 3
    elif  4<= value <=5 :
        return 4
    elif 6<= value <=7 :
        return 5
    elif 8<= value <=9 :
        return 6
    elif 10<= value <=11 :
        return 7
    elif 12<= value <=13:
        return 8
    elif 14<= value <=15 :
        return 9
    else:
        return 10

def calc_level(value):
    """
    Функция для подсчета диапазонов
    :param value: значение
    :return:
    """
    if 1<=value <= 2:
        return f'низкий'
    elif 3 <= value <= 4:
        return f'средний ближе к низкому'
    elif 5 <= value <= 6:
        return f'средний ближе к высокому'
    elif value == 7:
        return f'высокий'
    else:
        return f'очень высокий'


def calc_value_r(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,3,5,10,14,18,19]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward



def calc_r_sten(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value ==1:
        return 1
    elif 2<= value <=3:
        return 2
    elif 4<= value <=5:
        return 3
    elif 6<= value <=7:
        return 4
    elif 8<= value <=9:
        return 5
    elif 10<= value <=11:
        return 6
    elif 12<= value <=13:
        return 7
    elif 14<= value <=15:
        return 8
    elif 16<= value <=17:
        return 9
    else:
        return 10

def calc_value_b(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,7,16,17,21,25,26,30]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_b_sten(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value ==1:
        return 1
    elif 2<= value <=3:
        return 2
    elif 4<= value <=6:
        return 3
    elif 7<= value <=8:
        return 4
    elif 9<= value <=11:
        return 5
    elif 12<= value <=14:
        return 6
    elif 15<= value <=16:
        return 7
    elif 17<= value <=18:
        return 8
    elif 19<= value <=21:
        return 9
    else:
        return 10


def calc_value_so(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,8,12,13,22,28,29]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward

def calc_so_sten(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value ==0:
        return 1
    elif 1<= value <=2:
        return 2
    elif 3<= value <=4:
        return 3
    elif 5<= value <=6:
        return 4
    elif 7<= value <=8:
        return 5
    elif 9<= value <=10:
        return 6
    elif 11<= value <=12:
        return 7
    elif 13<= value <=14:
        return 8
    elif 15<= value <=16:
        return 9
    else:
        return 10

def calc_ip_sten(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<=value <=7:
        return 1
    elif 8<= value <=14:
        return 2
    elif 15<= value <=21:
        return 3
    elif 22<= value <=28:
        return 4
    elif 29<= value <=35:
        return 5
    elif 36<= value <=42:
        return 6
    elif 43<= value <=49:
        return 7
    elif 50<= value <=56:
        return 8
    elif 57<= value <=63:
        return 9
    else:
        return 10


def create_itog_stens(row):
    """
    Функция для создания строки с итоговым стеном
    :param row: строка с результатами
    :return:
    """
    lst_out = list(map(str,row))
    return '-'.join(lst_out)


def create_list_on_level_mipt(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
    """
    Функция для создания списков по уровням шкал
    :param base_df: датафрейм с результатами
    :param out_dct: словарь с датафреймами
    :param lst_level: список уровней по которым нужно сделать списки
    :param dct_prefix: префиксы для названий листов
    :return: обновлейнный out dct
    """
    for key,value in dct_prefix.items():
        dct_level = dict()
        for level in lst_level:
            temp_df = base_df[base_df[key] == level]
            if temp_df.shape[0] != 0:
                if level == 'средний ближе к низкому':
                    level = 'ближе к низкому'
                elif level == 'средний ближе к высокому':
                    level = 'ближе к высокому'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_mipthz(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level = ['низкий', 'средний ближе к низкому', 'средний ближе к высокому','высокий','очень высокий']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий', 'средний ближе к низкому', 'средний ближе к высокому','высокий','очень высокий',
                                       'Итого'])  # Основная шкала

    # Интегральные показатели
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'С_Стен',
                                                    'С_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_r_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Р_Стен',
                                                    'Р_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_b_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Б_Стен',
                                                    'Б_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)
    svod_count_one_level_so_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'СО_Стен',
                                                    'СО_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_ip_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ИП_Стен',
                                                    'ИП_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['С_Стен',
                                              'Р_Стен',
                                              'Б_Стен',
                                              'СО_Стен',
                                              'ИП_Стен',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['С_Стен',
                            'Р_Стен',
                            'Б_Стен',
                            'СО_Стен',
                            'ИП_Стен',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)
    dct_rename_cols_mean = {'С_Стен': 'Ср. значение стена Сверстники',
                            'Р_Стен': 'Ср. значение стена Родители',
                            'Б_Стен': 'Ср. значение стена Будущее',
                            'СО_Стен': 'Ср. значение стена Самооценка',
                            'ИП_Стен': 'Ср. значение стена Интегральный показатель'}

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

    out_dct.update({f'Ср {out_name}': svod_mean_one_df,
                    f'С {out_name}': svod_count_one_level_s_df,
                    f'Р {out_name}': svod_count_one_level_r_df,
                    f'Б {out_name}': svod_count_one_level_b_df,
                    f'СО {out_name}': svod_count_one_level_so_df,
                    f'ИП {out_name}': svod_count_one_level_ip_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий', 'средний ближе к низкому', 'средний ближе к высокому','высокий','очень высокий',
                                                  'Итого']

            # Интегральные показатели
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'С_Стен',
                                                         'С_Уровень',
                                                         lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_r_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'Р_Стен',
                                                         'Р_Уровень',
                                                         lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_b_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'Б_Стен',
                                                         'Б_Уровень',
                                                         lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_so_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'СО_Стен',
                                                          'СО_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_ip_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'ИП_Стен',
                                                          'ИП_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['С_Стен',
                                                      'Р_Стен',
                                                      'Б_Стен',
                                                      'СО_Стен',
                                                      'ИП_Стен',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['С_Стен',
                                    'Р_Стен',
                                    'Б_Стен',
                                    'СО_Стен',
                                    'ИП_Стен',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)
            dct_rename_cols_mean = {'С_Стен': 'Ср. значение стена Сверстники',
                                    'Р_Стен': 'Ср. значение стена Родители',
                                    'Б_Стен': 'Ср. значение стена Будущее',
                                    'СО_Стен': 'Ср. значение стена Самооценка',
                                    'ИП_Стен': 'Ср. значение стена Интегральный показатель'}

            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'С {name_column}': svod_count_column_level_s_df,
                            f'Р {name_column}': svod_count_column_level_r_df,
                            f'Б {name_column}': svod_count_column_level_b_df,
                            f'СО {name_column}': svod_count_column_level_so_df,
                            f'ИП {name_column}': svod_count_column_level_ip_df,
                            })
        return out_dct


def processing_mipt_hvan_zaycev(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        union_base_df = base_df.copy()  # делаем копию анкетной части чтобы потом соединить ее с ответной частью
        quantity_cols_base_df = base_df.shape[1]  # количество колонок в анкетной части

        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 30:  # проверяем количество колонок с вопросами
            raise BadCountColumnsMIPTHZ

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Поругался с родителями',
                          'Думаешь о том, что делать после окончания школы',
                          'Твои родители жалуются на свое здоровье',
                          'Ты случайно обидел своих одноклассников',
                          'Родители не могут покупать тебе престижные вещи',
                          'На тебя не обращают внимания окружающие',
                          'Думаешь, что не сможешь получить достойное образование',
                          'Слышишь по телевизору о введении более строгих вступительных экзаменах в ВУЗы',
                          'Твои друзья не считаются с твоим мнением',
                          'Не оправдываешь ожиданий своих близких',

                          'Сверстники критикуют твой внешний вид',
                          'Не можешь справиться с каким – либо заданием, делом',
                          'Думаешь о том, за что тебя можно любить',
                          'Твоих родителей обсуждают твои друзья',
                          'Не с кем поделиться своими переживаниями',
                          'Думаешь о том, что когда-нибудь можешь оказаться безработным',
                          'Слышишь о происходящих в мире террористических актах',
                          'У тебя нет достаточного количества карманных денег',
                          'Родители не понимают твоих проблем',
                          'Не можешь позволить себе те же развлечения, что и твои сверстники',

                          'Думаешь о выборе профессии',
                          'Сравниваешь себя со сверстниками, умеющими добиваться успеха, поставленных целей',
                          'Чувствуешь, что многие сверстники тебя не понимают',
                          'Думаешь, что если бы у тебя были такие же вещи как у некоторых твоих одноклассников, то ты пользовался бы такой же популярностью, как они',
                          'Думаешь о том, что родители зарабатывают недостаточно денег, чтобы помочь тебе встать на ноги',
                          'Тебе хотелось бы быть независимым от родителей, но у тебя нет для этого средств',
                          'Тебе хотелось бы чем-нибудь выделиться из сверстников, но тебе не хватает смелости',
                          'Понимаешь, что у твоих близких нет причин тобой гордиться',
                          'Думаешь, что тебе не хватит способностей для достижения успеха в жизни',
                          'Представляешь выпускные экзамены в школе',
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
            raise BadOrderMIPTHZ

        # словарь для замены слов на числа
        dct_replace_value = {'нет': 0,
                             'немного': 1,
                             'сильно': 2,
                             'очень сильно': 3,
                             }
        valid_values = [0, 1, 2, 3]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(30):
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
            raise BadValueMIPTHZ

        base_df['С_Сырое'] = answers_df.apply(calc_value_s, axis=1)
        base_df['С_Стен'] = base_df['С_Сырое'].apply(calc_s_sten)
        base_df['С_Уровень'] = base_df['С_Стен'].apply(calc_level)

        base_df['Р_Сырое'] = answers_df.apply(calc_value_r, axis=1)
        base_df['Р_Стен'] = base_df['Р_Сырое'].apply(calc_r_sten)
        base_df['Р_Уровень'] = base_df['Р_Стен'].apply(calc_level)

        base_df['Б_Сырое'] = answers_df.apply(calc_value_b, axis=1)
        base_df['Б_Стен'] = base_df['Б_Сырое'].apply(calc_b_sten)
        base_df['Б_Уровень'] = base_df['Б_Стен'].apply(calc_level)

        base_df['СО_Сырое'] = answers_df.apply(calc_value_so, axis=1)
        base_df['СО_Стен'] = base_df['СО_Сырое'].apply(calc_so_sten)
        base_df['СО_Уровень'] = base_df['СО_Стен'].apply(calc_level)

        base_df['ИП_Сырое'] = answers_df.sum(axis=1)
        base_df['ИП_Стен'] = base_df['ИП_Сырое'].apply(calc_ip_sten)
        base_df['ИП_Уровень'] = base_df['ИП_Стен'].apply(calc_level)

        # Упорядочиваем
        result_df = base_df.iloc[:, quantity_cols_base_df:]  # отсекаем часть с результатами чтобы упорядочить
        lst_stens = [column for column in result_df.columns if 'Стен' in column]
        result_df['Итоговые_стены'] = result_df[lst_stens].apply(create_itog_stens, axis=1)
        new_order_lst = ['Итоговые_стены',
                         'С_Стен', 'Р_Стен', 'Б_Стен', 'СО_Стен','ИП_Стен',

                         'С_Уровень', 'Р_Уровень', 'Б_Уровень','СО_Уровень', 'ИП_Уровень',

                         'С_Сырое', 'Р_Сырое', 'Б_Сырое', 'СО_Сырое','ИП_Сырое',
                         ]
        result_df = result_df.reindex(columns=new_order_lst)  # изменяем порядок
        base_df = pd.concat([union_base_df, result_df], axis=1)  # соединяем и перезаписываем base_df

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Стены
        part_df['МИПТХЗ_Итоговые_стены'] = base_df['Итоговые_стены']
        part_df['МИПТХЗ_С_Стен'] = base_df['С_Стен']
        part_df['МИПТХЗ_Р_Стен'] = base_df['Р_Стен']
        part_df['МИПТХЗ_Б_Стен'] = base_df['Б_Стен']
        part_df['МИПТХЗ_СО_Стен'] = base_df['СО_Стен']
        part_df['МИПТХЗ_ИП_Стен'] = base_df['ИП_Стен']

        # Уровни
        part_df['МИПТХЗ_С_Уровень'] = base_df['С_Уровень']
        part_df['МИПТХЗ_Р_Уровень'] = base_df['Р_Уровень']
        part_df['МИПТХЗ_Б_Уровень'] = base_df['Б_Уровень']
        part_df['МИПТХЗ_СО_Уровень'] = base_df['СО_Уровень']
        part_df['МИПТХЗ_ИП_Уровень'] = base_df['ИП_Уровень']

        # Значения
        part_df['МИПТХЗ_С_Сырое'] = base_df['С_Сырое']
        part_df['МИПТХЗ_Р_Сырое'] = base_df['Р_Сырое']
        part_df['МИПТХЗ_Б_Сырое'] = base_df['Б_Сырое']
        part_df['МИПТХЗ_СО_Сырое'] = base_df['СО_Сырое']
        part_df['МИПТХЗ_ИП_Сырое'] = base_df['ИП_Сырое']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        base_df.sort_values(by='ИП_Сырое', ascending=False, inplace=True)  # сортируем

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   }

        # Делаем свод по шкалам
        dct_svod_integral = {'С_Стен': 'С_Уровень',
                             'Р_Стен': 'Р_Уровень',
                             'Б_Стен': 'Б_Уровень',
                             'СО_Стен': 'СО_Уровень',
                             'ИП_Стен': 'ИП_Уровень',

                             }

        dct_rename_svod_integral = {'С_Стен': 'Сверстники',
                                    'Р_Стен': 'Родители',
                                    'Б_Стен': 'Будущее',
                                    'СО_Стен': 'Самооценка',
                                    'ИП_Стен': 'Интегральный показатель',
                                    }

        lst_integral = ['низкий', 'средний ближе к низкому', 'средний ближе к высокому','высокий','очень высокий']
        base_svod_integral_df = create_union_svod(base_df, dct_svod_integral, dct_rename_svod_integral, lst_integral)

        # Считаем среднее по шкалам
        avg_a = round(base_df['С_Стен'].mean(), 2)
        avg_b = round(base_df['Р_Стен'].mean(), 2)
        avg_c = round(base_df['Б_Стен'].mean(), 2)
        avg_so = round(base_df['СО_Стен'].mean(), 2)
        avg_d = round(base_df['ИП_Стен'].mean(), 2)

        avg_dct = {'Среднее значение стена шкалы Сверстники': avg_a,
                   'Среднее значение стена шкалы Родители': avg_b,
                   'Среднее значение стена шкалы Будущее': avg_c,
                   'Среднее значение стена шкалы Самооценка': avg_so,
                   'Среднее значение стена Интегрального показателя': avg_d,

                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        out_dct.update({'Свод Шкалы': base_svod_integral_df,
                        'Среднее': avg_df}
                       )

        dct_prefix = {'С_Уровень': 'С',
                      'Р_Уровень': 'Р',
                      'Б_Уровень': 'Б',
                      'СО_Уровень': 'СО',
                      'ИП_Уровень': 'ИП',
                      }

        out_dct = create_list_on_level_mipt(base_df, out_dct, lst_integral, dct_prefix)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_mipthz(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderMIPTHZ:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика измерения подростковой тревожности Хван Зайцев обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueMIPTHZ:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Методика измерения подростковой тревожности Хван Зайцев обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsMIPTHZ:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Методика измерения подростковой тревожности Хван Зайцев\n'
                             f'Должно быть 30 колонок с ответами')









