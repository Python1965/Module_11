
# Домашнее задание по теме "Обзор сторонних библиотек Python"
# ***************************************************************************************
# Задача:
# Выберите одну или несколько сторонних библиотек Python, например, requests, pandas, numpy,
# matplotlib, pillow.После выбора библиотек(-и) изучите документацию к ней(ним), ознакомьтесь
# с их основными возможностями # и функциями.
#
# Если вы выбрали:
#   pandas - считать данные из файла, выполнить простой анализ данных (на своё усмотрение)
#            и вывести результаты в консоль.
#   numpy -  создать массив чисел, выполнить математические операции с массивом и вывести
#            результаты в консоль.
#
#  ****************************************************************************************
#
#               ********* ОДНОФАКТОРНЫЙ ДИСПЕРСИОННЫЙ АНАЛИЗ *********
#
#                       на основе лекций курса "СТАТИСТИКА",
#
#                            который я недавно окончил
#
#  ****************************************************************************************
# Содержание задачи.
#
# Генотерапия позволяет корректировать работу дефективного гена, ответственного за развитие
# заболевания. В эксперименте сравнивалась эффективность четырех различных типов терапии.
# Результаты наблюдений сведены в группы "A", "B", "C" и "D", и содержатся в файле
# genetherapy.csv.
#
# Необходимо сраванить группы наблюдений между собой методом однофакторного дисперсионного
# анализа.
#   - В этом случае нулевая гипотеза H0 будет предполагать, что на самом деле в генеральной
#     совокупности никаких значимых различий нет; более того - они все равны друг другу:
#       H0:  M1 = M2 = M3 = M4
#
#   - Альтернативная гипотеза H1 будет утверждать обратное, т.е. хотя бы пара средних
#     значений различаются между собой:
#       H1:  M1 != M2 != M3 != M4
#
# Файл данных скачать по ссылке
# https://stepik.org/media/attachments/lesson/8083/genetherapy.csv
#
# ****************************************************************************************

from scipy.stats import f
import numpy as np
import pandas as pd

def single_disp(data_df):

    # mean_of_all_groups = data_df.mean(axis=[,'A',], kipna=True, numeric_only=True)
    # specific_mean = data_df.loc[:, ['A']].mean(axis='columns', numeric_only=True)
    # specific_mean = data_df.loc[:, ['A']].mean()

    # data_lst = list(data_df.to_dict('list').values())
    data_dic = data_df.to_dict('list')
    data_lst = list(data_dic.values())
    number_of_groups = len(data_lst)

    # Данные из всех групп одним списком
    all_groups = []
    for item in data_lst:
        all_groups += item

    # X__ - среднее значение всех наблюдений
    mean_of_all_groups = np.mean(all_groups)

    # SST - сумма всех квадратов отклонений от среднего для всех наблюдений
    # (общая изменчивость данных)
    sum_of_squared_total = sum([(item - mean_of_all_groups) ** 2 for item in all_groups])

    # dF для SST - Число степеней свободы для всех наблюдений
    df_of_sst = len(all_groups) - 1

    # SSW - сумма квадратов отклонений от среднего внутригрупповая
    sum_of_squared_within = 0
    for group in data_lst:
        gr_mean = np.mean(group)
        sum_of_squared_within += sum([(item - gr_mean) ** 2 for item in group])

    # dF для SSW - число степеней свободы внутригрупповое
    df_of_ssw = len(all_groups) - number_of_groups

    # SSB - Сумма квадратов межгрупповая
    sum_of_squared_between = \
        sum([len(item) * (np.mean(item) - mean_of_all_groups) ** 2 for item in data_lst])

    #  dF для SSB -  Число степеней свободы межгрупповое
    df_of_ssb = number_of_groups - 1

    # Расчитаем F-значение, основной показатель дисперсионного анализа
    F = (sum_of_squared_between / df_of_ssb) / (sum_of_squared_within / df_of_ssw)

    # Расчитаем  вероятность истинности нулевой гипотезы
    P_value = f.sf(F, df_of_ssb, df_of_ssw)

    # Обработаем полученный результат
    if P_value >= 0.05:
        return f"Мы не отклоняем нулевую гипотезу, так как P_value = {P_value}"
    else:
        return (f"Мы отклоняем нулевую гипотезу, так как P_value = {P_value}. Гипотеза H1 верна,\n"
                f"то есть как минимум 2 группы наблюдений различаются между собой в Генеральной совокупонсти")


if __name__ == '__main__':

    lst_A = []
    lst_B = []
    lst_C = []
    lst_D = []

    with open("genetherapy.csv", 'r', encoding='utf-8') as file:
        for line in file:

            lst_tmp = line.rstrip().replace('"', '').split(",")
            if lst_tmp[1] == "Therapy": continue

            if lst_tmp[1] == "A": lst_A.append(float(lst_tmp[0]))
            elif lst_tmp[1] == "B": lst_B.append(float(lst_tmp[0]))
            elif lst_tmp[1] == "C": lst_C.append(float(lst_tmp[0]))
            elif lst_tmp[1] == "D": lst_D.append(float(lst_tmp[0]))

    dic_ALL = {}
    dic_ALL["A"] = lst_A
    dic_ALL["B"] = lst_B
    dic_ALL["C"] = lst_C
    dic_ALL["D"] = lst_D

    data = pd.DataFrame(dic_ALL)

    result = single_disp(data)
    print()
    print(result)
