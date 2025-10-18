"""
Скрипт для обработки результатов теста Опросник мотивации к избеганию неудач Элерс Котик
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import calc_count_scale,round_mean

class BadValueKAF(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsKAF(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 30
    """
    pass

def calc_value_avoid_fail(row):
    """
    Обработка результатов тестирования
    """
    value_avoid = 0 # количество совпадений с ключом

    # 1
    if row[0] == 'бдительный':
        value_avoid += 1

    # 2
    if row[1] != 'упрямый':
        value_avoid += 1

    # 3
    if row[2] != 'решительный':
        value_avoid += 1

    # 4
    if row[3] == 'внимательный':
        value_avoid += 1

    # 5
    if row[4] == 'трусливый':
        value_avoid += 1

    # 6
    if row[5] == 'предусмотрительный':
        value_avoid += 1

    # 7
    if row[6] != 'хладнокровный':
        value_avoid += 1

    # 8
    if row[7] == 'боязливый':
        value_avoid += 1

    # 9
    if row[8] != 'непредусмотрительный':
        value_avoid += 1

    # 10
    if row[9] == 'добросовестный':
        value_avoid += 1

    # 11
    if row[10] != 'неустойчивый':
        value_avoid += 1

    # 12
    if row[11] != 'небрежный':
        value_avoid += 1

    # 13
    if row[12] != 'опрометчивый':
        value_avoid += 1

    # 14
    if row[13] == 'внимательный':
        value_avoid += 1

    # 15
    if row[14] == 'рассудительный':
        value_avoid += 1

    # 16
    if row[15] != 'предприимчивый':
        value_avoid += 1

    # 17
    if row[16] =='робкий':
        value_avoid += 1

    # 18
    if row[17] == 'малодушный':
        value_avoid += 1

    # 19
    if row[18] != 'нервный':
        value_avoid += 1

    # 20
    if row[19] !='авантюрный':
        value_avoid += 1

    # 21
    if row[20] == 'предусмотрительный':
        value_avoid += 1

    # 22
    if row[21] == 'укрощенный':
        value_avoid += 1

    # 23
    if row[22] != 'беззаботный':
        value_avoid +=1

    # 24
    if row[23] != 'храбрый':
        value_avoid += 1

    # 25
    if row[24] == 'предвидящий':
        value_avoid += 1

    # 26
    if row[25] == 'пугливый':
        value_avoid += 1

    # 27
    if row[26] == 'пессимистичный':
        value_avoid += 1

    # 28
    if row[27] != 'предприимчивый':
        value_avoid += 1

    # 29
    if row[28] != 'неорганизованный':
        value_avoid += 1

    # 30
    if row[29] == 'бдительный':
        value_avoid += 1

    return value_avoid



def calc_level_avoid_fail(value:int):
    """
    Уровень мотивации к успеху
    :param value: значение
    :return:
    """
    if value <= 10:
        return 'низкий уровень мотивации к избеганию неудач'
    elif 11 <= value <= 16:
        return 'средний уровень мотивации к избеганию неудач'
    elif 17 <= value <= 20:
        return 'высокий уровень мотивации к избеганию неудач'
    else:
        return 'слишком высокий уровень мотивации к избеганию неудач'


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


def create_result_kaf(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий уровень мотивации к избеганию неудач','средний уровень мотивации к избеганию неудач','высокий уровень мотивации к избеганию неудач',
                 'слишком высокий уровень мотивации к избеганию неудач']
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend(['низкий уровень мотивации к избеганию неудач','средний уровень мотивации к избеганию неудач','высокий уровень мотивации к избеганию неудач',
                 'слишком высокий уровень мотивации к избеганию неудач',
                               'Итого'])  # Основная шкала

    svod_count_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Значение_Избегание',
                                               'Уровень_Избегание',
                                               lst_reindex_main_level_cols, lst_level)

    # Считаем среднее
    svod_mean_df = calc_mean(base_df, lst_svod_cols, 'Значение_Избегание')
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
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий уровень мотивации к избеганию неудач','средний уровень мотивации к избеганию неудач','высокий уровень мотивации к избеганию неудач',
                 'слишком высокий уровень мотивации к избеганию неудач',
                               'Итого']

            svod_count_column_level_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                       'Значение_Избегание',
                                                       'Уровень_Избегание',
                                                       lst_reindex_column_level_cols, lst_level)

            # Считаем среднее
            svod_mean_column_df = calc_mean(base_df, [lst_svod_cols[idx]], 'Значение_Избегание')
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
                            f'Ср. {name_column}': svod_mean_column_df})

        return out_dct






def processing_kotik_avoiding_fail(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 30:  # проверяем количество колонок с вопросами
            raise BadCountColumnsKAF

        answers_df.columns = [f'Вопрос {i}' for i in range(1, 31)]

        # делаем список списков
        valid_values = [['смелый','бдительный','предприимчивый'],
                        ['кроткий','робкий','упрямый'],
                        ['осторожный','решительный','пессимистичный'],
                        ['непостоянный','бесцеремонный','внимательный'],
                        ['неумный','трусливый','не думающий'],
                        ['ловкий','бойкий','предусмотрительный'],
                        ['хладнокровный','колеблющийся','удалой'],
                        ['стремительный','легкомысленный','боязливый'],
                        ['не задумывающийся','жеманный','непредусмотрительный'],
                        ['оптимистичный','добросовестный','чуткий'],
                        ['меланхоличный','сомневающийся','неустойчивый'],
                        ['трусливый','небрежный','взволнованный'],
                        ['опрометчивый','тихий','боязливый'],
                        ['внимательный','неблагоразумный','смелый'],
                        ['рассудительный','быстрый','мужественный'],
                        ['предприимчивый','осторожный','предусмотрительный'],
                        ['взволнованный','рассеянный','робкий'],
                        ['малодушный','неосторожный','бесцеремонный'],
                        ['пугливый','нерешительный','нервный'],
                        ['исполнительный','преданный','авантюрный'],
                        ['предусмотрительный','бойкий','отчаянный'],
                        ['укрощенный','безразличный','небрежный'],
                        ['осторожный','беззаботный','терпеливый'],
                        ['разумный','заботливый','храбрый'],
                        ['предвидящий','неустрашимый','добросовестный'],
                        ['поспешный','пугливый','беззаботный'],
                        ['рассеянный','опрометчивый','пессимистичный'],
                        ['осмотрительный','рассудительный','предприимчивый'],
                        ['тихий','неорганизованный','боязливый'],
                        ['оптимистичный','бдительный','беззаботный'],
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
            raise BadValueKAF

        base_df[f'Значение_Избегание'] = answers_df.apply(calc_value_avoid_fail, axis=1)
        base_df['Уровень_Избегание'] = base_df['Значение_Избегание'].apply(calc_level_avoid_fail)  # Уровень Избегание

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        # Общая тревожность
        part_df['МИН_Избегание_Значение'] = base_df['Значение_Избегание']
        part_df['МИН_Избегание_Уровень'] = base_df['Уровень_Избегание']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Значение_Избегание', ascending=False, inplace=True)  # сортируем

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['низкий уровень мотивации к избеганию неудач', 'средний уровень мотивации к избеганию неудач',
                   'высокий уровень мотивации к избеганию неудач', 'слишком высокий уровень мотивации к избеганию неудач'])

        svod_level_df = pd.pivot_table(base_df, index='Уровень_Избегание',
                                       values='Значение_Избегание',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['Значение_Избегание'] / svod_level_df[
                'Значение_Избегание'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)
        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'Значение_Избегание': 'Количество'},
                                inplace=True)

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        lst_level = ['низкий уровень мотивации к избеганию неудач', 'средний уровень мотивации к избеганию неудач',
                   'высокий уровень мотивации к избеганию неудач', 'слишком высокий уровень мотивации к избеганию неудач']
        dct_level = dict()

        for level in lst_level:
            temp_df = base_df[base_df['Уровень_Избегание'] == level]
            if temp_df.shape[0] != 0:
                if level == 'низкий уровень мотивации к избеганию неудач':
                    level = 'низкий'
                elif level == 'средний уровень мотивации к избеганию неудач':
                    level = 'средний'
                elif level == 'высокий уровень мотивации к избеганию неудач':
                    level = 'умеренно высокий'
                else:
                    level = 'слишком высокий'

                dct_level[level] = temp_df

        out_dct.update(dct_level)

        """
                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_kaf(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df
    except BadValueKAF:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник мотивации к избеганию неудач Элерс Котик обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsKAF:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник мотивации к избеганию неудач Элерс Котик\n'
                             f'Должно быть 30 колонок с ответами')












