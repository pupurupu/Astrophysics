import numpy as np
import math as m
import pandas as pd


def average_value(obj_time_sec, obj_count):
    obj_average_time_sec = []
    obj_average_count = []
    c = 0
    for r in range(len(obj_time_sec)):
        value_time_sec = obj_time_sec[r + c]
        value_count = obj_count[r + c]
        z = 1
        while obj_time_sec[r + c + 1] - obj_time_sec[r + c] <= 60:
            value_time_sec += obj_time_sec[r + c + 1]
            value_count += obj_count[r + c + 1]
            z += 1
            c += 1
            if (r + c + 1) == len(obj_time_sec):
                break
        average_time_sec = value_time_sec / z
        average_count = value_count / z
        obj_average_time_sec.append(average_time_sec)
        obj_average_count.append(average_count)
        if (r + c + 1) == len(obj_time_sec):
            break
    return obj_average_time_sec, obj_average_count


def extrapolation(x1, x2, x, y1, y2):
    y_ = y1 + (x - x1) * (y2 - y1) / (x2 - x1)
    fon_inter_count.append(y_)


def interpolation_linear(x_, x, y, x1):
    for w in range(len(x) - 1):
        if x[w] == x_:
            y_ = y[w]
        elif x[w + 1] == x_:
            y_ = y[w + 1]
        elif (x[w] < x_) and (x_ < x[w + 1]):
            a = (y[w + 1] - y[w]) / (x[w + 1] - x[w])
            b = y[w] - a * x[w]
            y_ = a * x_ + b
            if x_ == x1:
                fon_inter_count.append(y_)


def recalculation_time(t, split_smb, unit):
    hour, min, t_hm = 0, 0, 0
    if unit == 'second':
        while t > 86399:
            t -= 86399
        hour = t // 3600
        t %= 3600
        min = t // 60
    elif unit == 'hour':
        while t >= 24:
            t -= 24
        hour = int(t)
        min = (t - hour) * 60
    if split_smb == ':':
        t_hm = "%02d:%02d" % (hour, min)
    elif split_smb == ' ':  # !!!изменен разделитель
        t_hm = "%02d:%02d" % (hour, min)
    return t_hm


# filter = str(input("Фильтр: " ))
# print('Значения с точностью до минут')
# right_ascension = input("Прямое восхождение: " ).split('-')
# right_ascension = int(right_ascension[0])*60 + int(right_ascension[1])
# declination = input("Склонение: " ).split('-')
# declination = int(declination[0])*60 + int(declination[1])
# longitude = input("Долгота: " ).split('-')
# longitude = int(longitude[0])*60 + int(longitude[1])
# latitude = input("Широта: " ).split('-')
# latitude = int(latitude[0])*60 + int(latitude[1])
# siderial_time = input("Звездное время: " ).split('-')
# siderial_time = int(siderial_time[0])*60 + int(siderial_time[1])
filter = 'U'
right_ascension = 10 * 60 + 19.6
declination = 19 * 60 + 52.2
longitude = 41 * 60 + 27
longitude_angle = longitude / 15
time_zone = m.ceil(longitude_angle / 60)
latitude = 43 * 60 + 49
sidereal_time_0 = 10 * 60 + 49.1
k_ = 1.0027379093

# File = str(input("Путь к файлу: "))
# f = open(f"{File}", 'r')
f = open("C:/Users/tyuli/OneDrive/Рабочий стол/ADLeo.txt", "r")
lines = f.readlines()
columns = 0
index_Time, index_Texp, index_filter = 0, 0, 0
for line in lines:
    if 'Object' and 'Time' in line:
        row = line.split(' ')
        for index, parameter in enumerate(row):
            if 'Time' in parameter:
                index_Time = index
            if 'Texp' in parameter:
                index_Texp = index
            if filter in parameter:
                index_filter = index
        break
    else:
        columns += 1

fon_time = []  # время отсчетов fon
fon_time_sec = []  # время отсчетов fon в секундах
fon_count = []  # отсчеты fon
comp_time = []  # время отсчетов comp
comp_time_sec = []  # время отсчетов comp в секундах
comp_count = []  # отсчеты comp
object_type = ''  # для сортировки данных fon, comp и tok
# Сортировка данных
for j in range(columns + 1, len(lines)):
    lines_array = lines[j].split(' ')
    if lines_array[0] == 'fon':
        fon_time.append(lines_array[index_Time])
        time = lines_array[index_Time].split(':')
        time = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
        if time < 12 * 3600:
            time += 24 * 3600
        fon_time_sec.append(time)
        count = int(lines_array[index_filter]) / int(lines_array[index_Texp])
        fon_count.append(count)
        object_type = 'fon'
    elif lines_array[0] == 'comp':
        comp_time.append(lines_array[index_Time])
        time = lines_array[index_Time].split(':')
        time = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
        if time < 12 * 3600:
            time += 24 * 3600
        comp_time_sec.append(time)
        count = int(lines_array[index_filter]) / int(lines_array[index_Texp])
        comp_count.append(count)
        object_type = 'comp'
    elif lines_array[0] == 'tok':
        object_type = 'tok'
    elif lines_array[0] == '-':
        time = lines_array[index_Time].split(':')
        time = int(time[0]) * 3600 + int(time[1]) * 60 + int(time[2])
        if time < 12 * 3600:
            time += 24 * 3600
        count = int(lines_array[index_filter]) / int(lines_array[index_Texp])
        if object_type == 'fon':
            fon_time.append(lines_array[index_Time])
            fon_time_sec.append(time)
            fon_count.append(count)
        elif object_type == 'comp':
            comp_time.append(lines_array[index_Time])
            comp_time_sec.append(time)
            comp_count.append(count)
f.close()
# Усреднение данных
fon_average_time_sec, fon_average_count = average_value(fon_time_sec, fon_count)
comp_average_time_sec, comp_average_count = average_value(comp_time_sec, comp_count)
# Получение отсчетов fon на моменты времени comp
fon_inter_count = []
for k in range(len(comp_average_count)):
    new_array = np.linspace(fon_average_time_sec[0],
                            fon_average_time_sec[len(fon_average_time_sec) - 1], 30)
    new_array = np.append(new_array, comp_average_time_sec[k])
    new_array = np.sort(new_array)
    for i in range(len(new_array)):
        interpolation_linear(new_array[i], fon_average_time_sec,
                             fon_average_count, comp_average_time_sec[k])
    if comp_average_time_sec[k] > fon_average_time_sec[len(fon_average_time_sec) - 1]:
        extrapolation(fon_average_time_sec[len(fon_average_time_sec) - 2],
                      fon_average_time_sec[len(fon_average_time_sec) - 1],
                      comp_average_time_sec[k], fon_average_count[len(fon_average_count) - 2],
                      fon_average_count[len(fon_average_count) - 1])
# Получение отсчетов на звезду
star_count = []
for i in range(len(fon_inter_count)):
    star_count.append(comp_average_count[i] - fon_inter_count[i])

comp_time_absorption = []  # время
mst = []  # среднее солнечное время
sidereal_time = []  # Звездное время наблюдения
hour_angle = []  # Часовой угол
air_mass = []  # Воздушная масса
# Вычисление воздушной массы
for k in range(len(comp_average_time_sec)):
    comp_time_absorption.append(recalculation_time(comp_average_time_sec[k], " ", 'second'))
    if comp_average_time_sec[k] / 3600 >= 24:
        mst_ = (comp_average_time_sec[k] - 24) / 3600 - time_zone + longitude_angle / 60
    else:
        mst_ = comp_average_time_sec[k] / 3600 - time_zone + longitude_angle / 60
    mst.append(recalculation_time(mst_, " ", 'hour'))
    sidereal_time_ = sidereal_time_0 / 60 + mst_ * k_
    sidereal_time.append(recalculation_time(sidereal_time_, " ", 'hour'))
    hour_angle_ = sidereal_time_ - right_ascension / 60
    hour_angle.append(recalculation_time(mst_, " ", 'hour'))
    air_mass_ = 1 / (m.sin(m.radians(latitude / 60)) * m.sin(m.radians(declination / 60)) +
                     m.cos(m.radians(latitude / 60)) * m.cos(m.radians(declination / 60)) *
                     m.cos(m.radians(hour_angle_ * 15)))
    air_mass.append(air_mass_)

df1 = pd.DataFrame({'T(мск)': comp_time_absorption,
                    'm': mst, 's': sidereal_time,
                    't': hour_angle, 'M': air_mass})

# Получение звездной величины
magnitude = []
for p in range(len(star_count)):
    magnitude.append((-2.5 * m.log10(star_count[p])))
# Усреднение некоторых значений воздушной массы и звездной величины
air_mass_average = air_mass
magnitude_average = magnitude
time_star = comp_average_time_sec
for s in range(len(air_mass)):
    for i in range(len(air_mass_average)):
        am1 = air_mass_average[s]
        am2 = air_mass_average[i]
        m1 = magnitude_average[s]
        m2 = magnitude_average[i]
        t1 = comp_average_time_sec[s]
        t2 = comp_average_time_sec[i]
        if s != i and abs(am1 - am2) < 0.005 and abs(m1 - m2) < 0.005:
            new_air_mass = (am1 + am2) / 2
            new_magnitude = (m1 + m2) / 2
            air_mass_average[s] = new_air_mass
            air_mass_average.remove(am2)
            magnitude_average[s] = new_magnitude
            magnitude_average.remove(m2)
            new_time_star = (t1 + t2) / 2
            time_star[s] = new_time_star
            time_star.remove(t2)
            break
    if s == len(air_mass_average) - 1:
        break
# Коэффициент экстинкции
absorption_coefficients = []  # коэффициент экстинкции
time_interval = []  # промежуток времени
time_absorption = []  # среднее время промежутка
for j in range(len(magnitude_average) - 1):
    a_ = (magnitude_average[j] - magnitude_average[j + 1]) / (air_mass_average[j] - air_mass_average[j + 1])
    t_ = (time_star[j + 1] + time_star[j]) / 2
    absorption_coefficients.append(a_)
    time_interval.append(recalculation_time(t_, ":", "second"))
    time_absorption.append(f'{recalculation_time(time_star[j], ":", "second")} - '
                           f'{recalculation_time(time_star[j + 1], ":", "second")}')

df2 = pd.DataFrame({'Возд.масса': air_mass_average,
                    'Зв.величина': magnitude_average})

df3 = pd.DataFrame({'Время': time_absorption,
                    'Средн.время': time_interval,
                    'Коэф.экстинкции': absorption_coefficients})

print('----------------------------------')
print(df1.to_string(justify='right', index=False))
print('----------------------------------')
print(df2.to_string(justify='right', index=False))
print('-------------------------------------------')
print(df3.to_string(justify='right', index=False))
print('-------------------------------------------')
