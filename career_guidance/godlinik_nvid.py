"""
Скрипт для обработки результатов теста Направленность на вид инженерной деятельности
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean, create_union_svod,calc_count_scale


class BadValueNVID(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass


class BadCountColumnsNVID(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 24
    """
    pass


def extract_key_max_value(cell: str) -> str:
    """
    Функция для извлечения ключа с максимальным значением
    :param cell: строка формата ключ - значение;
    :return: ключ словаря в формате строки
    """
    # проверяем если некорректное значение
    if 'Скопируйте правильные значения для указанных вопросов из квадратных скобок' in cell:
        return cell
    dct_result = {}
    cell = cell.replace('\n', '')  # убираем переносы
    lst_temp = cell.split(';')  # сплитим по точке с запятой
    for result in lst_temp:
        # отбрасываем пустую строку
        if result:
            key, value = result.split(': ')  # извлекаем ключ и значение
            dct_result[key] = int(value)

    # возвращаем элемент с максимальным значением
    return max(dct_result, key=dct_result.get)


def extract_max_value(cell: str):
    """
    Функция для извлечения значения ключа с максимальным значением , ха звучит странно
    :param cell: строка формата ключ - значение;
    :return: ключ словаря в формате строки
    """
    # проверяем если некорректное значение
    if 'Скопируйте правильные значения для указанных вопросов из квадратных скобок' in cell:
        return 0
    dct_result = {}
    cell = cell.replace('\n', '')  # убираем переносы
    lst_temp = cell.split(';')  # сплитим по точке с запятой
    for result in lst_temp:
        # отбрасываем пустую строку
        if result:
            key, value = result.split(': ')  # извлекаем ключ и значение
            dct_result[key] = int(value)

    # возвращаем элемент с максимальным значением
    return dct_result[max(dct_result, key=dct_result.get)]


def processing_result_nvid(row):
    """
    Обработка результатов тестирования
    """

    # Создаем словарь для хранения данных
    dct_type = {'научно-исследовательская деятельность': 0,
                'проектно-конструкторская': 0,
                'производственная': 0,
                'организаторская': 0,
                }

    # 1
    if row[0] == 'Планировать и проводить эксперименты для проверки научных гипотез, догадок, выявления закономерностей':
        dct_type['научно-исследовательская деятельность'] += 1
    elif row[0] == 'Эксплуатировать машины, механизмы, приборы (управлять, следить, регулировать)':
        dct_type['производственная'] += 1

    # 2
    if row[1] == 'Проектировать, конструировать новые приборы, машины, механизмы':
        dct_type['проектно-конструкторская'] += 1
    elif row[1] == 'Организовывать, планировать, координировать производственную деятельность людей':
        dct_type['организаторская'] += 1

    # 3
    if row[2] == 'Обеспечивать эффективную безаварийную работу сложных технических устройств':
        dct_type['производственная'] += 1
    elif row[2] == 'Вносить усовершенствования в конструкцию технических устройств':
        dct_type['проектно-конструкторская'] += 1

    # 4
    if row[3] == 'Разрабатывать и внедрять в производство современные формы и методы организации труда':
        dct_type['организаторская'] += 1
    elif row[3] == 'Искать оптимальные решения научных и технических проблем, формулировать новые задачи':
        dct_type['научно-исследовательская деятельность'] += 1

    # 5
    if row[4] == 'Эксплуатировать машины, механизмы, приборы (управлять, следить, регулировать)':
        dct_type['производственная'] += 1
    elif row[4] == 'Организовывать, планировать координировать производственную деятельность людей':
        dct_type['организаторская'] += 1

    # 6
    if row[5] == 'Искать оптимальные решения научных и технических проблем, формулировать новые задачи':
        dct_type['научно-исследовательская деятельность'] += 1
    elif row[5] == 'Вносить усовершенствования в конструкцию технических устройств':
        dct_type['проектно-конструкторская'] += 1

    # 7
    if row[6] == 'Обеспечивать эффективную безаварийную работу сложных технических устройств':
        dct_type['производственная'] += 1
    elif row[6] == 'Искать оптимальные решения научных и технических проблем, формулировать новые задачи':
        dct_type['научно-исследовательская деятельность'] += 1

    # 8
    if row[7] == 'Разрабатывать и внедрять в производство современные формы и методы организации труда':
        dct_type['организаторская'] += 1
    elif row[7] == 'Вносить усовершенствования в конструкцию технических устройств':
        dct_type['проектно-конструкторская'] += 1

    # 9
    if row[8] == 'Проектировать, конструировать новые приборы, машины, механизмы':
        dct_type['проектно-конструкторская'] += 1
    elif row[8] == 'Эксплуатировать машины, механизмы, приборы (управлять следить, регулировать)':
        dct_type['производственная'] += 1

    # 10
    if row[9] == 'Планировать и проводить эксперименты для проверки научных гипотез, догадок, выявлять закономерности':
        dct_type['научно-исследовательская деятельность'] += 1
    elif row[9] == 'Организовывать, планировать, координировать производственную деятельность людей':
        dct_type['организаторская'] += 1

    # 11
    if row[10] == 'Разрабатывать и внедрять в производство современные формы и методы организации труда':
        dct_type['организаторская'] += 1
    elif row[10] == 'Обеспечивать эффективную безаварийную работу сложных технических устройств':
        dct_type['производственная'] += 1

    # 12
    if row[11] == 'Проектировать, конструировать новые приборы, машины, механизмы':
        dct_type['проектно-конструкторская'] += 1
    elif row[11] == 'Планировать и проводить эксперименты для проверки гипотез, догадок, выявлять закономерности':
        dct_type['научно-исследовательская деятельность'] += 1

    # 13
    if row[12] == 'Искать оптимальные решения научных и технических проблем, формулировать новые задачи':
        dct_type['научно-исследовательская деятельность'] += 1
    elif row[12] == 'Эксплуатировать машины, механизмы, приборы (управлять следить, регулировать)':
        dct_type['производственная'] += 1

    # 14
    if row[13] == 'Вносить усовершенствования в конструкцию технических устройств':
        dct_type['проектно-конструкторская'] += 1
    elif row[13] == 'Организовывать, планировать, координировать производственную деятельность людей':
        dct_type['организаторская'] += 1

    # 15
    if row[14] == 'Эксплуатировать машины, механизмы, приборы (управлять, следить, регулировать)':
        dct_type['производственная'] += 1
    elif row[14] == 'Вносить усовершенствования в конструкцию технических устройств':
        dct_type['проектно-конструкторская'] += 1

    # 16
    if row[15] == 'Организовывать, планировать, координировать производственную деятельность людей':
        dct_type['организаторская'] += 1
    elif row[15] == 'Искать оптимальные решения научных и технических проблем, формулировать новые задачи':
        dct_type['научно-исследовательская деятельность'] += 1

    # 17
    if row[16] == 'Обеспечивать эффективную безаварийную работу сложных технических устройств':
        dct_type['производственная'] += 1
    elif row[16] == 'Организовывать, планировать, координировать производственную деятельность людей':
        dct_type['организаторская'] += 1

    # 18
    if row[17] == 'Искать оптимальные решения научных и технических проблем, формулировать новые задачи':
        dct_type['научно-исследовательская деятельность'] += 1
    elif row[17] == 'Проектировать, конструировать новые приборы, машины, механизмы':
        dct_type['проектно-конструкторская'] += 1

    # 19
    if row[18] == 'Обеспечивать эффективную безаварийную работу сложных технических устройств':
        dct_type['производственная'] += 1
    elif row[18] == 'Планировать и проводить эксперименты для проверки научных гипотез, догадок, выявлять закономерности':
        dct_type['научно-исследовательская деятельность'] += 1

    # 20
    if row[19] == 'Разрабатывать и внедрять в производство современные методы и формы организации труда':
        dct_type['организаторская'] += 1
    elif row[19] == 'Проектировать, конструировать новые приборы, машины, механизмы':
        dct_type['проектно-конструкторская'] += 1

    # 21
    if row[20] == 'Планировать, проводить эксперименты для проверки научных гипотез, догадок, выявлять закономерности':
        dct_type['научно-исследовательская деятельность'] += 1
    elif row[20] == 'Разрабатывать и внедрять в производство современные формы и методы организации труда':
        dct_type['организаторская'] += 1

    # 22
    if row[21] == 'Проектировать, конструировать новые приборы, машины, механизмы':
        dct_type['проектно-конструкторская'] += 1
    elif row[21] == 'Обеспечивать эффективную безаварийную работу сложных технических устройств':
        dct_type['производственная'] += 1

    # 23
    if row[22] == 'Разрабатывать и внедрять в производство современные методы, формы организации труда':
        dct_type['организаторская'] += 1
    elif row[22] == 'Обеспечивать эффективную безаварийную работу сложных технических устройств':
        dct_type['производственная'] += 1

    # 24
    if row[23] == 'Вносить усовершенствования в конструкцию технических устройств':
        dct_type['проектно-конструкторская'] += 1
    elif row[23] == 'Планировать и проводить эксперименты для проверки научных гипотез, догадок, выявлять закономерности':
        dct_type['научно-исследовательская деятельность'] += 1


    # сортируем по убыванию
    result_lst = sorted(dct_type.items(), key=lambda t: t[1], reverse=True)
    begin_str = '\n'
    # создаем строку с результатами
    for sphere, value in result_lst:
        begin_str += f'{sphere}: {value};\n'

    # добавляем описание
    return begin_str


def calc_level_nvid(value):
    """
    Функция для подсчета уровня склонности к то или иной сфере
    """
    if 0 <= value <= 8:
        return 'склонность не выражена'
    elif 9 <= value <= 12:
        return 'склонность выражена'


def create_result_godlinik_nvid(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['склонность не выражена', 'склонность выражена']

    lst_sphere = ['научно-исследовательская деятельность', 'проектно-конструкторская', 'производственная',
                  'организаторская']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['склонность не выражена', 'склонность выражена',
                                                      'Итого'])

    lst_reindex_one_sphere_cols = lst_svod_cols.copy()
    lst_reindex_one_sphere_cols.extend( ['научно-исследовательская деятельность', 'проектно-конструкторская', 'производственная',
                  'организаторская','Итого'])

    svod_count_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                               'Значение_ведущего_вида',
                                               'Уровень_выраженности',
                                               lst_reindex_one_level_cols, lst_level)

    svod_count_one_sphere_df = calc_count_scale(base_df, lst_svod_cols,
                                                'Значение_ведущего_вида',
                                                'Ведущий_вид',
                                                lst_reindex_one_sphere_cols, lst_sphere)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_ведущего_вида',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_ведущего_вида',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_ведущего_вида': 'Среднее значение ведущего вида',
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
                    f'Уровень {out_name}': svod_count_one_level_df,
                    f'Вид {out_name}': svod_count_one_sphere_df,
                    })
    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'склонность не выражена', 'склонность выражена',
                                             'Итого']

            lst_reindex_column_sphere_cols = [lst_svod_cols[idx], 'научно-исследовательская деятельность', 'проектно-конструкторская', 'производственная',
              'организаторская','Итого']

            svod_count_column_level_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                          'Значение_ведущего_вида',
                                                          'Уровень_выраженности',
                                                          lst_reindex_column_level_cols, lst_level)

            svod_count_column_sphere_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                           'Значение_ведущего_вида',
                                                           'Ведущий_вид',
                                                           lst_reindex_column_sphere_cols, lst_sphere)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=['Значение_ведущего_вида',
                                                         ],
                                                 aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_ведущего_вида',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_ведущего_вида': 'Среднее значение ведущего вида',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)


            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Уровень {name_column}': svod_count_column_level_df,
                            f'Вид {name_column}': svod_count_column_sphere_df,
                            })
        return out_dct






def processing_godlinik_nvid(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if answers_df.shape[1] != 24:
            raise BadCountColumnsNVID
        # Переименовываем колонки
        answers_df.columns = [f'Вопрос_ №{i}' for i in range(1, 25)]

        valid_values = [
            ['Планировать и проводить эксперименты для проверки научных гипотез, догадок, выявления закономерностей',
             'Эксплуатировать машины, механизмы, приборы (управлять, следить, регулировать)'],
            ['Проектировать, конструировать новые приборы, машины, механизмы',
             'Организовывать, планировать, координировать производственную деятельность людей'],
            ['Обеспечивать эффективную безаварийную работу сложных технических устройств',
             'Вносить усовершенствования в конструкцию технических устройств'],
            ['Разрабатывать и внедрять в производство современные формы и методы организации труда',
             'Искать оптимальные решения научных и технических проблем, формулировать новые задачи'],
            ['Эксплуатировать машины, механизмы, приборы (управлять, следить, регулировать)',
             'Организовывать, планировать координировать производственную деятельность людей'],
            ['Искать оптимальные решения научных и технических проблем, формулировать новые задачи',
             'Вносить усовершенствования в конструкцию технических устройств'],
            ['Обеспечивать эффективную безаварийную работу сложных технических устройств',
             'Искать оптимальные решения научных и технических проблем, формулировать новые задачи'],
            ['Разрабатывать и внедрять в производство современные формы и методы организации труда',
             'Вносить усовершенствования в конструкцию технических устройств'],
            ['Проектировать, конструировать новые приборы, машины, механизмы',
             'Эксплуатировать машины, механизмы, приборы (управлять следить, регулировать)'],
            ['Планировать и проводить эксперименты для проверки научных гипотез, догадок, выявлять закономерности',
             'Организовывать, планировать, координировать производственную деятельность людей'],
            ['Разрабатывать и внедрять в производство современные формы и методы организации труда',
             'Обеспечивать эффективную безаварийную работу сложных технических устройств'],
            ['Проектировать, конструировать новые приборы, машины, механизмы',
             'Планировать и проводить эксперименты для проверки гипотез, догадок, выявлять закономерности'],
            ['Искать оптимальные решения научных и технических проблем, формулировать новые задачи',
             'Эксплуатировать машины, механизмы, приборы (управлять следить, регулировать)'],
            ['Вносить усовершенствования в конструкцию технических устройств',
             'Организовывать, планировать, координировать производственную деятельность людей'],
            ['Эксплуатировать машины, механизмы, приборы (управлять, следить, регулировать)',
             'Вносить усовершенствования в конструкцию технических устройств'],
            ['Организовывать, планировать, координировать производственную деятельность людей',
             'Искать оптимальные решения научных и технических проблем, формулировать новые задачи'],
            ['Обеспечивать эффективную безаварийную работу сложных технических устройств',
             'Организовывать, планировать, координировать производственную деятельность людей'],
            ['Искать оптимальные решения научных и технических проблем, формулировать новые задачи',
             'Проектировать, конструировать новые приборы, машины, механизмы'],
            ['Обеспечивать эффективную безаварийную работу сложных технических устройств',
             'Планировать и проводить эксперименты для проверки научных гипотез, догадок, выявлять закономерности'],
            ['Разрабатывать и внедрять в производство современные методы и формы организации труда',
             'Проектировать, конструировать новые приборы, машины, механизмы'],
            ['Планировать, проводить эксперименты для проверки научных гипотез, догадок, выявлять закономерности',
             'Разрабатывать и внедрять в производство современные формы и методы организации труда'],
            ['Проектировать, конструировать новые приборы, машины, механизмы',
             'Обеспечивать эффективную безаварийную работу сложных технических устройств'],
            ['Разрабатывать и внедрять в производство современные методы, формы организации труда',
             'Обеспечивать эффективную безаварийную работу сложных технических устройств'],
            ['Вносить усовершенствования в конструкцию технических устройств',
             'Планировать и проводить эксперименты для проверки научных гипотез, догадок, выявлять закономерности']
            ]

        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for idx, lst_values in enumerate(valid_values):
            mask = ~answers_df.iloc[:, idx].isin(lst_values)  # проверяем на допустимые значения
            # Получаем строки с отличающимися значениями
            result_check = answers_df.iloc[:, idx][mask]

            if len(result_check) != 0:
                error_row = list(map(lambda x: x + 2, result_check.index))
                error_row = list(map(str, error_row))
                error_row_lst = [f'В {idx + 1} вопросной колонке на строке {value}' for value in error_row]
                error_in_column = ','.join(error_row_lst)
                lst_error_answers.append(error_in_column)

        if len(lst_error_answers) != 0:
            error_message = ';'.join(lst_error_answers)
            raise BadValueNVID

        base_df[f'Распределение'] = answers_df.apply(processing_result_nvid, axis=1)
        base_df[f'Ведущий_вид'] = base_df[f'Распределение'].apply(
            extract_key_max_value)
        base_df[f'Значение_ведущего_вида'] = base_df[f'Распределение'].apply(
            extract_max_value)
        base_df[f'Уровень_выраженности'] = base_df[f'Значение_ведущего_вида'].apply(
            calc_level_nvid)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['НВИД_Распределение'] = base_df['Распределение']
        part_df['НВИД_Ведущий_вид'] = base_df['Ведущий_вид']
        part_df['НВИД_Вид_Значение'] = base_df['Значение_ведущего_вида']
        part_df['НВИД_Вид_Уровень'] = base_df['Уровень_выраженности']

        base_df.sort_values(by='Значение_ведущего_вида', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Делаем свод по уровню
        dct_svod_level = {'Значение_ведущего_вида': 'Уровень_выраженности',
                          }
        dct_rename_svod_level = {'Значение_ведущего_вида': 'Количество',
                                 }
        # Списки для шкал
        lst_level = ['склонность не выражена', 'склонность выражена']
        base_svod_level_df = create_union_svod(base_df, dct_svod_level, dct_rename_svod_level, lst_level)

        # Делаем свод по сфере
        dct_svod_sphere = {'Значение_ведущего_вида': 'Ведущий_вид',
                           }

        dct_rename_svod_sphere = {'Значение_ведущего_вида': 'Количество',
                                  }

        # Списки для шкал
        lst_sphere = ['научно-исследовательская деятельность', 'проектно-конструкторская', 'производственная',
                      'организаторская']

        base_svod_sphere_df = create_union_svod(base_df, dct_svod_sphere, dct_rename_svod_sphere, lst_sphere)

        # считаем среднее значение
        avg_main = round(base_df['Значение_ведущего_вида'].mean(), 2)

        avg_dct = {'Среднее значение Ведущий вид': avg_main,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Среднее': avg_df,
                   'Свод по уровням': base_svod_level_df,
                   }

        # Листы по уровням
        dct_level = dict()
        for level in lst_level:
            temp_df = base_df[base_df['Уровень_выраженности'] == level]
            if temp_df.shape[0] != 0:
                if level == 'склонность не выражена':
                    level = 'не выражена'
                elif level == 'склонность выражена':
                    level = 'выражена'
                dct_level[level] = temp_df
        out_dct.update(dct_level)

        # Добавляем свод по сферам
        out_dct.update({
            'Свод по видам': base_svod_sphere_df,
        })
        # Листы по сферам
        dct_sphere = dict()
        for sphere in lst_sphere:
            temp_df = base_df[base_df['Ведущий_вид'] == sphere]
            if temp_df.shape[0] != 0:
                if sphere == 'научно-исследовательская деятельность':
                    sphere = 'научно-исследовательская'
                dct_sphere[sphere] = temp_df
        out_dct.update(dct_sphere)

        """
                          Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                          """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_godlinik_nvid(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadValueNVID:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Направленность на вид инженерной деятельности Годлиник обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsNVID:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Направленность на вид инженерной деятельности Годлиник\n'
                             f'Должно быть 24 колонки с ответами')
