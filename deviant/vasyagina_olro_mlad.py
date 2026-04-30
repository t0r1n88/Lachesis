"""
Скрипт для обработки результатов Скрининговая методика оценки личностных ресурсов обучающихся Васягина, Григорян, Баринова форма 1 для 5-8 классов
"""

import pandas as pd
import re
from tkinter import messagebox
from lachesis_support_functions import round_mean_two,calc_count_scale,create_union_svod, create_list_on_level

class BadOrderOLROVML(Exception):
    """
    Исключение для обработки случая когда колонки не совпадают
    """
    pass


class BadValueOLROVML(Exception):
    """
    Исключение для неправильных значений в вариантах ответов
    """
    pass

class BadCountColumnsOLROVML(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 46
    """
    pass


def calc_value_k(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [5,12,16,24,36,43]
    lst_neg = []
    value_forward = 0  # результат
    for idx, value in enumerate(row,1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 3
                elif value == 1:
                    value_forward += 2
                elif value == 2:
                    value_forward += 1
                elif value == 3:
                    value_forward += 0
    return value_forward

def calc_level_k(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if 0<= value <= 6:
        return f'0-6'
    elif 7 <= value <= 11:
        return f'7-11'
    elif 12 <= value <= 14:
        return f'12-14'
    else:
        return f'15-18'


def calc_value_lr(row):
    """
    Функция для подсчета значения
    :return: число
    """
    lst_pr = [3,9,13,18,22,23,25,26,34,42,46,
              1,2,4,6,7,8,10,11,14,15,17,19,20,21,27,28,29,
              30,31,32,33,35,37,38,39,40,41,44,45]
    lst_neg = [ 1,2,4,6,7,8,10,11,14,15,17,19,20,21,27,28,29,
              30,31,32,33,35,37,38,39,40,41,44,45]
    value_forward = 0  # результат
    for idx, value in enumerate(row, 1):
        if idx in lst_pr:
            if idx not in lst_neg:
                value_forward += value
            else:
                if value == 0:
                    value_forward += 3
                elif value == 1:
                    value_forward += 2
                elif value == 2:
                    value_forward += 1
                elif value == 3:
                    value_forward += 0
    return value_forward


def calc_level_lr(value):
    """
    Функция для подсчета уровня
    :param value:
    :return:
    """
    if value <= 50:
        return f'низкий уровень'
    elif 51 <= value <= 87:
        return f'средний уровень'
    else:
        return f'высокий уровень'


def create_result_orlo_vas_ml(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_l = ['0-6', '7-11', '12-14','15-18']

    lst_reindex_one_level_l_cols = lst_svod_cols.copy()
    lst_reindex_one_level_l_cols.extend(['0-6', '7-11', '12-14','15-18',
                                       'Итого'])  # Основная шкала

    svod_count_one_level_l_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'К_Значение',
                                                 'К_Диапазон',
                                                 lst_reindex_one_level_l_cols, lst_l)

    lst_level = ['высокий уровень','средний уровень','низкий уровень']

    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend(['высокий уровень','средний уровень','низкий уровень',
                                       'Итого'])  # Основная шкала

    # АД
    svod_count_one_level_s_df = calc_count_scale(base_df, lst_svod_cols,
                                                 'ЛР_Значение',
                                                 'ЛР_Уровень',
                                                 lst_reindex_one_level_cols, lst_level)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['К_Значение',
                                              'ЛР_Значение',
                                              ],
                                      aggfunc=round_mean_two)
    svod_mean_one_df.reset_index(inplace=True)

    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['К_Значение',
                            'ЛР_Значение',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'К_Значение': 'Ср. Шкала контроля',
                            'ЛР_Значение': 'Ср. Шкала Личностные ресурсы',
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
                    f'К {out_name}': svod_count_one_level_l_df,
                    f'ЛР {out_name}': svod_count_one_level_s_df,
                    })

    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            lst_reindex_column_level_l_cols = [lst_svod_cols[idx], '0-6', '7-11', '12-14','15-18',
                                             'Итого']

            svod_count_column_level_l_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                         'К_Значение',
                                                         'К_Диапазон',
                                                         lst_reindex_column_level_l_cols, lst_l)

            lst_reindex_column_level_cols = [lst_svod_cols[idx], 'высокий уровень','средний уровень','низкий уровень',
                                             'Итого']

            # АД
            svod_count_column_level_s_df = calc_count_scale(base_df, lst_svod_cols[idx],
                                                            'ЛР_Значение',
                                                            'ЛР_Уровень',
                                                            lst_reindex_column_level_cols, lst_level)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['К_Значение',
                                                      'ЛР_Значение',
                                                      ],
                                              aggfunc=round_mean_two)
            svod_mean_column_df.reset_index(inplace=True)

            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['К_Значение',
                                    'ЛР_Значение',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'К_Значение': 'Ср. Шкала контроля',
                                    'ЛР_Значение': 'Ср. Шкала Личностные ресурсы',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            # Готовим наименование
            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]
            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'К {name_column}': svod_count_column_level_l_df,
                            f'ЛР {name_column}': svod_count_column_level_s_df,
                            })
        return out_dct






def processing_olro_vas_mlad(base_df: pd.DataFrame, answers_df: pd.DataFrame, lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 46:  # проверяем количество колонок с вопросами
            raise BadCountColumnsOLROVML

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        lst_check_cols = ['Я веду себя не так, как хочу, а так, как ждут от меня окружающие',
                          'Часто я подчиняюсь сложившимся обстоятельствам',
                          'Я всегда контролирую ситуацию настолько, насколько это необходимо',
                          'Иногда от усталости я теряю интерес ко всему',
                          'Меня любят все мои приятели',
                          'Я часто сомневаюсь в собственных решениях',
                          'Временами все, что я делаю, кажется мне бесполезным',
                          'Иногда я мечтаю о спокойной жизни',
                          'Мне нравится моя постоянная занятость',
                          'Меня раздражают события, вынуждающие меня менять свой распорядок дня',

                          'Даже хорошо выспавшись, я с трудом заставляю себя встать с постели',
                          'Я всегда делаю только то, что нравится другим',
                          'Мне нравится ставить перед собой труднодостижимые цели и добиваться их',
                          'Бывает так, что непредвиденные трудности меня утомляют',
                          'Мысли о будущем временами пугают меня',
                          'Я никогда не вру',
                          'Часто вечером я чувствую себя совершенно без сил',
                          'Мне нравится заводить новые знакомства',
                          'Часто проблемы кажутся мне неразрешимыми',
                          'Сейчас мне было бы легче жить, если бы в прошлом у меня было меньше проблем и разочарований',

                          'Временами я ощущаю свою ненужность',
                          'У меня есть уверенность, что все задуманное я могу воплотить в жизнь',
                          'Испытав неудачу, я все равно буду пытаться достичь своей цели',
                          'Я никогда не откладываю на завтра то, что следует сделать сегодня',
                          'Обычно окружающие внимательно меня слушают',
                          'Я всегда знаю, чем заняться',
                          'Кажется, что жизнь проходит мимо меня',
                          'Я откладываю сложные дела на потом',
                          'Окружающие меня недооценивают',
                          'Бывает, жизнь кажется мне скучной и неинтересной',

                          'Мои мечты редко сбываются',
                          'Я часто сожалею о сделанном',
                          'Если бы была возможность, я бы многое изменил в прошлом',
                          'Меня уважают за упорство и непреклонность',
                          'Я не могу повлиять на неожиданные проблемы',
                          'Я всегда говорю только правду',
                          'Я довольно часто откладываю на завтра то, что трудноосуществимо, или то, в чем нет уверенности',
                          'Бывает, я чувствую свою ненужность даже в кругу друзей',
                          'Порой мне кажется, что все мои усилия бесполезны',
                          'Я с трудом сближаюсь с другими людьми',

                          'Часто я предпочитаю «плыть» по течению',
                          'Я с удовольствием воплощаю новые идеи',
                          'Я всегда придерживаюсь общепринятых правил поведения',
                          'Часто я не довожу начатое до конца',
                          'Иногда от количества проблем у меня опускаются руки',
                          'Обычно я учусь и работаю с удовольствием',
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
            raise BadOrderOLROVML

        # словарь для замены слов на числа
        dct_replace_value = {'нет': 0,
                             'скорее нет, чем да': 1,
                             'скорее да, чем нет': 2,
                             'да': 3,
                             }
        valid_values = [0, 1, 2, 3]
        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов
        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(46):
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
            raise BadValueOLROVML

        base_df['К_Значение'] = answers_df.apply(calc_value_k, axis=1)
        base_df['К_Диапазон'] = base_df['К_Значение'].apply(calc_level_k)

        base_df['ЛР_Значение'] = answers_df.apply(calc_value_lr, axis=1)
        base_df['ЛР_Уровень'] = base_df['ЛР_Значение'].apply(calc_level_lr)

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()

        # Основные шкалы
        part_df['ОЛРО_ВГБ_МЛ_К_Значение'] = base_df['К_Значение']
        part_df['ОЛРО_ВГБ_МЛ_К_Диапазон'] = base_df['К_Диапазон']

        part_df['ОЛРО_ВГБ_МЛ_ЛР_Значение'] = base_df['ЛР_Значение']
        part_df['ОЛРО_ВГБ_МЛ_ЛР_Диапазон'] = base_df['ЛР_Уровень']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)  # Датафрейм для проверки

        base_df.sort_values(by='К_Значение', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_l = {'К_Значение': 'К_Диапазон',
                      }

        dct_rename_svod_l = {'К_Значение': 'Шкала контроля (социальная желательность)',
                             }

        lst_l = ['0-6', '7-11', '12-14','15-18']

        base_svod_l_df = create_union_svod(base_df, dct_svod_l, dct_rename_svod_l, lst_l)

        # Делаем свод  по  шкалам
        dct_svod_sub = {'ЛР_Значение': 'ЛР_Уровень',
                        }

        dct_rename_svod_sub = {'ЛР_Значение': 'Шкала личностных ресурсов"',
                               }

        lst_sub = [ 'высокий уровень','средний уровень','низкий уровень']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_sub)

        avg_vcha = round(base_df['К_Значение'].mean(), 2)
        avg_o = round(base_df['ЛР_Значение'].mean(), 2)

        avg_dct = {'Среднее значение шкалы Контроля': avg_vcha,
                   'Среднее значение шкалы Личностные ресурсы': avg_o,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df,
                   'Список для проверки': out_answer_df,
                   'Свод К': base_svod_l_df,
                   'Свод ЛР': base_svod_sub_df,
                   'Среднее': avg_df,
                   }

        dct_l = {
            'К_Диапазон': 'К',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_l, dct_l)

        dct_prefix = {
            'ЛР_Уровень': 'ЛР',
        }

        out_dct = create_list_on_level(base_df, out_dct, lst_sub, dct_prefix)

        """
                        Сохраняем в зависимости от необходимости делать своды по определенным колонкам
                        """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df

        else:
            out_dct = create_result_orlo_vas_ml(base_df, out_dct, lst_svod_cols)
            return out_dct, part_df

    except BadOrderOLROVML:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Скрининговая методика оценки личностных ресурсов обучающихся Васягина, Григорян, Баринова форма 1 для 5-8 классов  обнаружены неправильные вопросы. Проверьте названия колонок с вопросами:\n'
                             f'{error_order_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вопросов из руководства пользователя программы Лахесис.')
    except BadValueOLROVML:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Скрининговая методика оценки личностных ресурсов обучающихся Васягина, Григорян, Баринова форма 1 для 5-8 классов  обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message[:5000]}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsOLROVML:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Скрининговая методика оценки личностных ресурсов обучающихся Васягина, Григорян, Баринова форма 1 для 5-8 классов \n'
                             f'Должно быть 46 колонок с ответами')















