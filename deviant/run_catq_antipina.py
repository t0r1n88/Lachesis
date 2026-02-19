"""
Скрипт для обработки результатов теста Опросник Типология киберагрессии, CATQ Адаптация С.С. Антипина

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod

class BadOrderCATQRA(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueCATQRA(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsCATQRA(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 23
    """
    pass


def calc_value_ioka(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,4,5,6]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward


def calc_value_poka(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [7,8,9,10,11,12]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value
    return value_forward
def calc_value_pika(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [13,14,15,16,17,18]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return value_forward
def calc_value_iika(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [19,20,21,22,23]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value

    return value_forward

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 23<= value <= 33:
        return f'23-33'
    elif 34 <= value <= 46:
        return f'34-46'
    elif 47 <= value <= 70:
        return f'47-70'
    else:
        return f'71-92'



def create_list_on_level_catq(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_catq_run_antip(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['71-92', '47-70', '34-46', '23-33']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['71-92', '47-70', '34-46', '23-33',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'СППКА_Значение',
                                                   'СППКА_Диапазон',
                                                   lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ИОКА_Значение',
                                              'ПОКА_Значение',
                                              'ПИКА_Значение',
                                              'ИИКА_Значение',
                                              'СППКА_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ИОКА_Значение', 'ПОКА_Значение',
                            'ПИКА_Значение', 'ИИКА_Значение','СППКА_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ИОКА_Значение': 'Ср. Импульсивно-ответная киберагрессия',
                            'ПОКА_Значение': 'Ср. Произвольно-ответная киберагрессия',
                            'ПИКА_Значение': 'Ср. Произвольно-инициативная киберагрессия',
                            'ИИКА_Значение': 'Ср. Импульсивно-инициативная киберагрессия',
                            'СППКА_Значение': 'Ср. Суммарный показатель проявления киберагрессии',
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
                    f'СППКА {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'71-92', '47-70', '34-46', '23-33',
                                                  'Итого']
            # ВЧА
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'СППКА_Значение',
                                                            'СППКА_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ИОКА_Значение',
                                                      'ПОКА_Значение',
                                                      'ПИКА_Значение',
                                                      'ИИКА_Значение',
                                                      'СППКА_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИОКА_Значение', 'ПОКА_Значение',
                                    'ПИКА_Значение', 'ИИКА_Значение', 'СППКА_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ИОКА_Значение': 'Ср. Импульсивно-ответная киберагрессия',
                                    'ПОКА_Значение': 'Ср. Произвольно-ответная киберагрессия',
                                    'ПИКА_Значение': 'Ср. Произвольно-инициативная киберагрессия',
                                    'ИИКА_Значение': 'Ср. Импульсивно-инициативная киберагрессия',
                                    'СППКА_Значение': 'Ср. Суммарный показатель проявления киберагрессии',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'СППКА {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct






def processing_catq_run_antip(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 23:  # проверяем количество колонок с вопросами
            raise BadCountColumnsCATQRA

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я использую Интернет, чтобы отомстить тому, кто отправляет мне обидное сообщение',
                          'Если кто-то в Интернете пытается разозлить меня, я резко на это реагирую, размещая соответствующие тексты и репосты в ответ',
                          'Если кто-то насмехается надо мной в социальных сетях, я расстраиваюсь и сразу же пишу в ответ плохое сообщение',
                          'Если кто-то пытается унижать меня в онлайн, я отвечаю тем же',
                          'Если кто-то пишет мне что-то обидное в сети, я сразу же отправляю негативное сообщение в ответ',
                          'Если кто-то критикует меня в онлайн-сообщениях или репостах, я часто реагирую агрессивно, не думая о последствиях',
                          'Если бы кто-то причинял мне вред в онлайн-переписках, я бы не сразу стал отвечать',
                          'Если кто-то попытается обидеть меня в чате, я отвечу ему в удобное для меня время',
                          'Я часто возвращаюсь к переписке с теми, кто высмеивает меня в Интернете, я много думаю об этом и переживаю',
                          'Когда я злюсь на кого-то, я обдумываю план мести в Интернете',

                          'Если бы я хотел отомстить кому-то, я бы воспользовался социальными сетями в Интернете, планируя свои действия',
                          'Если я вижу неприятное сообщение обо мне в сети, я расстраиваюсь и долго вынашиваю план как бы мне поквитаться с обидчиком',
                          'Если мне кто-то не нравится, я воспользуюсь социальными сетями, чтобы настроить других против него',
                          'Иногда я объединяюсь с друзьями, чтобы над кем-то поиздеваться в онлайн',
                          'Иногда мне нравится унижать других людей в онлайн-переписках',
                          'Когда мне не нравится человек, я могу использовать злостные переписки в чате, делая все возможное, чтобы он не чувствовал себя частью нашей группы',
                          'Я могу использовать фэйковую страницу в Интернете, чтобы разрушить чужую дружбу',
                          'Я иногда способен кого-то публично унизить, переписываясь в чате',
                          'Мне весело обсуждать кого-то в Интернете, а другим кажется, что я злобно высмеиваю кого-то',
                          'Я могу высмеивать незнакомых мне людей в Интернете, не переживая за последствия',
                          'Если я веселюсь и шучу в Интернете, я не думаю, что мои шутки могут кому-то сделать больно',
                          'Я постоянно раздражаю людей в онлайн-переписках, считая это забавным',
                          'Шутить онлайн так весело, что меня не беспокоит, могу ли я кого-нибудь обидеть своими шутками или нет',
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
            raise BadOrderCATQRA

        # словарь для замены слов на числа
        dct_replace_value = {'точно не про меня': 4,
                             'скорее не про меня': 3,
                             'скорее про меня': 2,
                             'точно про меня': 1,
                             }
        valid_values = [1, 2, 3, 4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(19):
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
            raise BadValueCATQRA

        base_df['ИОКА_Значение'] = answers_df.apply(calc_value_ioka, axis=1)
        base_df['ПОКА_Значение'] = answers_df.apply(calc_value_poka, axis=1)
        base_df['ПИКА_Значение'] = answers_df.apply(calc_value_pika, axis=1)
        base_df['ИИКА_Значение'] = answers_df.apply(calc_value_iika, axis=1)
        base_df['СППКА_Значение'] = answers_df.sum(axis=1)
        base_df['СППКА_Диапазон'] = base_df['СППКА_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ОТКАРА_ИОКА_Значение'] = base_df['ИОКА_Значение']
        part_df['ОТКАРА_ПОКА_Значение'] = base_df['ПОКА_Значение']
        part_df['ОТКАРА_ПИКА_Значение'] = base_df['ПИКА_Значение']
        part_df['ОТКАРА_ИИКА_Значение'] = base_df['ИИКА_Значение']

        part_df['ОТКАРА_СППКА_Значение'] = base_df['СППКА_Значение']
        part_df['ОТКАРА_СППКА_Диапазон'] = base_df['СППКА_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='СППКА_Значение', ascending=True, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'СППКА_Значение': 'СППКА_Диапазон',
                        }

        dct_rename_svod_sub = {'СППКА_Значение': 'Диапазон Суммарный показатель проявления киберагрессии (бо́льшее значение по шкале означает меньшую степень проявления агрессии)',
                               }

        lst_sub = ['71-92', '47-70', '34-46', '23-33']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ИОКА_Значение'].mean(), 2)
        avg_o = round(base_df['ПОКА_Значение'].mean(), 2)
        avg_ruvs = round(base_df['ПИКА_Значение'].mean(), 2)
        avg_iika = round(base_df['ИИКА_Значение'].mean(), 2)

        avg_psp = round(base_df['СППКА_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Импульсивно-ответная киберагрессия': avg_vcha,
                   'Среднее значение шкалы Произвольно-ответная киберагрессия': avg_o,
                   'Среднее значение шкалы Произвольно-инициативная киберагрессия': avg_ruvs,
                   'Среднее значение шкалы Импульсивно-инициативная киберагрессия': avg_iika,

                   'Среднее значение Суммарный показатель проявления киберагрессии': avg_psp,
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

        dct_prefix = {'СППКА_Диапазон': 'СППКА',
                      }

        out_dct = create_list_on_level_catq(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_catq_run_antip(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderCATQRA:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Типология киберагрессии, CATQ Антипина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueCATQRA:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Типология киберагрессии, CATQ Антипина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsCATQRA:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник Типология киберагрессии, CATQ Антипина\n'
                             f'Должно быть 23 колонки с ответами')






