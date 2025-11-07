"""
Скрипт для обработки результатов теста Шкала депрессии, тревоги и стресса, DASS-21 Адаптация А. А. Золотарева

"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod


class BadOrderDTOZ(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueDTOZ(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsDTOZ(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 21
    """
    pass


def calc_value_depress(row):
    """
    Функция для подсчета значения шкалы Депрессия
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [3,5,10,13,16,17,21]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_level_depress(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value == 0:
        return 'низкий уровень DASS'
    elif 1 <= value <= 8:
        return 'средний уровень DASS'
    else:
        return 'высокий уровень DASS'



def calc_value_anxiety(row):
    """
    Функция для подсчета значения шкалы Тревога
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [2,4,7,9,15,19,20]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_level_anxiety(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value == 0:
        return 'низкий уровень DASS'
    elif 1 <= value <= 7:
        return 'средний уровень DASS'
    else:
        return 'высокий уровень DASS'


def calc_value_stress(row):
    """
    Функция для подсчета значения шкалы Тревога
    :param row: строка с ответами
    :return: число
    """
    lst_pr = [1,6,8,11,12,14,18]

    value_forward = 0 # счетчик прямых ответов

    for idx, value in enumerate(row):
        if idx +1 in lst_pr:
            value_forward += value

    return value_forward


def calc_level_stress(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0 <= value == 1:
        return 'низкий уровень DASS'
    elif 2 <= value <= 10:
        return 'средний уровень DASS'
    else:
        return 'высокий уровень DASS'



def create_list_on_level_dass(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'низкий уровень DASS':
                    level = 'низкий'
                elif level == 'средний уровень DASS':
                    level = 'средний'
                else:
                    level = 'высокий'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct

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
                                       aggfunc=round_mean_two)
    calc_mean_df.reset_index(inplace=True)
    calc_mean_df.rename(columns={val_cat:'Среднее значение'},inplace=True)
    return calc_mean_df


def create_result_dass_twenty_one_zolotareva(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий уровень DASS','средний уровень DASS','высокий уровень DASS']
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend(['низкий уровень DASS','средний уровень DASS','высокий уровень DASS',
                               'Итого'])  # Основная шкала

    svod_count_one_dep_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Депрессия_Значение',
                                                    'Депрессия_Уровень',
                                                    lst_reindex_main_level_cols,lst_level)

    svod_count_one_anx_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Тревога_Значение',
                                                    'Тревога_Уровень',
                                                    lst_reindex_main_level_cols,lst_level)

    svod_count_one_st_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'Стресс_Значение',
                                                    'Стресс_Уровень',
                                                    lst_reindex_main_level_cols,lst_level)

    # Считаем среднее по шкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                  index=lst_svod_cols,
                                  values=['Депрессия_Значение',
                                          'Тревога_Значение',
                                          'Стресс_Значение',
                                          ],
                                  aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Депрессия_Значение',
                            'Тревога_Значение',
                            'Стресс_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Депрессия_Значение': 'Ср. Деп',
                            'Тревога_Значение': 'Ср. Тр',
                            'Стресс_Значение': 'Ср. Ст'

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

    out_dct.update({f'Деп {out_name}': svod_count_one_dep_df,
                    f'Тр {out_name}': svod_count_one_anx_df,
                    f'Ст {out_name}': svod_count_one_st_df,
                    f'Ср. {out_name}': svod_mean_one_df})

    if len(lst_svod_cols) == 1:
        return out_dct

    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий уровень DASS','средний уровень DASS','высокий уровень DASS',
                               'Итого']
            svod_count_column_dep_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Депрессия_Значение',
                                                        'Депрессия_Уровень',
                                                        lst_reindex_column_level_cols, lst_level)

            svod_count_column_anx_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                        'Тревога_Значение',
                                                        'Тревога_Уровень',
                                                        lst_reindex_column_level_cols, lst_level)

            svod_count_column_st_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                       'Стресс_Значение',
                                                       'Стресс_Уровень',
                                                       lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по шкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Депрессия_Значение',
                                                         'Тревога_Значение',
                                                         'Стресс_Значение',
                                                         ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Депрессия_Значение',
                                    'Тревога_Значение',
                                    'Стресс_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Депрессия_Значение': 'Ср. Деп',
                                    'Тревога_Значение': 'Ср. Тр',
                                    'Стресс_Значение': 'Ср. Ст'

                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Деп {name_column}': svod_count_column_dep_df,
                            f'Тр {name_column}': svod_count_column_anx_df,
                            f'Ст {name_column}': svod_count_column_st_df,
                            f'Ср. {name_column}': svod_mean_column_df})
        return out_dct





def processing_dass_twenty_one_zolotareva(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 21:  # проверяем количество колонок с вопросами
            raise BadCountColumnsDTOZ

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Мне было трудно успокоиться',
                          'Я чувствовал(а) сухость во рту',
                          'Мне кажется, что я не испытывал(а) никаких позитивных чувств',
                          'У меня были проблемы с дыханием (например, учащенное дыхание, одышка при отсутствии физической активности)',
                          'Мне было трудно проявить инициативу для того, чтобы что-то сделать',
                          'Я слишком остро реагировал(а) на некоторые ситуации',
                          'У меня была дрожь (например, в руках)',
                          'Я чувствовал(а), что трачу много нервов',
                          'Меня тревожили ситуации, в которых я мог(ла) запаниковать и выглядеть глупо',
                          'Я чувствовал(а), что мне не на что надеяться',
                          'Я обнаруживал(а) себя взволнованным(ой)',
                          'Мне было трудно расслабиться',
                          'Я чувствовал(а) себя унылым(ой) и подавленным(ой)',
                          'Я был(а) нетерпим(а) ко всему, что мешало мне в моих делах',
                          'Я был(а) близок(ка) к панике',
                          'Я не мог(ла) ничем увлечься',
                          'Мне казалось, что как человек я ничего не стою',
                          'Я чувствовал(а), что был(а) довольно обидчив(а)',
                          'Я чувствовал(а) работу своего сердца при отсутствии физической активности (например, ощущение увеличения частоты сердечных сокращений, пропуска сердечных ударов)',
                          'Мне было страшно без всякой на то причины',
                          'Мне казалось, что жизнь бессмысленна',
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
            raise BadOrderDTOZ

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 0,
                             'редко': 1,
                             'часто': 2,
                             'почти всегда': 3,
                             }

        valid_values = [0, 1, 2, 3]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(21):
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
            raise BadValueDTOZ

        base_df = pd.DataFrame()

        base_df['Депрессия_Значение'] = answers_df.apply(calc_value_depress, axis=1)
        base_df['Депрессия_Уровень'] = base_df['Депрессия_Значение'].apply(
            calc_level_depress)

        base_df['Тревога_Значение'] = answers_df.apply(calc_value_anxiety, axis=1)
        base_df['Тревога_Уровень'] = base_df['Тревога_Значение'].apply(
            calc_level_anxiety)

        base_df['Стресс_Значение'] = answers_df.apply(calc_value_stress, axis=1)
        base_df['Стресс_Уровень'] = base_df['Стресс_Значение'].apply(
            calc_level_stress)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ДАССДО_З_Деп_Значение'] = base_df['Депрессия_Значение']
        part_df['ДАССДО_З_Деп_Уровень'] = base_df['Депрессия_Уровень']

        part_df['ДАССДО_З_Тр_Значение'] = base_df['Тревога_Значение']
        part_df['ДАССДО_З_Тр_Уровень'] = base_df['Тревога_Уровень']

        part_df['ДАССДО_З_Ст_Значение'] = base_df['Стресс_Значение']
        part_df['ДАССДО_З_Ст_Уровень'] = base_df['Стресс_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)
        base_df.sort_values(by='Депрессия_Значение', ascending=False, inplace=True)  # сортируем

        # считаем среднее значение по шкалам
        avg_dep = round(base_df['Депрессия_Значение'].mean(), 2)
        avg_anx = round(base_df['Тревога_Значение'].mean(), 2)
        avg_str = round(base_df['Стресс_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Депрессия': avg_dep,
                   'Среднее значение шкалы Тревога': avg_anx,
                   'Среднее значение шкалы Стресс': avg_str}

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # Делаем свод по шкалам
        dct_svod_sub = {'Депрессия_Значение': 'Депрессия_Уровень',
                        'Тревога_Значение': 'Тревога_Уровень',
                        'Стресс_Значение': 'Стресс_Уровень',
                        }

        dct_rename_svod_sub = {'Депрессия_Значение': 'Депрессия',
                               'Тревога_Значение': 'Тревога',
                               'Стресс_Значение': 'Стресс',
                               }

        # Списки для шкал
        lst_level = ['низкий уровень DASS','средний уровень DASS','высокий уровень DASS']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод по шкалам': base_svod_sub_df,
                   'Среднее по шкалам': avg_df,
                   }

        dct_prefix = {'Депрессия_Уровень': 'Деп',
                      'Тревога_Уровень': 'Тр',
                      'Стресс_Уровень': 'Ст',
                      }

        out_dct = create_list_on_level_dass(base_df, out_dct, lst_level, dct_prefix)
        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_dass_twenty_one_zolotareva(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df
    except BadOrderDTOZ:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала депрессии, тревоги и стресса, DASS-21 Золотарева обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueDTOZ:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала депрессии, тревоги и стресса, DASS-21 Золотарева обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsDTOZ:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала депрессии, тревоги и стресса, DASS-21 Золотарева\n'
                             f'Должно быть 21 колонка с ответами')













