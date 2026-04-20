"""
Скрипт для обработки результатов Опросник риска буллинга А.А. Бочавер и др.
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderBORB(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueBORB(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsBORB(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 48
    """
    pass

def calc_value_nb(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,3,7,11,12,16,20,31,33,34,36,46,
              8,21,32,35]
    lst_neg = [8,21,32,35]
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


def calc_value_b(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [15,17,26,27,41,47,
              19,25,28,44,48]
    lst_neg = [19,25,28,44,48]
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


def calc_value_ro(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [4,22,37,39,43,
              2,5,6,38,42]
    lst_neg = [2,5,6,38,42]
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


def calc_value_rp(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [9,10,13,14,18,23,24,29,30,40,45]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if value == 'да':
                value_forward += 1
    return value_forward



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




def processing_school_orb_bochaver(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
    if len(answers_df.columns) != 48:  # проверяем количество колонок с вопросами
        raise BadCountColumnsBORB

    # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
    clean_df_lst = []
    for name_column in answers_df.columns:
        clean_name = re.sub(r'.\d+$', '', name_column)
        clean_df_lst.append(clean_name)

    answers_df.columns = clean_df_lst

    lst_check_cols = ['В вашем классе принято мешать друг другу, лезть, приставать',
                      'В вашем классе принято вместе развлекаться после уроков',
                      'В вашем классе принято шутить над кем-нибудь так, чтобы смеялся весь класс',
                      'В вашем классе принято драться',
                      'В вашем классе принято ходить друг к другу в гости',
                      'В вашем классе принято заступаться за своих',
                      'В вашем классе принято обзываться',
                      'В вашем классе принято не мешать друг другу заниматься, чем захочется',
                      'В вашем классе есть кто-то кого все уважают',
                      'В вашем классе есть кто-то кого все боятся',

                      'В вашем классе есть кто-то над кем все смеются',
                      'В вашем классе есть кто-то кем часто недовольны учителя',
                      'В вашем классе есть кто-то на кого хочется быть похожим',
                      'В вашем классе есть кто-то с кем лучше не спорить',
                      'В вашем классе есть кто-то кто никогда не прогуливает',
                      'В вашем классе есть кто-то с кем даже учитель не может справиться',
                      'Как к вам в классе обращаются обычно учителя? По имени',
                      'Как к вам в классе обращаются обычно учителя? По имени и отчеству',
                      'Как к вам в классе обращаются обычно учителя? По фамилии',
                      'Как к вам в классе обращаются обычно учителя? По прозвищам',

                      'Когда в школе происходит драка, вы удивляетесь',
                      'Когда в школе происходит драка, вы не обращаете внимания, это обычное дело',
                      'Когда в школе происходит драка, вы присоединяетесь, встав на чью-то сторону',
                      'Когда в школе происходит драка, вы много это потом обсуждаете между собой в классе',
                      'Ценные вещи стараюсь не носить в школу вообще',
                      'Ценные вещи спокойно оставляю в классе',
                      'Ценные вещи можно оставить в коридоре',
                      'Ценные вещи был случай, что украли',
                      'Ценные вещи оставляю в раздевалке',
                      'Вызов к директору – это хотят за что-то похвалить',

                      'В вашей школе мат, ругательства звучат на переменах в личных разговорах',
                      'В вашей школе мат, ругательства не приняты вообще',
                      'В вашей школе курят в туалетах, под лестницами',
                      'В вашей школе стены, мебель исписанные, испачканные',
                      'Если кто-то начинает орать, драться, класс «встает на уши»; что нужно, чтобы это прекратилось? Кто-то из учеников должен сказать «хватит»',
                      'Если кто-то начинает орать, драться, класс «встает на уши»; что нужно, чтобы это прекратилось? Должен прийти директор',
                      'Если кто-то начинает орать, драться, класс «встает на уши»; что нужно, чтобы это прекратилось? Это прекратится, когда все устанут',
                      'В школе вам в целом нравится, приятно, интересно',
                      'В школе вам в целом не нравится, плохо, никто ни с кем не дружит',
                      'Перемену я провожу захожу к друзьям в другие классы',

                      'Когда ваш класс едет куда-то с учителями это обычная ситуация',
                      'Когда ваш класс едет куда-то с учителями вам это нравится, это весело',
                      'Когда ваш класс едет куда-то с учителями вы стараетесь не ездить',
                      'Когда ваш класс едет куда-то с учителями учителям это сложно, они каждый говорят, что это «в последний раз»',
                      'Ваш класс имеет репутацию отличников',
                      'Ваш класс имеет репутацию хулиганов',
                      'Ваш класс имеет репутацию самого обычного, ничем не отличающегося от других классов в школе',
                      'Ваш класс имеет репутацию класса, в котором никто не хочет быть классным руководителем'
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
        raise BadOrderBORB

    valid_values = ['да','нет']
    # Проверяем, есть ли значения, отличающиеся от указанных в списке
    lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

    for i in range(48):
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
        raise BadValueBORB

    base_df['ИО_НБ_Значение'] = answers_df.apply(calc_value_nb, axis=1)
    base_df['ИО_НБ_Диапазон'] = base_df['ИО_НБ_Значение'].apply(lambda x:calc_level_sub(x,16))

    base_df['ИО_Б_Значение'] = answers_df.apply(calc_value_b, axis=1)
    base_df['ИО_Б_Диапазон'] = base_df['ИО_Б_Значение'].apply(lambda x: calc_level_sub(x, 11))

    base_df['ИО_РО_Значение'] = answers_df.apply(calc_value_ro, axis=1)
    base_df['ИО_РО_Диапазон'] = base_df['ИО_РО_Значение'].apply(lambda x: calc_level_sub(x, 10))

    base_df['ИО_РП_Значение'] = answers_df.apply(calc_value_rp, axis=1)
    base_df['ИО_РП_Диапазон'] = base_df['ИО_РП_Значение'].apply(lambda x: calc_level_sub(x, 11))

    if len(lst_svod_cols) == 0:
        base_df['ГО_НБ_Значение'] = round(base_df['ИО_НБ_Значение'].sum() / len(base_df), 1)
        base_df['ГО_Б_Значение'] = round(base_df['ИО_Б_Значение'].sum() / len(base_df), 1)
        base_df['ГО_РО_Значение'] = round(base_df['ИО_РО_Значение'].sum() / len(base_df), 1)
        base_df['ГО_РП_Значение'] = round(base_df['ИО_РП_Значение'].sum() / len(base_df), 1)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ОРББ_ГО_НБ_Значение'] = base_df['ГО_НБ_Значение']
        part_df['ОРББ_ГО_Б_Значение'] = base_df['ГО_Б_Значение']
        part_df['ОРББ_ГО_РО_Значение'] = base_df['ГО_РО_Значение']
        part_df['ОРББ_ГО_РП_Значение'] = base_df['ГО_РП_Значение']


        part_df['ОРББ_ИО_НБ_Значение'] = base_df['ИО_НБ_Значение']
        part_df['ОРББ_ИО_НБ_Диапазон'] = base_df['ИО_НБ_Диапазон']

        part_df['ОРББ_ИО_Б_Значение'] = base_df['ИО_Б_Значение']
        part_df['ОРББ_ИО_Б_Диапазон'] = base_df['ИО_Б_Диапазон']

        part_df['ОРББ_ИО_РО_Значение'] = base_df['ИО_РО_Значение']
        part_df['ОРББ_ИО_РО_Диапазон'] = base_df['ИО_РО_Диапазон']

        part_df['ОРББ_ИО_РП_Значение'] = base_df['ИО_РП_Значение']
        part_df['ОРББ_ИО_РП_Диапазон'] = base_df['ИО_РП_Диапазон']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        # Соединяем анкетную часть с результатной
        base_df.sort_values(by='ИО_НБ_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ИО_НБ_Значение': 'ИО_НБ_Диапазон',
                        'ИО_Б_Значение': 'ИО_Б_Диапазон',
                        'ИО_РО_Значение': 'ИО_РО_Диапазон',
                        'ИО_РП_Значение': 'ИО_РП_Диапазон',
                        }

        dct_rename_svod_sub = {'ИО_НБ_Значение': 'ИО диапазона в % шкалы Небезопасность',
                               'ИО_Б_Значение': 'ИО диапазона в % шкалы Благополучие',
                               'ИО_РО_Значение': 'ИО диапазона в % шкалы Разобщенность',
                               'ИО_РП_Значение': 'ИО диапазона в % шкалы Равноправие',
                               }

        lst_sub = ['0-24%', '25-49%', '50-74%','75-100%']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        # Делаем свод  по  шкалам
        dct_svod_pr_sub = {'ИО_НБ_Значение': 'ИО_НБ_Диапазон',
                        'ИО_РО_Значение': 'ИО_РО_Диапазон',
                        }

        dct_rename_svod_pr_sub = {'ИО_НБ_Значение': 'ИО диапазона в % шкалы Небезопасность',
                               'ИО_РО_Значение': 'ИО диапазона в % шкалы Разобщенность',
                               }

        base_svod_sub_pr_df = create_union_svod(base_df, dct_svod_pr_sub, dct_rename_svod_pr_sub, lst_sub)


        dct_svod_apr_sub = {
                        'ИО_Б_Значение': 'ИО_Б_Диапазон',
                        'ИО_РП_Значение': 'ИО_РП_Диапазон',
                        }

        dct_rename_svod_apr_sub = {
                               'ИО_Б_Значение': 'ИО диапазона в % шкалы Благополучие',
                               'ИО_РП_Значение': 'ИО диапазона в % шкалы Равноправие',
                               }

        base_svod_sub_apr_df = create_union_svod(base_df, dct_svod_apr_sub, dct_rename_svod_apr_sub, lst_sub)





        avg_nb = round(base_df['ИО_НБ_Значение'].mean(), 2)
        avg_b = round(base_df['ИО_Б_Значение'].mean(), 2)
        avg_ro = round(base_df['ИО_РО_Значение'].mean(), 2)
        avg_rp = round(base_df['ИО_РП_Значение'].mean(), 2)

        avg_dct = {'Среднее значение Индивидуальная оценка шкалы Небезопасность': avg_nb,
                   'Среднее значение Индивидуальная оценка шкалы Благополучие': avg_b,
                   'Среднее значение Индивидуальная оценка шкалы Разобщенность': avg_ro,
                   'Среднее значение Индивидуальная оценка шкалы Равноправие': avg_rp,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод Предикторы': base_svod_sub_pr_df,
                   'Свод Антипредикторы': base_svod_sub_apr_df,
                   'Свод Шкалы': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix = {'ИО_НБ_Диапазон': 'НБ',
                      'ИО_Б_Диапазон': 'Б',
                      'ИО_РО_Диапазон': 'РО',
                      'ИО_РП_Диапазон': 'РП',
                      }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        return out_dct, part_df





