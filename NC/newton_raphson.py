from sympy import lambdify, diff, latex, symbols
from utils import r

def newton_raphson(fn, xi, iter=1):
    x = symbols('x')
    
    out_str = ""
    dev_fn = lambdify(x, diff(fn))
    f = lambdify(x, fn)

    if iter == 1:
        out_str += f"Newton-Raphson method is given as:\n"
        out_str += f"$$ x_{{i+1}} = x_i - \\frac{{f(x_i)}}{{f'(x_i)}} $$\n"
        out_str += f"Here $$ f(x) = {latex(fn)} $$\n $$ f'(x)= {latex(diff(fn))} $$\n"
    
    out_str += f"\\textbf{{Iteration {iter}}}\n\n"
    out_str += f"$$ x_{iter} = x_{iter - 1} - \\frac{{f(x_{iter - 1})}}{{f'(x_{iter - 1})}} $$\n"
    out_str += f"$$ f(x_{iter-1}) = f({r(xi)}) = {r(f(xi))} $$\n"
    out_str += f"$$ f'(x_{iter-1}) = f'({r(xi)}) = {r(dev_fn(xi))} $$\n"
    out_str += f"$$ x_{iter} = {r(xi)} - \\left[\\frac{{{r(f(xi))}}}{{{r(dev_fn(xi))}}}\\right] $$\n"
    x_val = xi - (f(xi) / dev_fn(xi))
    out_str += f"$$ x_{iter} = {r(x_val)} $$\n"

    error = None
    if iter > 1:
        out_str += "\n\\textbf{Error}\n\n"
        out_str += f"$$ \\text{{Error}} = \\frac{{\\left|\\text{{latest value}} - \\text{{previous value}}\\right|}}{{\\left|\\text{{latest value}}\\right|}} \\times 100 $$\n"
        out_str += f"$$ \\text{{Error}} = \\frac{{\\left|{r(x_val)} - {r(xi)}\\right|}}{{\\left|{r(x_val)}\\right|}} \\times 100 $$\n"
        error = abs(x_val - xi)/abs(x_val) * 100
        out_str += f"$$ \\text{{Error}} = {r(error, 2)} \\% $$\n"


    if error is not None and error < 0.0001:
        return out_str

    out_str += newton_raphson(fn, x_val, iter+1)
    return out_str


if __name__ == '__main__':
    from sympy import exp
    x = symbols('x')

    print(newton_raphson(exp(-1 * x) - x, 0))
    # print(newton_raphson(28.16*x**2 - 3.14*x**3 - 90, 0))
