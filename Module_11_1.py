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
#  В приложении к ссылке на GitHub напишите комментарий о возможностях, которые предоставила
#  вам выбранная библиотека и как вы расширили возможности Python с её помощью.
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

def single_disp(data):

    # Выделяем группы для операции над данными
    first_group = [i for i in data[1]]
    second_group = [i for i in data[2]]
    third_group = [i for i in data[3]]
    fourth_group = [i for i in data[4]]

    number_of_groups = len([first_group, second_group, third_group, fourth_group])

    # Все группы тут
    all_groups = first_group + second_group + third_group + fourth_group

    # среднее значение всей группы
    mean_of_all_groups = np.mean(all_groups)

    # Общая изменчивость наших данных, здесь мы расчитали сумму всех квадратов отклонение от среднего
    sum_of_squared_total = sum([(i - mean_of_all_groups) ** 2 for i in all_groups])

    # Число степеней свободы в SST
    df_of_sst = len(all_groups) - 1

    # для расчета суммы квадратов  расчитаем сумму квадратов всех групп
    mean1 = np.mean(first_group)
    mean2 = np.mean(second_group)
    mean3 = np.mean(third_group)
    mean4 = np.mean(fourth_group)
    ssw1 = sum([(i - mean1) ** 2 for i in first_group])
    ssw2 = sum([(i - mean2) ** 2 for i in second_group])
    ssw3 = sum([(i - mean3) ** 2 for i in third_group])
    ssw4 = sum([(i - mean4) ** 2 for i in fourth_group ])

    # сумма квадратов внутригрупповая
    sum_of_squared_within = ssw1 + ssw2 + ssw3 + ssw4

    # Число степеней свободы внутригрупповое
    df_of_ssw = len(all_groups) - number_of_groups

    # Теперь узнаем на сколько наши групповые отклоняются от общегрупповых средних

    # для вычета из каждой группы
    for_minus_from_each_group = [first_group, second_group, third_group, fourth_group]
    sum_of_squared_between = \
        sum([number_of_groups * (np.mean(i) - mean_of_all_groups) ** 2 for i in for_minus_from_each_group])

    # Число степеней свободы межгрупповое
    df_of_ssb = number_of_groups - 1

    # Расчитаем F-значение, основной показатель дисперсионного анализа
    F = (sum_of_squared_between / df_of_ssb) / (sum_of_squared_within / df_of_ssw)

    # Расчитаем  вероятность истинности нулевой гипотезы
    P_value = f.sf(F, df_of_ssb, df_of_ssw)

    # Обработаем полученный результат
    if P_value >= 0.05:
        return f"Мы не отклоняем нулевую гипотезу, так как P_value = {P_value}"
    else:
        return f"Мы отклоняем нулевую гипотезу, то есть P value = {P_value}, H1 верна то есть как минимум 2 группы данных различаются между собой в Генеральной совокупонсти"


if __name__ == '__main__':

    dic_ALL = {}
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

    dic_ALL[1] = lst_A
    dic_ALL[2] = lst_B
    dic_ALL[3] = lst_C
    dic_ALL[4] = lst_D

    data = pd.DataFrame(dic_ALL)

    result = single_disp(data)
    print(result)