import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math as m


def lk(x, x_, k, s):
    l = 1
    for j in range(s - n, s + 1):
        if j != k:
            l *= (x_ - x[j]) / (x[k] - x[j])
    return (l)


def Ln(L_, n, x_, x, y):
    L = 0

    for i in range(len(x) - 1):
        if x[i] == x_:
            L = y[i]
            L_.append(L)
            break

        elif x[i + 1] == x_:
            L = y[i + 1]
            L_.append(L)
            break

        elif (x[i] < x_) and (x_ < x[i + 1]):
            s = i + n_
            for k in range(s - n, s + 1):
                L += y[k] * lk(x, x_, k, s)
            L_.append(L)


def coefficient_reg_inv_analit(x, y):
    size = len(x)
    numer_w1 = size * sum(x[i] * y[i] for i in range(0, size)) - sum(x) * sum(y)
    denom = size * sum((x[i]) ** 2 for i in range(0, size)) - (sum(x)) ** 2
    numer_w0 = -sum(x) * sum(x[i] * y[i] for i in range(0, size)) + sum((x[i]) ** 2 for i in range(0, size)) * sum(y)

    w1 = numer_w1 / denom
    w0 = numer_w0 / denom
    return w0, w1


data = pd.read_table("sim-id.txt", sep='|', header=None, on_bad_lines='skip')
data.columns = ["#", "dist(asec)", "prob.", "link ref", "link", "identifier",
                "typ", "coord1 (ICRS,J2000/2000)", "Mag U", "Mag B", "Mag V",
                "Mag R", "Mag I", "spec. type", "#bib", "#not"]
data = data.replace(" ", "", regex=True)

B_V_0 = [-0.35, -0.31, -0.16, 0, 0.13, 0.27, 0.42, 0.58, 0.70, 0.89, 1.18, 1.45, 1.63]
U_B_0 = [-1.15, -1.06, -0.55, -0.02, 0.1, 0.07, 0.03, 0.05, 0.19, 0.47, 1.10, 1.28, 1.2]
M_V = [-5.8, -4.1, -1.1, 0.7, 2, 2.6, 3.4, 4.4, 5.1, 5.9, 7.3, 9, 11.8]

x_ = np.linspace(B_V_0[0], B_V_0[len(B_V_0) - 1], 100)
n = 2
n_ = 1
L_ = []
M_ = []
for i in range(len(x_)):
    Ln(L_, n, x_[i], B_V_0, U_B_0)
for i in range(len(x_)):
    Ln(M_, n, x_[i], B_V_0, M_V)

V_all = []
B_V_all = []
U_B_all = []
typ_all = []
obj = []
count_all = 0

V = []
B_V = []
U_B = []
count = 0

V_int = []
B_V_int = []
U_B_int = []
count_int = 0

for i in range(3, len(data)):
    if ("NGC6611" in data['identifier'][i] and data['Mag U'][i] != "~" and data['Mag B'][i] != "~" and
            data['Mag V'][i] != "~" and data['identifier'][i] not in obj):
        V_all.append(float(data['Mag V'][i]))
        B_V_all.append(float(data['Mag B'][i]) - float(data['Mag V'][i]))
        U_B_all.append(float(data['Mag U'][i]) - float(data['Mag B'][i]))
        typ_all.append(data['typ'][i])
        obj.append(data['identifier'][i])
        count_all += 1
        if (data['typ'][i] == "*" or data['typ'][i] == "Y*O"):
            V.append(float(data['Mag V'][i]))
            B_V.append(float(data['Mag B'][i]) - float(data['Mag V'][i]))
            U_B.append(float(data['Mag U'][i]) - float(data['Mag B'][i]))
            count += 1
            if (1.3 <= (float(data['Mag B'][i]) - float(data['Mag V'][i])) <= 2.17 and
                    1 <= (float(data['Mag U'][i]) - float(data['Mag B'][i])) <= 2):
                V_int.append(float(data['Mag V'][i]))
                B_V_int.append(float(data['Mag B'][i]) - float(data['Mag V'][i]))
                U_B_int.append(float(data['Mag U'][i]) - float(data['Mag B'][i]))
                count_int += 1

[w0_2, w1_2] = coefficient_reg_inv_analit(B_V_int, U_B_int)

x = []
y = []
x.append(min(B_V_int))
y.append(min(B_V_int) * w1_2 + w0_2)
x.append(max(B_V_int))
y.append(max(B_V_int) * w1_2 + w0_2)

x0 = np.average(x)
y0 = np.average(y)
x1 = x0
y1 = y0

x_igr = np.flip(x_)
y_igr = np.flip(L_)

ans = "incorrect"
count = 0
while ans == "incorrect":
    c = 0
    for xj in x_igr:
        if (x0 - 0.02) <= xj <= (x0 + 0.02) and (y0 - 0.01) <= y_igr[np.where(x_igr == xj)[0][0]] <= (y0 + 0.01):
            ans = "correct"
            break
        elif xj > (x0 + 0.2) or xj < (x0 - 0.2):
            break
        else:
            c = 1
    if c == 1:
        x0 = x0 - 0.02
        y0 = y0 - 0.72 * 0.02
    count += 1
    if count == 15:
        break
x2 = x0
y2 = y0
E_B_V = x1 - x2

[w0_22, w1_22] = coefficient_reg_inv_analit(B_V_int, V_int)
xV = []
yV = []
xV.append(min(B_V_int))
yV.append(min(B_V_int) * w1_22 + w0_22)
xV.append(max(B_V_int))
yV.append(max(B_V_int) * w1_22 + w0_22)

x_igr_v = np.flip(x_)
y_igr_v = np.flip(M_)
x0_v = x1 - E_B_V
y0_v = x1 * w1_22 + w0_22
count = 0
v_v = []
for xi in x_igr_v:
    if (x0_v-0.02) <= xi <= (x0_v+0.02):
        v_v.append(y_igr_v[np.where(x_igr == xi)[0][0]])
m_M = y0_v - np.average(v_v)

print("E_B_V = ", E_B_V)
print("m_M = ", m_M)
lgR = (m_M - 3.1*E_B_V + 5) / 5
R = 10**lgR
print("R = ", R)

plt.plot(x_, L_, color='red', label = "ГП")
plt.scatter(B_V_int, U_B_int, color='yellow', label = "до сдвига")
plt.scatter(B_V_int-(x1-x2), U_B_int-(y1-y2), color='pink', label = "после сдвига")
plt.plot(x, y, color="orange", label = "средняя линия звезд \n до сдвига")
plt.plot([x1, x2], [y1, y2], color="black", label = "линия смещения")
plt.gca().invert_yaxis()
plt.grid()
plt.legend()
plt.xlabel("B_V")
plt.ylabel("U_B")

plt.show()

plt.plot(x_, M_, color='red', label = "ГП")
plt.scatter(B_V_int, V_int, color='yellow', label = "до сдвига")
plt.scatter(B_V_int - E_B_V, V_int, color='pink', label = "после сдвига")
plt.plot(xV, yV, color="orange", label = "средняя линия звезд \n до сдвига")
plt.plot([x1, x0_v], [y0_v, y0_v], color="black", label = "линия смещения")
plt.plot([x0_v, x0_v], [y0_v, np.average(v_v)], color="black", label = "линия смещения")
plt.gca().invert_yaxis() 
plt.grid() 
plt.legend()
plt.xlabel("B_V")
plt.ylabel("M_v, m_v")

plt.show()
