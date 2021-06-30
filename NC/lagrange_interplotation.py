from functools import reduce
import operator

from utils import r


def lagrange(x_data, y_data, x, n=1):
    out_str = f"$$ f_{{{n}}}(x) = "
    
    if n is None:
        n = min(len(x_data), 4)
    
    i = [i for i, e in enumerate(x_data[:-1]) if x_data[i] < x and x < x_data[i+1]][0]
    nearest = list(sum(zip(range(i, -1, -1), range(i+1, len(x_data))), ()))[:n+1]
    nearest_x = list(map(lambda i: x_data[i], nearest))
    nearest_y = list(map(lambda i: y_data[i], nearest))
    print(nearest_x, nearest_y)
    
    terms = []
    
    for j in range(0, n+1):
        s = "\\frac{"
        s += ''.join([f'(x - x_{i})' for i in range(0, n+1) if i != j])
        s += "}{"
        s += ''.join([f'(x_{j} - x_{i})' for i in range(0, n+1) if i != j])
        s += f"}}f(x_{j})"
        terms.append(s)

    out_str += " + ".join(terms)
    out_str += f" $$\n\n$$ f_{{{n}}}({x}) = "
    
    terms = []
    terms2 = []
    val = 0
    for j in range(0, n+1):
        s = "\\frac{"
        s += ''.join([f'({r(x)} - {r(nearest_x[i])})' for i in range(0, n+1) if i != j])
        s += "}{"
        s += ''.join([f'({r(nearest_x[j])} - {r(nearest_x[i])})' for i in range(0, n+1) if i != j])
        s += f"}} ({r(nearest_y[j])})"
        terms.append(s)
        
        u = reduce(operator.mul, [x - nearest_x[i] for i in range(0, n+1) if i != j], 1)
        b = reduce(operator.mul, [nearest_x[j] - nearest_x[i] for i in range(0, n+1) if i != j], 1.0)
        
        terms2.append(f'\\frac{{{r(u)}}}{{{r(b)}}}({r(nearest_y[j])})')
        
        val += u/b * nearest_y[j]

    out_str += " + ".join(terms)
    out_str += " $$\n\n"
    out_str += f"$$ f_{{{n}}}({x}) = {' + '.join(terms2)} $$\n\n"
    out_str += f"$$ f_{{{n}}}({x}) = {r(val)} $$"
    return out_str
    

if __name__ == '__main__':
    print(lagrange([0, 1, 2, 4], [1, 1, 5, 6], 1.5, n=3))
