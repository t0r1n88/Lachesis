"""
Скрипт для обработки результатов теста Шкала оценки влияния травматического события (ШОВТС) в адаптации Тарабриной
"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,calc_count_scale


class BadOrderSHOVTST(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueSHOVTST(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsSHOVTST(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 22
    """
    pass




def calc_level_shovts(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value <= 20:
        return '0-20'
    elif 21 <= value <= 40:
        return '21-40'
    elif 41 <= value <= 60:
        return '41-60'
    elif 61 <= value <= 80:
        return '61-80'
    else:
        return '81-110'


def calc_value_invasion(row):
    """
       Функция для подсчета значения субшкалы Вторжение
       :param row: строка с ответами
       :return: число
       """
    lst_pr = [1,2,3,6,9,16,20]  # вопросы
    result = 0  # результат
    for idx, value in enumerate(row):
        if idx + 1 in lst_pr:
            result += value

    return result


def calc_value_avoidance(row):
    """
       Функция для подсчета значения субшкалы Избегание
       :param row: строка с ответами
       :return: число
       """
    lst_pr = [5,7,8,11,12,13,17,22]  # вопросы
    result = 0  # результат
    for idx, value in enumerate(row):
        if idx + 1 in lst_pr:
            result += value

    return result

def calc_value_excitability(row):
    """
       Функция для подсчета значения субшкалы Физиологическая возбудимость
       :param row: строка с ответами
       :return: число
       """
    lst_pr = [4,10,14,15,18,19,21]  # вопросы
    result = 0  # результат
    for idx, value in enumerate(row):
        if idx + 1 in lst_pr:
            result += value

    return result

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





def create_result_shovts(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['0-20','21-40','41-60','61-80','81-110']
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend(['0-20','21-40','41-60','61-80','81-110',
                               'Итого'])  # Основная шкала

    svod_count_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Значение_ШОВТС',
                                                    'Диапазон_ШОВТС',
                                                    lst_reindex_main_level_cols,lst_level)

    # Считаем среднее
    svod_mean_df = calc_mean(base_df, lst_svod_cols, 'Значение_ШОВТС')
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
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'0-20','21-40','41-60','61-80','81-110',
                               'Итого']

            svod_count_column_level_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                       'Значение_ШОВТС',
                                                       'Диапазон_ШОВТС',
                                                       lst_reindex_column_level_cols, lst_level)

            # Считаем среднее
            svod_mean_column_df = calc_mean(base_df, [lst_svod_cols[idx]], 'Значение_ШОВТС')
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
                            f'Ср. {name_column}': svod_mean_column_df})

        return out_dct








def processing_shovts_tarabrina(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 22:  # проверяем количество колонок с вопросами
            raise BadCountColumnsSHOVTST

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst
        lst_check_cols = ['Любое напоминание об этом событии (ситуации) заставляло меня заново переживать все случившееся',
                          'Я не мог спокойно спать по ночам',
                          'Некоторые вещи заставляли меня все время думать о том, что со мной случилось',
                          'Я чувствовал постоянное раздражение и гнев',
                          'Я не позволял себе расстраиваться, когда я думал об этом событии или что-то напоминало мне о нем',
                          'Я думал о случившемся против своей воли',
                          'Мне казалось, что всего случившегося со мной как будто не было на самом деле или все, что тогда происходило, было нереальным',
                          'Я старался избегать всего, что могло бы мне напомнить о случившемся',
                          'Отдельные картины случившегося внезапно возникали в сознании',
                          'Я был все время напряжен и сильно вздрагивал, если что-то внезапно пугало меня',
                          'Я старался не думать о случившемся',
                          'Я понимал, что меня до сих пор буквально переполняют тяжелые переживания по поводу того, что случилось, но ничего не делал, чтобы их избежать',
                          'Я чувствовал что-то вроде оцепенения, и все мои переживания по поводу случившегося были как будто парализованы',
                          'Я вдруг замечал, что действую или чувствую себя так, как будто бы все еще нахожусь в той ситуации',
                          'Мне было трудно заснуть',
                          'Меня буквально захлестывали непереносимо тяжелые переживания, связанные с той ситуацией',
                          'Я старался вытеснить случившееся из памяти',
                          'Мне было трудно сосредоточить внимание на чем-либо',
                          'Когда что-то напоминало мне о случившемся, я испытывал неприятные физические ощущения – потел, дыхание сбивалось, начинало тошнить, учащался пульс и т.п.',
                          'Мне снились тяжелые сны о том, что со мной случилось',
                          'Я был постоянно насторожен и все время ожидал, что случится что-то плохое',
                          'Я старался ни с кем не говорить о случившемся']

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
            raise BadOrderSHOVTST

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 0,
                             'редко': 1,
                             'иногда': 3,
                             'часто': 5,
                            }

        valid_values = [0, 1, 3, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(22):
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
            raise BadValueSHOVTST

        base_df = pd.DataFrame()

        base_df['Значение_ШОВТС'] = answers_df.sum(axis=1)
        base_df['Диапазон_ШОВТС'] = base_df['Значение_ШОВТС'].apply(
            calc_level_shovts)

        base_df['Значение_субшкалы_Вторжение'] = answers_df.apply(calc_value_invasion,axis=1)
        base_df['Значение_субшкалы_Избегание'] = answers_df.apply(calc_value_avoidance,axis=1)
        base_df['Значение_субшкалы_Физ_Возбудимость'] = answers_df.apply(calc_value_excitability,axis=1)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ШОВТС_Т_Значение'] = base_df['Значение_ШОВТС']
        part_df['ШОВТС_Т_Диапазон'] = base_df['Диапазон_ШОВТС']

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)

        base_df.sort_values(by='Значение_ШОВТС', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['0-20','21-40','41-60','61-80','81-110'])

        svod_level_df = pd.pivot_table(base_df, index='Диапазон_ШОВТС',
                                       values='Значение_ШОВТС',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_ШОВТС'] / svod_level_df[
                'Значение_ШОВТС'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_ШОВТС': 'Количество'},
                                inplace=True)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['0-20','21-40','41-60','61-80','81-110']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Диапазон_ШОВТС'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_shovts(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderSHOVTST:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала оценки влияния травматического события (ШОВТС) Тарабрина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueSHOVTST:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала оценки влияния травматического события (ШОВТС) Тарабрина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsSHOVTST:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала оценки влияния травматического события (ШОВТС) Тарабрина\n'
                             f'Должно быть 22 колонки с ответами')








