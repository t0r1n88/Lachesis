"""
Скрипт для обработки результатов Опросник перфекционизма Гаранян, Холмогорова, Юдеева
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod,create_list_on_level

class BadOrderOPGHU(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOPGHU(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOPGHU(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 18
    """
    pass

def calc_level_ip(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<=value <= 18:
        return f'0-18'
    elif 19<= value<= 37:
        return '19-37'
    elif 38<= value<= 56:
        return '38-56'
    else:
        return f'57-72'


def calc_level_sub(value,quantity):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """

    result =round((value / quantity) * 100)

    if 0<= result <= 24:
        return f'0-24%'
    elif 25 <= result <= 49:
        return f'25-49%'
    elif 50 <= result <= 74:
        return f'50-74%'
    else:
        return f'75-100%'



def calc_value_oos(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,2,3,6,8,9,14]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward

def calc_value_vs(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [10,12,16,17,18]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward


def calc_value_ns(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,5,7,11,13,15]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward


def create_result_op_garanyan(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_l = ['0-18', '19-37', '38-56', '57-72']

    lst_reindex_one_level_l_cols = lst_svod_cols.copy()
    lst_reindex_one_level_l_cols.extend(['0-18', '19-37', '38-56', '57-72',
                                       'Итого'])  # Основная шкала

    # Ложь
    svod_count_one_level_l_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИП_Значение',
                                                 'ИП_Диапазон',
                                                 lst_reindex_one_level_l_cols, lst_l)

    lst_level = ['0-24%', '25-49%', '50-74%', '75-100%']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['0-24%', '25-49%', '50-74%', '75-100%',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_oos_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ООС_Значение',
                                                 'ООС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_vs_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ВС_Значение',
                                                 'ВС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_ns_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'НС_Значение',
                                                 'НС_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ИП_Значение',
                                              'ООС_Значение',
                                              'ВС_Значение',
                                              'НС_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ИП_Значение',
                            'ООС_Значение',
                            'ВС_Значение',
                            'НС_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                            'ООС_Значение': 'Ср. Озабоченность оценками со стороны других',
                            'ВС_Значение': 'Ср. Высокие стандарты',
                            'НС_Значение': 'Ср. Негативное селектирование',
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
                    f'ИП {out_name}': svod_count_one_level_l_df,
                    f'ООС {out_name}': svod_count_one_level_oos_df,
                    f'ВС {out_name}': svod_count_one_level_vs_df,
                    f'НС {out_name}': svod_count_one_level_ns_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_l_cols = [lst_svod_cols[idx], '0-18', '19-37', '38-56', '57-72',
                                             'Итого']
            # Ложь
            svod_count_column_level_l_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'ИП_Значение',
                                                         'ИП_Диапазон',
                                                         lst_reindex_column_level_l_cols, lst_l)

            lst_reindex_column_level_cols = [lst_svod_cols[idx], '0-24%', '25-49%', '50-74%', '75-100%',
                                             'Итого']

            # АД
            svod_count_column_level_oos_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                           'ООС_Значение',
                                                           'ООС_Диапазон',
                                                           lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_vs_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'ВС_Значение',
                                                          'ВС_Диапазон',
                                                          lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_ns_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'НС_Значение',
                                                          'НС_Диапазон',
                                                          lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ИП_Значение',
                                                      'ООС_Значение',
                                                      'ВС_Значение',
                                                      'НС_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИП_Значение',
                                    'ООС_Значение',
                                    'ВС_Значение',
                                    'НС_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ИП_Значение': 'Ср. Интегральный показатель',
                                    'ООС_Значение': 'Ср. Озабоченность оценками со стороны других',
                                    'ВС_Значение': 'Ср. Высокие стандарты',
                                    'НС_Значение': 'Ср. Негативное селектирование',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИП {name_column}': svod_count_column_level_l_df,
                            f'ООС {name_column}': svod_count_column_level_oos_df,
                            f'ВС {name_column}': svod_count_column_level_vs_df,
                            f'НС {name_column}': svod_count_column_level_ns_df,
                            })
        return out_dct
















def processing_op_ghu(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        count_descr_cols = base_df.shape[1]  # количество анкетных колонок
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 18:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOPGHU

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Когда меня хвалят, мне кажется, что я произвожу лучшее впечатление, чем я есть на самом деле',
                          'Когда люди хвалят меня за что-либо выполненное мною, я боюсь, что не смогу в будущем оправдывать их ожидания',
                          'Я опасаюсь, что важные для меня люди могут обнаружить, что я менее способный, чем они думали обо мне',
                          'Я чаще вспоминаю случаи, в которых я проявил себя не лучшим образом, чем эпизоды, в которых я был на высоте',
                          'Я редко выполняю разные виды деятельности настолько хорошо, насколько мне хотелось бы',
                          'Мне часто кажется, что многие люди справляются с работой лучше, чем я',
                          'Когда я задумываюсь о своей жизни, мне кажется, что я достиг очень немногого',
                          'Когда я добиваюсь хорошего результата в чем-либо, у меня возникают сомнения, смогу ли я повторить его',
                          'Я часто сравниваю не в свою пользу мои способности со способностями окружающих и думаю, что они умнее и удачливей меня',
                          'Я недоволен собой, если я не достиг максимально хорошего результата, возможного в данном виде деятельности',

                          'После какого-либо не слишком удачного контакта я страшно расстраиваюсь и потом неделями все перебираю, что я сказал или сделал не так',
                          'Я никогда не останавливаюсь на достигнутом, добившись чего-то, сразу ставлю себе новую цель',
                          'Если приложенные мною в какой-либо области усилия не приводят к ощутимому в реальной жизни результату, то я считаю, что это время потрачено зря, даже если получал в то время удовольствие',
                          'Творения других людей (книги, фильмы, какие-то другие полученные ими результаты) часто служат мне напоминанием о том, как я мало достиг',
                          'Я часто терзаюсь мыслями о собственном несовершенстве',
                          'В своей работе я ориентируюсь на самые высокие стандарты',
                          'За какое бы дело я ни брался, меня не устраивает средний результат',
                          'В своих жизненных целях и задачах я ориентируюсь на людей, способных и многого достигших'
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
            raise BadOrderOPGHU

            # словарь для замены слов на числа
        dct_replace_value = {'безусловно, нет': 0,
                             'пожалуй, нет': 1,
                             'пожалуй, да': 3,
                             'безусловно, да': 4,
                             }
        valid_values = [0,1,3,4]

        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(18):
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
            raise BadValueOPGHU

        base_df['ИП_Значение'] = answers_df.sum(axis=1)
        base_df['ИП_Диапазон'] = base_df['ИП_Значение'].apply(calc_level_ip)

        base_df['ООС_Значение'] = answers_df.apply(calc_value_oos, axis=1)
        base_df['ООС_Диапазон'] = base_df['ООС_Значение'].apply(lambda x: calc_level_sub(x, 28))

        base_df['ВС_Значение'] = answers_df.apply(calc_value_vs, axis=1)
        base_df['ВС_Диапазон'] = base_df['ВС_Значение'].apply(lambda x: calc_level_sub(x, 20))

        base_df['НС_Значение'] = answers_df.apply(calc_value_ns, axis=1)
        base_df['НС_Диапазон'] = base_df['НС_Значение'].apply(lambda x: calc_level_sub(x, 24))

        # Создаем датафрейм для создания части в общий датафрейм
        temp_df = base_df.copy()  # делаем копию
        part_df = temp_df.iloc[:, count_descr_cols:]
        part_df = part_df.add_prefix('ОПГХЮ_')

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИП_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_l = {'ИП_Значение': 'ИП_Диапазон',
                      }

        dct_rename_svod_l = {'ИП_Значение': 'Интегральный показатель',
                             }

        lst_l = ['0-18', '19-37', '38-56', '57-72']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_l)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ООС_Значение': 'ООС_Диапазон',
                        'ВС_Значение': 'ВС_Диапазон',
                        'НС_Значение': 'НС_Диапазон',
                        }

        dct_rename_svod_sub = {'ООС_Значение': 'Озабоченность оценками со стороны других',
                               'ВС_Значение': 'Высокие стандарты',
                               'НС_Значение': 'Негативное селектирование',
                               }

        lst_sub = ['0-24%', '25-49%', '50-74%', '75-100%']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_ip = round(base_df['ИП_Значение'].mean(), 2)
        avg_oos = round(base_df['ООС_Значение'].mean(), 2)
        avg_vs = round(base_df['ВС_Значение'].mean(), 2)
        avg_ns = round(base_df['НС_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Интегрального показателя': avg_ip,
                   'Среднее значение шкалы Озабоченность оценками со стороны других': avg_oos,
                   'Среднее значение шкалы Высокие стандарты': avg_vs,
                   'Среднее значение шкалы Негативное селектирование': avg_ns,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод ИП': base_svod_l_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_l = {
            'ИП_Диапазон': 'ИП',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_l, dct_l)

        dct_prefix = {
            'ООС_Диапазон': 'ООС',
            'ВС_Диапазон': 'ВС',
            'НС_Диапазон': 'НС',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_op_garanyan(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderOPGHU:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник перфекционизма Гаранян, Холмогорова, Юдеева обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOPGHU:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник перфекционизма Гаранян, Холмогорова, Юдеева обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOPGHU:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник перфекционизма Гаранян, Холмогорова, Юдеева\n'
                             f'Должно быть 18 колонок с ответами')











