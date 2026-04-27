"""
Скрипт для обработки результатов Опросник Контроль поведения Сергиенко, Виленская, Ветрова
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOKPSVV(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOKPSVV(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOKPSVV(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 27
    """
    pass


def calc_level_okp(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1<= value <= 30:
        return f'1-30'
    elif 31 <= value <= 60:
        return f'31-60'
    elif 61 <= value <= 90:
        return f'61-90'
    elif 91 <= value <= 115:
        return f'91-115'
    else:
        return f'116-135'


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1<= value <= 9:
        return f'1-9'
    elif 10 <= value <= 19:
        return f'10-19'
    elif 20 <= value <= 29:
        return f'20-29'
    elif 30 <= value <= 39:
        return f'30-39'
    else:
        return f'40-45'



def calc_value_kk(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,6,8,10,14,19,21,24,26]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward

def calc_value_ak(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,4,7,11,13,15,17,22,25]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward

def calc_value_vk(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,5,9,12,16,18,20,23,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward



def create_result_okp_sergienko(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_l = ['1-30', '31-60', '61-90', '91-115','116-135']

    lst_reindex_one_level_l_cols = lst_svod_cols.copy()
    lst_reindex_one_level_l_cols.extend(['1-30', '31-60', '61-90', '91-115','116-135',
                                         'Итого'])  # Основная шкала

    # ИП
    svod_count_one_level_l_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ОКП_Значение',
                                                 'ОКП_Диапазон',
                                                 lst_reindex_one_level_l_cols, lst_l)

    lst_level = ['1-9', '10-19', '20-29', '30-39','40-45']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['1-9', '10-19', '20-29', '30-39','40-45',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'КК_Значение',
                                                 'КК_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_i_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ЭК_Значение',
                                                 'ЭК_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_ap_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ВК_Значение',
                                                 'ВК_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)


    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ОКП_Значение',
                                              'КК_Значение',
                                              'ЭК_Значение',
                                              'ВК_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ОКП_Значение',
                            'КК_Значение',
                            'ЭК_Значение',
                            'ВК_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ОКП_Значение': 'Ср. Общий контроль поведения',
                            'КК_Значение': 'Ср. Когнитивный контроль',
                            'ЭК_Значение': 'Ср. Эмоциональный контроль',
                            'ВК_Значение': 'Ср. Волевой контроль',
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
                    f'ОКП {out_name}': svod_count_one_level_l_df,
                    f'КК {out_name}': svod_count_one_level_s_df,
                    f'ЭК {out_name}': svod_count_one_level_i_df,
                    f'ВК {out_name}': svod_count_one_level_ap_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_l_cols = [lst_svod_cols[idx], '1-30', '31-60', '61-90', '91-115','116-135',
                                             'Итого']

            # Ложь
            svod_count_column_level_l_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'ОКП_Значение',
                                                         'ОКП_Диапазон',
                                                         lst_reindex_column_level_l_cols, lst_l)

            lst_reindex_column_level_cols = [lst_svod_cols[idx], '1-9', '10-19', '20-29', '30-39','40-45',
                                             'Итого']

            # АД
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'КК_Значение',
                                                            'КК_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_i_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ЭК_Значение',
                                                            'ЭК_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ap_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ВК_Значение',
                                                            'ВК_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ОКП_Значение',
                                                      'КК_Значение',
                                                      'ЭК_Значение',
                                                      'ВК_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ОКП_Значение',
                                    'КК_Значение',
                                    'ЭК_Значение',
                                    'ВК_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ОКП_Значение': 'Ср. Общий контроль поведения',
                                    'КК_Значение': 'Ср. Когнитивный контроль',
                                    'ЭК_Значение': 'Ср. Эмоциональный контроль',
                                    'ВК_Значение': 'Ср. Волевой контроль',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ОКП {name_column}': svod_count_column_level_l_df,
                            f'КК {name_column}': svod_count_column_level_s_df,
                            f'ЭК {name_column}': svod_count_column_level_i_df,
                            f'ВК {name_column}': svod_count_column_level_ap_df,
                            })
        return out_dct






def processing_okp_serg(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 27:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOKPSVV

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Мне всегда понятно, какие чувства я испытываю в данный момент',
                          'Мне трудно заводить новых друзей',
                          'Мои решения больше зависят от моего настроения, чем от поставленных мной целей',
                          'Слушая музыку, стихи, рассматривая картину, я всегда понимаю, какие эмоции выражает произведение искусства',
                          'Я могу отказаться от своих целей, если сталкиваюсь с серьезными трудностями',
                          'Стремлюсь, чтобы результат в точности соответствовал моим ожиданиям',
                          'Я умею поддерживать в себе хорошее настроение',
                          'Я всегда хорошо представляю себе, что я должен получить',
                          'Я продолжаю добиваться своего, несмотря на неудачи',
                          'Меня раздражает необходимость планировать всё в мельчайших подробностях',

                          'Я понимаю причины смены настроения у окружающих',
                          'Я всегда выполняю обещанное',
                          'Если кто-то на меня обижен, я теряюсь и не знаю, как восстановить с ним хорошие отношения',
                          'Если я вижу, что задача для меня не решаема, я прекращаю попытки её решить',
                          'Если мне грустно, то это надолго',
                          'Несмотря на моё настроение, я завершу начатое дело в любом случае',
                          'Мне удается поднять настроение в компании',
                          'Меня легко отвлечь от того, чем я занят',
                          'Я лучше могу оценить свои результаты, чем другие люди',
                          'Мне часто хочется бросить то, что я делаю, если что-то не получается',

                          'Я планирую каждый свой будущий день',
                          'Мне трудно разобраться в причинах моих чувств',
                          'Я умею не отвлекаться на постороннее при достижении намеченной цели',
                          'Я тщательно планирую все, что необходимо сделать',
                          'Надо постараться, чтобы испортить мне настроение',
                          'Я делаю ошибки, потому что не сразу замечаю изменение ситуации',
                          'Я стараюсь доводить дело до конца, невзирая на препятствия',
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
            raise BadOrderOKPSVV

        # словарь для замены слов на числа
        dct_replace_value = {'это совершенно не обо мне': 1,
                             'это ко мне скорее не относится, чем относится': 2,
                             'затрудняюсь ответить': 3,
                             'это похоже на меня': 4,
                             'это точно про меня': 5,
                             }
        valid_values = [1, 2, 3, 4,5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(27):
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
            raise BadValueOKPSVV

        base_df['ОКП_Значение'] = answers_df.sum(axis=1)
        base_df['ОКП_Диапазон'] = base_df['ОКП_Значение'].apply(calc_level_okp)

        base_df['КК_Значение'] = answers_df.apply(calc_value_kk, axis=1)
        base_df['КК_Диапазон'] = base_df['КК_Значение'].apply(calc_level)

        base_df['ЭК_Значение'] = answers_df.apply(calc_value_ak, axis=1)
        base_df['ЭК_Диапазон'] = base_df['ЭК_Значение'].apply(calc_level)

        base_df['ВК_Значение'] = answers_df.apply(calc_value_vk, axis=1)
        base_df['ВК_Диапазон'] = base_df['ВК_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ОКПСВВ_ОКП_Значение'] = base_df['ОКП_Значение']
        part_df['ОКПСВВ_ОКП_Диапазон'] = base_df['ОКП_Диапазон']

        part_df['ОКПСВВ_КК_Значение'] = base_df['КК_Значение']
        part_df['ОКПСВВ_КК_Диапазон'] = base_df['КК_Диапазон']

        part_df['ОКПСВВ_ЭК_Значение'] = base_df['ЭК_Значение']
        part_df['ОКПСВВ_ЭК_Диапазон'] = base_df['ЭК_Диапазон']

        part_df['ОКПСВВ_ВК_Значение'] = base_df['ВК_Значение']
        part_df['ОКПСВВ_ВК_Диапазон'] = base_df['ВК_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ОКП_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_l = {'ОКП_Значение': 'ОКП_Диапазон',
                      }

        dct_rename_svod_l = {'ОКП_Значение': 'Общий контроль поведения',
                             }

        lst_l = ['1-30', '31-60', '61-90', '91-115','116-135']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_l)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'КК_Значение': 'КК_Диапазон',
                        'ЭК_Значение': 'ЭК_Диапазон',
                        'ВК_Значение': 'ВК_Диапазон',
                        }

        dct_rename_svod_sub = {'КК_Значение': 'Когнитивный контроль"',
                               'ЭК_Значение': 'Эмоциональный контроль',
                               'ВК_Значение': 'Волевой контроль',
                               }

        lst_sub = ['1-9', '10-19', '20-29', '30-39','40-45']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ОКП_Значение'].mean(), 2)
        avg_o = round(base_df['КК_Значение'].mean(), 2)
        avg_ruvs = round(base_df['ЭК_Значение'].mean(), 2)
        avg_ap = round(base_df['ВК_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Общий контроль поведения': avg_vcha,
                   'Среднее значение шкалы Когнитивный контроль"': avg_o,
                   'Среднее значение шкалы Эмоциональный контроль': avg_ruvs,
                   'Среднее значение шкалы Волевой контроль': avg_ap,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод ОКП': base_svod_l_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_l = {
            'ОКП_Диапазон': 'ОКП',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_l, dct_l)

        dct_prefix = {
            'КК_Диапазон': 'КК',
            'ЭК_Диапазон': 'ЭК',
            'ВК_Диапазон': 'ВК',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_okp_sergienko(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderOKPSVV:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Контроль поведения Сергиенко, Виленская, Ветрова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOKPSVV:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник Контроль поведения Сергиенко, Виленская, Ветрова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOKPSVV:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник Контроль поведения Сергиенко, Виленская, Ветрова\n'
                             f'Должно быть 27 колонок с ответами')




