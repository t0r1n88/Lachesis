"""
Скрипт для обработки результатов теста Профессиональные установки подростков Андреева
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import convert_to_int,round_mean,create_union_svod,calc_count_scale,create_list_on_level

class BadOrderPUP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass

class BadValuePUP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsPUP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 24
    """
    pass


def processing_result_pup(row):
    """
Функция для вычисления итогового балла
"""

    # Создаем словарь для хранения данных
    dct_type = {'Уверенность в будущем выборе': 0, 'Нерешительность в выборе профессии': 0}
    lst_confidence = [1, 2, 4, 5, 7, 8, 9, 12, 13, 15, 17, 18, 19, 20, 22, 23]
    lst_indecision = [0, 3, 6, 10, 11, 14, 16, 21]
    for idx, value in enumerate(row):
        if idx in lst_confidence:
            dct_type['Уверенность в будущем выборе'] += value
        else:
            dct_type['Нерешительность в выборе профессии'] += value

    begin_str = (f'\nУверенность в будущем выборе: {dct_type["Уверенность в будущем выборе"]}; \n'
                 f'Нерешительность в выборе профессии: {dct_type["Нерешительность в выборе профессии"]}')
    return begin_str






def calc_value_confidence(row):
    """
    Функция для подсчета уровня уверенности
    :param row: строка с ответами респондента
    :return:
    """
    value_confidence = 0 # счетчик уверенности
    lst_confidence = [1,2,4,5,7,8,9,12,13,15,17,18,19,20,22,23]


    for idx,value in enumerate(row):
        if idx in lst_confidence:
            value_confidence += value

    return value_confidence


def calc_level_confidence(value):
    """
    Функция для вычисления уровня уверенности
    :param value: числовое значение
    :return: строка с уровнем
    """
    if 0 <= value <= 53:
        return 'низкий'
    elif 54 <= value <= 66:
        return 'средний'
    elif 67 <= value:
        return 'высокий'


def calc_value_indecision(row):
    """
    Функция для подсчета уровня неуверенности
    :param row: строка с ответами респондента
    :return:
    """
    value_indecision = 0 # счетчик уверенности
    lst_indecision = [0,3,6,10,11,14,16,21]

    for idx,value in enumerate(row):
        if idx in lst_indecision:
            value_indecision += value

    return value_indecision


def calc_level_indecision(value):
    """
    Функция для вычисления уровня неуверенности
    :param value: числовое значение
    :return: строка с уровнем
    """
    if 0 <= value <= 12:
        return 'низкий'
    elif 13 <= value <= 19:
        return 'средний'
    elif 20 <= value:
        return 'высокий'


def create_result_andreeva_pup(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий', 'средний','высокий']


    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['низкий', 'средний','высокий',
                                                      'Итого'])

    svod_count_one_level_resh_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Значение_уверенности',
                                               'Уровень_уверенности',
                                               lst_reindex_one_level_cols,lst_level)
    svod_count_one_level_noresh_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Значение_нерешительности',
                                               'Уровень_нерешительности',
                                               lst_reindex_one_level_cols,lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_уверенности','Значение_нерешительности'
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_уверенности','Значение_нерешительности'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_уверенности': 'Среднее значение уверенности',
                            'Значение_нерешительности': 'Среднее значение нерешительности',
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
                    f'Ув {out_name}': svod_count_one_level_resh_df,
                    f'Нер {out_name}': svod_count_one_level_noresh_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'низкий', 'средний','высокий',
                                             'Итого']

            svod_count_column_level_resh_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'Значение_уверенности',
                                                          'Уровень_уверенности',
                                                          lst_reindex_column_level_cols, lst_level)

            svod_count_column_level_noresh_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'Значение_нерешительности',
                                                          'Уровень_нерешительности',
                                                          lst_reindex_column_level_cols, lst_level)


            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Значение_уверенности','Значение_нерешительности'
                                                         ],
                                                 aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_уверенности','Значение_нерешительности'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_уверенности': 'Среднее значение Уверенности',
                                    'Значение_нерешительности': 'Среднее значение Нерешительности',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)


            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Ув {name_column}': svod_count_column_level_resh_df,
                            f'Нер {name_column}': svod_count_column_level_noresh_df,
                            })
        return out_dct





def processing_andreeva_pup(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if answers_df.shape[1] != 24:
            raise BadCountColumnsPUP

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я слишком плохо знаю мир профессий', 'Выбор профессии не должен делаться под влиянием эмоций',
                          'Я могу отказаться от многих удовольствий ради престижной будущей профессии',
                          'Мне нужна поддержка и помощь в выборе профессии',
                          'Я чувствую, что уже пора готовиться к будущей профессии',
                          'Я верю, что стану первоклассным специалистом',
                          'Мне трудно сделать выбор между привлекательными профессиями',
                          'Я верю, что смогу развить свои способности ради будущей профессии',
                          'Я знаю, что найду профессию по себе',
                          'Я чувствую себя уверенно, когда знаю, что мой профессиональный выбор одобряют другие люди',
                          'Совершенно не знаю, на что ориентироваться при выборе профессии',
                          'Реклама многих профессий редко соответствует их реальному содержанию',
                          'Я надеюсь, что выбранная профессия позволит раскрыть мою индивидуальность',
                          'Я надеюсь, что моя профессия будет востребованной в будущем',
                          'Совершенно не знаю, с чего мне начать свой профессиональный путь',
                          'Я верю, что работа даст мне независимость от родителей',
                          'В выборе профессии я слишком поддаюсь внешним влияниям, советам, примерам',
                          'Я знаю, на какого профессионала я хочу стать похожим',
                          'Я надеюсь, что я буду с удовольствием заниматься выбранной профессией',
                          'Я приложу все усилия, чтобы сделать успешную карьеру',
                          'Я совсем не стремлюсь к взрослой и самостоятельной жизни',
                          'Я плохо представляю свое профессиональное будущее',
                          'Для меня важна не профессия, а карьера',
                          'В будущей профессии мне хотелось бы стать известным человеком'
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
            raise BadOrderPUP

        answers_df = answers_df.applymap(convert_to_int)  # приводим к инту
        # проверяем правильность
        valid_values = [1, 2, 3, 4, 5, 6]
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(24):
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
            raise BadValuePUP

        base_df[f'Распределение'] = answers_df.apply(processing_result_pup, axis=1)
        base_df[f'Значение_уверенности'] = answers_df.apply(calc_value_confidence, axis=1)
        base_df['Уровень_уверенности'] = base_df['Значение_уверенности'].apply(calc_level_confidence)
        base_df[f'Значение_нерешительности'] = answers_df.apply(calc_value_indecision, axis=1)
        base_df['Уровень_нерешительности'] = base_df['Значение_нерешительности'].apply(calc_level_indecision)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ПУП_Распределение'] = base_df['Распределение']
        part_df['ПУП_Уверенность_Значение'] = base_df['Значение_уверенности']
        part_df['ПУП_Уверенность_Уровень'] = base_df['Уровень_уверенности']
        part_df['ПУП_Нерешительность_Значение'] = base_df['Значение_нерешительности']
        part_df['ПУП_Нерешительность_Уровень'] = base_df['Уровень_нерешительности']

        base_df.sort_values(by='Значение_уверенности', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Создаем строку с описанием
        description_result = """
        Шкала оценки результатов уверенности в будущем выборе
        больше 67 баллов – высокая;
        54-66 баллов – средняя;
        53 и ниже баллов – низкая.
    
        Шкала оценки результатов нерешительности в выборе профессии
        больше 20 баллов – высокая;
        13-19 баллов – средняя;
        12 и ниже баллов – низкая.
    
        Полученные результаты уверенности и неуверенности позволяют выявить психологическую готовность старшеклассников к переходу на следующий возрастной этап, связанный с выбором профессии и получением профессионального образования.      
                """
        # создаем описание результата
        base_df[f'Описание_результата'] = 'Профессиональные установки подростков.\nРезультат тестирования:\n' + base_df[
            f'Распределение'] + '\n' + description_result
        part_df['ПУП_Описание_результата'] = base_df[f'Описание_результата']

        # Делаем свод по уровню
        dct_svod_level = {'Значение_уверенности': 'Уровень_уверенности',
                          'Значение_нерешительности': 'Уровень_нерешительности'
                          }
        dct_rename_svod_level = {'Значение_уверенности': 'Количество Уверенность',
                                 'Значение_нерешительности': 'Количество Нерешительность'
                                 }
        # Списки для шкал
        lst_level = ['низкий', 'средний', 'высокий']
        base_svod_level_df = create_union_svod(base_df, dct_svod_level, dct_rename_svod_level, lst_level)

        # считаем среднее значение
        avg_resh = round(base_df['Значение_уверенности'].mean(), 2)
        avg_no_resh = round(base_df['Значение_нерешительности'].mean(), 2)

        avg_dct = {'Среднее значение Уверенность': avg_resh,
                   'Среднее значение Нерешительность': avg_no_resh
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Среднее': avg_df,
                   'Свод по уровням': base_svod_level_df,
                   }

        dct_prefix = {'Уровень_уверенности': 'Ув',
                      'Уровень_нерешительности': 'Нер',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_level, dct_prefix)

        """
                          Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                          """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_andreeva_pup(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadOrderPUP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Профессиональные установки подростков Андреева обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValuePUP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Профессиональные установки подростков Андреева обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsPUP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Профессиональные установки подростков Андреева\n'
                             f'Должно быть 24 колонки с ответами')




