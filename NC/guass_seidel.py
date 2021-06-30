from sympy import latex, factor, lambdify
from utils import r


def gauss_seidel_method(x_exp, y_exp, z_exp=None, x_val=0, y_val=0, z_val=0, iter=1):
    out_str = ""
    x, y, z = symbols('x y z')

    new_values = [x_val, y_val, z_val]

    out_str += f"\\textbf{{Iteration {iter}}}\n\n"
    out_str += f"Substitute $y={r(new_values[1])}$, $z={r(new_values[2])}$\n"
    out_str += f"$$ x = {latex(factor(x_exp))} ="
    new_values[0] = float(lambdify((x, y, z), x_exp)(*new_values))
    out_str += f"{r(new_values[0])} $$\n\n"

    out_str += f"Substitute $x={r(new_values[0])}$, $z={r(new_values[2])}$\n"
    out_str += f"$$ y = {latex(factor(y_exp))} ="
    new_values[1] = float(lambdify((x, y, z), y_exp)(*new_values))
    out_str += f"{r(new_values[1])} $$\n\n"

    if z_exp:
        out_str += f"Substitute $x={r(new_values[0])}$, $y={r(new_values[1])}$\n"
        out_str += f"$$ z = {latex(factor(z_exp))} ="
        new_values[2] = float(lambdify((x, y, z), z_exp)(*new_values))
        out_str += f"{r(new_values[2])} $$\n\n"

    out_str += f"After Iteration {iter}\n"
    out_str += f"$$ (x, y, z) = ({', '.join([r(v) for v in new_values])})$$\n\n"

    if iter != 1:
        out_str += f"\\textbf{{Approximate Error}}\n\n"
        out_str += f"$$ \\epsilon_a(x) = \\frac{{\\left|\\text{{latest value of x}} - \\text{{previous value of x}}\\right|}}{{\\left|\\text{{latest value of x}}\\right|}} \\times 100 $$\n"
        out_str += f"$$ \\epsilon_a(x) = \\frac{{\\left|{r(new_values[0])} - ({r(x_val)})\\right|}}{{\\left|{r(new_values[0])}\\right|}} \\times 100 $$\n"

        e_x = abs(new_values[0] - x_val) / abs(new_values[0]) * 100
        out_str += f"$$ \\epsilon_a(x) = {r(e_x, 2)} \% $$\n"

        out_str += f"$$ \\epsilon_a(y) = \\frac{{\\left|\\text{{latest value of y}} - \\text{{previous value of y}}\\right|}}{{\\left|\\text{{latest value of y}}\\right|}} \\times 100 $$\n"
        out_str += f"$$ \\epsilon_a(y) = \\frac{{\\left|{r(new_values[1])} - ({r(y_val)})\\right|}}{{\\left|{r(new_values[1])}\\right|}} \\times 100 $$\n"

        e_y = abs(new_values[1] - y_val) / abs(new_values[1]) * 100
        out_str += f"$$ \\epsilon_a(y) = {r(e_y, 2)} \% $$\n\n"

        if z_exp:
            out_str += f"$$ \\epsilon_a(z) = \\frac{{\\left|\\text{{latest value of z}} - \\text{{previous value of z}}\\right|}}{{\\left|\\text{{latest value of z}}\\right|}} \\times 100 $$\n"
            out_str += f"$$ \\epsilon_a(z) = \\frac{{\\left|{r(new_values[2])} - ({r(z_val)})\\right|}}{{\\left|{r(new_values[2])}\\right|}} \\times 100 $$\n"

            e_z = abs(new_values[2] - z_val) / abs(new_values[2]) * 100
            out_str += f"$$ \\epsilon_a(z) = {r(e_z, 2)} \% $$\n\n"

    if iter < 5:
        x_val, y_val, z_val = new_values
        out_str += gauss_seidel_method(x_exp, y_exp, z_exp, x_val, y_val, z_val, iter+1)

    return out_str


if __name__ == '__main__':
    from sympy import solve, Eq, symbols
    x, y = symbols('x y')

    print(gauss_seidel_method(
        solve(Eq(3*x+2*y, 4), y)[0],
        solve(Eq(x - 2*y, 5), x)[0],
        # solve(Eq(-3*x -y + 7*z, -34), z)[0],
    ))
