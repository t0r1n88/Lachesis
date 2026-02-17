"""
Скрипт для обработки результатов теста Опросник киберагрессии CYBA Альварез-Гарсия Шаров
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_list_on_level,create_union_svod


class BadOrderCYBAAGSH(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueCYBAAGSH(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsCYBAAGSH(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 19
    """
    pass


def calc_value_i(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,12,18]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward

def calc_value_s(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,3,6,9,14]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            value_forward += value


    return value_forward


def calc_value_vvka(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,5,7,8,10,11,13,15,16,17,19]
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
    if 19<= value <= 38:
        return f'19-38'
    elif 39 <= value <= 58:
        return f'39-58'
    elif 59 <= value <= 65:
        return f'59-65'
    else:
        return f'66-76'


def create_list_on_level_cyba(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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



def create_result_cyba_ag_sharov(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['19-38', '39-58', '59-65','66-76']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['19-38', '39-58', '59-65','66-76',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_vcha_df = calc_count_scale(base_df, lst_svod_cols,
                                                   'ИШКА_Значение',
                                                   'ИШКА_Диапазон',
                                                   lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['И_Значение',
                                              'С_Значение',
                                              'ВВКА_Значение',
                                              'ИШКА_Значение',

                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['И_Значение', 'С_Значение',
                            'ВВКА_Значение', 'ИШКА_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'И_Значение': 'Ср. Имперсонация',
                            'С_Значение': 'Ср. Секстинг',
                            'ВВКА_Значение': 'Ср. Вербально-визуальная киберагрессия',
                            'ИШКА_Значение': 'Ср. Интегративная шкала киберагрессии',
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
                    f'ИШКА {out_name}': svod_count_one_level_vcha_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'19-38', '39-58', '59-65','66-76',
                                                  'Итого']
            # ВЧА
            svod_count_column_level_vcha_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ИШКА_Значение',
                                                            'ИШКА_Диапазон',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['И_Значение',
                                                      'С_Значение',
                                                      'ВВКА_Значение',
                                                      'ИШКА_Значение',

                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['И_Значение', 'С_Значение',
                                    'ВВКА_Значение', 'ИШКА_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'И_Значение': 'Ср. Имперсонация',
                                    'С_Значение': 'Ср. Секстинг',
                                    'ВВКА_Значение': 'Ср. Вербально-визуальная киберагрессия',
                                    'ИШКА_Значение': 'Ср. Интегративная шкала киберагрессии',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИШКА {name_column}': svod_count_column_level_vcha_df,
                            })
        return out_dct






def processing_cyba_ag_sharov(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 19:  # проверяем количество колонок с вопросами
            raise BadCountColumnsCYBAAGSH

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я выдал(а) себя за кого-то другого в сети Интернет, публикуя комментарии под его / ее именем',
                          'Я делал(а) фотографии или видеозаписи сексуального или непристойного содержания (например, на пляже, в раздевалке...) без согласия снимаемых участников и делился(лась) ими с другими пользователями с помощью мобильного телефона или Интернета',
                          'Я разместил(а) подделанные (измененные) фотографии других людей в сети Интернет для того, чтобы причинить им боль или высмеять их',
                          'Я удалил(а) из списка контактов или отказал(а) в общении другому человеку в чате, социальной сети или программе обмена мгновенными сообщениями (мессенджере), хотя он / она ничего мне не сделал(а)',
                          'Чтобы вывести кого-то из себя, я позвонил(а) на мобильный телефон и сознательно молчал(а), когда на звонок ответили',
                          'Я разместил(а) реальные компрометирующие фотографии или видео человека в Интернете без его / ее разрешения, чтобы причинить ему / ей боль или посмеяться над ним / ней',
                          'Я звонил(а) по телефону, чтобы оскорбить или подразнить кого-то',
                          'Я дразнил(а) кого-то, оставляя оскорбительные или обидные комментарии в социальных сетях',
                          'Используя мобильный телефон или Интернет, я поделился(лась) с другими пользователями компрометирующими изображениями или видео другого человека без его / ее разрешения',
                          'Я кого-то ударил(а), записал(а) это на видео, а потом поделился(лась) этим материалом в сети',

                          'Я оскорбил(а) кого-то, используя текстовые сообщения (СМС) или программы обмена мгновенными сообщениями (мессенджеры)',
                          'Я выдал(а) себя за кого-то другого, создав ложный профиль пользователя, с помощью которого оскорблял(а) или высмеивал(а) кого-то',
                          'Я подал(а) ложную жалобу на кого-то на форуме, в социальной сети или онлайн-игре, что привело к его / ее исключению',
                          'Я подтолкнул(а) другого человека к тому, что он / она не хотел(а) делать, угрожая поделиться с другими пользователями содержанием частных разговоров с ним / с ней или его / ее фотографиями',
                          'Я заставил(а) кого-то сделать что-то унизительное, записал(а) это на видео, а затем поделился(лась) этим с другими пользователями, чтобы подразнить его / ее',
                          'Я вступил(а) в сговор с другими людьми с целью игнорировать кого-то в социальных сетях',
                          'Я делал(а) анонимные звонки для того, чтобы угрожать или пугать кого-то',
                          'Я получил(а) пароль другого человека и отправлял(а) неприятные сообщения, притворяясь, что они были от него / нее, чтобы доставить кому-то неприятности',
                          'Я опубликовал(а) слухи о ком-то в социальной сети'
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
            raise BadOrderCYBAAGSH

        # словарь для замены слов на числа
        dct_replace_value = {'всегда': 4,
                             'часто': 3,
                             'редко': 2,
                             'никогда': 1,
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
            raise BadValueCYBAAGSH

        # Субшкалы
        base_df['И_Значение'] = answers_df.apply(calc_value_i, axis=1)
        base_df['С_Значение'] = answers_df.apply(calc_value_s, axis=1)
        base_df['ВВКА_Значение'] = answers_df.apply(calc_value_vvka, axis=1)
        base_df['ИШКА_Значение'] = answers_df.sum(axis=1)
        base_df['ИШКА_Диапазон'] = base_df['ИШКА_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ОКААГШ_И_Значение'] = base_df['И_Значение']
        part_df['ОКААГШ_С_Значение'] = base_df['С_Значение']
        part_df['ОКААГШ_ВВКА_Значение'] = base_df['ВВКА_Значение']
        part_df['ОКААГШ_ИШКА_Значение'] = base_df['ИШКА_Значение']
        part_df['ОКААГШ_ИШКА_Диапазон'] = base_df['ИШКА_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИШКА_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ИШКА_Значение': 'ИШКА_Диапазон',
                        }

        dct_rename_svod_sub = {'ИШКА_Значение': 'Интегративная шкала киберагрессии',
                               }

        lst_sub = ['19-38', '39-58', '59-65','66-76']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['И_Значение'].mean(), 2)
        avg_o = round(base_df['С_Значение'].mean(), 2)
        avg_ruvs = round(base_df['ВВКА_Значение'].mean(), 2)

        avg_psp = round(base_df['ИШКА_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Имперсонация': avg_vcha,
                   'Среднее значение шкалы Секстинг': avg_o,
                   'Среднее значение шкалы Вербально-визуальная киберагрессия': avg_ruvs,

                   'Среднее значение Интегративная шкала киберагрессии': avg_psp,
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

        dct_prefix = {'ИШКА_Диапазон': 'ИШКА',
                      }

        out_dct = create_list_on_level_cyba(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_cyba_ag_sharov(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderCYBAAGSH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник киберагрессии Альварез-Гарсия, CYBA Шаров обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueCYBAAGSH:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Опросник киберагрессии Альварез-Гарсия, CYBA Шаров обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsCYBAAGSH:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Опросник киберагрессии Альварез-Гарсия, CYBA Шаров\n'
                             f'Должно быть 19 колонок с ответами')











