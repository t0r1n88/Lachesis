"""
Скрипт для обработки результатов теста шкала оценки интенсивности боевого опыта Тарабрина
"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,calc_count_scale

class BadOrderSIWET(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSIWET(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsSIWET(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 7
    """
    pass

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 5:
        return '0-5'
    elif 6 <= value <= 10:
        return '6-10'
    elif 11 <= value <= 15:
        return '11-15'
    elif 16 <= value <= 20:
        return '16-20'
    else:
        return '20-26'


def calc_mean(df:pd.DataFrame,lst_cat:list,val_cat):
    """
    Функция для создания сводных датафреймов

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формиваться свод
    :return:датафрейм
    """
    calc_mean_df = pd.pivot_table(df, index=lst_cat,
                                       values=val_cat,
                                       aggfunc=round_mean)
    calc_mean_df.reset_index(inplace=True)
    calc_mean_df.rename(columns={val_cat:'Среднее значение'},inplace=True)
    return calc_mean_df


def create_result_scale_intensity_war_exp(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['0-5','6-10','11-15','16-20','20-26']
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend(['0-5','6-10','11-15','16-20','20-26',
                               'Итого'])  # Основная шкала

    svod_count_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Значение_ШОИБО',
                                                    'Диапазон_ШОИБО',
                                                    lst_reindex_main_level_cols,lst_level)

    # Считаем среднее
    svod_mean_df = calc_mean(base_df, lst_svod_cols, 'Значение_ШОИБО')
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
                    f'Ср. {out_name}': svod_mean_df})

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'0-5','6-10','11-15','16-20','20-26',
                               'Итого']

            svod_count_column_level_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                       'Значение_ШОИБО',
                                                       'Диапазон_ШОИБО',
                                                       lst_reindex_column_level_cols, lst_level)

            # Считаем среднее
            svod_mean_column_df = calc_mean(base_df, [lst_svod_cols[idx]], 'Значение_ШОИБО')
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
                            f'Ср. {name_column}': svod_mean_column_df})

        return out_dct






def processing_scale_intensity_war_exp(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 7:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSIWET

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Сколько раз вы ходили в военный дозор, принимали участие в десантной операции или выполняли другое задание в условиях повышенной опасности?',
                          'Сколько месяцев вы находились в зоне обстрела со стороны противника?',
                          'Как часто вы находились в окружении врага?',
                          'Сколько человек в вашем подразделении было убито, ранено или пропало без вести во время военных действий?',
                          'Сколько раз вы участвовали в обстреле противника?',
                          'Сколько раз вы наблюдали, как кто-то был убит или ранен в ходе боевых действий?',
                          'Сколько раз вы подвергались опасности быть убитым или раненым (пулями, снарядами, холодным оружием), попадали в засаду, в другие очень опасные ситуации?'
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
            raise BadOrderSIWET

        valid_values = [['ни разу','1-2 раза','3-12 раз','13-50 раз','более чем 50 раз'],
                        ['ни разу','менее 1 месяца','1-3 месяца','4-6 месяцев','более чем 6 месяцев'],
                        ['ни разу','1-2 раза','3-12 раз','более 12 раз'],
                        ['ни одного','между 1-25%','между 26-50%','более чем 50%'],
                        ['ни разу', '1-2 раза', '3-12 раз', '13-50 раз', 'более чем 50 раз'],
                        ['ни разу', '1-2 раза', '3-12 раз', '13-50 раз', 'более чем 50 раз'],
                        ['ни разу', '1-2 раза', '3-12 раз', '13-50 раз', 'более чем 50 раз'],
                        ]

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
            raise BadValueSIWET

        # словарь для замены слов на числа
        dct_replace_value = {'ни разу': 0,
                             'ни одного': 0,

                             '1-2 раза':1,
                             'менее 1 месяца':1,
                             'между 1-25%':1,

                             '3-12 раз':2,
                             '1-3 месяца':2,
                             'между 26-50%':2,

                             '13-50 раз':3,
                             '4-6 месяцев':3,
                             'более 12 раз':3,
                             'более чем 50%':3,

                             'более чем 50 раз':4,
                             'более чем 6 месяцев':4,
                             }

        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        base_df = pd.DataFrame()

        base_df['Значение_ШОИБО'] = answers_df.sum(axis=1)
        base_df['Диапазон_ШОИБО'] = base_df['Значение_ШОИБО'].apply(
            calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ШОИБО_Т_Значение'] = base_df['Значение_ШОИБО']
        part_df['ШОИБО_Т_Диапазон'] = base_df['Диапазон_ШОИБО']

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)

        base_df.sort_values(by='Значение_ШОИБО', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['0-5','6-10','11-15','16-20','20-26'])

        svod_level_df = pd.pivot_table(base_df, index='Диапазон_ШОИБО',
                                       values='Значение_ШОИБО',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_ШОИБО'] / svod_level_df[
                'Значение_ШОИБО'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_ШОИБО': 'Количество'},
                                inplace=True)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['0-5','6-10','11-15','16-20','20-26']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Диапазон_ШОИБО'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_scale_intensity_war_exp(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderSIWET:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала оценки интенсивности боевого опыта Тарабрина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSIWET:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала оценки интенсивности боевого опыта Тарабрина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSIWET:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала оценки интенсивности боевого опыта Тарабрина\n'
                             f'Должно быть 7 колонок с ответами')





