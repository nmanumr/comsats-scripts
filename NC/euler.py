from utils import r
from sympy import lambdify

def euler(f, h, y0, x0=0, iterations=5, i=1):
    out_str = f"\\textbf{{Iteration {i}}}\n"
    x, y = symbols('x y')
    
    fn = lambdify((x, y), f)
    y1 = y0 + fn(x0, y0) * h
    
    out_str += f'$$ y_{i} = y_{i-1} + f(x_{i-1}, y_{i-1})h $$\n'
    out_str += f'$$ y_{i} = {r(y0)} + f({r(x0)}, {r(y0)})\\times({r(h)}) $$\n'
    out_str += f'$$ y_{i} = {r(y0)} + ({r(fn(x0, y0))})\\times({r(h)}) $$\n'
    out_str += f'$$ y_{i} = {r(y1)} $$\n'
    
    out_str += f'\n$$ (x_{i}, y_{i}) = ({r(h+x0)}, {r(y1)}) $$\n'
    
    if iterations > 1:
        out_str += euler(f, h, y1, h+x0, iterations-1, i+1)
        
    return out_str


if __name__ == '__main__':
    from sympy import sqrt, symbols

    x, y = symbols('x y')

    print(euler((1+4*x)*sqrt(y), 0.5, 1))

