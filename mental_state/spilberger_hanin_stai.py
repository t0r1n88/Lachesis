"""
Скрипт для обработки результатов теста Шкала реактивной и личностной тревожности STAI Спилбергер Ханин
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderSTAISH(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSTAISH(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSTAISH(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 40
    """
    pass


def calc_value_st(row):
    """
    Функция для подсчета значения
    :return: число
    """

    lst_pr = [3,4,6,7,9,12,13,14,17,18,
              1,2,5,8,10,11,15,16,19,20]
    value_forward = 0  # результат
    value_back = 0
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx in (3,4,6,7,9,12,13,14,17,18):
                value_forward += value
            elif idx in (1,2,5,8,10,11,15,16,19,20):
                value_back += value

    return value_forward- value_back + 50


def calc_level(value):
    """
    Функция для подсчета диапазонов
    :param value: значение
    :return:
    """
    if 0 <= value <= 30:
        return 'низкий'
    elif 31 <=value <= 45:
        return 'средний'
    else:
        return 'высокий'


def calc_value_lt(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [22,23,24,25,28,29,31,32,34,35,37,38,40,
              21,26,27,30,33,36,39]
    value_forward = 0  # результат
    value_back = 0
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx in (22,23,24,25,28,29,31,32,34,35,37,38,40):
                value_forward += value
            elif idx in ( 21,26,27,30,33,36,39):
                value_back += value

    return value_forward - value_back + 35

def create_result_stai_spil_han(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий', 'средний', 'высокий']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий', 'средний', 'высокий',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_st_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'СТ_Значение',
                                                    'СТ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_lt_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ЛТ_Значение',
                                                    'ЛТ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                          'СТ_Значение',
                                          'ЛТ_Значение'
                                      ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['СТ_Значение','ЛТ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'СТ_Значение': 'Ср. Ситуативная тревожность',
                            'ЛТ_Значение': 'Ср. Личностная тревожность'
                            }
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
                    f'СТ {out_name}': svod_count_one_level_st_df,
                    f'ЛТ {out_name}': svod_count_one_level_lt_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий', 'средний', 'высокий',
                                                  'Итого']
            svod_count_column_level_st_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'СТ_Значение',
                                                          'СТ_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_lt_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'ЛТ_Значение',
                                                          'ЛТ_Уровень',
                                                          lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=[
                                                  'СТ_Значение',
                                                  'ЛТ_Значение'
                                              ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['СТ_Значение', 'ЛТ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'СТ_Значение': 'Ср. Ситуативная тревожность',
                                    'ЛТ_Значение': 'Ср. Личностная тревожность'
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'СТ {name_column}': svod_count_column_level_st_df,
                            f'ЛТ {name_column}': svod_count_column_level_lt_df,
                            })
        return out_dct








def processing_stai_spil_han(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 40:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSTAISH

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я спокоен',
                          'Мне ничто не угрожает',
                          'Я нахожусь в напряжении',
                          'Я испытываю сожаление',
                          'Я чувствую себя свободно',
                          'Я расстроен',
                          'Меня волнуют возможные неудачи',
                          'Я чувствую себя отдохнувшим',
                          'Я встревожен',
                          'Я испытываю чувство внутреннего удовлетворения',

                          'Я уверен в себе',
                          'Я нервничаю',
                          'Я не нахожу себе места',
                          'Я взвинчен',
                          'Я не чувствую скованности, напряженности',
                          'Я доволен',
                          'Я озабочен',
                          'Я слишком возбужден и мне не по себе',
                          'Мне радостно',
                          'Мне приятно',

                          'Я испытываю удовольствие',
                          'Я очень легко устаю',
                          'Я легко могу заплакать',
                          'Я хотел бы быть таким же счастливым, как другие люди',
                          'Нередко я проигрываю из-за того, что недостаточно быстро принимаю решения',
                          'Обычно я чувствую себя бодрым',
                          'Я спокоен, хладнокровен и собран',
                          'Ожидаемые трудности обычно очень беспокоят меня',
                          'Я слишком переживаю из-за пустяков',
                          'Я вполне счастлив',

                          'Я принимаю все близко к сердцу',
                          'Мне не хватает уверенности в себе',
                          'Обычно я чувствую себя в безопасности',
                          'Я стараюсь избегать критических ситуаций и трудностей',
                          'У меня бывает хандра',
                          'Я доволен',
                          'Всякие пустяки отвлекают и волнуют меня',
                          'Я так сильно переживаю свои разочарования, что потом долго не могу забыть о них',
                          'Я уравновешенный человек',
                          'Меня охватывает сильное беспокойство, когда я думаю о своих делах и заботах'
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
            raise BadOrderSTAISH

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 1,
                             'почти никогда': 2,
                             'часто': 3,
                             'почти всегда': 4,
                             }
        valid_values = [1, 2, 3, 4]
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
            raise BadValueSTAISH

        base_df['СТ_Значение'] = answers_df.apply(calc_value_st, axis=1)
        base_df['СТ_Уровень'] = base_df['СТ_Значение'].apply(calc_level)

        base_df['ЛТ_Значение'] = answers_df.apply(calc_value_lt, axis=1)
        base_df['ЛТ_Уровень'] = base_df['ЛТ_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ШРЛТСХ_СТ_Значение'] = base_df['СТ_Значение']
        part_df['ШРЛТСХ_СТ_Уровень'] = base_df['СТ_Уровень']

        part_df['ШРЛТСХ_ЛТ_Значение'] = base_df['ЛТ_Значение']
        part_df['ШРЛТСХ_ЛТ_Уровень'] = base_df['ЛТ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ЛТ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'СТ_Значение': 'СТ_Уровень',
                        'ЛТ_Значение': 'ЛТ_Уровень',
                        }

        dct_rename_svod_sub = {
            'СТ_Значение': 'Уровень Ситуативная тревожность',
            'ЛТ_Значение': 'Уровень Личностная тревожность',
        }

        lst_sub = ['низкий', 'средний', 'высокий']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_st = round(base_df['СТ_Значение'].mean(), 2)
        avg_lt = round(base_df['ЛТ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Ситуативная тревожность': avg_st,
                   'Среднее значение шкалы Личностная тревожность': avg_lt,
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

        dct_prefix = {'СТ_Уровень': 'СТ',
                      'ЛТ_Уровень': 'ЛТ',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_stai_spil_han(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderSTAISH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала реактивной и личностной тревожности STAI Спилбергер Ханин обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSTAISH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала реактивной и личностной тревожности STAI Спилбергер Ханин обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSTAISH:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала реактивной и личностной тревожности STAI Спилбергер Ханин\n'
                             f'Должно быть 40 колонок с ответами')



