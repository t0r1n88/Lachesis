"""
Скрипт для обработки результатов теста Шкала проявлений тревоги Тейлор, TMAS Адаптация В.Г. Норакидзе

"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderTMASN(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueTMASN(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsTMASN(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 60
    """
    pass

def calc_value_sj(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [2,10,55,
              16,20,27,29,41,51,59]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx in (2,10,55):
                if value == 'ВЕРНО':
                    value_forward += 1
            elif idx in (16,20,27,29,41,51,59):
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
        return f'9-10'


def calc_value_t(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [6,7,9,11,12,13,15,18,21,23,24,25,26,28,
              30,31,32,33,34,35,36,37,38,40,42,44,45,46,47,48,49,50,51,54,56,60,
              1,3,4,5,8,14,17,19,22,39,43,52,57,58]
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx in (6,7,9,11,12,13,15,18,21,23,24,25,26,28,
              30,31,32,33,34,35,36,37,38,40,42,44,45,46,47,48,49,50,51,54,56,60):
                if value == 'ВЕРНО':
                    value_forward += 1
            elif idx in (1,3,4,5,8,14,17,19,22,39,43,52,57,58):
                if value == 'НЕВЕРНО':
                    value_forward += 1
    return value_forward


def calc_level(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<=value <= 5:
        return f'низкий'
    elif 6 <= value <= 15:
        return f'средний ближе к низкому'
    elif 16 <= value <= 25:
        return f'средний ближе к высокому'
    elif 26<=value == 40:
        return f'высокий'
    else:
        return f'очень высокий'


def create_list_on_level_tmas(base_df:pd.DataFrame,out_dct:dict,lst_level:list,dct_prefix:dict):
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
                if level == 'средний ближе к низкому':
                    level = 'ближе к низкому'
                elif level == 'средний ближе к высокому':
                    level = 'ближе к высокому'
                dct_level[f'{dct_prefix[key]}. {level}'] = temp_df
        out_dct.update(dct_level)

    return out_dct


def create_result_tmas_teyl_nor(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """

    lst_level_sj = ['0-2', '3-5', '6-8','9-10']

    lst_reindex_one_level_sj_cols = lst_svod_cols.copy()
    lst_reindex_one_level_sj_cols.extend(['0-2', '3-5', '6-8','9-10',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_sj_df = calc_count_scale(base_df, lst_svod_cols,
                                                    'СЖ_Значение',
                                                    'СЖ_Диапазон',
                                                    lst_reindex_one_level_sj_cols, lst_level_sj)

    lst_t_sub = ['низкий', 'средний ближе к низкому', 'средний ближе к высокому','высокий','очень высокий']
    lst_reindex_one_level_t_cols = lst_svod_cols.copy()
    lst_reindex_one_level_t_cols.extend(
        ['низкий', 'средний ближе к низкому', 'средний ближе к высокому','высокий','очень высокий',
         'Итого'])  # Основная шкала

    svod_count_one_level_t_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'Т_Значение',
                                                 'Т_Уровень',
                                                 lst_reindex_one_level_t_cols, lst_t_sub)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=[
                                          'СЖ_Значение', 'Т_Значение'
                                      ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['СЖ_Значение', 'Т_Значение'
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'СЖ_Значение': 'Ср. значение Социальная желательность',
                            'Т_Значение': 'Ср. значение Тревожность',
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
            lst_reindex_column_level_sj_cols = [lst_svod_cols[idx], '0-2', '3-5', '6-8','9-10',
                                                'Итого']

            svod_count_column_level_sj_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                             'СЖ_Значение',
                                                             'СЖ_Диапазон',
                                                             lst_reindex_column_level_sj_cols, lst_level_sj)

            lst_reindex_column_level_t_cols = [lst_svod_cols[idx], 'низкий', 'средний ближе к низкому', 'средний ближе к высокому','высокий','очень высокий',
                                               'Итого']

            svod_count_column_level_t_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'Т_Значение',
                                                            'Т_Уровень',
                                                            lst_reindex_column_level_t_cols, lst_t_sub)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                                 index=[lst_svod_cols[idx]],
                                                 values=[
                                                     'СЖ_Значение', 'Т_Значение'
                                                 ],
                                                 aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['СЖ_Значение', 'Т_Значение'
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'СЖ_Значение': 'Ср. значение Социальная желательность',
                                    'Т_Значение': 'Ср. значение Тревожность',
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


def processing_tmas_teylor_nor(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 60:  # проверяем количество колонок с вопросами
            raise BadCountColumnsTMASN

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я могу долго работать, не уставая',
                          'Я всегда выполняю свои обещания, не считаясь с тем, удобно мне это или нет',
                          'Обычно руки и ноги у меня теплые',
                          'У меня редко болит голова',
                          'Я уверен в своих силах',
                          'Ожидание меня нервирует',
                          'Порой мне кажется, что я ни на что не годен',
                          'Обычно я чувствую себя вполне счастливым',
                          'Я не могу сосредоточиться на чем-либо одном',
                          'В детстве я всегда немедленно и безропотно выполнял все то, что мне поручали',

                          'Раз в месяц или чаще у меня бывает расстройство желудка',
                          'Я часто ловлю себя на том, что меня что-то тревожит',
                          'Я думаю, что я не более нервный, чем большинство других людей',
                          'Я не слишком застенчив',
                          'Жизнь для меня почти всегда связана с большим напряжением',
                          'Иногда бывает, что я говорю о вещах, в которых не разбираюсь',
                          'Я краснею не чаще, чем другие',
                          'Я часто расстраиваюсь из-за пустяков',
                          'Я редко замечаю у себя сердцебиение или одышку',
                          'Не все люди, которых я знаю, мне нравятся',

                          'Я не могу уснуть, если меня что-то тревожит',
                          'Обычно я спокоен и меня нелегко расстроить',
                          'Меня часто мучают ночные кошмары',
                          'Я склонен все принимать слишком всерьез',
                          'Когда я нервничаю, у меня усиливается потливость',
                          'У меня беспокойный и прерывистый сон',
                          'В играх я предпочитаю скорее выигрывать, чем проигрывать',
                          'Я более чувствителен, чем большинство других людей',
                          'Бывает, что нескромные шутки и остроты вызывают у меня смех',
                          'Я хотел бы быть так же доволен своей жизнью, как, вероятно, довольны другие',

                          'Мой желудок сильно беспокоит меня',
                          'Я постоянно озабочен своими материальными и служебными делами',
                          'Я настороженно отношусь к некоторым людям, хотя знаю, что они не могут причинить мне вреда',
                          'Мне порой кажется, что передо мной нагромождены такие трудности, которых мне не преодолеть',
                          'Я легко прихожу в замешательство',
                          'Временами я становлюсь настолько возбужденным, что это мешает мне заснуть',
                          'Я предпочитаю уклоняться от конфликтов и затруднительных положений',
                          'У меня бывают приступы тошноты и рвоты',
                          'Я никогда не опаздывал на свидания или работу',
                          'Временами я определенно чувствую себя бесполезным',

                          'Иногда мне хочется выругаться',
                          'Почти всегда я испытываю тревогу в связи с чем-либо или с кем-либо',
                          'Меня беспокоят возможные неудачи',
                          'Я часто боюсь, что вот-вот покраснею',
                          'Меня нередко охватывает отчаяние',
                          'Я — человек нервный и легко возбудимый',
                          'Я часто замечаю, что мои руки дрожат, когда, я пытаюсь что-нибудь сделать',
                          'Я почти всегда испытываю чувство голода',
                          'Мне не хватает уверенности в себе',
                          'Я легко потею даже в прохладные дни',

                          'Я часто мечтаю о таких вещах, о которых лучше никому не рассказывать',
                          'У меня очень редко болит живот',
                          'Я считаю, что мне очень трудно сосредоточиться на какой-либо задаче или работе',
                          'У меня бывают периоды такого сильного беспокойства, что я не могу долго усидеть на одном месте',
                          'Я всегда отвечаю на письма сразу же после прочтения',
                          'Я легко расстраиваюсь',
                          'Практически я никогда не краснею',
                          'У меня гораздо меньше различных опасений и страхов, чем у моих друзей и знакомых',
                          'Бывает, что я откладываю на завтра то, что следует сделать сегодня',
                          'Обычно я работаю с большим напряжением',
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
            raise BadOrderTMASN

        valid_values = ['ВЕРНО', 'НЕВЕРНО']
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
            raise BadValueTMASN

        base_df['СЖ_Значение'] = answers_df.apply(calc_value_sj, axis=1)
        base_df['СЖ_Диапазон'] = base_df['СЖ_Значение'].apply(calc_level_sj)

        base_df['Т_Значение'] = answers_df.apply(calc_value_t, axis=1)
        base_df['Т_Уровень'] = base_df['Т_Значение'].apply(calc_level)


        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        part_df['ШПТТН_СЖ_Значение'] = base_df['СЖ_Значение']
        part_df['ШПТТН_СЖ_Диапазон'] = base_df['СЖ_Диапазон']

        part_df['ШПТТН_Т_Значение'] = base_df['Т_Значение']
        part_df['ШПТТН_Т_Уровень'] = base_df['Т_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='Т_Значение', inplace=True, ascending=False)

        # Делаем свод по шкале Социальная желаемость
        dct_svod_sj_sub = {'СЖ_Значение': 'СЖ_Диапазон',
                           }

        dct_rename_svod_sj_sub = {'СЖ_Значение': 'Диапазон Социальная желательность',
                                  }

        lst_sj_sub = ['0-2', '3-5', '6-8','9-10']

        base_svod_sj_sub_df = create_union_svod(base_df, dct_svod_sj_sub, dct_rename_svod_sj_sub, lst_sj_sub)

        # Делаем свод по шкале Тревожность
        dct_svod_t_sub = {'Т_Значение': 'Т_Уровень',
                          }

        dct_rename_svod_t_sub = {'Т_Значение': 'Тревожность',
                                 }

        lst_t_sub = ['низкий', 'средний ближе к низкому', 'средний ближе к высокому','высокий','очень высокий']

        base_svod_t_sub_df = create_union_svod(base_df, dct_svod_t_sub, dct_rename_svod_t_sub, lst_t_sub)

        avg_sj = round(base_df['СЖ_Значение'].mean(), 2)
        avg_t = round(base_df['Т_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Социальной желательности': avg_sj,
                   'Средние значение шкалы Тревожность ': avg_t,
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
        out_dct = create_list_on_level_tmas(base_df, out_dct, lst_t_sub, dct_prefix_t)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_tmas_teyl_nor(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df


    except BadOrderTMASN:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала проявлений тревоги Тейлор Норакидзе обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueTMASN:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала проявлений тревоги Тейлор Норакидзе обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsTMASN:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала проявлений тревоги Тейлор Норакидзе\n'
                             f'Должно быть 60 колонок с ответами')