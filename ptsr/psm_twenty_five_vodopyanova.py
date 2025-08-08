"""
Скрипт для обработки результатов теста Шкала психологического стресса PSM-25 Адаптация Н. Е. Водопьянова

"""
import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean,calc_count_scale


class BadOrderPSMSTFZ(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValuePSMSTFZ(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsPSMSTFZ(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 25
    """
    pass




def calc_value(row):
    """
    Функция для подсчета значения
    :param row: строка с ответами
    :return: число
    """

    value_forward = 0 # счетчик прямых ответов
    value_reverse = 0 # счетчик обратных ответов
    lst_reverse = [14] # обратный подсчет

    for idx, value in enumerate(row):
        if idx + 1 in lst_reverse:
            # print(f'Обратный подсчет {idx +1}')# Для проверки корректности
            if value == 8:
                value_reverse += 1
            elif value == 7:
                value_reverse += 2
            elif value == 6:
                value_reverse += 3
            elif value == 5:
                value_reverse += 4
            elif value == 4:
                value_reverse += 5
            elif value == 3:
                value_reverse += 6
            elif value == 2:
                value_reverse += 7
            elif value == 1:
                value_reverse += 8
        else:
            # print(f'Прямой подсчет {idx +1}') # Для проверки корректности

            value_forward += value


    return value_forward + value_reverse

def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <= 99:
        return 'низкий уровень ППН'
    elif 100 <= value <= 155:
        return 'средний уровень ППН'
    else:
        return 'высокий уровень ППН'

def create_list_on_level_psm(base_df:pd.DataFrame, out_dct:dict, lst_level:list, dct_prefix:dict):
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
                if level == 'низкий уровень ППН':
                    level = 'низкий'
                elif level == 'средний уровень ППН':
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
                                       aggfunc=round_mean)
    calc_mean_df.reset_index(inplace=True)
    calc_mean_df.rename(columns={val_cat:'Среднее значение'},inplace=True)
    return calc_mean_df

def create_result_psm_twenty_five_vodopyanova(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_level = ['низкий уровень ППН','средний уровень ППН','высокий уровень ППН']
    lst_reindex_main_level_cols = lst_svod_cols.copy()
    lst_reindex_main_level_cols.extend(['низкий уровень ППН','средний уровень ППН','высокий уровень ППН',
                               'Итого'])  # Основная шкала

    svod_count_one_level_df = calc_count_scale(base_df, lst_svod_cols,
                                               'ППН_Значение',
                                               'ППН_Уровень',
                                               lst_reindex_main_level_cols, lst_level)

    # Считаем среднее
    svod_mean_df = calc_mean(base_df, lst_svod_cols, 'ППН_Значение')
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

    out_dct.update({f'Свод {out_name}': svod_count_one_level_df,
                    f'Ср. {out_name}': svod_mean_df})

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'низкий уровень ППН','средний уровень ППН','высокий уровень ППН',
                               'Итого']

            svod_count_column_level_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                       'ППН_Значение',
                                                       'ППН_Уровень',
                                                       lst_reindex_column_level_cols, lst_level)

            # Считаем среднее
            svod_mean_column_df = calc_mean(base_df, [lst_svod_cols[idx]], 'ППН_Значение')
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Свод {name_column}': svod_count_column_level_df,
                            f'Ср. {name_column}': svod_mean_column_df})

        return out_dct




def processing_psm_twenty_five_vodopyanova(result_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param result_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = result_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 25:  # проверяем количество колонок с вопросами
            raise BadCountColumnsPSMSTFZ

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я напряжен и взволнован (взвинчен)',
                          'У меня ком в горле, и (или) я ощущаю сухость во рту',
                          'Я перегружен работой. Мне совсем не хватает времени',
                          'Я проглатываю пищу или забываю поесть',
                          'Я обдумываю свои идеи снова и снова; я меняю свои планы; мои мысли постоянно повторяются',
                          'Я чувствую себя одиноким, изолированным и непонятым',
                          'Я страдаю от физического недомогания; у меня болит голова, напряжены мышцы шеи, боли в спине, спазмы в желудке',
                          'Я поглощён мыслями, измучен или обеспокоен',
                          'Меня внезапно бросает то в жар, то в холод',
                          'Я забываю о встречах или делах, которые должен сделать или решить',
                          'Я легко могу заплакать',
                          'Я чувствую себя уставшим',
                          'Я крепко стискиваю зубы',
                          'Я не спокоен',
                          'Мне тяжело дышать, и (или) у меня внезапно перехватывает дыхание',
                          'Я имею проблемы с пищеварением и с кишечником (боли, колики, расстройства или запоры)',
                          'Я взволнован, обеспокоен или смущен',
                          'Я легко пугаюсь; шум или шорох заставляет меня вздрагивать',
                          'Мне необходимо более чем полчаса для того, чтобы заснуть',
                          'Я сбит с толку; мои мысли спутаны; мне не хватает сосредоточенности, и я не могу сконцентрировать внимание',
                          'У меня усталый вид; мешки или круги под глазами',
                          'Я чувствую тяжесть на своих плечах',
                          'Я встревожен. Мне необходимо постоянно двигаться; я не могу устоять на одном месте',
                          'Мне трудно контролировать свои поступки, эмоции, настроение или жесты',
                          'Я напряжен'
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
            raise BadOrderPSMSTFZ

        # словарь для замены слов на числа
        dct_replace_value = {'никогда': 1,
                             'крайне редко': 2,
                             'очень редко': 3,
                             'редко': 4,
                             'иногда': 5,
                             'часто': 6,
                             'очень часто': 7,
                             'постоянно (ежедневно)': 8
                             }

        valid_values = [1, 2, 3, 4,5,6,7,8]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(25):
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
            raise BadValuePSMSTFZ

        base_df = pd.DataFrame()

        base_df['ППН_Значение'] = answers_df.apply(calc_value,axis=1)
        base_df['ППН_Уровень'] = base_df['ППН_Значение'].apply(calc_level)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ПСМ_ДП_В_Значение'] = base_df['ППН_Значение']
        part_df['ПСМ_ДП_В_Уровень'] = base_df['ППН_Уровень']

        # Соединяем анкетную часть с результатной
        base_df = pd.concat([result_df, base_df], axis=1)

        base_df.sort_values(by='ППН_Значение', ascending=False, inplace=True)  # сортируем
        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Общий свод по уровням общей шкалы всего в процентном соотношении
        base_svod_all_df = pd.DataFrame(
            index=['низкий уровень ППН','средний уровень ППН','высокий уровень ППН'])

        svod_level_df = pd.pivot_table(base_df, index='ППН_Уровень',
                                       values='ППН_Значение',
                                       aggfunc='count')

        svod_level_df['% от общего'] = round(
            svod_level_df['ППН_Значение'] / svod_level_df[
                'ППН_Значение'].sum(), 3) * 100

        base_svod_all_df = base_svod_all_df.join(svod_level_df)

        # # Создаем суммирующую строку
        base_svod_all_df.loc['Итого'] = svod_level_df.sum()
        base_svod_all_df.reset_index(inplace=True)
        base_svod_all_df.rename(columns={'index': 'Уровень', 'ППН_Значение': 'Количество'},
                                inplace=True)
        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод Общий': base_svod_all_df,
                   }

        dct_prefix = {'ППН_Уровень': 'ППН',
                      }

        out_dct = create_list_on_level_psm(base_df, out_dct, ['низкий уровень ППН', 'средний уровень ППН', 'высокий уровень ППН'], dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_psm_twenty_five_vodopyanova(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df
    except BadOrderPSMSTFZ:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала психологического стресса PSM-25 Водопьянова обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValuePSMSTFZ:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала психологического стресса PSM-25 Водопьянова обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsPSMSTFZ:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала психологического стресса PSM-25 Водопьянова\n'
                             f'Должно быть 25 колонок с ответами')







