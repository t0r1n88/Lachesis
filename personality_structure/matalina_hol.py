"""
Скрипт для обработки результатов Экспресс-диагностика характерологических особенностей личности Маталина
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderHOLM(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueHOLM(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsHOLM(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 60
    """
    pass


def calc_value_a(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,3,9,11,14,17,19,22,25,27,30,35,38,41,43,46,49,53,57,
              6,33,51,55,59]
    lst_neg = [6,33,51,55,59]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward

def calc_value_n(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,5,7,10,13,15,18,21,23,26,29,
              31,34,37,39,42,45,47,50,52,54,56,58,60]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 'да':
                value_forward += 1

    return value_forward


def calc_value_l(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [8,16,24,28,36,44,
              4,12,20,32,40,48]
    lst_neg = [4,12,20,32,40,48]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                if value == 'да':
                    value_forward += 1
            else:
                if value == 'нет':
                    value_forward += 1

    return value_forward

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<=value <= 5:
        return f'0-5'
    elif 6<= value<= 12:
        return '6-12'
    elif 13<= value<= 18:
        return '13-18'
    else:
        return f'19-24'

def calc_level_l(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<=value <= 2:
        return f'0-2'
    elif 3<= value<= 5:
        return '3-5'
    elif 6<= value<= 8:
        return '6-8'
    else:
        return f'9-12'


def create_result_hol_matalina(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_l = ['0-2', '3-5', '6-8','9-12']

    lst_reindex_one_level_l_cols = lst_svod_cols.copy()
    lst_reindex_one_level_l_cols.extend(['0-2', '3-5', '6-8','9-12',
                                       'Итого'])  # Основная шкала

    # Ложь
    svod_count_one_level_l_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Л_Значение',
                                                 'Л_Диапазон',
                                                 lst_reindex_one_level_l_cols, lst_l)

    lst_level = ['0-5', '6-12', '13-18','19-24']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['0-5', '6-12', '13-18','19-24',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_a_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Э_Значение',
                                                 'Э_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_n_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Н_Значение',
                                                 'Н_Диапазон',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Л_Значение',
                                              'Э_Значение',
                                              'Н_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Л_Значение',
                            'Э_Значение',
                            'Н_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Л_Значение': 'Ср. Ложь',
                            'Э_Значение': 'Ср. Экстраверсия',
                            'Н_Значение': 'Ср. Нейротизм',
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
                    f'Л {out_name}': svod_count_one_level_l_df,
                    f'Э {out_name}': svod_count_one_level_a_df,
                    f'Н {out_name}': svod_count_one_level_n_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_l_cols = [lst_svod_cols[idx], '0-2', '3-5', '6-8','9-12',
                                             'Итого']
            # Ложь
            svod_count_column_level_l_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'Л_Значение',
                                                         'Л_Диапазон',
                                                         lst_reindex_column_level_l_cols, lst_l)

            lst_reindex_column_level_cols = [lst_svod_cols[idx], '0-5', '6-12', '13-18','19-24',
                                             'Итого']

            # АД
            svod_count_column_level_a_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Э_Значение',
                                                            'Э_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_n_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Н_Значение',
                                                            'Н_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['Л_Значение',
                                                      'Э_Значение',
                                                      'Н_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Л_Значение',
                                    'Э_Значение',
                                    'Н_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Л_Значение': 'Ср. Ложь',
                                    'Э_Значение': 'Ср. Экстраверсия',
                                    'Н_Значение': 'Ср. Нейротизм',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Л {name_column}': svod_count_column_level_l_df,
                            f'Э {name_column}': svod_count_column_level_a_df,
                            f'Н {name_column}': svod_count_column_level_n_df,
                                })
        return out_dct












def processing_hol_mat(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 60:  # проверяем количество колонок с вопросами
            raise BadCountColumnsHOLM

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Любишь ли ты шум и суету возле себя?',
                          'Часто ли ты нуждаешься в друзьях, которые могли бы тебя поддержать?',
                          'Ты всегда находишь быстрый ответ, когда тебя о чем-нибудь просят?',
                          'Бывает ли так, что ты раздражен чем-нибудь?',
                          'Часто ли у тебя меняется настроение?',
                          'Верно ли, что тебе легче и приятнее с книгами, чем с ребятами?',
                          'Часто ли тебе мешают уснуть разные мысли?',
                          'Ты всегда делаешь так, как тебе говорят?',
                          'Любишь ли ты подшучивать над кем-нибудь?',
                          'Ты когда-нибудь чувствовал себя несчастным, хотя для этого не было настоящей причины?',

                          'Можешь ли ты сказать о себе, что ты веселый, живой человек?',
                          'Ты когда-нибудь нарушал правила поведения в школе?',
                          'Верно ли, что ты часто раздражен чем-нибудь?',
                          'Нравится ли тебе всё делать в быстром темпе? (если же, наоборот, склонен к неторопливости, ответь «нет»).',
                          'Ты переживаешь из-за всяких страшных событий, которые чуть было не произошли, хотя все кончилось хорошо?',
                          'Тебе можно доверить любую тайну?',
                          'Можешь ли ты без особого труда внести оживление в скучную компанию сверстников?',
                          'Бывает ли так, что у тебя без всякой причины (физические нагрузки) сильно бьется сердце?',
                          'Делаешь ли ты обычно первый шаг для того, чтобы подружиться с кем-нибудь?',
                          'Ты когда-нибудь говорил неправду?',

                          'Ты легко расстраиваешься, когда критикуют тебя и твою работу?',
                          'Ты часто шутишь и рассказываешь смешные истории своим друзьям?',
                          'Ты часто чувствуешь себя усталым?',
                          'Ты всегда сначала делаешь уроки, а всё остальное потом?',
                          'Ты обычно весел и всем доволен?',
                          'Обидчив ли ты?',
                          'Ты очень любишь общаться с другими ребятами?',
                          'Всегда ли ты выполняешь просьбы родных о помощи по хозяйству?',
                          'У тебя бывает головокружение?',
                          'Бывает ли так, что твои действия и поступки ставят других людей в неловкое положение?',

                          'Ты часто чувствуешь, что тебе что-нибудь надоело?',
                          'Любишь ли ты иногда похвастаться?',
                          'Ты чаще всего сидишь и молчишь, когда попадаешь в общество незнакомых людей?',
                          'Волнуешься ли ты иногда так, что не можешь усидеть на месте?',
                          'Ты обычно быстро принимаешь решения?',
                          'Ты никогда не шумишь в классе, даже когда нет учителя?',
                          'Тебе часто снятся страшные сны?',
                          'Можешь ли ты дать волю чувствам и повеселиться в обществе друзей?',
                          'Тебя легко огорчить?',
                          'Случалось ли тебе плохо говорить о ком-нибудь?',

                          'Верно ли, что ты обычно говоришь и действуешь быстро, не задерживаясь особенно на обдумывание?',
                          'Если оказываешься в глупом положении, то потом долго переживаешь?',
                          'Тебе очень нравятся шумные и веселые игры?',
                          'Ты всегда ешь то, что тебе подают?',
                          'Тебе трудно ответить «нет», когда тебя о чем-нибудь просят?',
                          'Ты любишь часто ходить в гости?',
                          'Бывают ли такие моменты, когда тебе не хочется жить?',
                          'Был ли ты когда-нибудь груб с родителями?',
                          'Считают ли тебя ребята веселым и живым человеком?',
                          'Ты часто отвлекаешься, когда делаешь уроки?',

                          'Ты чаще сидишь и смотришь, чем принимаешь активное участие в общем веселье?',
                          'Тебе обычно бывает трудно уснуть из-за разных мыслей?',
                          'Бываешь ли ты совершенно уверен, что сможешь справиться с делом, которое должен выполнить?',
                          'Бывает ли, что ты чувствуешь себя одиноким?',
                          'Ты стесняешься заговорить первым с новыми людьми?',
                          'Ты часто спохватываешься, когда уже поздно что-нибудь исправить?',
                          'Когда кто-нибудь из ребят кричит на тебя, ты тоже кричишь в ответ?',
                          'Бывает ли так, что ты иногда чувствуешь себя веселым или печальным без всякой причины?',
                          'Ты считаешь, что трудно получить настоящее удовольствие от оживленной компании сверстников?',
                          'Тебе часто приходится волноваться из-за того, что ты сделал что-нибудь, не подумав?',
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
            raise BadOrderHOLM

        valid_values = ['да','нет']
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(60):
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
            raise BadValueHOLM

        base_df['Л_Значение'] = answers_df.apply(calc_value_l, axis=1)
        base_df['Л_Диапазон'] = base_df['Л_Значение'].apply(calc_level_l)

        base_df['Э_Значение'] = answers_df.apply(calc_value_a, axis=1)
        base_df['Э_Диапазон'] = base_df['Э_Значение'].apply(calc_level)

        base_df['Н_Значение'] = answers_df.apply(calc_value_n, axis=1)
        base_df['Н_Диапазон'] = base_df['Н_Значение'].apply(calc_level)



        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ХОЛМ_Л_Значение'] = base_df['Л_Значение']
        part_df['ХОЛМ_Л_Диапазон'] = base_df['Л_Диапазон']

        part_df['ХОЛМ_Э_Значение'] = base_df['Э_Значение']
        part_df['ХОЛМ_Э_Диапазон'] = base_df['Э_Диапазон']

        part_df['ХОЛМ_Н_Значение'] = base_df['Н_Значение']
        part_df['ХОЛМ_Н_Диапазон'] = base_df['Н_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Э_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_l = {'Л_Значение': 'Л_Диапазон',
                        }

        dct_rename_svod_l = {'Л_Значение': 'Ложь',
                               }

        lst_l = ['0-2', '3-5', '6-8','9-12']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_l)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Э_Значение': 'Э_Диапазон',
                        'Н_Значение': 'Н_Диапазон',
                        }

        dct_rename_svod_sub = {'Э_Значение': 'Экстраверсия"',
                               'Н_Значение': 'Нейротизм',
                               }

        lst_sub = ['0-5', '6-12', '13-18','19-24']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['Л_Значение'].mean(), 2)
        avg_o = round(base_df['Э_Значение'].mean(), 2)
        avg_ruvs = round(base_df['Н_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Ложь': avg_vcha,
                   'Среднее значение шкалы Экстраверсия': avg_o,
                   'Среднее значение шкалы Нейротизм': avg_ruvs,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод Ложь': base_svod_l_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_l = {
                      'Л_Диапазон': 'Л',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_l, dct_l)


        dct_prefix = {
                      'Э_Диапазон': 'Э',
                      'Н_Диапазон': 'Н',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)
        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_hol_matalina(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderHOLM:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Экспресс-диагностика характерологических особенностей личности Маталина обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueHOLM:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Экспресс-диагностика характерологических особенностей личности Маталина обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsHOLM:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Экспресс-диагностика характерологических особенностей личности Маталина\n'
                             f'Должно быть 60 колонок с ответами')



