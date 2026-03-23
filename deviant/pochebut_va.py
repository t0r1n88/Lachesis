"""
Скрипт для обработки результатов Виды агрессивности Л.Г. Почебут
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderVAP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueVAP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsVAP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 40
    """
    pass

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <= 10:
        return f'низкий уровень агрессивности'
    elif 11 <= value <= 24:
        return f'средний уровень агрессивности'
    else:
        return f'высокий уровень агрессивности'


def calc_value_va(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,9,10,25,26,33,17]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx != 17:
                if value == 1:
                    value_forward += 1
            else:
                if value == 0:
                    value_forward += 1

    return value_forward


def calc_value_fa(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,4,11,18,19,28,34,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx != 27:
                if value == 1:
                    value_forward += 1
            else:
                if value == 0:
                    value_forward += 1

    return value_forward

def calc_value_pa(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,12,13,21,29,35,36,20]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx != 20:
                if value == 1:
                    value_forward += 1
            else:
                if value == 0:
                    value_forward += 1

    return value_forward

def calc_value_ea(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,14,15,22,30,37,38,23]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx != 23:
                if value == 1:
                    value_forward += 1
            else:
                if value == 0:
                    value_forward += 1

    return value_forward

def calc_value_sa(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,8,16,24,32,39,40,31]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx != 31:
                if value == 1:
                    value_forward += 1
            else:
                if value == 0:
                    value_forward += 1

    return value_forward


def calc_level_sub(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <= 2:
        return f'низкий уровень агрессивности'
    elif 3 <= value <= 4:
        return f'средний уровень агрессивности'
    else:
        return f'высокий уровень агрессивности'

def create_list_on_level_vap(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'низкий уровень агрессивности':
                    level = 'низкий'
                elif level == 'средний уровень агрессивности':
                    level = 'средний'
                else:
                    level = 'высокий'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_va_pochebut(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий уровень агрессивности', 'средний уровень агрессивности', 'высокий уровень агрессивности']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий уровень агрессивности', 'средний уровень агрессивности', 'высокий уровень агрессивности',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_k_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИП_Значение',
                                                 'ИП_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_d_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ВА_Значение',
                                                 'ВА_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # ИЗ
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ФА_Значение',
                                                 'ФА_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # ИЗ
    svod_count_one_level_pa_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ПА_Значение',
                                                 'ПА_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # ИЗ
    svod_count_one_level_ea_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ЭА_Значение',
                                                 'ЭА_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # ИЗ
    svod_count_one_level_sa_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СА_Значение',
                                                 'СА_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ИП_Значение',
                                              'ВА_Значение',
                                              'ФА_Значение',

                                              'ПА_Значение',
                                              'ЭА_Значение',
                                              'СА_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ИП_Значение',
                            'ВА_Значение',
                            'ФА_Значение',

                            'ПА_Значение',
                            'ЭА_Значение',
                            'СА_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                            'ВА_Значение': 'Ср. Вербальная агрессия',
                            'ФА_Значение': 'Ср. Физическая агрессия',
                            'ПА_Значение': 'Ср. Предметная агрессия',
                            'ЭА_Значение': 'Ср. Эмоциональная агрессия',
                            'СА_Значение': 'Ср. Самоагрессия',
                            }
    svod_mean_one_df.rename(columns=dct_rename_cols_mean, inplace=True)

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
                    f'ИП {out_name}': svod_count_one_level_k_df,
                    f'ВА {out_name}': svod_count_one_level_d_df,
                    f'ФА {out_name}': svod_count_one_level_s_df,

                    f'ПА {out_name}': svod_count_one_level_pa_df,
                    f'ЭА {out_name}': svod_count_one_level_ea_df,
                    f'СА {out_name}': svod_count_one_level_sa_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'низкий уровень агрессивности', 'средний уровень агрессивности', 'высокий уровень агрессивности',
                                             'Итого']

            # АД
            svod_count_column_level_k_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'ИП_Значение',
                                                         'ИП_Уровень',
                                                         lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_d_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'ВА_Значение',
                                                         'ВА_Уровень',
                                                         lst_reindex_column_level_cols, lst_level)
            # ИЗ
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'ФА_Значение',
                                                         'ФА_Уровень',
                                                         lst_reindex_column_level_cols, lst_level)
            # ИЗ
            svod_count_column_level_pa_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'ПА_Значение',
                                                          'ПА_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)
            # ИЗ
            svod_count_column_level_ea_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'ЭА_Значение',
                                                          'ЭА_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)
            # ИЗ
            svod_count_column_level_sa_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'СА_Значение',
                                                          'СА_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ИП_Значение',
                                                      'ВА_Значение',
                                                      'ФА_Значение',

                                                      'ПА_Значение',
                                                      'ЭА_Значение',
                                                      'СА_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИП_Значение',
                                    'ВА_Значение',
                                    'ФА_Значение',

                                    'ПА_Значение',
                                    'ЭА_Значение',
                                    'СА_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                                    'ВА_Значение': 'Ср. Вербальная агрессия',
                                    'ФА_Значение': 'Ср. Физическая агрессия',
                                    'ПА_Значение': 'Ср. Предметная агрессия',
                                    'ЭА_Значение': 'Ср. Эмоциональная агрессия',
                                    'СА_Значение': 'Ср. Самоагрессия',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИП {name_column}': svod_count_column_level_k_df,
                            f'ВА {name_column}': svod_count_column_level_d_df,
                            f'ФА {name_column}': svod_count_column_level_s_df,

                            f'ПА {name_column}': svod_count_column_level_pa_df,
                            f'ЭА {name_column}': svod_count_column_level_ea_df,
                            f'СА {name_column}': svod_count_column_level_sa_df,
                            })
        return out_dct













def processing_va_pochebut(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 40:  # проверяем количество колонок с вопросами
            raise BadCountColumnsVAP

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Во время спора я часто повышаю голос',
                          'Если меня кто-то раздражает, я могу сказать ему все, что о нем думаю',
                          'Если мне необходимо будет прибегнуть к физической силе для защиты своих прав, я, не раздумывая, сделаю это',
                          'Когда я встречаю неприятного мне человека, я могу позволить себе незаметно ущипнуть или толкнуть его',
                          'Увлекшись спором с другим человеком, я могу стукнуть кулаком по столу, чтобы привлечь к себе внимание или доказать свою правоту',
                          'Я постоянно чувствую, что другие не уважают мои права',
                          'Вспоминая прошлое, порой мне бывает обидно за себя',
                          'Хотя я и не подаю вида, иногда меня гложет зависть',
                          'Если я не одобряю поведение своих знакомых, то я прямо говорю им об этом',
                          'В сильном гневе я употребляю крепкие выражения, сквернословлю',

                          'Если кто-нибудь поднимет на меня руку, я постараюсь ударить его первым',
                          'Я бываю настолько взбешен, что швыряю разные предметы',
                          'У меня часто возникает потребность переставить в квартире мебель или полностью сменить ее',
                          'В общении с людьми я часто чувствую себя «пороховой бочкой», которая постоянно готова взорваться',
                          'Порой у меня появляется желание зло пошутить над другим человеком',
                          'Когда я сердит, то обычно мрачнею',
                          'В разговоре с человеком я стараюсь его внимательно выслушать, не перебивая',
                          'В молодости у меня часто «чесались кулаки» и я всегда был готов пустить их в ход',
                          'Если я знаю, что человек намеренно меня толкнул, то дело может дойти до драки',
                          'Творческий беспорядок на моем рабочем столе позволяет мне эффективно работать',

                          'Я помню, что бывал настолько сердитым, что хватал все, что попадало под руку, и ломал',
                          'Иногда люди раздражают меня только одним своим присутствием',
                          'Я часто удивляюсь, какие скрытые причины заставляют другого человека делать мне что-нибудь хорошее',
                          'Если мне нанесут обиду, у меня пропадет желание разговаривать с кем бы то ни было',
                          'Иногда я намеренно говорю гадости о человеке, которого не люблю',
                          'Когда я взбешен, я кричу самое злобное ругательство',
                          'В детстве я избегал драк',
                          'Я знаю, по какой причине и когда можно кого-нибудь ударить',
                          'Когда я взбешен, то могу хлопнуть дверью',
                          'Мне кажется, что окружающие люди меня не любят',

                          'Я постоянно делюсь с другими своими чувствами и переживаниями',
                          'Очень часто своими словами и действиями я сам себе приношу вред',
                          'Когда люди орут на меня, я отвечаю тем же',
                          'Если кто-нибудь ударит меня первым, я в ответ ударю его',
                          'Меня раздражает, когда предметы лежат не на своем месте',
                          'Если мне не удается починить сломавшийся или порвавшийся предмет, то я в гневе ломаю или рву его окончательно',
                          'Другие люди мне всегда кажутся преуспевающими',
                          'Когда я думаю об очень неприятном мне человеке, я могу прийти в возбуждение от желания причинить ему зло',
                          'Иногда мне кажется, что судьба сыграла со мной злую шутку',
                          'Если кто-нибудь обращается со мной не так, как следует, я очень расстраиваюсь по этому поводу'
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
            raise BadOrderVAP

        # словарь для замены слов на числа
        dct_replace_value = {'нет': 0,
                             'да': 1,
                             }
        valid_values = [0, 1]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(40):
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
            raise BadValueVAP

        base_df['ИП_Значение'] = answers_df.sum(axis=1)
        base_df['ИП_Уровень'] = base_df['ИП_Значение'].apply(calc_level)

        base_df['ВА_Значение'] = answers_df.apply(calc_value_va,axis=1)
        base_df['ВА_Уровень'] = base_df['ВА_Значение'].apply(calc_level_sub)

        base_df['ФА_Значение'] = answers_df.apply(calc_value_fa,axis=1)
        base_df['ФА_Уровень'] = base_df['ФА_Значение'].apply(calc_level_sub)

        base_df['ПА_Значение'] = answers_df.apply(calc_value_pa,axis=1)
        base_df['ПА_Уровень'] = base_df['ПА_Значение'].apply(calc_level_sub)

        base_df['ЭА_Значение'] = answers_df.apply(calc_value_ea,axis=1)
        base_df['ЭА_Уровень'] = base_df['ЭА_Значение'].apply(calc_level_sub)

        base_df['СА_Значение'] = answers_df.apply(calc_value_sa,axis=1)
        base_df['СА_Уровень'] = base_df['СА_Значение'].apply(calc_level_sub)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ТАП_ИП_Значение'] = base_df['ИП_Значение']
        part_df['ТАП_ИП_Уровень'] = base_df['ИП_Уровень']

        part_df['ТАП_ВА_Значение'] = base_df['ВА_Значение']
        part_df['ТАП_ВА_Уровень'] = base_df['ВА_Уровень']

        part_df['ТАП_ФА_Значение'] = base_df['ФА_Значение']
        part_df['ТАП_ФА_Уровень'] = base_df['ФА_Уровень']

        part_df['ТАП_ПА_Значение'] = base_df['ПА_Значение']
        part_df['ТАП_ПА_Уровень'] = base_df['ПА_Уровень']

        part_df['ТАП_ЭА_Значение'] = base_df['ЭА_Значение']
        part_df['ТАП_ЭА_Уровень'] = base_df['ЭА_Уровень']

        part_df['ТАП_СА_Значение'] = base_df['СА_Значение']
        part_df['ТАП_СА_Уровень'] = base_df['СА_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИП_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ИП_Значение': 'ИП_Уровень',
                        'ВА_Значение': 'ВА_Уровень',
                        'ФА_Значение': 'ФА_Уровень',

                        'ПА_Значение': 'ПА_Уровень',
                        'ЭА_Значение': 'ЭА_Уровень',
                        'СА_Значение': 'СА_Уровень',
                        }

        dct_rename_svod_sub = {'ИП_Значение': 'Интегральный показатель',
                               'ВА_Значение': 'Вербальная агрессия',
                               'ФА_Значение': 'Физическая агрессия',

                               'ПА_Значение': 'Предметная агрессия',
                               'ЭА_Значение': 'Эмоциональная агрессия',
                               'СА_Значение': 'Самоагрессия',
                               }

        lst_sub = ['низкий уровень агрессивности', 'средний уровень агрессивности', 'высокий уровень агрессивности']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ИП_Значение'].mean(), 2)
        avg_o = round(base_df['ВА_Значение'].mean(), 2)
        avg_ruvs = round(base_df['ФА_Значение'].mean(), 2)

        avg_pa = round(base_df['ПА_Значение'].mean(), 2)
        avg_ea = round(base_df['ЭА_Значение'].mean(), 2)
        avg_sa = round(base_df['СА_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Интегрального показателя': avg_vcha,
                   'Среднее значение шкалы Вербальная агрессия': avg_o,
                   'Среднее значение шкалы Физическая агрессия': avg_ruvs,

                   'Среднее значение шкалы Предметная агрессия': avg_pa,
                   'Среднее значение шкалы Эмоциональная агрессия': avg_ea,
                   'Среднее значение шкалы Самоагрессия': avg_sa,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix = {'ИП_Уровень': 'ИП',
                      'ВА_Уровень': 'ВА',
                      'ФА_Уровень': 'ФА',

                      'ПА_Уровень': 'ПА',
                      'ЭА_Уровень': 'ЭА',
                      'СА_Уровень': 'СА',
                      }

        out_dct = create_list_on_level_vap(base_df, out_dct, lst_sub, dct_prefix)
        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_va_pochebut(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderVAP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста агрессивности Почебут обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueVAP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста агрессивности Почебут обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsVAP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест агрессивности Почебут\n'
                             f'Должно быть 40 колонок с ответами')










