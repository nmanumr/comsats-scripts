from utils import r
from sympy import lambdify, latex


def rk4(f, h, x0, y0, iterations=2, i=1):
    out_str = f"\\textbf{{Iteration {i}}}\n"
    out_str += f'($x_{i-1}$, $y_{i-1}$) = ({r(x0)}, {r(y0)})\n\n'
    
    out_str += f'$$ y_{i} = y_{i-1} + \\frac{{1}}{{6}}\\left[k_1+2k_2+2k_3+k_4\\right]h $$\n'
    out_str += 'Where,\n'
    out_str += f'$$ k_1 = f(x_{i-1}, y_{i-1}) $$\n'
    out_str += f'$$ k_2 = f(x_{i-1}+\\frac{{1}}{{2}}h, y_{i-1}+\\frac{{1}}{{2}}k_1h) $$\n'
    out_str += f'$$ k_3 = f(x_{i-1}+\\frac{{1}}{{2}}h, y_{i-1}+\\frac{{1}}{{2}}k_2h) $$\n'
    out_str += f'$$ k_4 = f(x_{i-1}+h, y_{i-1}+k_3h) $$\n\n'
    
    x, y = symbols('x y')
    fn = lambdify((x, y), f)
    k1 = fn(x0, y0)
    k2 = fn(x0+1/2*h, y0+1/2*k1*h)
    k3 = fn(x0+1/2*h, y0+1/2*k2*h)
    k4 = fn(x0+h, y0+k3*h)
    y2 = y0 + 1/6*(k1+2*k2+2*k3+k4)*h
    
    out_str += f'$$ k_1 = f({r(x0)}, {r(y0)}) = {latex(f)} = {r(k1)} $$\n'
    out_str += f'$$ k_2 = f\\left({r(x0)}+\\frac{{1}}{{2}}({h}), {r(y0)}+\\frac{{1}}{{2}}({r(k1)})({h})\\right) = {latex(f)} = {r(k2)} $$\n'
    out_str += f'$$ k_3 = f\\left({r(x0)}+\\frac{{1}}{{2}}({h}), {r(y0)}+\\frac{{1}}{{2}}({r(k2)})({h})\\right) = {latex(f)} = {r(k3)} $$\n'
    out_str += f'$$ k_4 = f\\left({r(x0)}+({h}), {r(y0)}+({r(k3)})({h})\\right) = {latex(f)} = {r(k4)} $$\n'
    
    out_str += f'\n Substituting values\n'
    out_str += f'$$ y_{i} = {r(y0)} + \\frac{{1}}{{6}}\\left[{r(k1)}+2({r(k2)})+2({r(k3)})+{r(k4)}\\right]({r(h)}) = {r(y2)} $$\n'
    
    out_str += f'\n$$ (x_{i}, y_{i}) = ({r(h+x0)}, {r(y2)}) $$\n'
    
    if iterations > 1:
        out_str += rk4(f, h, h+x0, y2, iterations-1, i+1)
        
    return out_str


if __name__ == '__main__':
    from sympy import symbols

    x, y = symbols('x y')
    print(rk4((x+0-y)/2, 0.2, 0, 1, 2))
