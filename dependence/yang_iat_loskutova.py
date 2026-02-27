"""
Скрипт для обработки результатов Тест на интернет-зависимость IAT Янг Лоскутова
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderIATYL(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueIATYL(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsIATYL(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 20
    """
    pass


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 20<= value <= 49:
        return f'нет ИЗ'
    elif 50 <= value <= 79:
        return f'склонность к ИЗ'
    else:
        return f'наличие ИЗ'


def create_list_on_level_iat(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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


def create_result_iat_yang_los(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['нет ИЗ', 'склонность к ИЗ', 'наличие ИЗ']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['нет ИЗ', 'склонность к ИЗ', 'наличие ИЗ',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'ИЗ_Значение',
                                                    'ИЗ_Уровень',
                                                    lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                              'ИЗ_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend(([ 'ИЗ_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ИЗ_Значение': 'Ср. Интернет зависимость',
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
                    f'ИЗ {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'нет ИЗ', 'склонность к ИЗ', 'наличие ИЗ',
                                                  'Итого']

            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'ИЗ_Значение',
                                                               'ИЗ_Уровень',
                                                               lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=[
                                                  'ИЗ_Значение',
                                              ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИЗ_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ИЗ_Значение': 'Ср. Интернет зависимость',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИЗ {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct










def processing_iat_yang_los(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 20:  # проверяем количество колонок с вопросами
            raise BadCountColumnsIATYL

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Замечаете ли Вы, что проводите в интернете больше времени, чем намеревались?',
                          'Пренебрегаете ли Вы домашними делами, чтобы проводить больше времени в сети?',
                          'Бывает ли так, что Вы предпочитаете пребывание в сети общению с близкими?',
                          'Заводите ли Вы новые знакомства с другими интернет-пользователями?',
                          'Высказывают ли Ваши близкие недовольство по поводу того, что Вы слишком много времени проводите в интернете?',
                          'Влияет ли негативно увлечение интернетом на Вашу работу или учебу?',
                          'Проверяете ли Вы электронную почту, прежде чем заняться другими важными делами?',
                          'Бывает ли так, что из-за серфинга в интернете Вы не успеваете выполнить какую-либо работу?',
                          'Бывает ли так, что Вы отпираетесь и скрытничаете, когда Вас спрашивают, чем Вы занимаетесь в сети?',
                          'Замещаете ли Вы беспокоящие мысли о проблемах в реальной жизни утешительными мыслями о том, чем Вы заняты в Интернете?',

                          'Бывает ли так, что Вы с нетерпением предвкушаете, что вновь окажетесь в сети?',
                          'Ощущаете ли Вы, что жизнь без Интернета скучна, пуста и безрадостна?',
                          'Бывает ли так, что Вы ругаетесь, кричите или иным образом выражаете свою досаду, когда кто-то пытается отвлечь Вас от пребывания в сети?',
                          'Бывает ли так, что Вы недосыпаете, потому что засиживаетесь в сети допоздна?',
                          'Бывает ли так, что, находясь вне сети, Вы поглощены мыслями о том, чем займетесь в Интернете или мысленно представляете, что Вы находитесь в сети?',
                          'Часто ли Вы говорите себе «еще чуть-чуть, еще несколько минут», находясь в сети?',
                          'Бывали ли у Вас неудачные попытки сократить количество времени, проводимого в Интернете?',
                          'Бывало ли так, что Вы пытались скрыть от окружающих количество времени, которое Вы поводите в Интернете?',
                          'Случается ли так, что Вы предпочитаете провести время в Интернете вместо того, чтобы выбраться куда-либо с друзьями?',
                          'Бывают ли случаи, когда Вы не в настроении, подавлены или нервозны, будучи вне сети и отмечаете, что это состояние проходит, как только Вы снова оказываетесь в интернете?',
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
            raise BadOrderIATYL

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 1,
                             'редко': 2,
                             'иногда': 3,
                             'часто': 4,
                             'очень часто': 5,
                             }
        valid_values = [1, 2, 3, 4, 5]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
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
            raise BadValueIATYL

        base_df['ИЗ_Значение'] = answers_df.sum(axis=1)
        base_df['ИЗ_Уровень'] = base_df['ИЗ_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы

        part_df['ТИЗЯЛ_Значение'] = base_df['ИЗ_Значение']
        part_df['ТИЗЯЛ_Уровень'] = base_df['ИЗ_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИЗ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ИЗ_Значение': 'ИЗ_Уровень',
                        }

        dct_rename_svod_sub = {
            'ИЗ_Значение': 'Уровень интернет зависимости',
        }

        lst_sub = ['нет ИЗ', 'склонность к ИЗ', 'наличие ИЗ']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_psp = round(base_df['ИЗ_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Интернет зависимости': avg_psp,
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

        dct_prefix = {'ИЗ_Уровень': 'ИЗ',
                      }

        out_dct = create_list_on_level_iat(base_df, out_dct, lst_sub, dct_prefix)

        """
                                Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                                """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_iat_yang_los(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderIATYL:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста на интернет-зависимость IAT Янг Лоскутова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueIATYL:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста на интернет-зависимость IAT Янг Лоскутова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsIATYL:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест на интернет-зависимость IAT Янг Лоскутова\n'
                             f'Должно быть 20 колонок с ответами')



