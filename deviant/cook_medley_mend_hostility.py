"""
Скрипт для обработки результатов теста Шкала враждебности Кука-Медлей Менджерицкая
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_list_on_level,create_union_svod


class BadOrderCMMH(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueCMMH(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsCMMH(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 27
    """
    pass



def calc_value_cyn(row):
    """
    Функция для подсчета значения шкалы Цинизм
    :return: число
    """
    lst_pr = [1,2,3,4,6,7,9,10,11,12,19,20,22]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level_cyn(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 25:
        return 'низкий показатель'
    elif 26 <= value <= 40:
        return 'ближе к низкому'
    elif 41 <= value <= 65:
        return 'ближе к высокому'
    else:
        return 'высокий показатель'


def calc_value_agr(row):
    """
    Функция для подсчета значения шкалы Агрессивность
    :return: число
    """
    lst_pr = [5,14,15,16,21,23,24,26,27]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level_agr(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 15:
        return 'низкий показатель'
    elif 16 <= value <= 30:
        return 'ближе к низкому'
    elif 31 <= value <= 45:
        return 'ближе к высокому'
    else:
        return 'высокий показатель'

def calc_value_hos(row):
    """
    Функция для подсчета значения шкалы Враждебность
    :return: число
    """
    lst_pr = [8,13,17,18,25]
    value_forward = 0  # результат
    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward

def calc_level_hos(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1 <= value <= 10:
        return 'низкий показатель'
    elif 11 <= value <= 18:
        return 'ближе к низкому'
    elif 19 <= value <= 25:
        return 'ближе к высокому'
    else:
        return 'высокий показатель'


def create_list_on_level_cmmh(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'низкий показатель':
                    level = 'низкий'
                elif level == 'высокий показатель':
                    level = 'высокий'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct

def create_result_cook_medley_mend_hostility(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий показатель', 'ближе к низкому', 'ближе к высокому', 'высокий показатель']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['низкий показатель', 'ближе к низкому', 'ближе к высокому', 'высокий показатель',
                                       'Итого'])  # Основная шкала

    # Цинизм
    svod_count_one_level_cyn_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'Цинизм_Значение',
                                                  'Цинизм_Уровень',
                                                  lst_reindex_one_level_cols, lst_level)

    # Агрессивность
    svod_count_one_level_agr_df = calc_count_scale(base_df, lst_svod_cols,
                                                      'Агрессивность_Значение',
                                                      'Агрессивность_Уровень',
                                                      lst_reindex_one_level_cols, lst_level)

    # Враждебность
    svod_count_one_level_hos_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'Враждебность_Значение',
                                                   'Враждебность_Уровень',
                                                   lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Цинизм_Значение',
                                              'Агрессивность_Значение',
                                              'Враждебность_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Цинизм_Значение', 'Агрессивность_Значение',
                            'Враждебность_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Цинизм_Значение': 'Ср. Цинизм',
                            'Агрессивность_Значение': 'Ср. Агрессивность',
                            'Враждебность_Значение': 'Ср. Враждебность',
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
                    f'Ц {out_name}': svod_count_one_level_cyn_df,
                    f'А {out_name}': svod_count_one_level_agr_df,
                    f'В {out_name}': svod_count_one_level_hos_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий показатель', 'ближе к низкому', 'ближе к высокому', 'высокий показатель',
                                                  'Итого']

            # Цинизм
            svod_count_column_level_cyn_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'Цинизм_Значение',
                                                             'Цинизм_Уровень',
                                                             lst_reindex_column_level_cols, lst_level)

            # Агрессивность
            svod_count_column_level_agr_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                                 'Агрессивность_Значение',
                                                                 'Агрессивность_Уровень',
                                                                 lst_reindex_column_level_cols, lst_level)

            # Враждебность
            svod_count_column_level_hos_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                              'Враждебность_Значение',
                                                              'Враждебность_Уровень',
                                                              lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Цинизм_Значение',
                                                         'Агрессивность_Значение',
                                                         'Враждебность_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Цинизм_Значение', 'Агрессивность_Значение',
                                    'Враждебность_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Цинизм_Значение': 'Ср. Цинизм',
                                    'Агрессивность_Значение': 'Ср. Агрессивность',
                                    'Враждебность_Значение': 'Ср. Враждебность',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Ц {name_column}': svod_count_column_level_cyn_df,
                            f'А {name_column}': svod_count_column_level_agr_df,
                            f'В {name_column}': svod_count_column_level_hos_df,
                            })
        return out_dct







def processing_cook_medley_mend_hostility(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 27:  # проверяем количество колонок с вопросами
            raise BadCountColumnsCMMH

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я часто встречаю людей, называющих себя экспертами, хотя они таковыми не являются',
                          'Мне часто приходилось выполнять указания людей, которые знали меньше, чем я',
                          'Многих людей можно обвинить в аморальном поведении',
                          'Многие люди преувеличивают тяжесть своих неудач, чтобы получить сочувствие и помощь',
                          'Временами мне приходилось грубить людям, которые вели себя невежливо по отношению ко мне и действовали мне на нервы',
                          'Большинство людей заводят друзей, потому что друзья могут быть полезны',
                          'Часто необходимо затратить много усилий, чтобы убедить других в своей правоте',
                          'Люди часто разочаровывали меня',
                          'Обычно люди требуют большего уважения своих прав, чем стремятся уважать права других',
                          'Большинство людей не нарушают закон, потому что боятся быть пойманными',
                          'Зачастую люди прибегают к нечестным способам, чтобы не потерять возможной выгоды',
                          'Я считаю, что многие люди используют ложь, для того чтобы двигаться дальше',
                          'Существуют люди, которые настолько мне неприятны, что я невольно радуюсь, когда их постигают неудачи',
                          'Я часто могу отойти от своих принципов, чтобы превзойти своего противника',
                          'Если люди поступают со мной плохо, я обязательно отвечаю им тем же, хотя бы из принципа',
                          'Как правило, я отчаянно отстаиваю свою точку зрения',
                          'Некоторые члены моей семьи имеют привычки, которые меня раздражают',
                          'Я не всегда легко соглашаюсь с другими',
                          'Никого никогда не заботит то, что с тобой происходит',
                          'Более безопасно никому не верить',
                          'Я могу вести себя дружелюбно с людьми, которые, по моему мнению, поступают неверно',
                          'Многие люди избегают ситуаций, в которых они должны помогать другим',
                          'Я не осуждаю людей за то, что они стремятся присвоить себе все, что только можно',
                          'Я не виню человека за то, что он в своих целях использует других людей, позволяющих ему это делать',
                          'Меня раздражает, когда другие отрывают меня от дела',
                          'Мне бы определенно понравилось, если бы преступника наказали его же преступлением',
                          'Я не стремлюсь скрыть плохое мнение о других людях',
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
            raise BadOrderCMMH

        # словарь для замены слов на числа
        dct_replace_value = {'обычно': 6,
                             'часто': 5,
                             'иногда': 4,
                             'случайно': 3,
                             'редко': 2,
                             'никогда': 1,
                             }

        valid_values = [1, 2, 3, 4, 5, 6]
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
            raise BadValueCMMH


        base_df['Цинизм_Значение'] = answers_df.apply(calc_value_cyn, axis=1)
        base_df['Цинизм_Уровень'] = base_df['Цинизм_Значение'].apply(calc_level_cyn)

        base_df['Агрессивность_Значение'] = answers_df.apply(calc_value_agr, axis=1)
        base_df['Агрессивность_Уровень'] = base_df['Агрессивность_Значение'].apply(calc_level_agr)

        base_df['Враждебность_Значение'] = answers_df.apply(calc_value_hos, axis=1)
        base_df['Враждебность_Уровень'] = base_df['Враждебность_Значение'].apply(calc_level_hos)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ШВКМ_М_Ц_Значение'] = base_df['Цинизм_Значение']
        part_df['ШВКМ_М_Ц_Уровень'] = base_df['Цинизм_Уровень']

        part_df['ШВКМ_М_А_Значение'] = base_df['Агрессивность_Значение']
        part_df['ШВКМ_М_А_Уровень'] = base_df['Агрессивность_Уровень']

        part_df['ШВКМ_М_В_Значение'] = base_df['Враждебность_Значение']
        part_df['ШВКМ_М_В_Уровень'] = base_df['Враждебность_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки
        base_df.sort_values(by='Цинизм_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Цинизм_Значение': 'Цинизм_Уровень',
                        'Агрессивность_Значение': 'Агрессивность_Уровень',
                        'Враждебность_Значение': 'Враждебность_Уровень',
                        }

        dct_rename_svod_sub = {'Цинизм_Значение': 'Цинизм',
                               'Агрессивность_Значение': 'Агрессивность',
                               'Враждебность_Значение': 'Враждебность',
                               }

        lst_sub = ['низкий показатель', 'ближе к низкому','ближе к высокому', 'высокий показатель']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # считаем среднее значение по шкалам
        avg_cyn = round(base_df['Цинизм_Значение'].mean(), 2)
        avg_agr = round(base_df['Агрессивность_Значение'].mean(), 2)
        avg_hos = round(base_df['Враждебность_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Цинизм': avg_cyn,
                   'Среднее значение шкалы Агрессивность': avg_agr,
                   'Среднее значение шкалы Враждебность': avg_hos,
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

        dct_prefix = {'Цинизм_Уровень': 'Ц',
                      'Агрессивность_Уровень': 'А',
                      'Враждебность_Уровень': 'В',
                      }

        out_dct = create_list_on_level_cmmh(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_cook_medley_mend_hostility(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df



    except BadOrderCMMH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала враждебности Кука-Медлей Менджерицкая обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueCMMH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала враждебности Кука-Медлей Менджерицкая обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsCMMH:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала враждебности Кука-Медлей Менджерицкая\n'
                             f'Должно быть 27 колонок с ответами')










