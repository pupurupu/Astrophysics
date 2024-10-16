import pandas as pd
import math as m


def parallax(a_, P_, M_):
    return a_ / ((P_ * P_ * (M_)) ** (1 / 3))


def interpolation_linear(x, y, x1):
    if x[0] > x[len(x) - 1]:
        x.reverse()
        y.reverse()
    y_ = 0
    for w in range(len(x) - 1):
        if x[w] == x1:
            y_ = y[w]
            break
        elif (x[w] < x1) and (x1 < x[w + 1]):
            a = (y[w + 1] - y[w]) / (x[w + 1] - x[w])
            b = y[w] - a * x[w]
            y_ = a * x1 + b
            break
    return y_


def definition_of_dynamic_parallax(Parallax1):
    absolute_mV1 = round(mV1 + 5 + 5 * m.log10(Parallax1), 2)
    absolute_mV2 = round(mV2 + 5 + 5 * m.log10(Parallax1), 2)
    print("m_v1 = ", "%.02f" % absolute_mV1)
    print("m_v2 = ", "%.02f" % absolute_mV2)

    M_bol1 = round(absolute_mV1 + BC_sp1, 2)
    M_bol2 = round(absolute_mV2 + BC_sp2, 2)
    print("M_bol1 = ", "%.02f" % M_bol1)
    print("M_bol2 = ", "%.02f" % M_bol2)

    Mass_sol1 = round(10 ** (interpolation_linear(M_BOL_DATA, LOG_DATA, M_bol1)), 2)
    Mass_sol2 = round(10 ** (interpolation_linear(M_BOL_DATA, LOG_DATA, M_bol2)), 2)
    print("Mass_1 = ", "%.02f" % Mass_sol1)
    print("Mass_2 = ", "%.02f" % Mass_sol2)

    Parallax2 = round(parallax(a_, P, Mass_sol1 + Mass_sol2), 3)
    print(f"Параллакс 2 = {'%.03f' % Parallax2}\"")

    return Parallax2


data = pd.read_csv('C:/Users/tyuli/OneDrive/Рабочий стол/data_parallax.txt', delimiter='\t')
data.columns=['N', 'Звезда', 'Коорд. 2000.0', 'mV1',
              'mV2', 'Sp1', 'Sp2', 'P (лет)', 'а']

M_V_DATA = [-5.8, -4.1, -1.1, 0.7, 2, 2.6, 3.4, 4.4, 5.1, 5.9, 7.3, 9, 11.8]
BC_DATA = [-4, -2.8, -1.5, -0.4, -0.12, -0.06, 0, -0.03, -0.07, -0.19, -0.6, -1.19, -2.3]

M_BOL_DATA = [12.1, 10.9, 9.7, 8.4, 6.6, 4.7, 2.7, 0.7, -1.1, -2.9, -4.6, -6.3, -7.6, -8.9, -10.2]
LOG_DATA = [-1, -0.8, -0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6, 0.8, 1, 1.2, 1.4, 1.6, 1.8]

for i in range(len(data)):
    print("-------\n", data['Звезда'].iloc[i])
    print("--------------------")

    M1, M2 = 1, 1
    a_ = float(data['а'].iloc[i])
    P = float(data['P (лет)'].iloc[i])
    mV1 = float(str(data['mV1'].iloc[i]).replace(' ', ''))
    mV2 = float(str(data['mV2'].iloc[i]).replace(' ', ''))

    m_v_sp1 = float(input(f"Значение M_v для {data['Sp1'].iloc[i]}: ", ))
    m_v_sp2 = float(input(f"Значение M_v для {data['Sp2'].iloc[i]}: ", ))

    BC_sp1 = interpolation_linear(M_V_DATA, BC_DATA, m_v_sp1)
    BC_sp2 = interpolation_linear(M_V_DATA, BC_DATA, m_v_sp2)

    Parallax1 = parallax(a_, P, M1 + M2)
    print(f"Параллакс 1 = {'%.03f' % Parallax1}\"")

    Parallax2 = definition_of_dynamic_parallax(Parallax1)
    print("--------------------")

    count = 1
    while abs(Parallax1 - Parallax2) > 0.001:
        Parallax1 = Parallax2
        print(f"Параллакс 1 = {'%.03f' % Parallax1}\"")

        Parallax2 = definition_of_dynamic_parallax(Parallax1)
        print("--------------------")

        count +=1

    print("Количество итераций: ", count)
    print(f"Значение динамического параллакса: {'%.03f' % Parallax2}\"")