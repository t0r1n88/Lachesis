# Скрипт для обработки результатов теста Профессиональное выгорание методика Н. Е. Водопьяновой на основе модели К. Маслач и С. Джексон
import pandas as pd




def processing_vod_prof_burnout(base_df: pd.DataFrame, answers_df: pd.DataFrame):
    """
    Функция для обработки
    :param base_df: часть датафрейма с описательными колонками
    :param answers_df: часть датафрейма с ответами
    """
    print('Burnout!')
