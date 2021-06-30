from utils import r


def newton_interpolation(x_data, y_data, x, n=None):
    outstr = ''
    if n is None:
        n = min(len(x_data), 4)
    
    i = [i for i, e in enumerate(x_data[:-1]) if x_data[i] < x and x < x_data[i+1]][0]
    nearest = list(sum(zip(range(i, -1, -1), range(i+1, len(x_data))), ()))[:n+1]
    nearest_x = list(map(lambda i: x_data[i], nearest))
    nearest_y = list(map(lambda i: y_data[i], nearest))
        
    outstr += f'\\begin{{tabular}}{{ c c {("c "*n)}}}\n$x_i$ & $f(x_i)$ & '
    outstr += ' fold & '.join([str(i) for i in range(1, n+1)]) 
    outstr +=' fold\\\\\n\\hline\n'
    
    table = [[] for i in range(n+2)]
    table_val = [[0 for j in range(n-i+2)] for i in range(n+2)]
    table[0] = nearest_x
    table[1] = nearest_y
    table_val[0] = nearest_x
    table_val[1] = nearest_y
    
    for i in range(n+1):
        outstr += f'$x_{i}$ & $f(x_{i})$'
        if i < n:
            outstr += f' & $f[x_{i+1}, x_{i}]$'
            table[2].append((i+1, i))
        elif n >= 1:
            outstr += ' & '
        if i < n-1:
            outstr += f' & $f[x_{i+2}, x_{i+1}, x_{i}]$'
            table[3].append((i+2, i+1, i))
        elif n >= 2:
            outstr += ' & '
        if i < n-2:
            outstr += f' & $f[x_{i+3}, x_{i+2}, x_{i+1}, x_{i}]$'
            table[4].append((i+3, i+2, i+1, i))
        elif n >= 3:
            outstr += ' & '
        outstr += '\\\\\n'
        
    outstr += '\\end{tabular}\n\n'
    
    for i in range(len(nearest)):
        outstr += f'$$ x_{i}={nearest_x[i]}, f(x_{i})={nearest_y[i]} $$\n'
    
    for i, fold in enumerate(table[2:]):
        outstr += f'\\textbf{{Fold {i+1}}}\n'
        for j, e in enumerate(fold):
            outstr += f'$$ f(x_{", x_".join([str(x) for x in e])}) ='
            if type(table[i+1][j]) is tuple:
                outstr += f'\\frac{{f[x_{", x_".join([str(x) for x in table[i+1][j+1]])}] - f[x_{", x_".join([str(x) for x in table[i+1][j]])}]}}{{x_{e[0]} - x_{e[-1]}}}'
            else:
                outstr += f'\\frac{{f(x_{e[0]}) - f(x_{e[-1]})}}{{x_{e[0]} - x_{e[-1]}}}'
            outstr += f' = \\frac{{{r(table_val[i+1][j+1])} - {r(table_val[i+1][j])}}}{{{r(table_val[0][e[0]])} - {r(table_val[0][e[-1]])}}} = '
            
            table_val[i+2][j] = (table_val[i+1][j+1] - table_val[i+1][j])/(table_val[0][e[0]] - table_val[0][e[-1]])
            outstr += r(table_val[i+2][j])
            outstr += ' $$\n'
    
    outstr += f'\n\\begin{{tabular}}{{ c c {("c "*n)}}}\n$x_i$ & $f(x_i)$ & '
    outstr += ' fold & '.join([str(i) for i in range(1, n+1)]) 
    outstr +=' fold\\\\\n\\hline\n'
    for i in range(n+1):
        outstr += ' & '.join([f'${r(table_val[j][i])}$' for j in range(n+2-i)])
        outstr += ' & '.join(['' for j in range(i)])
        outstr += '\\\\\n'
    outstr += '\\end{tabular}\n\n'
    outstr += '\\textbf{Interpolating Polynomial}\n'
    
    str1 = f'$$ f_{n}(x) = f(x_0)'
    str2 = f'$$ f_{n}(x) = {r(table_val[1][0])}'
    ans = table_val[1][0]
    
    for i in range(1, n+1):
        temp = table_val[i+1][0]
        str1 += f' + f[x_{", x_".join([str(j) for j in range(i, -1, -1)])}]'
        str2 += f' + ({r(table_val[i+1][0])})'
        for j in range(i-1, -1, -1):
            str1 += f'(x-x_{j})'
            str2 += f'(x-{r(table_val[0][j])})'
            temp *= (x-table_val[0][j])
        ans += temp
    
    outstr += f'{str1} $$\n{str2} $$\n'
    outstr += f'$$ f_{n}({x}) = {r(ans)} $$\n'
    
    return outstr
    

if __name__ == '__main__':
    # print(newton_interpolation([15, 18, 22, 26], [24, 37, 25, 0], 18, n=2))
    print(newton_interpolation([.5, 1.5, 2.5, 3, 4], [-.45, .6, .7, 1.88, 6], 2.3, n=3))
