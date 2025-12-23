"""
Скрипт для обработки тестов
"""
# Тесты Профессиональное выгорание
from prof_burnout.vodopyanova_pedagog_prof_burnout import processing_vod_ped_prof_burnout # Профессиональное выгорание педагогов Водопьянова
from prof_burnout.boiko_ilin_emotional_burnout import processing_boiko_ilin_emotional_burnout # Эмоциональное выгорание Бойко Ильин
from prof_burnout.kapponi_burnout import processing_kapponi_burnout # Выгорание Каппони Новак
from prof_burnout.maslach_prof_burnount_vodopyanova import processing_maslach_prof_burnout_vod # Профессиональное выгорание Маслач Водопьянова
from prof_burnout.boiko_emotional_burnout import processing_boiko_emotional_burnout # Профессиональное выгорание Бойко
from prof_burnout.bat_short_version_demkin import processing_short_bat_demkin # BAT краткая версия Демкин
from prof_burnout.rukavishnikov_psych_burnout import processing_rukav_psych_burnout # Опросник психологического выгорания Рукавишников

# Тесты ментальное и психологическое состояние
from mental_state.goncharova_adoptation_first_course import processing_goncharova_adoptation_first_course # Экспресс-диагностика первокурсников Гончарова
from mental_state.aizenk_self_mental_state import processing_aizenk_self_mental_state # Самодиагностика психического состояния Айзенк
from mental_state.rodjers_daimond_sneg_soc_psych_adapt import processing_rodjers_daimond_sneg_soc_psych_adapt # Шкала социально психологического состояния Роджерс Даймонд Снегирева
from mental_state.doskin_san import processing_doskin_san # Опросник Самочувствие Активность Настроение Доскин Мирошниченко

from mental_state.voz_well_being import processing_voz_well_being # Индекс общего самочувствия ВОЗ 1999
from mental_state.kondash_anxiety_school import processing_kondash_anxiety_school # Шкала тревожности Кондаша Школьники
from mental_state.kondash_anxiety_student import processing_kondash_anxiety_student # Шкала тревожности Кондаша Студенты
from mental_state.bek_depress import processing_bek_depress # Шкала депрессии Бека
from mental_state.bek_hopelessness import processing_bek_hopelessness # Шкала безнадежности Бека
from mental_state.zung_depress import processing_zung_depress # Шкала депресси Цунга
from mental_state.dass_twenty_one_zolotareva import processing_dass_twenty_one_zolotareva # Шкала депрессии, тревоги и стресса, DASS-21 Золотарева
from mental_state.psm_twenty_five_vodopyanova import processing_psm_twenty_five_vodopyanova # Шкала психологического стресса PSM-25 Водопьянова
from mental_state.scl_k_nine_zolotareva import processing_scl_k_nine_zolotareva # Симптоматический опросник SCL-K-9 Золотарева
from mental_state.scl_r_nineteen_tarabrina import processing_scl_r_nineteen_tarabrina # SCL-90-R Тарабрина

# Тесты предложенные РЦО
from mental_state.philips_school_anxiety import processing_philips_school_anxiety # Тест школьной тревожности Филлипса



# Тесты Лидерство, эмоциональный интеллект
from ei_leadership.lusin_ei import processing_lusin_ei # Эмоциональный интеллект Люсин
from ei_leadership.kovalev_level_self_assesment import processing_usk # Уровень самооценки Ковалев
from ei_leadership.fedor_kos_one import processing_kos_one # КОС-1 Федоришин

# Тесты остракизм, буллинг
from ostrakizm.boykina_shnpo import processing_boykina_shnpo # Шкала нарушенных потребностей, Остракизм Бойкина
from ostrakizm.boykina_shso import processing_boykina_shso # Шкала субъективного остракизма Бойкина
from ostrakizm.norkina_vbs_school import processing_norkina_vbs_school # Выявление буллинг структуры Норкина Школьники
from ostrakizm.norkina_vbs_student import processing_norkina_vbs_student # Выявление буллинг структуры Норкина Студенты

# Тесты девиантное поведение
from deviant.leus_sdp import processing_leus_sdp # Склонность к девиантному поведению Леус
from deviant.bass_darki_hvan_hostility import processing_bass_darki_hvan_hostility # Опросник враждебности Басс Дарки Хван
from deviant.bass_perry_enikopolov_agres import processing_bass_perry_enikopolov_agress # Опросник агрессивности Басс Перри Еникополов
from deviant.cook_medley_mend_hostility import processing_cook_medley_mend_hostility # Шкала враждебности Кука-Медлей Менджерицкая

# Профориентационные тесты
from career_guidance.shein_cok import processing_shein_cok # Якоря карьеры ЦОК Шейн
from career_guidance.holland_ptl import processing_holland_ptl # Профессиональный тип личности Голланд
from career_guidance.rezapkina_spp import processing_rezapkina_spp # Сфера профессиональных предпочтений Резапкина
from career_guidance.klimov_azbel_ddo import processing_ddo # Дифференциально-диагностический опросник Климов Азбель
from career_guidance.golomshtok_azbel_map_interests import processing_gol_azb_map_interest # Карта интересов Голомшток Азбель
from career_guidance.azbel_prof_identity import processing_azbel_prof_identity # Профессиональная идентичность Азбель
from career_guidance.rezapkina_hp import processing_rezapkina_hp # Характер профессия Резапкина
from career_guidance.azbel_sitt import processing_azbel_sitt # Склонность к исполнительскому или творческому труду Азбель
from career_guidance.grezov_ntfp import processing_grezov_ntfp # Наемный труд фриланс предпринимательство Грецов
from career_guidance.andreeva_pup import processing_andreeva_pup # Профессиональные установки подростков Андреева
from career_guidance.godlinik_nvid import processing_godlinik_nvid # Направленность на вид инженерной деятельности Годлиник

# ПТСР
from ptsr.military_missisip_scale import processing_misisip_scale_military_option # Миссисипская шкала ПТСР военный вариант
from ptsr.civil_missisip_scale import processing_misisip_scale_civil_option # Миссисипская шкала ПТСР гражданский вариант
from ptsr.shovts_tarabrina import processing_shovts_tarabrina # Шкала оценки влияния травматического события (ШОВТС) Тарабрина
from ptsr.scale_intensity_war_exp import processing_scale_intensity_war_exp # Шкала оценки интенсивности боевого опыта Тарабрина
from ptsr.screening_ptsr import processing_scrining_ptsr # Скрининнг ПТСР Brewin
from ptsr.forecast_two_rybnikov import processing_forecast_two_rybnikov # Методика оценки нервно-психической устойчивости «Прогноз-2» В.Ю. Рыбников


# Мотивация, риск, избегание неудач
from motivation.kotik_motiv_target import processing_kotik_motiv_target # Опросник мотивации к достижению цели, к успеху Элерс Котик
from motivation.kotik_avoiding_fail import processing_kotik_avoiding_fail # Опросник мотивации к избеганию неудач Элерс Котик
from motivation.kotik_risk_appetite import processing_kotik_risk_appetite # Опросник оценки склонности к риску, RSK (Г. Шуберт)

# Структура личности
from personality_structure.kettel_pf_fourteen_rukav_sokolova import processing_kettel_pf_ruk_sok # Тест Кеттела для подростков
from personality_structure.acope_polskaya import processing_acope_polskaya # Копинг стратегии для подростков Польская
from personality_structure.lazarus_wcq_nipni import processing_lazarus_wcq_nipni # Копинг стратегии Лазарус НИПНИ Бехтерева





from lachesis_support_functions import write_df_to_excel, del_sheet, count_attention # функции для создания итогового файла

import pandas as pd
pd.options.mode.chained_assignment = None
from tkinter import messagebox
import re


class NotSameSize(Exception):
    """
    Исключение для проверки совпадают ли размеры таблицы с количеством колонок требуемых для выполнения тестов указанных в параметрах
    """
    pass

class NotCorrectParamsTests(Exception):
    """
    Исключение для проверки есть ли хотя бы один реализованный тест
    """
    pass

class NotCorrectSvodCols(Exception):
    """
    Исключение для проверки корректности строки с колонками по которым нужно сделать свод
    """
    pass

class BadSvodCols(Exception):
    """
    Исключение для проверки правильности введенной строки с перечислением колонок по которым нужно сделать свод
    """
    pass


def check_svod_cols(df:pd.DataFrame,str_svod_cols:str,threshold:int):
    """
    Фцнкция для проверки корректности
    :param df: датафрейм с анкетными данными
    :param str_svod_cols: строка с порядоквыми номерами
    :param threshold: количество колонок в анкетной части
    :return: список
    """
    try:
        result = re.findall(r'\d+',str_svod_cols)
        if result:
            if len(result) == 1:
                value = int(result[0])
                if value > threshold:
                    raise NotCorrectSvodCols
                elif value == 0:
                    raise NotCorrectSvodCols
                else:
                    return [df.columns[value-1]]
            elif len(result) == 2:
                for idx,value in enumerate(result):
                    value = int(value)
                    if value > threshold:
                        raise NotCorrectSvodCols
                    elif value == 0:
                        raise NotCorrectSvodCols
                    else:
                        result[idx] = df.columns[value-1]
                return result
            elif len(result) == 3:
                for idx,value in enumerate(result):
                    value = int(value)
                    if value > threshold:
                        raise NotCorrectSvodCols
                    elif value == 0:
                        raise NotCorrectSvodCols
                    else:
                        result[idx] = df.columns[value-1]
                return result
            else:
                raise NotCorrectSvodCols

        else:
            return []
    except:
        raise NotCorrectSvodCols



def generate_result_all_age(params_adults: str, data_adults: str, end_folder: str, threshold_base: int, svod_cols:str):
    """
    Функция для генерации результатов комплексного теста для взрослых
    :param params_adults: какие тесты используются и в каком порядке
    :param data_adults: файл с данными
    :param end_folder: конечная папка
    :param threshold_base: количество колонок с вводными данными
    :param svod_cols: строка с перечислением колонок по которым нужно сделать свод
    :return:
    """
    try:

        dct_tests = {'Профессиональное выгорание педагогов Водопьянова': (processing_vod_ped_prof_burnout, 22),
                     'Эмоциональное выгорание Бойко Ильин': (processing_boiko_ilin_emotional_burnout, 35),
                     'Выгорание Каппони Новак': (processing_kapponi_burnout, 10),
                     'Профессиональное выгорание Маслач Водопьянова': (processing_maslach_prof_burnout_vod, 22),
                     'Эмоциональное выгорание Бойко': (processing_boiko_emotional_burnout, 84),
                     'BAT краткая версия Демкин': (processing_short_bat_demkin, 12),
                     'Опросник психологического выгорания Рукавишников': (processing_rukav_psych_burnout, 72),

                     'Экспресс-диагностика адаптации первокурсников Гончарова': (processing_goncharova_adoptation_first_course, 11),
                     'Самооценка психических состояний Айзенк': (processing_aizenk_self_mental_state, 40),
                     'Социально-психологическая адаптированность Роджерс Даймонд Снегирева': (processing_rodjers_daimond_sneg_soc_psych_adapt, 101),
                     'САН Доскин Мирошников': (processing_doskin_san, 30),
                     'Индекс общего самочувствия ВОЗ 1999': (processing_voz_well_being, 5),
                     'Шкала тревожности Кондаша Школьники': (processing_kondash_anxiety_school, 30),
                     'Шкала тревожности Кондаша Студенты': (processing_kondash_anxiety_student, 30),
                     'Шкала депрессии Бека': (processing_bek_depress, 52),
                     'Шкала безнадежности Бека': (processing_bek_hopelessness, 20),
                     'Шкала депрессии Цунга': (processing_zung_depress, 20),

                     'Школьная тревожность Филлипс': (processing_philips_school_anxiety, 58),


                     'Эмоциональный интеллект Люсин': (processing_lusin_ei, 46),
                     'Уровень самооценки Ковалев': (processing_usk, 32),
                     'КОС-1': (processing_kos_one, 40),

                     'ШНПО ПМ Бойкина':(processing_boykina_shnpo,20),
                     'Шкала субъективного остракизма Бойкина':(processing_boykina_shso,14),
                     'Выявление буллинг-структуры Норкина Школьники':(processing_norkina_vbs_school,25),
                     'Выявление буллинг-структуры Норкина Студенты':(processing_norkina_vbs_student,25),

                     'Склонность к девиантному поведению Леус': (processing_leus_sdp, 75),
                     'BDHI Хван': (processing_bass_darki_hvan_hostility, 75),
                     'BPAQ-24 Еникополов': (processing_bass_perry_enikopolov_agress, 24),
                     'CMHS Менджерицкая': (processing_cook_medley_mend_hostility, 27),

                     'ЦОК':(processing_shein_cok,41),
                     'ПТЛ':(processing_holland_ptl,30),
                     'СПП':(processing_rezapkina_spp,24),
                     'ДДО':(processing_ddo,30),
                     'Карта интересов Голомшток Азбель':(processing_gol_azb_map_interest,144),
                     'Профессиональная идентичность Азбель':(processing_azbel_prof_identity,20),
                     'Характер и профессия Резапкина':(processing_rezapkina_hp,24),
                     'СИТТ Азбель':(processing_azbel_sitt,12),
                     'НТФП Грецов':(processing_grezov_ntfp,24),
                     'Профессиональные установки подростков Андреева':(processing_andreeva_pup,24),
                     'НВИД Годлиник':(processing_godlinik_nvid,24),


                     'Миссисипская шкала ПТСР-В':(processing_misisip_scale_military_option,35),
                     'Миссисипская шкала ПТСР-Г':(processing_misisip_scale_civil_option,39),
                     'ШОВТС Тарабрина':(processing_shovts_tarabrina,22),
                     'SCL-K-9 Золотарева':(processing_scl_k_nine_zolotareva,9),
                     'Шкала оценки интенсивности боевого опыта':(processing_scale_intensity_war_exp,7),
                     'Опросник на скрининг ПТСР':(processing_scrining_ptsr,10),
                     'SCL-90-R Тарабрина':(processing_scl_r_nineteen_tarabrina,90),
                     'Прогноз-2 Рыбников':(processing_forecast_two_rybnikov,86),
                     'DASS 21 Золотарева':(processing_dass_twenty_one_zolotareva,21),
                     'PSM-25 Водопьянова':(processing_psm_twenty_five_vodopyanova,25),

                     'Опросник мотивации к достижению цели, к успеху Элерс Котик': (processing_kotik_motiv_target, 41),
                     'Опросник мотивации к избеганию неудач Элерс Котик': (processing_kotik_avoiding_fail, 30),
                     'Опросник оценки склонности к риску Шуберт Котик': (processing_kotik_risk_appetite, 25),

                     'Кеттел 14-PF Рукавишников Соколова': (processing_kettel_pf_ruk_sok, 142),
                     'ACOPE Польская': (processing_acope_polskaya, 54),
                     'WCQ НИПНИ Бехтерева': (processing_lazarus_wcq_nipni, 50),






                     }  # словарь с наименованием теста функцией для его обработки и количеством колонок

        dct_out_name_tests = {'Профессиональное выгорание педагогов Водопьянова': 'Профессиональное выгорание педагогов Водопьянова',
                              'Эмоциональное выгорание Бойко Ильин': 'Эмоциональное выгорание Бойко Ильин',
                              'Выгорание Каппони Новак': 'Экспресс-оценка выгорания Каппони Новак',
                              'Профессиональное выгорание Маслач Водопьянова': 'Профессиональное выгорание Маслач Водопьянова',
                              'Эмоциональное выгорание Бойко': 'Эмоциональное выгорание Бойко',
                              'BAT краткая версия Демкин': 'BAT краткая версия Демкин',
                              'Опросник психологического выгорания Рукавишников': 'Опросник психологического выгорания Рукавишников',

                              'Экспресс-диагностика адаптации первокурсников Гончарова': 'Экспресс-диагностика адаптации первокурсников Гончарова',
                              'Самооценка психических состояний Айзенк': 'Самооценка психических состояний Айзенк',
                              'Социально-психологическая адаптированность Роджерс Даймонд Снегирева': 'Социально-психологическая адаптированность Роджерс Даймонд Снегирева',
                              'САН Доскин Мирошников': 'САН Доскин Мирошников',

                              'Индекс общего самочувствия ВОЗ 1999': 'Индекс общего самочувствия ВОЗ 1999',
                              'Шкала тревожности Кондаша Школьники': 'Шкала тревожности Кондаша Школьники',
                              'Шкала тревожности Кондаша Студенты': 'Шкала тревожности Кондаша Студенты',
                              'Шкала депрессии Бека': 'Шкала депрессии Бека',
                              'Шкала безнадежности Бека': 'Шкала безнадежности Бека',
                              'Шкала депрессии Цунга': 'Шкала депрессии Цунга',
                              'Школьная тревожность Филлипс': 'Школьная тревожность Филлипс',

                              'Эмоциональный интеллект Люсин': 'Эмоциональный интеллект Люсин',
                              'Уровень самооценки Ковалев': 'Уровень самооценки Ковалев',
                              'КОС-1': 'КОС-1 Федоришин',

                              'ШНПО ПМ Бойкина': 'Шкала нарушенных потребностей остракизм Бойкина',
                              'Шкала субъективного остракизма Бойкина': 'Шкала субъективного остракизма Бойкина',
                              'Выявление буллинг-структуры Норкина Школьники': 'Выявление буллинг-структуры Норкина Школьники',
                              'Выявление буллинг-структуры Норкина Студенты': 'Выявление буллинг-структуры Норкина Студенты',

                              'Склонность к девиантному поведению Леус': 'Склонность к девиантному поведению Леус',
                              'BDHI Хван': 'Опросник враждебности Басса-Дарки Хван',
                              'BPAQ-24 Еникополов': 'Опросник диагностики агрессии Басса-Перри, BPAQ-24 Еникополов',
                              'CMHS Менджерицкая': 'Шкала враждебности Кука-Медлей Менджерицкая',

                              'ЦОК': 'Якоря карьеры ЦОК',
                              'ПТЛ': 'Профессиональный тип личности',
                              'СПП': 'Сфера профессиональных предпочтений',
                              'ДДО': 'Дифференциально-диагностический опросник',
                              'Карта интересов Голомшток Азбель': 'Карта интересов Голомшток Азбель',
                              'Профессиональная идентичность Азбель': 'Профессиональная идентичность Азбель',
                              'Характер и профессия Резапкина': 'Характер и профессия Резапкина',
                              'СИТТ Азбель': 'Склонность к исполнительскому или творческому труду',
                              'НТФП Грецов': 'Наемный труд, фриланс, предпринимательство',
                              'Профессиональные установки подростков Андреева': 'Профессиональные установки подростков Андреева',
                              'НВИД Годлиник': 'Направленность на вид инженерной деятельности',

                              'Миссисипская шкала ПТСР-В': 'Миссисипская шкала ПТСР военный вариант',
                              'Миссисипская шкала ПТСР-Г': 'Миссисипская шкала ПТСР гражданский вариант',
                              'ШОВТС Тарабрина': 'Шкала оценки влияния травматического события Тарабрина',
                              'SCL-K-9 Золотарева': 'Симптоматический опросник SCL-K-9 Золотарева',
                              'Шкала оценки интенсивности боевого опыта': 'Шкала оценки интенсивности боевого опыта Тарабрина',
                              'Опросник на скрининг ПТСР': 'Опросник на скрининг ПТСР',
                              'SCL-90-R Тарабрина': 'Симптоматический опросник SCL-90-R Тарабрина',
                              'Прогноз-2 Рыбников': 'Оценка нервно-психической устойчивости «Прогноз-2',
                              'DASS 21 Золотарева': 'Шкала депрессии, тревоги и стресса, DASS-21',
                              'PSM-25 Водопьянова': 'Шкала психологического стресса PSM-25',


                              'Опросник мотивации к достижению цели, к успеху Элерс Котик': 'Опросник мотивации к достижению цели, к успеху Элерс Котик',
                              'Опросник мотивации к избеганию неудач Элерс Котик': 'Опросник мотивации к избеганию неудач Элерс Котик',
                              'Опросник оценки склонности к риску Шуберт Котик': 'Опросник оценки склонности к риску Шуберт Котик',


                              'Кеттел 14-PF Рукавишников Соколова': 'Опросник Кеттела 14PF Рукавишников Соколова',
                              'ACOPE Польская': 'Опросник копинг-установок подростков Польская',
                              'WCQ НИПНИ Бехтерева': 'Способы совладающего поведения Лазарус НИПНИ Бехтерева',


                              }  # словарь с наименованием теста функцией для его обработки и количеством колонок

        # Списки для проверки, чтобы листы Особое внимание и зона риска создавались только если в параметрах указаны эти тесты
        lst_alert_tests = ['Профессиональное выгорание педагогов Водопьянова','Эмоциональное выгорание Бойко Ильин',
                           'Выгорание Каппони Новак','Профессиональное выгорание Маслач Водопьянова','Эмоциональное выгорание Бойко',
                           'BAT краткая версия Демкин','Опросник психологического выгорания Рукавишников',

                           'Экспресс-диагностика адаптации первокурсников Гончарова','Самооценка психических состояний Айзенк',
                           'Социально-психологическая адаптированность Роджерс Даймонд Снегирева','САН Доскин Мирошников',

                           'Индекс общего самочувствия ВОЗ 1999','Шкала тревожности Кондаша Школьники','Шкала тревожности Кондаша Студенты',
                           'Шкала депрессии Бека','Шкала безнадежности Бека','Шкала депрессии Цунга',
                           'Школьная тревожность Филлипс',

                           'ШНПО ПМ Бойкина','Шкала субъективного остракизма Бойкина',

                           'Склонность к девиантному поведению Леус','BDHI Хван','BPAQ-24 Еникополов','CMHS Менджерицкая',

                           'Миссисипская шкала ПТСР-В','Миссисипская шкала ПТСР-Г','ШОВТС Тарабрина','SCL-K-9 Золотарева',
                           'Шкала оценки интенсивности боевого опыта','Опросник на скрининг ПТСР','SCL-90-R Тарабрина',
                           'Прогноз-2 Рыбников','DASS 21 Золотарева','PSM-25 Водопьянова'

                           ]
        lst_check_alert_tests = []

        # Списки для проверки наличия профориентационных тестов
        lst_career_tests = ['ЦОК','ПТЛ','СПП','ДДО','Профессиональная идентичность Азбель','Карта интересов Голомшток Азбель',
                            'Характер и профессия Резапкина','СИТТ Азбель','НТФП Грецов','Профессиональные установки подростков Андреева','НВИД Годлиник']
        lst_check_career_tests = []

        # Список тестов для которых нужно создание отдельных файлов
        lst_create_files_tests =['Кеттел 14-PF Рукавишников Соколова']


        params_df = pd.read_excel(params_adults, dtype=str, usecols='A',
                                  header=None)  # считываем какие тесты нужно использовать
        params_df.dropna(inplace=True)  # удаляем пустые строки
        lst_used_test = params_df.iloc[:, 0].tolist()  # получаем список
        lst_used_test = [value for value in lst_used_test if value in dct_tests.keys()]  # отбираем только те что прописаны

        if len(lst_used_test) == 0:
            raise NotCorrectParamsTests

        # создаем счетчик обработанных колонок
        threshold_finshed = threshold_base

        # Проверяем датафрейм на количество колонок
        df = pd.read_excel(data_adults, dtype=str)  # считываем датафрейм
        df.columns = list(map(str,df.columns)) # делаем строковыми названия колонок
        lst_name_cols = [col for col in df.columns if 'Unnamed' not in col]  # отбрасываем колонки без названия
        df = df[lst_name_cols]

        check_size_df = 0  # проверяем размер датафрейма чтобы он совпадал с количеством вопросов в тестах
        for name_test in lst_used_test:
            check_size_df += dct_tests[name_test][1]
        if check_size_df + threshold_base > df.shape[1]:
            raise NotSameSize

        base_df = df.iloc[:, :threshold_base]  # создаем датафрейм с данными не относящимися к тесту
        # делаем строковыми названия колонок
        base_df.columns = list(map(str, base_df.columns))

        # заменяем пробелы на нижнее подчеркивание и очищаем от пробельных символов в начале и конце
        base_df.columns = [column.strip().replace(' ', '_') for column in base_df.columns]

        # очищаем от всех символов кроме букв цифр
        base_df.columns = [re.sub(r'[^_\d\w]', '', column) for column in base_df.columns]

        # проверяем и обрабатываем строку с колонками по которым нужно делать свод
        lst_svod_cols = check_svod_cols(base_df,svod_cols,threshold_base)

        # Создаем копию датафрейма с анкетными данными для передачи в функцию
        base_df_for_func = base_df.copy()
        # Создаем копию анкетных данных для создания свода по всем тестам
        main_itog_df = base_df.copy()

        # создаем копию для датафрейма с результатами
        result_df = base_df.copy()

        # Перебираем полученные названия тестов
        for name_test in lst_used_test:
            """
            запускаем функцию хранящуюся в словаре
            передаем туда датафрейм с анкетными данными, датафрейм с данными теста, количество колонок которое занимает данный тест
            получаем 2 датафрейма с результатами для данного теста которые добавляем в основные датафреймы
            """
            # Присутствует ли тест среди тестов на где нужно выделять опасные состояния
            if name_test in lst_alert_tests:
                lst_check_alert_tests.append(name_test)

            # Присутствует ли тест среди профориентационных тестов
            if name_test in lst_career_tests:
                lst_check_career_tests.append(name_test)

            temp_base_df = base_df.copy()

            # получаем колонки относящиеся к тесту
            temp_df = df.iloc[:, threshold_finshed:threshold_finshed + dct_tests[name_test][1]]
            # Очищаем от лишних пробельных символов в начале и в конце
            lst_temp_cols = temp_df.columns
            lst_temp_cols = list(map(str,lst_temp_cols))
            lst_temp_cols = list(map(str.strip, lst_temp_cols))
            temp_df.columns = lst_temp_cols


            # обрабатываем и получаем датафреймы для добавления в основные таблицы
            # если тест не относится к Кеттелу или другим тестам для которых надо делать диграммы
            if name_test not in lst_create_files_tests:
                temp_dct,temp_itog_df = dct_tests[name_test][0](temp_base_df, temp_df,lst_svod_cols)
            else:
                temp_dct,temp_itog_df = dct_tests[name_test][0](temp_base_df, temp_df,lst_svod_cols,end_folder)

            base_df_for_func = pd.concat([base_df_for_func, temp_dct['Списочный результат']],
                                axis=1)  # соединяем анкетные данные и вопросы вместе с результатами
            result_df = pd.concat([result_df, temp_dct['Список для проверки']], axis=1)

            # Добавляем в итоговый свод
            main_itog_df = pd.concat([main_itog_df,temp_itog_df],axis=1)

            # Сохраняем в зависимости от типа теста. Если профориентационный то сохраняем через pandas,
            # чтобы текст в колонке Описание результата не обрезался
            if name_test in lst_check_career_tests:
                with pd.ExcelWriter(f'{end_folder}/{dct_out_name_tests[name_test]}.xlsx', engine='xlsxwriter') as writer:
                    for sheet_name, dataframe in temp_dct.items():
                        dataframe.to_excel(writer, sheet_name=sheet_name,index=False)
            else:
                temp_wb = write_df_to_excel(temp_dct, write_index=False)
                temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                temp_wb.save(f'{end_folder}/{dct_out_name_tests[name_test]}.xlsx')


            # увеличиваем предел обозначающий количество обработанных колонок
            threshold_finshed += dct_tests[name_test][1]

        # Сохраняем в удобном виде
        if len(lst_check_alert_tests) != 0:
            # Отбираем тех кто требует внимания.
            set_alert_value = ['высокий уровень выгорания','имеется выгорание','критический уровень выгорания','крайне высокий уровень',
                               '250-299','300 и более','очень высокий уровень','низкий уровень адаптации','выраженная социально-психологическая дезадаптация',
                               'очень высокий уровень тревожности','тяжелая депрессия','безнадежность тяжёлая','истинное депрессивное состояние',
                               'посттравматическое стрессовое расстройство','151-175','176-195','81-110','27-36','8-10','неблагоприятный','высокий уровень DASS','высокий уровень ППН',
                               'ярко выраженный признак','высокий показатель'
                               ] # особое внимание

            set_attention_value = ['пограничное выгорание','симптомы выгорания','начинающееся выгорание','средний уровень выгорания','высокий уровень','доминирующий симптом',
                                   'не благоприятное состояние','преобладает плохое настроение','низкий уровень самооценки','высокий уровень социального остракизма',
                                   'легкая степень социально-психологической дезадаптации','0-19','высокий уровень тревожности','умеренная депрессия','безнадежность умеренная',
                                   'субдепрессивное состояние или маскированная депрессия',
                                   'нарушение адаптации','126-150','61-80','20-26','6-7','высокий уровень ШТФ','ближе к высокому'
                                   ] # обратить внимание
            alert_df = main_itog_df[main_itog_df.isin(set_alert_value).any(axis=1)] # фильтруем требующих особого внимания
            if len(alert_df) == 0:
                alert_df = pd.DataFrame(columns=main_itog_df.columns)
            attention_df = main_itog_df[~main_itog_df.isin(set_alert_value).any(axis=1)] # получаем оставшихся
            attention_df = attention_df[attention_df.apply(lambda x:count_attention(x,set_attention_value),axis=1)]
            if len(attention_df) == 0:
                attention_df = pd.DataFrame(columns=main_itog_df.columns)


            # Сохраняем в зависимости от количества сводных колонок
            if len(lst_svod_cols) == 0:
                if len(base_df) != 0:
                    main_itog_df.sort_values(by=base_df.columns[0],inplace=True)
                temp_wb = write_df_to_excel({'Свод по всем тестам':main_itog_df,'Особое внимание':alert_df,'Зона риска':attention_df}, write_index=False)
                temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                temp_wb.save(f'{end_folder}/Общий результат.xlsx')

            elif len(lst_svod_cols) == 1:
                main_itog_df.sort_values(by=lst_svod_cols[0], inplace=True)  # сортируем
                svod_one_df = main_itog_df.groupby(by=lst_svod_cols[0]).agg({main_itog_df.columns[-1]:'count'}).rename(columns={main_itog_df.columns[-1]:'Количество прошедших тестирование'})
                svod_one_df = svod_one_df.reset_index()
                svod_one_df.sort_values(by='Количество прошедших тестирование',ascending=False,inplace=True)

                # очищаем название колонки по которой делали свод
                name_one = lst_svod_cols[0]
                name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
                name_one = name_one[:20]

                temp_wb = write_df_to_excel({'Свод по всем тестам':main_itog_df,'Особое внимание':alert_df,'Зона риска':attention_df,
                                             name_one:svod_one_df}, write_index=False)
                temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                temp_wb.save(f'{end_folder}/Общий результат.xlsx')

            elif len(lst_svod_cols) == 2:
                main_itog_df.sort_values(by=lst_svod_cols[0], inplace=True)  # сортируем
                svod_one_df = main_itog_df.groupby(by=lst_svod_cols[0]).agg({main_itog_df.columns[-1]:'count'}).rename(columns={main_itog_df.columns[-1]:'Количество прошедших тестирование'})
                svod_one_df = svod_one_df.reset_index()
                svod_one_df.sort_values(by='Количество прошедших тестирование',ascending=False,inplace=True)

                # очищаем название колонки по которой делали свод
                name_one = lst_svod_cols[0]
                name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
                name_one = name_one[:20]

                # Делаем по второй колонке
                svod_two_df = main_itog_df.groupby(by=lst_svod_cols[1]).agg({main_itog_df.columns[-1]: 'count'}).rename(
                    columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                svod_two_df = svod_two_df.reset_index()
                svod_two_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                # очищаем название колонки по которой делали свод
                name_two = lst_svod_cols[1]
                name_two = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_two)
                name_two = name_two[:20]

                all_svod_df = pd.pivot_table(data=main_itog_df,
                                             index=lst_svod_cols,
                                             values=main_itog_df.columns[-1],
                                             aggfunc='count',
                                             )

                all_svod_df = all_svod_df.reset_index()
                all_svod_df.rename(columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'},inplace=True)

                temp_wb = write_df_to_excel(
                    {'Свод по всем тестам': main_itog_df, 'Особое внимание': alert_df, 'Зона риска': attention_df,
                     name_one: svod_one_df,name_two:svod_two_df,f'{name_one[:12]}_{name_two[:12]}':all_svod_df}, write_index=False)
                temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                temp_wb.save(f'{end_folder}/Общий результат.xlsx')
            elif len(lst_svod_cols) == 3:
                main_itog_df.sort_values(by=lst_svod_cols[0], inplace=True)  # сортируем
                svod_one_df = main_itog_df.groupby(by=lst_svod_cols[0]).agg({main_itog_df.columns[-1]:'count'}).rename(columns={main_itog_df.columns[-1]:'Количество прошедших тестирование'})
                svod_one_df = svod_one_df.reset_index()
                svod_one_df.sort_values(by='Количество прошедших тестирование',ascending=False,inplace=True)

                # очищаем название колонки по которой делали свод
                name_one = lst_svod_cols[0]
                name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
                name_one = name_one[:20]

                # Делаем по второй колонке
                svod_two_df = main_itog_df.groupby(by=lst_svod_cols[1]).agg({main_itog_df.columns[-1]: 'count'}).rename(
                    columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                svod_two_df = svod_two_df.reset_index()
                svod_two_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                # очищаем название колонки по которой делали свод
                name_two = lst_svod_cols[1]
                name_two = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_two)
                name_two = name_two[:20]

                # делаем по третьей колонке
                # Делаем по второй колонке
                svod_three_df = main_itog_df.groupby(by=lst_svod_cols[2]).agg({main_itog_df.columns[-1]: 'count'}).rename(
                    columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                svod_three_df = svod_three_df.reset_index()
                svod_three_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                # очищаем название колонки по которой делали свод
                name_three = lst_svod_cols[2]
                name_three = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_three)
                name_three = name_three[:20]


                all_svod_df = pd.pivot_table(data=main_itog_df,
                                             index=lst_svod_cols,
                                             values=main_itog_df.columns[-1],
                                             aggfunc='count',
                                             )

                all_svod_df = all_svod_df.reset_index()
                all_svod_df.rename(columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'},inplace=True)

                temp_wb = write_df_to_excel(
                    {'Свод по всем тестам': main_itog_df, 'Особое внимание': alert_df, 'Зона риска': attention_df,
                     name_one: svod_one_df,name_two:svod_two_df,name_three:svod_three_df,f'{name_one[:7]}_{name_two[:7]}_{name_three[:7]}':all_svod_df}, write_index=False)
                temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                temp_wb.save(f'{end_folder}/Общий результат.xlsx')

        else:
            # Если есть профориентационные тесты, то сохраняем через пандас
            if len(lst_check_career_tests) != 0:
                if len(lst_svod_cols) == 0:
                    if len(base_df) != 0:
                        main_itog_df.sort_values(by=base_df.columns[0], inplace=True)
                    with pd.ExcelWriter(f'{end_folder}/Общий результат.xlsx', engine='xlsxwriter') as writer:
                        main_itog_df.to_excel(writer,sheet_name='Свод по всем тестам',index=False)
                elif len(lst_svod_cols) == 1:
                    main_itog_df.sort_values(by=lst_svod_cols[0], inplace=True)  # сортируем
                    svod_one_df = main_itog_df.groupby(by=lst_svod_cols[0]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_one_df = svod_one_df.reset_index()
                    svod_one_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_one = lst_svod_cols[0]
                    name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
                    name_one = name_one[:20]
                    with pd.ExcelWriter(f'{end_folder}/Общий результат.xlsx', engine='xlsxwriter') as writer:
                        for sheet_name, dataframe in {'Свод по всем тестам': main_itog_df, name_one: svod_one_df}.items():
                            dataframe.to_excel(writer, sheet_name=sheet_name,index=False)
                elif len(lst_svod_cols) == 2:
                    main_itog_df.sort_values(by=lst_svod_cols[0], inplace=True)  # сортируем
                    svod_one_df = main_itog_df.groupby(by=lst_svod_cols[0]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_one_df = svod_one_df.reset_index()
                    svod_one_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_one = lst_svod_cols[0]
                    name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
                    name_one = name_one[:20]

                    # Делаем по второй колонке
                    svod_two_df = main_itog_df.groupby(by=lst_svod_cols[1]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_two_df = svod_two_df.reset_index()
                    svod_two_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_two = lst_svod_cols[1]
                    name_two = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_two)
                    name_two = name_two[:20]

                    all_svod_df = pd.pivot_table(data=main_itog_df,
                                                 index=lst_svod_cols,
                                                 values=main_itog_df.columns[-1],
                                                 aggfunc='count',
                                                 )

                    all_svod_df = all_svod_df.reset_index()
                    all_svod_df.rename(columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'},
                                       inplace=True)

                    with pd.ExcelWriter(f'{end_folder}/Общий результат.xlsx', engine='xlsxwriter') as writer:
                        for sheet_name, dataframe in {'Свод по всем тестам': main_itog_df, name_one: svod_one_df,
                                                      name_two:svod_two_df,f'{name_one[:12]}_{name_two[:12]}': all_svod_df}.items():
                            dataframe.to_excel(writer, sheet_name=sheet_name,index=False)

                elif len(lst_svod_cols) == 3:
                    main_itog_df.sort_values(by=lst_svod_cols[0], inplace=True)  # сортируем
                    svod_one_df = main_itog_df.groupby(by=lst_svod_cols[0]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_one_df = svod_one_df.reset_index()
                    svod_one_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_one = lst_svod_cols[0]
                    name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
                    name_one = name_one[:20]

                    # Делаем по второй колонке
                    svod_two_df = main_itog_df.groupby(by=lst_svod_cols[1]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_two_df = svod_two_df.reset_index()
                    svod_two_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_two = lst_svod_cols[1]
                    name_two = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_two)
                    name_two = name_two[:20]

                    # делаем по третьей колонке
                    # Делаем по второй колонке
                    svod_three_df = main_itog_df.groupby(by=lst_svod_cols[2]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_three_df = svod_three_df.reset_index()
                    svod_three_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_three = lst_svod_cols[2]
                    name_three = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_three)
                    name_three = name_three[:20]

                    all_svod_df = pd.pivot_table(data=main_itog_df,
                                                 index=lst_svod_cols,
                                                 values=main_itog_df.columns[-1],
                                                 aggfunc='count',
                                                 )

                    all_svod_df = all_svod_df.reset_index()
                    all_svod_df.rename(columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'},
                                       inplace=True)


                    with pd.ExcelWriter(f'{end_folder}/Общий результат.xlsx', engine='xlsxwriter') as writer:
                        for sheet_name, dataframe in {'Свод по всем тестам': main_itog_df, name_one: svod_one_df,
                                                      name_two:svod_two_df,
                                                      name_three:svod_three_df,
                                                      f'{name_one[:7]}_{name_two[:7]}_{name_three[:7]}': all_svod_df}.items():
                            dataframe.to_excel(writer, sheet_name=sheet_name,index=False)










            else:
                # Сохраняем в зависимости от количества сводных колонок
                if len(lst_svod_cols) == 0:
                    temp_wb = write_df_to_excel(
                        {'Свод по всем тестам': main_itog_df},
                        write_index=False)
                    temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                    temp_wb.save(f'{end_folder}/Общий результат.xlsx')

                elif len(lst_svod_cols) == 1:
                    main_itog_df.sort_values(by=lst_svod_cols[0], inplace=True)  # сортируем
                    svod_one_df = main_itog_df.groupby(by=lst_svod_cols[0]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_one_df = svod_one_df.reset_index()
                    svod_one_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_one = lst_svod_cols[0]
                    name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
                    name_one = name_one[:20]

                    temp_wb = write_df_to_excel(
                        {'Свод по всем тестам': main_itog_df,
                         name_one: svod_one_df}, write_index=False)
                    temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                    temp_wb.save(f'{end_folder}/Общий результат.xlsx')

                elif len(lst_svod_cols) == 2:
                    main_itog_df.sort_values(by=lst_svod_cols[0], inplace=True)  # сортируем
                    svod_one_df = main_itog_df.groupby(by=lst_svod_cols[0]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_one_df = svod_one_df.reset_index()
                    svod_one_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_one = lst_svod_cols[0]
                    name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
                    name_one = name_one[:20]

                    # Делаем по второй колонке
                    svod_two_df = main_itog_df.groupby(by=lst_svod_cols[1]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_two_df = svod_two_df.reset_index()
                    svod_two_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_two = lst_svod_cols[1]
                    name_two = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_two)
                    name_two = name_two[:20]

                    all_svod_df = pd.pivot_table(data=main_itog_df,
                                                 index=lst_svod_cols,
                                                 values=main_itog_df.columns[-1],
                                                 aggfunc='count',
                                                 )

                    all_svod_df = all_svod_df.reset_index()
                    all_svod_df.rename(columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'},
                                       inplace=True)

                    temp_wb = write_df_to_excel(
                        {'Свод по всем тестам': main_itog_df,
                         name_one: svod_one_df, name_two: svod_two_df, f'{name_one[:12]}_{name_two[:12]}': all_svod_df},
                        write_index=False)
                    temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                    temp_wb.save(f'{end_folder}/Общий результат.xlsx')
                elif len(lst_svod_cols) == 3:
                    main_itog_df.sort_values(by=lst_svod_cols[0], inplace=True)  # сортируем
                    svod_one_df = main_itog_df.groupby(by=lst_svod_cols[0]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_one_df = svod_one_df.reset_index()
                    svod_one_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_one = lst_svod_cols[0]
                    name_one = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_one)
                    name_one = name_one[:20]

                    # Делаем по второй колонке
                    svod_two_df = main_itog_df.groupby(by=lst_svod_cols[1]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_two_df = svod_two_df.reset_index()
                    svod_two_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_two = lst_svod_cols[1]
                    name_two = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_two)
                    name_two = name_two[:20]

                    # делаем по третьей колонке
                    # Делаем по второй колонке
                    svod_three_df = main_itog_df.groupby(by=lst_svod_cols[2]).agg(
                        {main_itog_df.columns[-1]: 'count'}).rename(
                        columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'})
                    svod_three_df = svod_three_df.reset_index()
                    svod_three_df.sort_values(by='Количество прошедших тестирование', ascending=False, inplace=True)

                    # очищаем название колонки по которой делали свод
                    name_three = lst_svod_cols[2]
                    name_three = re.sub(r'[\[\]\'+()<> :"?*|\\/]', '_', name_three)
                    name_three = name_three[:20]

                    all_svod_df = pd.pivot_table(data=main_itog_df,
                                                 index=lst_svod_cols,
                                                 values=main_itog_df.columns[-1],
                                                 aggfunc='count',
                                                 )

                    all_svod_df = all_svod_df.reset_index()
                    all_svod_df.rename(columns={main_itog_df.columns[-1]: 'Количество прошедших тестирование'},
                                       inplace=True)

                    temp_wb = write_df_to_excel(
                        {'Свод по всем тестам': main_itog_df,
                         name_one: svod_one_df, name_two: svod_two_df, name_three: svod_three_df,
                         f'{name_one[:7]}_{name_two[:7]}_{name_three[:7]}': all_svod_df}, write_index=False)
                    temp_wb = del_sheet(temp_wb, ['Sheet', 'Sheet1', 'Для подсчета'])
                    temp_wb.save(f'{end_folder}/Общий результат.xlsx')



    except FileNotFoundError:
        messagebox.showerror('Лахеcис',
                                 f'Перенесите файлы которые вы хотите обработать или конечную папку в корень диска. Проблема может быть\n '
                                 f'в слишком длинном пути к обрабатываемым файлам')
    except PermissionError:
        messagebox.showerror('Лахеcис',
                                 f'Закройте все файлы созданные программой Лахесис и запустите повторно обработку'
                                 )
    except NotSameSize:
        messagebox.showerror('Лахеcис',
                                 f'Не совпадает количество колонок с ответами на тесты с эталонным количеством. В файле {df.shape[1]} колонок а должно быть {check_size_df+threshold_base}.')
    except NotCorrectParamsTests:
        messagebox.showerror('Лахеcис',
                                 f'В файле с параметрами тестирования (в котором вы указали использованные тесты) не найдено ни одного правильного названия теста.\nПроверьте написание названий тестов.')

    except NotCorrectSvodCols:
        messagebox.showerror('Лахеcис',
                                 f'Проверьте правильность написания порядковых номеров колонок по которым вы хотите сделать свод.\nПравильный формат это не более трех чисел разделенных запятой, начиная с цифры 1, '
                                 f'например 1,3 или 2 или 3,1,2 а если вам не нужны своды то оставьте это поле пустым.\n'
                                 f'Проверьте числа которые вы указали потому что, порядковый номер колонки не может превышать количество колонок в анкетной части вашего файла с ответами на тест.')
    else:
        messagebox.showinfo('Лахеcис',
                                'Данные успешно обработаны')


if __name__ == '__main__':
    main_params_adults = 'c:/Users/1/PycharmProjects/Lachesis/data/параметры РЦО 5-6 кл.xlsx'
    main_params_adults = 'c:/Users/1/PycharmProjects/Lachesis/data/параметры Мотивация риск неудача.xlsx'
    main_params_adults = 'c:/Users/1/PycharmProjects/Lachesis/data/параметры Кеттел 14-PF.xlsx'
    main_params_adults = 'c:/Users/1/PycharmProjects/Lachesis/data/параметры 4_0.xlsx'
    # main_params_adults = 'c:/Users/1/PycharmProjects/Lachesis/data/параметры Агрессивность.xlsx'

    main_adults_data = 'c:/Users/1/PycharmProjects/Lachesis/data/РЦО 5-6 класс.xlsx'
    main_adults_data = 'c:/Users/1/PycharmProjects/Lachesis/data/Мотивация,риск,неудача.xlsx'
    main_adults_data = 'c:/Users/1/PycharmProjects/Lachesis/data/Кеттел 14-PF Рукавишников Соколова.xlsx'
    main_adults_data = 'c:/Users/1/PycharmProjects/Lachesis/data/Батарея 4_0.xlsx'
    # main_adults_data = 'c:/Users/1/PycharmProjects/Lachesis/data/Агрессивность.xlsx'


    main_end_folder = 'c:/Users/1/PycharmProjects/Lachesis/data/Результат'
    main_quantity_descr_cols = 4
    main_svod_cols = ''

    generate_result_all_age(main_params_adults, main_adults_data, main_end_folder, main_quantity_descr_cols, main_svod_cols)

    print('Lindy Booth')
