"""
Скрипт для обработки результатов теста Опросник оценки склонности к риску, RSK (Г. Шуберт)
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import calc_count_scale,round_mean

class BadOrderKRA(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueKRA(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsKRA(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 25
    """
    pass


def calc_level_risk(value:int):
    """
    Уровень склонности к риску
    :param value: значение
    :return:
    """
    if value < -30:
        return 'слишком острожны'
    elif -30 <= value <= -11:
        return 'осторожны'
    elif -10 <= value <= 10:
        return 'средний уровень'
    elif 11 <= value <= 20:
        return 'склонны к риску'
    else:
        return 'склонны к безудержному риску'


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



def create_result_kra(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['слишком острожны', 'осторожны',
               'средний уровень', 'склонны к риску','склонны к безудержному риску']
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend(['слишком острожны', 'осторожны',
               'средний уровень', 'склонны к риску','склонны к безудержному риску',
                               'Итого'])  # Основная шкала

    svod_count_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Значение_Риск',
                                               'Уровень_Риск',
                                               lst_reindex_main_level_cols, lst_level)

    # Считаем среднее
    svod_mean_df = calc_mean(base_df, lst_svod_cols, 'Значение_Риск')
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
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'слишком острожны', 'осторожны',
               'средний уровень', 'склонны к риску','склонны к безудержному риску',
                               'Итого']

            svod_count_column_level_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                       'Значение_Риск',
                                                       'Уровень_Риск',
                                                       lst_reindex_column_level_cols, lst_level)

            # Считаем среднее
            svod_mean_column_df = calc_mean(base_df, [lst_svod_cols[idx]], 'Значение_Риск')
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
                            f'Ср. {name_column}': svod_mean_column_df})

        return out_dct





def processing_kotik_risk_appetite(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 25:  # проверяем количество колонок с вопросами
            raise BadCountColumnsKRA
        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Превысили бы вы установленную скорость, чтобы быстрее оказать необходимую медицинскую помощь тяжелобольному человеку?',
                          'Согласились бы вы ради хорошего заработка участвовать в опасной и длительной экспедиции?',
                          'Стали бы вы на пути, убегающего опасного взломщика?',
                          'Могли бы вы ехать на подножке товарного вагона при скорости более 100км/ч?',
                          'Можете ли вы на другой после бессонной ночи нормально работать?',
                          'Стали бы вы первым переходить очень холодную реку?',
                          'Одолжили бы вы другу большую сумму денег, будучи совсем не уверенны, что он сможет вернуть эти деньги?',
                          'Вошли бы вы вместе с укротителем в клетку со львами при его заверении, что это безопасно?',
                          'Могли бы вы под руководством извне залезть на высокую фабричную трубу?',
                          'Могли бы вы без тренировки управлять парусной лодкой?',
                          'Могли бы вы схватить за уздечку бегущую лошадь?',
                          'Могли бы вы после 10 стаканов пива ехать на велосипеде?',
                          'Могли бы вы совершать прыжок с парашютом?',
                          'Могли бы вы при необходимости проехать без билета от Таллинна до Москвы?',
                          'Могли бы вы совершить автотурне, если бы за рулем сидел ваш знакомый, который совсем недавно был в тяжелом дорожном происшествии?',
                          'Могли бы вы с 10-метровой высоты прыгнуть на тент пожарной команды?',
                          'Могли бы вы, чтобы избавиться от затяжной болезни с постельным режимом, пойти на опасную для жизни операцию?',
                          'Могли бы вы спрыгнуть с подножки товарного вагона, движущегося со скоростью 50км/ч?',
                          'Могли бы вы в виде исключения вместе с семью другими людьми, подняться в лифте, рассчитанном только на шесть человек?',
                          'Могли бы вы за большое денежное вознаграждение перейти с завязанными глазами оживленный уличный перекресток?',
                          'Взялись бы вы за опасную для жизни работу, если бы за нее хорошо платили?',
                          'Могли бы вы после 10 рюмок водки вычислять проценты?',
                          'Могли бы вы по указанию вашего начальника взяться за высоковольтный провод, если бы он заверил вас, что провод обесточен?',
                          'Могли бы вы после некоторых предварительных объяснений управлять вертолетом?',
                          'Могли бы вы, имея билеты, но без денег и продуктов, доехать из Москвы до Хабаровска?'
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
            raise BadOrderKRA

        # словарь для замены слов на числа
        dct_replace_value = {'полностью согласен': 2,
                             'больше да, чем нет': 1,
                             'ни да, ни нет, нечто среднее': 0,
                             'больше нет, чем да': -1,
                             'полное нет': -2}

        valid_values = [-2,-1,0, 1, 2]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(25):
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
            raise BadValueKRA

        base_df['Значение_Риск'] = answers_df.sum(axis=1)
        base_df['Уровень_Риск'] = base_df['Значение_Риск'].apply(calc_level_risk)  # Уровень Склонности к риску

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Общая тревожность
        part_df['ССР_Риск_Значение'] = base_df['Значение_Риск']
        part_df['ССР_Риск_Уровень'] = base_df['Уровень_Риск']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Значение_Риск', ascending=False, inplace=True)  # сортируем

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['слишком острожны', 'осторожны',
                   'средний уровень', 'склонны к риску','склонны к безудержному риску'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень_Риск',
                                       values='Значение_Риск',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_Риск'] / svod_level_df[
                'Значение_Риск'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)
        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_Риск': 'Количество'},
                                inplace=True)

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['слишком острожны', 'осторожны',
                   'средний уровень', 'склонны к риску','склонны к безудержному риску']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_Риск'] == level]
            if temp_df.shape[0] != 0:
                if level == 'склонны к безудержному риску':
                    level = 'безудержный риск'
                dct_level[level] = temp_df

        out_dct.update(dct_level)

        """
                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_kra(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df
    except BadOrderKRA:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник оценки склонности к риску Шуберт Котик обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueKRA:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник оценки склонности к риску Шуберт Котик обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsKRA:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник оценки склонности к риску Шуберт Котик\n'
                             f'Должно быть 25 колонок с ответами')



