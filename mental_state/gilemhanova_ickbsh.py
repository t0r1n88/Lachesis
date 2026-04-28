"""
Скрипт для обработки результатов Индекс социокультурной безопасности школьника Гилемханова
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderISKBSHG(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueISKBSHG(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsISKBSHG(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 35
    """
    pass


def calc_value_iskb(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,4,6,7,8,9,12,15,16,
              18,19,22,23,24,25,26,27,28,31,32,33,35,
              1,3,5,10,11,13,14,17,20,21,29,30,34]
    lst_neg = [1,3,5,10,11,13,14,17,20,21,29,30,34]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 4
                elif value == 2:
                    value_forward += 3
                elif value == 3:
                    value_forward += 2
                else:
                    value_forward += 1


    return value_forward


def calc_level_iskb(value):
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
    elif 91 <= value <= 120:
        return f'91-120'
    else:
        return f'121-140'


def calc_value_spu(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,7,12,22,31,32,21]
    lst_neg = [21]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 4
                elif value == 2:
                    value_forward += 3
                elif value == 3:
                    value_forward += 2
                else:
                    value_forward += 1


    return value_forward


def calc_level_spu(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 12:
        return f'ниже нормы'
    elif 12 <= value <= 20:
        return f'норма'
    else:
        return f'выше нормы'

def calc_value_spd(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [15,25,
              5,10,20,30]
    lst_neg = [5,10,20,30]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 4
                elif value == 2:
                    value_forward += 3
                elif value == 3:
                    value_forward += 2
                else:
                    value_forward += 1


    return value_forward


def calc_level_spd(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 11:
        return f'ниже нормы'
    elif 11 <= value <= 18:
        return f'норма'
    else:
        return f'выше нормы'


def calc_value_va(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [8,18,23,28,33,
              3,13,17]
    lst_neg = [3,13,17]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 1:
                    value_forward += 4
                elif value == 2:
                    value_forward += 3
                elif value == 3:
                    value_forward += 2
                else:
                    value_forward += 1


    return value_forward


def calc_level_va(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value < 9:
        return f'ниже нормы'
    elif 9 <= value <= 14:
        return f'норма'
    else:
        return f'выше нормы'

def create_result_iskbn_gilem(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_l = ['1-30', '31-60', '61-90', '91-120','121-140']

    lst_reindex_one_level_l_cols = lst_svod_cols.copy()
    lst_reindex_one_level_l_cols.extend(['1-30', '31-60', '61-90', '91-120','121-140',
                                       'Итого'])  # Основная шкала

    # ИП
    svod_count_one_level_l_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ИСКБ_Значение',
                                                 'ИСКБ_Диапазон',
                                                 lst_reindex_one_level_l_cols, lst_l)

    lst_level = ['ниже нормы', 'норма', 'выше нормы']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['ниже нормы', 'норма', 'выше нормы',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СПУ_Значение',
                                                 'СПУ_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)
    # АВА
    svod_count_one_level_i_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'СПД_Значение',
                                                 'СПД_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    svod_count_one_level_ap_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ВА_Значение',
                                                 'ВА_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['ИСКБ_Значение',
                                              'СПУ_Значение',
                                              'СПД_Значение',
                                              'ВА_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['ИСКБ_Значение',
                            'СПУ_Значение',
                            'СПД_Значение',
                            'ВА_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'ИСКБ_Значение': 'Ср. Индекс социокультурной безопасности',
                            'СПУ_Значение': 'Ср. Социально-психологическая уязвимость',
                            'СПД_Значение': 'Ср. Социально-психологическая дезинтеграция',
                            'ВА_Значение': 'Ср. Виртуальная аутизация',
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
                    f'ИСКБ {out_name}': svod_count_one_level_l_df,
                    f'СПУ {out_name}': svod_count_one_level_s_df,
                    f'СПД {out_name}': svod_count_one_level_i_df,
                    f'ВА {out_name}': svod_count_one_level_ap_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_l_cols = [lst_svod_cols[idx], '1-30', '31-60', '61-90', '91-120','121-140',
                                             'Итого']

            # Ложь
            svod_count_column_level_l_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'ИСКБ_Значение',
                                                         'ИСКБ_Диапазон',
                                                         lst_reindex_column_level_l_cols, lst_l)

            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'ниже нормы', 'норма', 'выше нормы',
                                             'Итого']

            # АД
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'СПУ_Значение',
                                                            'СПУ_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            # АВА
            svod_count_column_level_i_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'СПД_Значение',
                                                            'СПД_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)
            svod_count_column_level_ap_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ВА_Значение',
                                                            'ВА_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['ИСКБ_Значение',
                                                      'СПУ_Значение',
                                                      'СПД_Значение',
                                                      'ВА_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['ИСКБ_Значение',
                                    'СПУ_Значение',
                                    'СПД_Значение',
                                    'ВА_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'ИСКБ_Значение': 'Ср. Индекс социокультурной безопасности',
                                    'СПУ_Значение': 'Ср. Социально-психологическая уязвимость',
                                    'СПД_Значение': 'Ср. Социально-психологическая дезинтеграция',
                                    'ВА_Значение': 'Ср. Виртуальная аутизация',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'ИСКБ {name_column}': svod_count_column_level_l_df,
                            f'СПУ {name_column}': svod_count_column_level_s_df,
                            f'СПД {name_column}': svod_count_column_level_i_df,
                            f'ВА {name_column}': svod_count_column_level_ap_df,
                            })
        return out_dct






def processing_iskbsh_gil(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 35:  # проверяем количество колонок с вопросами
            raise BadCountColumnsISKBSHG

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я не взялся бы за опасную для жизни работу, даже если бы за нее хорошо платили',
                          'Считаю напрасным терпеть боль назло всем',
                          'Это заблуждение, что общаться в социальных сетях проще, чем «лицом к лицу» со сверстниками',
                          'Я считаю, что существуют четкие различия между правильным и неправильным',
                          'В моем классе благоприятный психологический климат',
                          'Почему-то как правило все шишки сыплются именно на меня',
                          'Когда я думаю о себе, меня посещают больше отрицательных и грустных мыслей, чем позитивных',
                          'Наиболее занимательная часть моей жизни протекает в интернете',
                          'Мне не трудно скрыть, если человек мне чем-то неприятен',
                          'Я удовлетворен теми отношениями, которые у меня сложились с одноклассниками',

                          'Я не получаю удовольствия от ощущения риска',
                          'Если другие люди вызывают у меня восторг и очарование, то в себе я больше разочаровываюсь и чувствую отвращение',
                          'Мне не нравится обезличенное общение в интернете',
                          'Любые религиозные течения имеют право на существование',
                          'Я хотел бы перейти в другой класс',
                          'Только неожиданные обстоятельства и чувство опасности позволяют мне по-настоящему проявить себя',
                          'Когда у меня что-то не получается я виню в этом прежде всего себя',
                          'В виртуальном пространстве интернета больше интересных событий, чем в моей реальной жизни',
                          'В споре может быть правильной только одна точка зрения',
                          'В моем классе благоприятные для саморазвития и учебы условия',

                          'Регулярно попадать в неприятные ситуации в школе – это не про меня',
                          'Я достаточно часто себя ругаю и упрекаю',
                          'Иногда приятно бывает скрываться за аватаркой',
                          'Человек, который думает не так, как я, вызывает у меня раздражение',
                          'Учителя, как правило, уважительно относятся только к прилежным ученикам',
                          'Для меня верно, что если быть виноватыми, то во всем и сразу',
                          'Я предпочитаю высказать недовольство, чем копить его в себе',
                          'В социальных сетях общение более свободное и занимательное',
                          'Я хочу, чтобы среди моих одноклассников были представители разных национальностей',
                          'Мне нравится школа, в которой я учусь',
                          'Для меня верно «Язык мой – враг мой»',
                          'Для меня стало нормой отпускать в свой адрес грубые и ужасные слова',
                          'Аватарка или статус инкогнито в социальных сетях позволяет мне больше и полнее проявлять себя, не отвлекаясь на несущественные детали',
                          'Приезжие должны иметь те же права, что и местные жители',
                          'Я могу свободно выражать свою точку зрения в классе, не думая о том, что кому-то она может не понравиться'
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
            raise BadOrderISKBSHG

        # словарь для замены слов на числа
        dct_replace_value = {
                             'нет': 1,
                             'скорее нет': 2,
                             'скорее да': 3,
                             'да': 4,
                             }
        valid_values = [1, 2, 3, 4]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(35):
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
            raise BadValueISKBSHG

        base_df['ИСКБ_Значение'] = answers_df.apply(calc_value_iskb, axis=1)
        base_df['ИСКБ_Диапазон'] = base_df['ИСКБ_Значение'].apply(calc_level_iskb)

        base_df['СПУ_Значение'] = answers_df.apply(calc_value_spu, axis=1)
        base_df['СПУ_Уровень'] = base_df['СПУ_Значение'].apply(calc_level_spu)

        base_df['СПД_Значение'] = answers_df.apply(calc_value_spd, axis=1)
        base_df['СПД_Уровень'] = base_df['СПД_Значение'].apply(calc_level_spd)

        base_df['ВА_Значение'] = answers_df.apply(calc_value_va, axis=1)
        base_df['ВА_Уровень'] = base_df['ВА_Значение'].apply(calc_level_va)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ИСКБШГ_ИСКБ_Значение'] = base_df['ИСКБ_Значение']
        part_df['ИСКБШГ_ИИСКБ_Диапазон'] = base_df['ИСКБ_Диапазон']

        part_df['ИСКБШГ_СПУ_Значение'] = base_df['СПУ_Значение']
        part_df['ИСКБШГ_СПУ_Уровень'] = base_df['СПУ_Уровень']

        part_df['ИСКБШГ_СПД_Значение'] = base_df['СПД_Значение']
        part_df['ИСКБШГ_СПД_Уровень'] = base_df['СПД_Уровень']

        part_df['ИСКБШГ_ВА_Значение'] = base_df['ВА_Значение']
        part_df['ИСКБШГ_ВА_Уровень'] = base_df['ВА_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='ИСКБ_Значение', ascending=True, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_l = {'ИСКБ_Значение': 'ИСКБ_Диапазон',
                      }

        dct_rename_svod_l = {'ИСКБ_Значение': 'Индекс социокультурной безопасности',
                             }

        lst_l = ['1-30', '31-60', '61-90', '91-120','121-140']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_l)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'СПУ_Значение': 'СПУ_Уровень',
                        'СПД_Значение': 'СПД_Уровень',
                        'ВА_Значение': 'ВА_Уровень',
                        }

        dct_rename_svod_sub = {'СПУ_Значение': 'Социально-психологическая уязвимость',
                               'СПД_Значение': 'Социально-психологическая дезинтеграция',
                               'ВА_Значение': 'Виртуальная аутизация',
                               }

        lst_sub = ['ниже нормы', 'норма', 'выше нормы']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['ИСКБ_Значение'].mean(), 2)
        avg_o = round(base_df['СПУ_Значение'].mean(), 2)
        avg_ruvs = round(base_df['СПД_Значение'].mean(), 2)
        avg_ap = round(base_df['ВА_Значение'].mean(), 2)

        avg_dct = {'Среднее значение индекса социокультурной безопасности': avg_vcha,
                   'Среднее значение шкалы Социально-психологическая уязвимость': avg_o,
                   'Среднее значение шкалы Социально-психологическая дезинтеграция': avg_ruvs,
                   'Среднее значение шкалы Виртуальная аутизация': avg_ap,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод ИСКБ': base_svod_l_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_l = {
            'ИСКБ_Диапазон': 'ИСКБ',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_l, dct_l)

        dct_prefix = {
            'СПУ_Уровень': 'СПУ',
            'СПД_Уровень': 'СПД',
            'ВА_Уровень': 'ВА',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_iskbn_gilem(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderISKBSHG:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Индекс социокультурной безопасности школьника Гилемханова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueISKBSHG:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Индекс социокультурной безопасности школьника Гилемханова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsISKBSHG:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Индекс социокультурной безопасности школьника Гилемханова\n'
                             f'Должно быть 35 колонок с ответами')





