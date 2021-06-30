from utils import r
from sympy import lambdify, simplify


def false_position(fn, xl, xu, last_xm=None, last_err=None, iter=1):
    out_str = f"\\textbf{{Iteration {iter}}}\n\n"
    out_str += "\n\\vspace{20pt}\\textbf{Step 1}\n"

    out_str += f"$$ x_{{l}} = {r(xl)}, x_{{u}} = {r(xu)} $$\n"
    out_str += f"$$ f(x_{{l}}) = f({r(xl)}) = {r(fn(xl))} $$\n"
    out_str += f"$$ f(x_{{u}}) = f({r(xu)}) = {r(fn(xu))} $$\n"

    if iter == 1:
        x = fn(xl) * fn(xu)
        out_str += f"$$ f(x_{{u}}) \\times f(x_{{l}}) = {r(fn(xl))} \\times {r(fn(xu))} $$\n"
        if x < 0:
            out_str += f"\nAs, $ f(x_{{u}}) \\times f(x_{{l}}) < 0 $ so $[{r(xl)}, {r(xu)}]$ bracket the roots.\n"

    out_str += "\n\\vspace{20pt}\n\\textbf{Step 2}\n"

    out_str += f"$$ x_{{m}} = x_{{u}} - \\left[\\frac{{f(x_{{u}}) \\times (x_{{l}} - x_{{u}}) }}{{f(x_{{l}}) - f(x_{{u}})}}\\right] $$\n"
    out_str += f"$$ x_{{m}} = {r(xu)} - \\left[\\frac{{{r(fn(xu))} \\times ({r(xl)} - {r(xu)}) }}{{{r(fn(xl))} - {r(fn(xu))}}}\\right] $$\n"
    xm = (fn(xu)*(xl-xu)/(fn(xl)-fn(xu)))
    out_str += f"$$ x_{{m}} = {r(xu)} - {r(xm)} $$\n"
    xm = xu - xm
    out_str += f"$$ x_{{m}} = {r(xm)} $$\n"

    error = None
    if last_xm:
        out_str += "\n\\vspace{20pt}\n\\textbf{Error}\n"

        error = abs((xm - last_xm) / xm) * 100

        out_str += f"$$ \\text{{Error}} = \\frac{{\\left|\\text{{latest value}} - \\text{{previous value}}\\right|}}{{\\left|\\text{{latest value}}\\right|}} \\times 100 $$\n"
        out_str += f"$$ \\text{{Error}} = \\frac{{\\left| {r(xm)} - {r(last_xm)} \\right|}}{{\\left| {r(xm)} \\right|}} \\times 100 $$\n"
        out_str += f"$$ \\text{{Error}} = {r(error)} \\% $$\n"

        if last_err is not None and last_err < error:
            return out_str

        if iter >= 4:
            return out_str

    out_str += "\n\\vspace{20pt}\n\\textbf{Step 3}\n\n"

    out_str += "Now, either $[x_{l}, x_{m}]$ or $[x_{m}, x_{u}]$ will bracket the roots.\n"
    x = fn(xl) * fn(xm)

    out_str += f"$$ f(x_{{l}}) \\times f(x_{{m}}) = {r(fn(xl))} \\times {r(fn(xm))} {'<' if x < 0 else '>'} 0 $$\n"

    if x < 0:
        out_str += f"\nSo, $[x_{{l}}, x_{{m}}] = [{r(xl)}, {r(xm)}]$ bracket the roots\n\n"
        xu = xm
    else:
        out_str += f"\nSo, $[x_{{m}}, x_{{u}}] = [{r(xm)}, {r(xu)}]$ bracket the roots\n\n"
        xl = xm

    out_str += false_position(fn, xl, xu, last_xm=xm,
                              last_err=error, iter=iter+1)
    return out_str


if __name__ == '__main__':
    from sympy import symbols
    x = symbols('x')
    print(false_position(lambdify(
        x, simplify(
            1 - ( 20**2 / (9.8 * (3 * x - x**2 / 2)**3)) * (3 + x))
        ), .5, 2.5
    ))
