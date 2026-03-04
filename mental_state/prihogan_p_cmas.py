"""
Скрипт для обработки результатов теста Шкала явной тревожности для подростков CMAS А.М. Прихожан
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderCMASPP(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueCMASPP(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsCMASPP(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 65
    """
    pass

class NotReqColumn(Exception):
    """
    Исключение для обработки случая когда нет обязательных колонок Пол
    """
    pass

class BadValueSexCMASPP(Exception):
    """
    Исключение для обработки случая когда в колонке Пол есть значения отличающиеся от Мужской или Женский
    """
    pass

class BadValueAgeCMASPP(Exception):
    """
    Исключение для обработки случая когда в колонке Возраст есть значения отличающиеся от 13 лет, 14 лет, 15 лет, 16 лет
    """
    pass


def calc_value_sj(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [18,31,47,49,52,65,5,11,21,37,54]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx in (18,31,47,49,52,65):
                if value == 'ВЕРНО':
                    value_forward += 1
            elif idx in (5,11,21,37,54):
                if value == 'НЕВЕРНО':
                    value_forward += 1
    return value_forward

def calc_level_sj(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<=value <= 2:
        return f'0-2'
    elif 3 <= value <= 5:
        return f'3-5'
    elif 6 <= value <= 8:
        return f'6-8'
    else:
        return f'9-11'



def calc_value_t(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [1,3,4,7,9,10,13,16,17,20,23,24,27,28,32,34,
              36,39,41,42,43,45,46,51,53,55,57,59,63,64,
              2,6,8,12,14,15,19,22,25,26,29,30,33,
              35,38,40,44,48,50,56,58,60,61,62]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx in (1,3,4,7,9,10,13,16,17,20,23,24,27,28,32,34,
                       36,39,41,42,43,45,46,51,53,55,57,59,63,64):
                if value == 'ВЕРНО':
                    value_forward += 1
            elif idx in (2,6,8,12,14,15,19,22,25,26,29,30,33,
                         35,38,40,44,48,50,56,58,60,61,62):
                if value == 'НЕВЕРНО':
                    value_forward += 1
    return value_forward


def calc_sten_t(row:pd.Series):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    sex, age, value = row
    if sex == 'Женский':
        if age == '13 лет':
            if 0<= value <=4:
                return 1
            elif 5<= value <=8:
                return 2
            elif 9<= value <=12:
                return 3
            elif 13<= value <=16:
                return 4
            elif 17<= value <=20:
                return 5
            elif 21<= value <=24:
                return 6
            elif 25<= value <=28:
                return 7
            elif 29<= value <=32:
                return 8
            elif 33<= value <=35:
                return 9
            else:
                return 10
        elif age == '14 лет':
            if 0<= value <=5:
                return 1
            elif 6<= value <=10:
                return 2
            elif 11<= value <=14:
                return 3
            elif 15<= value <=18:
                return 4
            elif 19<= value <=23:
                return 5
            elif 24<= value <=28:
                return 6
            elif 29<= value <=32:
                return 7
            elif 33<= value <=36:
                return 8
            elif 37<= value <=40:
                return 9
            else:
                return 10
        elif age == '15 лет':
            if 0<= value <=4:
                return 1
            elif 5<= value <=7:
                return 2
            elif 8<= value <=10:
                return 3
            elif 11<= value <=13:
                return 4
            elif 14<= value <=17:
                return 5
            elif 18<= value <=21:
                return 6
            elif 22<= value <=25:
                return 7
            elif 26<= value <=29:
                return 8
            elif 30<= value <=32:
                return 9
            else:
                return 10
        elif age == '16 лет':

            if 0<= value <=3:
                return 1
            elif 4<= value <=6:
                return 2
            elif 7<= value <=10:
                return 3
            elif 11<= value <=14:
                return 4
            elif 15<= value <=18:
                return 5
            elif 19<= value <=23:
                return 6
            elif 24<= value <=28:
                return 7
            elif 29<= value <=32:
                return 8
            elif 33<= value <=37:
                return 9
            else:
                return 10
    else:
        if age == '13 лет':
            if 0<= value <=3:
                return 1
            elif 4<= value <=7:
                return 2
            elif 8<= value <=11:
                return 3
            elif 12<= value <=15:
                return 4
            elif 16<= value <=19:
                return 5
            elif 20<= value <=23:
                return 6
            elif 24<= value <=26:
                return 7
            elif 27<= value <=29:
                return 8
            elif 30<= value <=32:
                return 9
            else:
                return 10
        elif age == '14 лет':
            if 0<= value <=3:
                return 1
            elif 4<= value <=7:
                return 2
            elif 8<= value <=10:
                return 3
            elif 11<= value <=14:
                return 4
            elif 15<= value <=18:
                return 5
            elif 19<= value <=21:
                return 6
            elif 22<= value <=24:
                return 7
            elif 25<= value <=27:
                return 8
            elif 28<= value <=30:
                return 9
            else:
                return 10
        elif age =='15 лет':
            if 0<= value <=3:
                return 1
            elif 4<= value <=6:
                return 2
            elif 7<= value <=10:
                return 3
            elif 11<= value <=14:
                return 4
            elif 15<= value <=17:
                return 5
            elif 18<= value <=20:
                return 6
            elif 21<= value <=24:
                return 7
            elif 25<= value <=28:
                return 8
            elif 29<= value <=33:
                return 9
            else:
                return 10
        elif age == '16 лет':
            if 0<= value <=2:
                return 1
            elif 3<= value <=5:
                return 2
            elif 6<= value <=8:
                return 3
            elif 9<= value <=11:
                return 4
            elif 12<= value <=15:
                return 5
            elif 16<= value <=18:
                return 6
            elif 19<= value <=22:
                return 7
            elif 23<= value <=26:
                return 8
            elif 27<= value <=30:
                return 9
            else:
                return 10


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 1<=value <= 2:
        return f'низкий'
    elif 3 <= value <= 6:
        return f'нормальный'
    elif 7 <= value <= 8:
        return f'несколько повышенный'
    elif value == 9:
        return f'явно повышенный'
    else:
        return f'очень высокий'


def create_result_p_cmas_prihogan(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level_sj = ['0-2', '3-5', '6-8','9-11']

    lst_reindex_one_level_sj_cols = lst_svod_cols.copy()
    lst_reindex_one_level_sj_cols.extend(['0-2', '3-5', '6-8','9-11',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_sj_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'СЖ_Значение',
                                                    'СЖ_Диапазон',
                                                    lst_reindex_one_level_sj_cols, lst_level_sj)

    lst_t_sub = ['низкий', 'нормальный', 'несколько повышенный','явно повышенный','очень высокий']

    lst_reindex_one_level_t_cols = lst_svod_cols.copy()
    lst_reindex_one_level_t_cols.extend(['низкий', 'нормальный', 'несколько повышенный','явно повышенный','очень высокий',
                                          'Итого'])  # Основная шкала

    svod_count_one_level_t_df = calc_count_scale(base_df, lst_svod_cols,
                                                  'Т_Стен',
                                                  'Т_Уровень',
                                                  lst_reindex_one_level_t_cols, lst_t_sub)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                          'СЖ_Значение','Т_Стен'
                                      ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['СЖ_Значение','Т_Стен'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'СЖ_Значение': 'Ср. значение Социальная желательность',
                            'Т_Стен': 'Ср. стен Тревожность',
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
                    f'СЖ {out_name}': svod_count_one_level_sj_df,
                    f'Т {out_name}': svod_count_one_level_t_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_sj_cols = [lst_svod_cols[idx],'0-2', '3-5', '6-8','9-11',
                                                  'Итого']

            svod_count_column_level_sj_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'СЖ_Значение',
                                                               'СЖ_Диапазон',
                                                               lst_reindex_column_level_sj_cols, lst_level_sj)

            lst_reindex_column_level_t_cols = [lst_svod_cols[idx],'низкий', 'нормальный', 'несколько повышенный','явно повышенный','очень высокий',
                                                  'Итого']

            svod_count_column_level_t_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                               'Т_Стен',
                                                               'Т_Уровень',
                                                               lst_reindex_column_level_t_cols, lst_t_sub)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=[
                                                  'СЖ_Значение', 'Т_Стен'
                                              ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['СЖ_Значение', 'Т_Стен'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'СЖ_Значение': 'Ср. значение Социальная желательность',
                                    'Т_Стен': 'Ср. стен Тревожность',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)
            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'СЖ {name_column}': svod_count_column_level_sj_df,
                            f'Т {name_column}': svod_count_column_level_t_df,
                            })
        return out_dct










def processing_p_cmas_prihog(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 65:  # проверяем количество колонок с вопросами
            raise BadCountColumnsCMASPP

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst


        # Проверяем наличие колонок Пол и Возраст
        diff_req_cols = {'Пол', 'Возраст'}.difference(set(base_df.columns))
        if len(diff_req_cols) != 0:
            raise NotReqColumn

        # на случай пустых
        base_df['Пол'].fillna('Не заполнено', inplace=True)
        # очищаем от лишних пробелов
        base_df['Пол'] = base_df['Пол'].apply(str.strip)

        base_df['Возраст'].fillna('Не заполнено', inplace=True)
        # очищаем от лишних пробелов
        base_df['Возраст'] = base_df['Возраст'].apply(str.strip)

        # Проверяем на пол
        diff_sex = set(base_df['Пол'].unique()).difference({'Мужской', 'Женский'})
        if len(diff_sex) != 0:
            raise BadValueSexCMASPP

        # Проверяем на возраст
        diff_age = set(base_df['Возраст'].unique()).difference({'13 лет', '14 лет', '15 лет', '16 лет'})
        if len(diff_age) != 0:
            raise BadValueAgeCMASPP

        lst_check_cols = ['Тебе трудно сосредоточиться на работе, выполнении задания',
                          'Ты можешь долго работать, не уставая',
                          'Тебя раздражает, если за тобой наблюдают, когда ты что-нибудь делаешь',
                          'Ты легко краснеешь',
                          'Не все люди, которых ты знаешь, тебе нравятся',
                          'Ты редко чувствуешь сильное сердцебиение',
                          'Временами ты чувствуешь, что ты хуже других',
                          'Ты очень редко смущаешься',
                          'Даже если все хорошо, ты ощущаешь какое-то беспокойство: вдруг произойдет что-то плохое',
                          'Иногда тебе хочется убежать, скрыться, хотя никаких видимых причин для этого нет',

                          'Нередко ты говоришь о том, в чем не разбираешься',
                          'Ты уверен, что ни в чем не хуже других',
                          'Ты часто чувствуешь, что другие люди недовольны тобой, осуждают тебя, хотя и не показывают этого',
                          'Ты почти ничего не боишься',
                          'Тебе нравится думать о своем будущем',
                          'Тебе очень трудно принять решение',
                          'Ты часто ловишь себя на том, что тебя что-то беспокоит, а что – непонятно',
                          'Ты всегда соблюдаешь правила',
                          'Тебя трудно разозлить, вывести из себя',
                          'Ты часто чувствуешь, что тебе трудно дышать',

                          'Иногда у тебя бывают такие мысли, о которых лучше никому не рассказывать',
                          'У тебя редко потеют руки',
                          'У тебя проблемы с желудком',
                          'Перед важными событиями у тебя пропадает аппетит, буквально «кусок в горло не лезет»',
                          'Тебе часто везет, про тебя можно сказать, что ты «везучий человек»',
                          'Чаще всего тебе безразлично, что думают о тебе окружающие',
                          'Часто тебе трудно глотать',
                          'Ты часто беспокоишься из-за того, что, как выясняется позже, не имеет никакого значения',
                          'Тебя трудно обидеть',
                          'Почти все свои поступки ты считаешь правильными',

                          'Ты никогда не хвастаешься',
                          'Когда ты думаешь о своем будущем, ты не можешь отделаться от мыслей о возможных неприятностях, несчастьях, которые могут с тобой произойти',
                          'Обычно ты легко засыпаешь',
                          'Ты сильно переживаешь из-за отметок',
                          'Обычно ты не боишься опоздать, не успеть что-нибудь сделать к сроку',
                          'Ты нередко испытываешь неуверенность в себе',
                          'Иногда ты обманываешь',
                          'Ты редко испытываешь чувство одиночества',
                          'Ты боишься осуждения со стороны других людей',
                          'Ты не боишься темноты',

                          'Ты нередко чувствуешь свою неуклюжесть, неловкость',
                          'Ты часто ощущаешь скованность, напряженность',
                          'Порой ты не можешь заснуть, потому что боишься увидеть страшный сон',
                          'Ты редко сожалеешь о своих поступках',
                          'У тебя часто болит голова',
                          'Ты боишься, что с родителями что-нибудь случится',
                          'Ты всегда соблюдаешь режим дня',
                          'Тебе нравится выступать на сцене, говорить публично, делать доклады перед классом',
                          'Ты никогда не откладываешь на завтра то, что нужно сделать сегодня',
                          'Тебя трудно вывести из себя',

                          'Тебе часто кажется, что другие ребята смеются над тобой',
                          'Ты со всеми ведешь себя вежливо',
                          'Нередко тебе кажется, что ты ни на что не годишься',
                          'Ты не всегда сдерживаешь свои обещания',
                          'Твои тревоги и опасения часто мешают тебе добиться успеха в учебе и других делах',
                          'Тебя не беспокоит состояние здоровья',
                          'Ты часто чувствуешь собственную беспомощность',
                          'Ты не боишься лечить зубы',
                          'Ты нередко испытываешь беспричинный страх',
                          'Ты не расстраиваешься из-за пустяков',

                          'Тебя мало беспокоят возможные неудачи',
                          'Ты любишь конкурсы, состязания',
                          'Когда приходится ждать, ты волнуешься, не можешь найти себе места',
                          'Тебя часто мучают ночные кошмары',
                          'Ты никогда не сплетничаешь',
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
            raise BadOrderCMASPP

        valid_values = ['ВЕРНО', 'НЕВЕРНО']
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(65):
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
            raise BadValueCMASPP

        base_df['СЖ_Значение'] = answers_df.apply(calc_value_sj, axis=1)
        base_df['СЖ_Диапазон'] = base_df['СЖ_Значение'].apply(calc_level_sj)

        base_df['Т_Значение'] = answers_df.apply(calc_value_t, axis=1)
        base_df['Т_Стен'] = base_df[['Пол', 'Возраст', 'Т_Значение']].apply(calc_sten_t, axis=1)
        base_df['Т_Уровень'] = base_df['Т_Стен'].apply(calc_level)


        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ПВШЯТП_СЖ_Значение'] = base_df['СЖ_Значение']
        part_df['ПВШЯТП_СЖ_Диапазон'] = base_df['СЖ_Диапазон']

        part_df['ПВШЯТП_Т_Значение'] = base_df['Т_Значение']
        part_df['ПВШЯТП_Т_Стен'] = base_df['Т_Стен']
        part_df['ПВШЯТП_Т_Уровень'] = base_df['Т_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Т_Значение', inplace=True, ascending=False)
        # Делаем свод по шкале Социальная желаемость
        dct_svod_sj_sub = {'СЖ_Значение': 'СЖ_Диапазон',
                           }

        dct_rename_svod_sj_sub = {'СЖ_Значение': 'Диапазон Социальная желательность',
                                  }

        lst_sj_sub = ['0-2', '3-5', '6-8', '9-11']

        base_svod_sj_sub_df = create_union_svod(base_df, dct_svod_sj_sub, dct_rename_svod_sj_sub, lst_sj_sub)

        # Делаем свод по шкале Тревожность
        dct_svod_t_sub = {'Т_Значение': 'Т_Уровень',
                          }

        dct_rename_svod_t_sub = {'Т_Значение': 'Тревожность',
                                 }

        lst_t_sub = ['низкий', 'нормальный', 'несколько повышенный', 'явно повышенный', 'очень высокий']

        base_svod_t_sub_df = create_union_svod(base_df, dct_svod_t_sub, dct_rename_svod_t_sub, lst_t_sub)

        avg_sj = round(base_df['СЖ_Значение'].mean(), 2)
        avg_t = round(base_df['Т_Стен'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Социальной желательности': avg_sj,
                   'Средний СТЕН шкалы Тревожность ': avg_t,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод СЖ': base_svod_sj_sub_df,
                   'Свод Т': base_svod_t_sub_df,
                   'Среднее': avg_df,
                   }

        dct_prefix_sj = {'СЖ_Диапазон': 'СЖ',
                         }

        out_dct = create_list_on_level(base_df, out_dct, lst_sj_sub, dct_prefix_sj)

        dct_prefix_t = {'Т_Уровень': 'Т',
                        }
        out_dct = create_list_on_level(base_df, out_dct, lst_t_sub, dct_prefix_t)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_p_cmas_prihogan(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderCMASPP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Подростковый вариант шкалы явной тревожности CMAS Прихожан обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueCMASPP:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Подростковый вариант шкалы явной тревожности CMAS Прихожан обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsCMASPP:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Подростковый вариант шкалы явной тревожности CMAS Прихожан\n'
                             f'Должно быть 65 колонок с ответами')

    except NotReqColumn:
        messagebox.showerror('Лахеcис',
                             f'В таблице отсутствуют обязательные колонки {diff_req_cols}\n'
                             f'В таблице обязательно должны быть колонка с названием Пол и колонка с названием Возраст')

    except BadValueSexCMASPP:
        messagebox.showerror('Лахеcис',
                             f'В колонке Пол найдены значения отличающиеся от допустимых {diff_sex}\n'
                             f'Допускаются значения: Мужской и Женский\n'
                             f'Прочитайте страницу 1 и 2 файла инструкции к тесту Подростковый вариант шкалы явной тревожности CMAS Прихожан')
    except BadValueAgeCMASPP:
        messagebox.showerror('Лахеcис',
                             f'В колонке Возраст найдены значения отличающиеся от допустимых {diff_age}\n'
                             f'Допускаются значения: 13 лет, 14 лет,15 лет, 16 лет\n'
                             f'Прочитайте страницу 1 и 2 файла инструкции к тесту Подростковый вариант шкалы явной тревожности CMAS Прихожан')







