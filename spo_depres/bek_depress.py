"""
Скрипт для обработки теста Шкала депрессии Бека
"""
from lachesis_support_functions import round_mean

import pandas as pd
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








def processing_bek_depress(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки результатов теста
    """

    try:
        out_answer_df = base_df.copy()  # делаем копию для последующего соединения с сырыми ответами
        if len(answers_df.columns) != 52:
            raise BadCountColumnsBekDepress

        count_descr_cols = base_df.shape[1] # получаем количество описательных колонок в начале

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

        check_answers_df = answers_df.copy() # делаем копию для проверки, чтобы заполнить наны нулями
        check_answers_df.fillna(0,inplace=True)
        # Проверяем правильность замены слов на цифры
        valid_values = [0, 1, 2, 3]

        # Проверяем, есть ли значения, отличающиеся от указанных в списке
        mask = ~check_answers_df.isin(valid_values)

        # Получаем строки с отличающимися значениями
        result_check = check_answers_df[mask.any(axis=1)]
        if len(result_check) != 0:
            error_row = list(map(lambda x: x + 2, result_check.index))
            error_row = list(map(str, error_row))
            error_message = ';'.join(error_row)
            raise BadValueBekDepress

        counter = 0 # счетчик обработанных колонок
        for i in range(1,14):
            temp_lst_cols = list(answers_df.columns)[counter:counter+4] # отрезаем 4 колонки
            base_df[f'Группа утверждений №{i}'] = answers_df[temp_lst_cols].apply(calc_value_bek_depress, axis=1)
            counter += 4

        lst_sum_cols = [value for value in base_df.columns if 'Группа утверждений' in value]
        base_df.insert(count_descr_cols,'Значение_уровня_депрессии',base_df[lst_sum_cols].sum(axis=1,numeric_only=True)) #получаем сумму значений
        base_df.insert(count_descr_cols + 1,'Уровень_депрессии',base_df['Значение_уровня_депрессии'].apply(calc_level_bek_depress)) # считаем уровень
        base_df.insert(count_descr_cols + 1,'Значение_нормы','0-9 баллов') # указываем норму

        # Создаем датафрейм для создания части в общий датафрейм
        part_df = pd.DataFrame(columns=['Значение_уровня_депрессии_Бек','Уровень_депрессии_Бек'])
        part_df['Значение_уровня_депрессии_Бек'] = base_df['Значение_уровня_депрессии']
        part_df['Уровень_депрессии_Бек'] = base_df['Уровень_депрессии']


        base_df.sort_values(by='Значение_уровня_депрессии',ascending=False,inplace=True) # сортируем




        # Делаем сводную таблицу средних значений.
        svod_all_df = pd.pivot_table(base_df,index=['Курс','Пол'],
                                     values=['Значение_уровня_депрессии'],
                                     aggfunc=round_mean)
        svod_all_df.reset_index(inplace=True)
        svod_all_df['Уровень_депрессии'] = svod_all_df['Значение_уровня_депрессии'].apply(calc_level_bek_depress) # считаем уровень

        # Делаем свод по количеству
        svod_all_count_df = pd.pivot_table(base_df,index=['Курс','Пол'],
                                     columns='Уровень_депрессии',
                                     values='Значение_уровня_депрессии',
                                     aggfunc='count',margins=True,margins_name='Итого')
        svod_all_count_df.reset_index(inplace=True)

        # Добавляем колонки с процентами
        if 'удовлетворительное эмоциональное состояние' in svod_all_count_df.columns:
            svod_all_count_df['% удовлетворительное эмоциональное состояние от общего'] = round(svod_all_count_df['удовлетворительное эмоциональное состояние'] / svod_all_count_df['Итого'],2)

        if 'легкая депрессия' in svod_all_count_df.columns:
            svod_all_count_df['% легкая депрессия  от общего'] = round(svod_all_count_df['легкая депрессия'] / svod_all_count_df['Итого'],2)
        if 'умеренная депрессия' in svod_all_count_df.columns:
            svod_all_count_df['% умеренная депрессия от общего'] = round(svod_all_count_df['умеренная депрессия'] / svod_all_count_df['Итого'],2)
        if 'тяжелая депрессия' in svod_all_count_df.columns:
            svod_all_count_df['% тяжелая депрессия от общего'] = round(svod_all_count_df['тяжелая депрессия'] / svod_all_count_df['Итого'],2)

        out_answer_df = pd.concat([out_answer_df,answers_df],axis=1)

        # Проверяем наличие колонки с наименованием группы
        if 'Группа' not in base_df.columns:
            # формируем словарь
            out_dct = {'Списочный результат':base_df,'Список для проверки':out_answer_df,
                'Средний результат':svod_all_df,'Количество':svod_all_count_df,
    }

            return out_dct, part_df
        else:


            # Делаем сводную таблицу средних значений.
            svod_all_group_df = pd.pivot_table(base_df, index=['Группа', 'Пол'],
                                               values=['Значение_уровня_депрессии'],
                                               aggfunc=round_mean)
            svod_all_group_df.reset_index(inplace=True)
            svod_all_group_df['Уровень_депрессии'] = svod_all_group_df['Значение_уровня_депрессии'].apply(
                calc_level_bek_depress)  # считаем уровень

            # Делаем свод по количеству
            svod_all_group_count_df = pd.pivot_table(base_df, index=['Группа', 'Пол'],
                                                     columns='Уровень_депрессии',
                                                     values='Значение_уровня_депрессии',
                                                     aggfunc='count', margins=True, margins_name='Итого')
            svod_all_group_count_df.reset_index(inplace=True)

            # Добавляем колонки с процентами
            if 'удовлетворительное эмоциональное состояние' in svod_all_group_count_df.columns:
                svod_all_group_count_df['% удовлетворительное эмоциональное состояние от общего'] = round(
                    svod_all_group_count_df['удовлетворительное эмоциональное состояние'] / svod_all_group_count_df[
                        'Итого'], 2)

            if 'легкая депрессия' in svod_all_group_count_df.columns:
                svod_all_group_count_df['% легкая депрессия  от общего'] = round(
                    svod_all_group_count_df['легкая депрессия'] / svod_all_group_count_df['Итого'], 2)
            if 'умеренная депрессия' in svod_all_group_count_df.columns:
                svod_all_group_count_df['% умеренная депрессия от общего'] = round(
                    svod_all_group_count_df['умеренная депрессия'] / svod_all_group_count_df['Итого'], 2)
            if 'тяжелая депрессия' in svod_all_group_count_df.columns:
                svod_all_group_count_df['% тяжелая депрессия от общего'] = round(
                    svod_all_group_count_df['тяжелая депрессия'] / svod_all_group_count_df['Итого'], 2)

            # делаем свод только по группам
            # Делаем сводную таблицу средних значений.
            svod_all_only_group_df = pd.pivot_table(base_df, index=['Группа'],
                                         values=['Значение_уровня_депрессии'],
                                         aggfunc=round_mean)
            svod_all_only_group_df.reset_index(inplace=True)
            svod_all_only_group_df['Уровень_депрессии'] = svod_all_only_group_df['Значение_уровня_депрессии'].apply(
                calc_level_bek_depress)  # считаем уровень

            # Делаем свод по количеству
            svod_all_only_group_count_df = pd.pivot_table(base_df, index=['Группа'],
                                                          columns='Уровень_депрессии',
                                                          values='Значение_уровня_депрессии',
                                                          aggfunc='count', margins=True, margins_name='Итого')
            svod_all_only_group_count_df.reset_index(inplace=True)

            # Добавляем колонки с процентами
            if 'удовлетворительное эмоциональное состояние' in svod_all_only_group_count_df.columns:
                svod_all_only_group_count_df['% удовлетворительное эмоциональное состояние от общего'] = round(
                    svod_all_only_group_count_df['удовлетворительное эмоциональное состояние'] /
                    svod_all_only_group_count_df[
                        'Итого'], 2)

            if 'легкая депрессия' in svod_all_only_group_count_df.columns:
                svod_all_only_group_count_df['% легкая депрессия  от общего'] = round(
                    svod_all_only_group_count_df['легкая депрессия'] / svod_all_only_group_count_df['Итого'], 2)
            if 'умеренная депрессия' in svod_all_only_group_count_df.columns:
                svod_all_only_group_count_df['% умеренная депрессия от общего'] = round(
                    svod_all_only_group_count_df['умеренная депрессия'] / svod_all_only_group_count_df['Итого'], 2)
            if 'тяжелая депрессия' in svod_all_only_group_count_df.columns:
                svod_all_only_group_count_df['% тяжелая депрессия от общего'] = round(
                    svod_all_only_group_count_df['тяжелая депрессия'] / svod_all_only_group_count_df['Итого'], 2)

            # формируем словарь
            out_dct = {'Списочный результат':base_df,'Список для проверки':out_answer_df,
                'Средний результат':svod_all_df,'Количество':svod_all_count_df,
                       'Ср_рез по группам': svod_all_only_group_df, 'Кол по группам': svod_all_only_group_count_df,
                       'Ср_рез по группам и полам':svod_all_group_df,'Кол по группам и полам':svod_all_group_count_df
                       }

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



















