import re

from sympy import Matrix, latex


def to_mat_str(mat):
    x = f"\\begin{{bmatrix}}"
    x += '\\\\\n'.join([' & '.join([str(n) for n in row]) for row in mat])
    x += f"\\end{{bmatrix}}"
    return x


def merge_lines(l1, l2, l3):
    out_str = '\\begin{flalign}\n\t\\nonumber'
    out_str += ' & '.join(l1)
    out_str += '&&\\\\\n\t\\nonumber'
    out_str += ' & '.join(l2)
    out_str += '&&\\\\\n\t\\nonumber'
    out_str += ' & '.join(l3)
    out_str += '\n\\end{flalign}\n\n'
    return out_str


def lu_decompose(mat):
    l_mat = [
        [
            f'l_{{{j + 1}{i + 1}}}' if i < j else (1 if i == j else 0)
            for i in range(len(mat[j]))
        ]
        for j in range(len(mat))
    ]
    u_mat = [
        [
            f'u_{{{j + 1}{i + 1}}}' if i >= j else 0
            for i in range(len(mat[j]))
        ]
        for j in range(len(mat))
    ]
    lu_mat = [
        [
            '+'.join([a if b == 1 else (b if a == 1 else f"{a}{b}") for a, b in zip(X_row, Y_col) if a != 0 and b != 0])
            for Y_col in zip(*u_mat)
        ]
        for X_row in l_mat
    ]

    l, u, _ = Matrix(mat).LUdecomposition()

    out_str = f"$$ \\begin{{bmatrix}}"
    out_str += '\\\\\n'.join(
        [' & '.join([f'l_{{{j + 1}{i + 1}}}' if i < j else ('1' if i == j else '0') for i in range(len(mat[j]))]) for j
         in range(len(mat))])
    out_str += f"\\end{{bmatrix}} \\begin{{bmatrix}}"
    out_str += '\\\\\n'.join(
        [' & '.join([f'u_{{{j + 1}{i + 1}}}' if i >= j else '0' for i in range(len(mat[j]))]) for j in range(len(mat))])
    out_str += f"\\end{{bmatrix}} = {to_mat_str(mat)} $$\n\n"

    out_str += f"$$ {to_mat_str(lu_mat)} = {to_mat_str(mat)} $$\n\n"

    l1, l2, l3 = [], [], []
    j = 0

    def replacer(i, n):
        def r(m):
            if int(m.group(2)) - 1 == i and int(m.group(3)) - 1 == n:
                return m.group(0)
            if m.group(1) == 'l':
                return '(' + str(l.row(int(m.group(2))-1)[int(m.group(3)) - 1]) + ')'
            if m.group(1) == 'u':
                return '(' + str(u.row(int(m.group(2))-1)[int(m.group(3)) - 1]) + ')'
            return m.group(0)

        return r

    for n in range(len(mat)):
        for i in range(n, len(mat[n])):
            if j % 3 == 0 and j > 0:
                out_str += merge_lines(l1, l2, l3)
                j = 0
                l1, l2, l3 = [], [], []

            l1.append(f'& {lu_mat[n][i]} = {mat[n][i]}')
            x = re.sub(r'(l|u)_\{(\d)(\d)\}', replacer(n, i), lu_mat[n][i])
            l2.append(f"\\implies & {x} = {mat[n][i]}" if len(lu_mat[n][i]) != 6 else '&')
            l3.append(f'\\implies & u_{{{n + 1}{i + 1}}} = {u.row(n)[i]}' if len(lu_mat[n][i]) != 6 else '&')
            j += 1

        for i in range(n + 1, len(mat)):
            if j % 3 == 0 and j > 0:
                out_str += merge_lines(l1, l2, l3)
                j = 0
                l1, l2, l3 = [], [], []

            l1.append(f'& {lu_mat[i][n]} = {mat[i][n]}')
            x = re.sub(r'(u|l)_\{(\d)(\d)\}', replacer(i, n), lu_mat[i][n])
            l2.append(f"\\implies & {x} = {mat[i][n]}" if len(lu_mat[i][n]) != 6 else '&')
            l3.append(f'\\implies & l_{{{i + 1}{n + 1}}} = {l.row(i)[n]}' if len(lu_mat[i][n]) != 6 else '&')
            j += 1

    out_str += merge_lines(l1, l2, l3)
    out_str += f"$$ L = {latex(l)}, U = {latex(u)} $$"

    return out_str


if __name__ == '__main__':
    print(lu_decompose([
        [8, 4, -1],
        [-2, 5, 1],
        [2, -1, 6]
    ]))

    # print(lu_decompose([
    #     [25, 5, 4],
    #     [10, 8, 16],
    #     [8, 12, 22]
    # ]))
