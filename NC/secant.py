# from sympy import
from utils import r


def secant_method(fn, x1, x0, iter=1):
    out_str = ''

    if iter == 1:
        out_str += f"Secant method is given as:\n"
        out_str += f"$$ x_{{i+1}} = x_i - \\left[\\frac{{f(x_i)(x_{{i-1}} - x_{{i}})}}{{f(x_{{i-1}}) - f(x_{{i}})}}\\right] $$\n"

    out_str += f"\\textbf{{Iteration {iter}}}\n\n"
    out_str += f"$$ x_{iter} = x_{iter - 1} - \\left[\\frac{{f(x_{iter - 1})(x_{{{iter - 2}}}-x_{iter - 1})}}{{f(x_{{{iter - 2}}}) - f(x_{{{iter - 1}}})}}\\right] $$\n"

    out_str += f"$$ f(x_{{{iter - 2}}}) = f({r(x0)}) = {r(fn(x0))} $$\n"
    out_str += f"$$ f(x_{{{iter - 1}}}) = f({r(x1)}) = {r(fn(x1))} $$\n"

    out_str += f"$$ x_{iter} = {r(x0)} - \\left[\\frac{{{r(fn(x1))}({r(x0)}-({r(x1)}))}}{{{r(fn(x0))} - ({r(fn(x1))}))}}\\right] $$\n"
    x_val = fn(x0) * (x0 - x1) / (fn(x0) - fn(x1))
    out_str += f"$$ x_{iter} = {r(x0)} - ({r(x_val)}) $$\n"
    x_val = x0 - x_val
    out_str += f"$$ x_{iter} = {r(x_val)} $$\n"

    error = None
    if iter > 1:
        out_str += "\n\\textbf{Error}\n\n"
        out_str += f"$$ \\text{{Error}} = \\frac{{\\left|\\text{{latest value}} - \\text{{previous value}}\\right|}}{{\\left|\\text{{latest value}}\\right|}} \\times 100 $$\n"
        out_str += f"$$ \\text{{Error}} = \\frac{{\\left|{r(x_val)} - ({r(x1)})\\right|}}{{\\left|{r(x_val)}\\right|}} \\times 100 $$\n"
        error = abs(x_val - x1)/abs(x_val) * 100
        out_str += f"$$ \\text{{Error}} = {r(error, 2)} \\% $$\n"

    if error is not None and error < 0.0001 or iter > 3:
        return out_str

    out_str += secant_method(fn, x_val, x1, iter+1)
    return out_str


if __name__ == '__main__':
    from sympy import lambdify, sin, cos, symbols

    x = symbols('x')
    print(secant_method(lambdify(x, sin(x) + cos(1-x**2) - 1), 3, 1))
