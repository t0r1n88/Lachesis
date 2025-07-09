"""
Скрипт для обработки результатов теста Шкала безадежности Бека
"""
from lachesis_support_functions import round_mean,create_union_svod
import pandas as pd
import re
from tkinter import messagebox


class BadOrderBekHopelessness(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueBekHopelessness(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsBekHopelessness(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass

def calc_value_hopelessness(row):
    """
    Функция для подсчета уровня безнадежности
    :param row: строка с ответами респондента
    :return:
    """
    value_hopelessness = 0 # счетчик безнадежности
    # обрабатываем
    if row[0] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[1] == 'ВЕРНО':
        value_hopelessness += 1
    if row[2] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[3] == 'ВЕРНО':
        value_hopelessness += 1
    if row[4] == 'НЕВЕРНО':
        value_hopelessness += 1

    if row[5] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[6] == 'ВЕРНО':
        value_hopelessness += 1
    if row[7] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[8] == 'ВЕРНО':
        value_hopelessness += 1
    if row[9] == 'НЕВЕРНО':
        value_hopelessness += 1

    if row[10] == 'ВЕРНО':
        value_hopelessness += 1
    if row[11] == 'ВЕРНО':
        value_hopelessness += 1
    if row[12] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[13] == 'ВЕРНО':
        value_hopelessness += 1
    if row[14] == 'НЕВЕРНО':
        value_hopelessness += 1

    if row[15] == 'ВЕРНО':
        value_hopelessness += 1
    if row[16] == 'ВЕРНО':
        value_hopelessness += 1
    if row[17] == 'ВЕРНО':
        value_hopelessness += 1
    if row[18] == 'НЕВЕРНО':
        value_hopelessness += 1
    if row[19] == 'ВЕРНО':
        value_hopelessness += 1

    return value_hopelessness

def calc_level_hopelessness(value):
    """
    Функция для вычисления уровня безнадежности
    :param value: числовое значение
    :return: строка с уровнем
    """
    if 0 <= value <= 3:
        return 'безнадёжность не выявлена'
    elif 4 <= value <= 8:
        return 'безнадежность лёгкая'
    elif 9 <= value <= 14:
        return 'безнадежность умеренная'
    elif value >= 15:
        return 'безнадежность тяжёлая'



def calc_count_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по шкалам

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
    count_df['% безнадёжность не выявлена от общего'] = round(
        count_df['безнадёжность не выявлена'] / count_df['Итого'], 2) * 100
    count_df['% безнадежность лёгкая от общего'] = round(
        count_df['безнадежность лёгкая'] / count_df['Итого'], 2) * 100
    count_df['% безнадежность умеренная от общего'] = round(
        count_df['безнадежность умеренная'] / count_df['Итого'], 2) * 100
    count_df['% безнадежность тяжёлая от общего'] = round(
        count_df['безнадежность тяжёлая'] / count_df['Итого'], 2) * 100

    return count_df

def create_result_bek_hopelessness(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['безнадёжность не выявлена', 'безнадежность лёгкая', 'безнадежность умеренная',
                                        'безнадежность тяжёлая','Итого'])

    svod_count_one_level_hopelessness_df = calc_count_level(base_df, lst_svod_cols,
                                                       'Значение_безнадежности',
                                                       'Уровень_безнадежности',
                                                       lst_reindex_one_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_безнадежности',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_безнадежности',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_безнадежности': 'Ср. Безнадежность',
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
                    f'Свод {out_name}': svod_count_one_level_hopelessness_df})

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            # Тревожность
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'безнадёжность не выявлена', 'безнадежность лёгкая', 'безнадежность умеренная',
                                        'безнадежность тяжёлая',
                                             'Итого']
            svod_count_column_level_hopelessness_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                               'Значение_безнадежности',
                                                               'Уровень_безнадежности',
                                                               lst_reindex_column_level_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Значение_безнадежности',
                                                         ],
                                                 aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_безнадежности',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_безнадежности': 'Ср. Безнадежность',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод {name_column}': svod_count_column_level_hopelessness_df})
        return out_dct




def processing_bek_hopelessness(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 20:
            raise BadCountColumnsBekHopelessness

        # Словарь для проверки вопросов
        lst_check_cols = ['Я жду будущего с надеждой и энтузиазмом',
                          'Мне пора сдаться, т.к. я ничего не могу изменить к лучшему',
                          'Когда дела идут плохо, мне помогает мысль, что так не может продолжаться всегда',
                          'Я не могу представить, на что будет похожа моя жизнь через 10 лет',
                          'У меня достаточно времени, чтобы завершить дела, которыми я больше всего хочу заниматься',
                          'В будущем, я надеюсь достичь успеха в том, что мне больше всего нравится',
                          'Будущее представляется мне во тьме',
                          'Я надеюсь получить в жизни больше хорошего, чем средний человек',
                          'У меня нет никаких просветов и нет причин верить, что они появятся в будущем',
                          'Мой прошлый опыт хорошо меня подготовил к будущему',
                          'Всё, что я вижу впереди - скорее, неприятности, чем радости',
                          'Я не надеюсь достичь того, чего действительно хочу',
                          'Когда я заглядываю в будущее, я надеюсь быть счастливее, чем я есть сейчас',
                          'Дела идут не так, как мне хочется',
                          'Я сильно верю в своё будущее',
                          'Я никогда не достигаю того, что хочу, поэтому глупо что-либо хотеть',
                          'Весьма маловероятно, что я получу реальное удовлетворение в будущем',
                          'Будущее представляется- мне расплывчатым и неопределённым',
                          'В будущем меня ждёт больше хороших дней, чем плохих',
                          'Бесполезно пытаться получить то, что я хочу, потому что, вероятно, я не добьюсь этого'
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
            raise BadOrderBekHopelessness

        valid_values = ['ВЕРНО', 'НЕВЕРНО']

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
            raise BadValueBekHopelessness


        base_df['Значение_безнадежности'] = answers_df.apply(calc_value_hopelessness, axis=1)
        base_df['Значение_нормы'] = '0-8 баллов'
        base_df['Уровень_безнадежности'] = base_df['Значение_безнадежности'].apply(calc_level_hopelessness)


        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ШБД_Безнадежность_Значение'] = base_df['Значение_безнадежности']
        part_df['ШБД_Безнадежность_Уровень'] = base_df['Уровень_безнадежности']


        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Значение_безнадежности', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Значение_безнадежности': 'Уровень_безнадежности',
                        }

        dct_rename_svod_sub = {'Значение_безнадежности': 'Безнадежность',
                               }

        # Списки для шкал
        lst_level = ['безнадёжность не выявлена', 'безнадежность лёгкая',
                     'безнадежность умеренная', 'безнадежность тяжёлая']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)

        # считаем среднее значение по шкалам
        avg_hopelessness = round(base_df['Значение_безнадежности'].mean(), 2)

        avg_dct = {'Среднее значение уровня безнадежность': avg_hopelessness,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод': base_svod_sub_df,
                   'Среднее': avg_df,
                   }
        dct_level = dict()
        for level in lst_level:
            temp_df = base_df[base_df['Уровень_безнадежности'] == level]
            if temp_df.shape[0] != 0:
                dct_level[level] = temp_df
        out_dct.update(dct_level)
        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_bek_hopelessness(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df


    except BadOrderBekHopelessness:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала безнадежности Бека обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueBekHopelessness:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала безнадежности Бека обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')

    except BadCountColumnsBekHopelessness:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала безнадежности Бека\n'
                             f'Должно быть 20 колонок с вопросами'
                            )


















