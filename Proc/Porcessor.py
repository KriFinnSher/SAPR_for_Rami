from collections import defaultdict
import numpy as np


def find_u(x, delta_0, delta_l, l, q, e, a):

    return round(delta_0 + (x / l) * (delta_l - delta_0) + (q * l**2) / (2 * e * a) * (x / l) * (1 - x / l), 4)


def find_n(x, delta_0, delta_l, l, q, e, a):

    return round((e * a / l) * (delta_l - delta_0) + (q * l / 2) * (1 - 2 * x / l), 4)


def find_sigma(n, a):

    return round(n / a, 4)


def find_b(pl, ql, lens, state):

    size = len(lens) + 2

    pl_part = [0] * size
    ql_part = [0] * size

    for p in pl:
        pl_part[p] = pl[p]

    for rod_num in ql:
        ql_part[rod_num] += ql[rod_num] * lens[rod_num] / 2
        ql_part[rod_num + 1] += ql[rod_num] * lens[rod_num] / 2

    b = [pl_part[i] + ql_part[i] for i in range(size)][1:]

    if state == 1 or state == 3:
        b[0] = 0
    if state == 2 or state == 3:
        b[-1] = 0

    return b


def find_A(k_mats, state):

    size = len(k_mats) + 1
    mat_A = [[0] * size for _ in range(size)]

    for l in range(size - 1):
        for i in range(2):
            for j in range(2):
                mat_A[i + l][j + l] += k_mats[l][i][j]

    if state == 1 or state == 3:
        mat_A[0][0] = 1
        for i in range(1, size):
            mat_A[0][i] = 0
            mat_A[i][0] = 0

    if state == 2 or state == 3:
        mat_A[-1][-1] = 1
        for i in range(0, size-1):
            mat_A[-1][i] = 0
            mat_A[i][-1] = 0

    return mat_A


def prepare_deltas(mat_A, mat_b):

    mat_A = np.array(mat_A)
    mat_b = np.array(mat_b)

    delta = np.linalg.solve(mat_A, mat_b)
    delta_rounded = np.round(delta, 4).tolist()

    return delta_rounded


def prepare_k_mats(input_data):

    k_mats = []

    f1 = input_data['f1']
    f2 = input_data['f2']
    A = input_data['A']
    L = input_data['L']
    E = input_data['E']
    sigma = input_data['sigma']
    q = input_data['q']

    lens = defaultdict(float)
    e_s = defaultdict(float)
    a_s = defaultdict(float)

    for i, bar in enumerate(zip(f1, f2, A, L, E, sigma, q)):
        lens[i+1] = float(bar[3])
        e_s[i+1] = float(bar[4])
        a_s[i+1] = float(bar[2])

    for k in range(1, len(input_data['f1']) + 1):
        small_k = [[e_s[k] * a_s[k] / lens[k], -e_s[k] * a_s[k] / lens[k]], [-e_s[k] * a_s[k] / lens[k], e_s[k] * a_s[k] / lens[k]]]
        k_mats.append(small_k)

    return k_mats


def find_deltas(input_data):
    f1 = input_data['f1']
    f2 = input_data['f2']
    A = input_data['A']
    L = input_data['L']
    E = input_data['E']
    sigma = input_data['sigma']
    q = input_data['q']

    lens = defaultdict(float)

    for i, bar in enumerate(zip(f1, f2, A, L, E, sigma, q)):
        lens[i+1] = float(bar[3])

    qs = {i+1: float(bar[-1]) for i, bar in enumerate(zip(f1, f2, A, L, E, sigma, q))}
    ps = defaultdict(float)
    for i in range(len(f1)):
        ps[i+1] += float(f1[i])
    for i in range(1, len(f2)):
        ps[i+1] += float(f2[i-1])

    b_mat = find_b(ps, qs, lens, input_data['op'])
    A_mat = find_A(prepare_k_mats(input_data), input_data['op'])

    return prepare_deltas(A_mat, b_mat)


def find_coordinates(input_data):
    line_1 = []
    line_2 = []
    line_3 = []

    temp_len = 0

    for i, rod_len in enumerate(input_data['L']):
        rod_len = float(rod_len)

        line_1.append(temp_len)
        line_1.append(rod_len + temp_len)

        line_2.append(find_section(input_data, i+1, 0)[1])
        line_2.append(find_section(input_data, i+1, rod_len)[1])

        line_3.append(find_section(input_data, i+1, 0)[2])
        line_3.append(find_section(input_data, i+1, rod_len)[2])

        temp_len += rod_len

    return line_1, line_2, line_3


def find_section(input_data, rod_num, section_x):

    delta_0 = find_deltas(input_data)[rod_num - 1]
    delta_l = find_deltas(input_data)[rod_num]

    rod_len = float(input_data['L'][rod_num-1])
    rod_e = float(input_data['E'][rod_num-1])
    rod_a = float(input_data['A'][rod_num-1])
    rod_q = float(input_data['q'][rod_num-1])

    section_u = round(find_u(section_x, delta_0, delta_l, rod_len, rod_q, rod_e, rod_a), 4)
    section_n = round(find_n(section_x, delta_0, delta_l, rod_len, rod_q, rod_e, rod_a), 4)
    section_sigma = round(find_sigma(section_n, rod_a), 4)

    return section_u, section_n, section_sigma