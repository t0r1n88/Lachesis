"""
Скрипт для обработки теста Шкала депрессии Бека
"""
from lachesis_support_functions import round_mean,create_union_svod

import pandas as pd
import re
from tkinter import messagebox




class BadValueBekDepress(Exception):
    """
    Исключение для обработки неправильных вариантов ответов для теста
    """
    pass

class BadCountColumnsBekDepress(Exception):
    """
    Исключение для обработки случая если количество колонок не равно 52
    """
    pass

def calc_value_bek_depress(ser:pd.Series):
    """
    Функция для подсчета баллов по каждой группе вопросов
    """
    lst_values = ser.tolist() # превращаем в список
    first = lst_values[0] # первое утверждение
    second = lst_values[1] # второе утверждение
    third = lst_values[2] # третье утверждение
    four = lst_values[3] # четвертое утверждение

    # считаем количество ответов в диапазоне
    count_answer_lst = [value for value in lst_values if pd.notna(value)] # отбрасываем незаполненное
    if len(count_answer_lst) > 2:
        # возвращаем либо второй либо третий вариант поскольку всего овтетов 4 то в любом случае какой то из них будет заполнен
        if pd.notna(second):
            return second
        else:
            return third
    # возвращаем результат суммирования
    return sum(count_answer_lst)


def calc_level_bek_depress(value):
    """
    Функция для подсчета уровня депрессии Бека
    """
    if 0 <= value <= 9:
        return 'удовлетворительное эмоциональное состояние'
    elif 10 <= value <= 19:
        return 'легкая депрессия'
    elif 20 <= value <= 22:
        return 'умеренная депрессия'
    else:
        return 'тяжелая депрессия'


def calc_count_level(df:pd.DataFrame, lst_cat:list, val_cat, col_cat, lst_cols:list):
    """
    Функция для создания сводных датафреймов по шкалам

    :param df: датафрейм с данными
    :param lst_cat:список колонок по которым будет формироваться свод
    :param val_cat:значение по которому будет формироваться свод
    :param col_cat: колонка по которой будет формироваться свод
    :param lst_cols: список с колонками
    :return:датафрейм
    """
    count_df = pd.pivot_table(df, index=lst_cat,
                                             columns=col_cat,
                                             values=val_cat,
                                             aggfunc='count', margins=True, margins_name='Итого')


    count_df.reset_index(inplace=True)
    count_df = count_df.reindex(columns=lst_cols)
    count_df['% удовлетворительное эмоциональное состояние от общего'] = round(
        count_df['удовлетворительное эмоциональное состояние'] / count_df['Итого'], 2) * 100
    count_df['% легкая депрессия от общего'] = round(
        count_df['легкая депрессия'] / count_df['Итого'], 2) * 100
    count_df['% умеренная депрессия от общего'] = round(
        count_df['умеренная депрессия'] / count_df['Итого'], 2) * 100
    count_df['% тяжелая депрессия от общего'] = round(
        count_df['тяжелая депрессия'] / count_df['Итого'], 2) * 100

    return count_df




def create_result_bek_depress(base_df:pd.DataFrame, out_dct:dict, lst_svod_cols:list):
    """
    Функция для подсчета результата если указаны колонки по которым нужно провести свод
    :param df: датафрейм с результатами
    :param out_dct: словарь с уже подсчитанными базовыми данными
    :param lst_svod_cols: список сводных колонок
    :return: словарь
    """
    lst_reindex_one_level_cols = lst_svod_cols.copy()
    lst_reindex_one_level_cols.extend( ['удовлетворительное эмоциональное состояние', 'легкая депрессия', 'умеренная депрессия',
                                        'тяжелая депрессия','Итого'])

    svod_count_one_level_depress_df = calc_count_level(base_df, lst_svod_cols,
                                                      'Значение_уровня_депрессии',
                                                      'Уровень_депрессии',
                                                      lst_reindex_one_level_cols)

    # Считаем среднее по субшкалам
    svod_mean_one_df = pd.pivot_table(base_df,
                                      index=lst_svod_cols,
                                      values=['Значение_уровня_депрессии',
                                              ],
                                      aggfunc=round_mean)
    svod_mean_one_df.reset_index(inplace=True)
    # упорядочиваем колонки
    new_order_cols = lst_svod_cols.copy()
    new_order_cols.extend((['Значение_уровня_депрессии',
                            ]))
    svod_mean_one_df = svod_mean_one_df.reindex(columns=new_order_cols)

    dct_rename_cols_mean = {'Значение_уровня_депрессии': 'Ср. Депрессия',
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
                    f'Свод {out_name}': svod_count_one_level_depress_df})
    if len(lst_svod_cols) == 1:
        return out_dct
    else:
        for idx, name_column in enumerate(lst_svod_cols):
            # Тревожность
            lst_reindex_column_level_cols = [lst_svod_cols[idx],'удовлетворительное эмоциональное состояние', 'легкая депрессия', 'умеренная депрессия',
                                        'тяжелая депрессия',
                                             'Итого']
            svod_count_column_level_depress_df = calc_count_level(base_df, lst_svod_cols[idx],
                                                               'Значение_уровня_депрессии',
                                                               'Уровень_депрессии',
                                                               lst_reindex_column_level_cols)

            # Считаем среднее по субшкалам
            svod_mean_column_df = pd.pivot_table(base_df,
                                              index=[lst_svod_cols[idx]],
                                              values=['Значение_уровня_депрессии',
                                                      ],
                                              aggfunc=round_mean)
            svod_mean_column_df.reset_index(inplace=True)
            # упорядочиваем колонки
            new_order_cols = [lst_svod_cols[idx]].copy()
            new_order_cols.extend((['Значение_уровня_депрессии',
                                    ]))
            svod_mean_column_df = svod_mean_column_df.reindex(columns=new_order_cols)

            dct_rename_cols_mean = {'Значение_уровня_депрессии': 'Ср. Депрессия',
                                    }
            svod_mean_column_df.rename(columns=dct_rename_cols_mean, inplace=True)

            name_column = lst_svod_cols[idx]
            name_column = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_column)
            name_column = name_column[:15]

            out_dct.update({f'Ср {name_column}': svod_mean_column_df,
                            f'Свод {name_column}': svod_count_column_level_depress_df})
        return out_dct










def processing_bek_depress(base_df: pd.DataFrame, answers_df: pd.DataFrame,lst_svod_cols:list):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    :param lst_svod_cols:  список с колонками по которым нужно делать свод
    """
    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 52:
            raise BadCountColumnsBekDepress

        # очищаем названия колонок от возможных сочетаний .1 которые добавляет пандас при одинаковых колонках
        clean_df_lst = []
        for name_column in answers_df.columns:
            clean_name = re.sub(r'.\d+$', '', name_column)
            clean_df_lst.append(clean_name)

        answers_df.columns = clean_df_lst

        count_descr_cols = base_df.shape[1]  # получаем количество описательных колонок в начале

        # словарь для замены слов на числа
        dct_replace_value = {'Мне не грустно': 0,
                             'Мне грустно или тоскливо': 1,
                             'Мне все время тоскливо или грустно и я ничего не могу с собой поделать': 2,
                             'Мне так грустно или печально, что я не могу этого вынести': 3,

                             'Я смотрю в будущее без особого разочарования': 0,
                             'Я испытываю разочарование в будущем': 1,
                             'Я чувствую, что мне нечего ждать впереди': 2,
                             'Я чувствую, что будущее безнадежно и поворота к лучшему быть не может': 3,

                             'Я не чувствую себя неудачником': 0,
                             'Я чувствую, что неудачи случались у меня чаще, чем у других людей': 1,
                             'Когда оглядываюсь на свою жизнь, я вижу лишь цепь неудач': 2,
                             'Я чувствую, что потерпел неудачу как личность (родители)': 3,

                             'У меня не потерян интерес к другим людям': 0,
                             'Я меньше, чем бывало, интересуюсь другими людьми': 1,
                             'У меня потерян почти весь интерес к другим людям и почти нет никаких чувств к ним': 2,
                             'У меня потерян всякий интерес к другим людям и они меня совершенно не заботят': 3,

                             'Я принимаю решения примерно так же легко, как всегда': 0,
                             'Я пытаюсь отсрочить принятые решения': 1,
                             'Принятие решений представляет для меня огромную трудность': 2,
                             'Я больше совсем не могу принимать решения': 3,

                             'Я не чувствую, что выгляжу сколько-нибудь хуже, чем обычно': 0,
                             'Меня беспокоит то, что я выгляжу непривлекательно': 1,
                             'Я чувствую, что в моем внешнем виде происходят постоянные изменения, делающие меня непривлекательным': 2,
                             'Я чувствую, что выгляжу гадко и отталкивающе': 3,

                             'Я не испытываю никакой особенной неудовлетворенности': 0,
                             'Ничто не радует меня так, как раньше': 1,
                             'Ничто больше не дает мне удовлетворения': 2,
                             'Меня не удовлетворяет всё': 3,

                             'Я не чувствую никакой особенной вины': 0,
                             'Большую часть времени я чувствую себя скверным и ничтожным': 1,
                             'У меня довольно сильное чувство вины': 2,
                             'Я чувствую себя очень скверным и никчемным': 3,

                             'Я могу работать примерно так же хорошо, как и раньше': 0,
                             'Мне нужно делать дополнительные усилия, чтобы что-то сделать': 1,
                             'Я с трудом заставляю себя делать что-либо': 2,
                             'Я не могу выполнять никакую работу': 3,

                             'Я не испытываю разочарования в себе': 0,
                             'Я разочарован в себе': 1,
                             'У меня отвращение к себе': 2,
                             'Я ненавижу себя': 3,

                             'У меня нет никаких мыслей о самоповреждении': 0,
                             'Я чувствую, что мне было бы лучше умереть': 1,
                             'У меня есть определенные планы совершения самоубийства': 2,
                             'Я покончу с собой при первой возможности': 3,

                             'Я устаю ничуть не больше, чем обычно': 0,
                             'Я устаю быстрее, чем раньше': 1,
                             'Я устаю от любого занятия': 2,
                             'Я устал чем бы то ни было заниматься': 3,

                             'Мой аппетит не хуже, чем обычно': 0,
                             'Мой аппетит не так хорош, как бывало': 1,
                             'Мой аппетит теперь гораздо хуже': 2,
                             'У меня совсем нет аппетита': 3,
                             }

        answers_df.replace(dct_replace_value, inplace=True)  # заменяем слова на цифры для подсчетов

        check_answers_df = answers_df.copy()  # делаем копию для проверки, чтобы заполнить наны нулями
        check_answers_df.fillna(0, inplace=True)
        # Проверяем правильность замены слов на цифры
        valid_values = [0, 1, 2, 3]

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        lst_error_answers = []  # список для хранения строк где найдены неправильные ответы

        for i in range(52):
            mask = ~check_answers_df.iloc[:, i].isin(valid_values)  # проверяем на допустимые значения
            result_check = check_answers_df.iloc[:, i][mask]
            if len(result_check) != 0:
                error_row = list(map(lambda x: x + 2, result_check.index))
                error_row = list(map(str, error_row))
                error_row_lst = [f'В {i + 1} вопросной колонке на строке {value}' for value in error_row]
                error_in_column = ','.join(error_row_lst)
                lst_error_answers.append(error_in_column)

        if len(lst_error_answers) != 0:
            error_message = ';'.join(lst_error_answers)
            raise BadValueBekDepress

        counter = 0  # счетчик обработанных колонок
        for i in range(1, 14):
            temp_lst_cols = list(answers_df.columns)[counter:counter + 4]  # отрезаем 4 колонки
            base_df[f'Группа утверждений №{i}'] = answers_df[temp_lst_cols].apply(calc_value_bek_depress, axis=1)
            counter += 4

        lst_sum_cols = [value for value in base_df.columns if 'Группа утверждений' in value]
        base_df.insert(count_descr_cols, 'Значение_уровня_депрессии',
                       base_df[lst_sum_cols].sum(axis=1, numeric_only=True))  # получаем сумму значений
        base_df.insert(count_descr_cols + 1, 'Уровень_депрессии',
                       base_df['Значение_уровня_депрессии'].apply(calc_level_bek_depress))  # считаем уровень
        base_df.insert(count_descr_cols + 1, 'Значение_нормы', '0-9 баллов')  # указываем норму
        # убираем колонки с ответами из основного списка
        lst_out_cols = [value for value in base_df.columns if 'Группа утверждений' not in value]
        base_df = base_df[lst_out_cols]

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame()
        part_df['ШДБ_Депрессия_Значение'] = base_df['Значение_уровня_депрессии']
        part_df['ШДБ_Депрессия_Уровень'] = base_df['Уровень_депрессии']

        out_answer_df = pd.concat([out_answer_df, answers_df], axis=1)

        base_df.sort_values(by='Значение_уровня_депрессии', ascending=False, inplace=True)  # сортируем

        # Делаем свод  по  шкалам
        dct_svod_sub = {'Значение_уровня_депрессии': 'Уровень_депрессии',
                        }

        dct_rename_svod_sub = {'Значение_уровня_депрессии': 'Депрессия',
                               }

        # Списки для шкал
        lst_level = ['удовлетворительное эмоциональное состояние', 'легкая депрессия',
                     'умеренная депрессия','тяжелая депрессия']

        base_svod_sub_df = create_union_svod(base_df, dct_svod_sub, dct_rename_svod_sub, lst_level)

        # считаем среднее значение по шкалам
        avg_depress = round(base_df['Значение_уровня_депрессии'].mean(), 2)

        avg_dct = {'Среднее значение уровня депрессии': avg_depress,
                   }

        avg_df = pd.DataFrame.from_dict(avg_dct, orient='index')
        avg_df = avg_df.reset_index()
        avg_df.columns = ['Показатель', 'Среднее значение']

        # формируем основной словарь
        out_dct = {'Списочный результат': base_df, 'Список для проверки': out_answer_df,
                   'Свод': base_svod_sub_df,
                   'Среднее': avg_df,
                   }
        dct_level = dict()
        for level in lst_level:
            temp_df = base_df[base_df['Уровень_депрессии'] == level]
            if temp_df.shape[0] != 0:
                if level == 'удовлетворительное эмоциональное состояние':
                    level = 'удовлетворительно'
                dct_level[level] = temp_df
        out_dct.update(dct_level)

        """
            Сохраняем в зависимости от необходимости делать своды по определенным колонкам
            """
        if len(lst_svod_cols) == 0:
            return out_dct, part_df
        else:
            out_dct = create_result_bek_depress(base_df, out_dct, lst_svod_cols)

            return out_dct, part_df

    except BadValueBekDepress:
        messagebox.showerror('Лахеcис',
                             f'При обработке вопросов теста Шкала депрессии Бека обнаружены неправильные варианты ответов. Проверьте ответы на указанных строках:\n'
                             f'{error_message}\n'
                             f'Используйте при создании Яндекс-формы написание вариантов ответа из руководства пользователя программы Лахесис.')


    except BadCountColumnsBekDepress:
        messagebox.showerror('Лахеcис',
                             f'Проверьте количество колонок с ответами на тест Шкала депрессии Бека\n'
                             f'Должно быть 52 колонки с ответами, то есть  13 вопросов по 4 колонки'
                            )










