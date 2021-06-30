from utils import r


def bisection_print(fn, xl, xu, last_xm=None, last_err=None, iter=1):
    out_str = f"\\textbf{{Iteration {iter}}}\n\n"
    out_str += "\n\\vspace{20pt}\\textbf{Step 1}\n"

    out_str += f"$$ x_{{l}} = {r(xl)}, x_{{u}} = {r(xu)} $$\n"
    out_str += f"$$ f(x_{{l}}) = {r(fn(xl))} $$\n"
    out_str += f"$$ f(x_{{u}}) = {r(fn(xu))} $$\n"

    if iter == 1:
        x = fn(xl) * fn(xu)
        out_str += f"$$ f(x_{{u}}) \\times f(x_{{l}}) = {r(fn(xl))} \\times {r(fn(xu))} = {r(x)} $$\n"
        if x < 0:
            out_str += f"\nAs, $ f(x_{{u}}) \\times f(x_{{l}}) < 0 $ so $[{r(xl)}, {r(xu)}]$ bracket the roots.\n"

    out_str += "\n\\vspace{20pt}\n\\textbf{Step 2}\n"

    xm = (xl + xu) /2
    out_str += f"$$ x_{{m}} = \\frac{{x_{{l}} + x_{{u}}}}{{2}} = \\frac{{{r(xl)} + {r(xu)}}}{{2}} = {r(xm)} $$\n"

    error = None
    if last_xm:
        out_str += "\n\\vspace{20pt}\n\\textbf{Error}\n"

        error = abs((xm - last_xm) / xm) * 100

        out_str += f"$$ \\text{{Error}} = \\frac{{{r(xm)} - {r(last_xm)} }}{{ {r(xm)} }} \\times 100 $$\n"
        out_str += f"$$ \\text{{Error}} = {r(error)} \\% $$\n"
        
        if error > .5:
            return out_str

    out_str += "\n\\vspace{20pt}\n\\textbf{Step 3}\n\n"
    
    out_str += "Now, either $[x_{l}, x_{m}]$ or $[x_{m}, x_{u}]$ will bracket the roots.\n"
    x = fn(xl) * fn(xm)
    if x < 0:
        out_str += f"$$ f(x_{{l}}) \\times f(x_{{m}}) = {r(fn(xl))} \\times {r(fn(xm))} < 0 $$\n"
        out_str += f"\nSo, $[x_{{l}}, x_{{m}}] = [{r(xl)}, {r(xm)}]$ bracket the roots\n\n"
        xu = xm
    else:
        out_str += f"$$ f(x_{{m}}) \\times f(x_{{u}}) = {r(fn(xm))} \\times {r(fn(xu))} < 0 $$\n"
        out_str += f"\nSo, $[x_{{m}}, x_{{u}}] = [{r(xm)}, {r(xu)}]$ bracket the roots\n\n"
        xl = xm

    out_str += bisection_print(fn, xl, xu, last_xm=xm, last_err=error, iter=iter+1)
    return out_str


if __name__ == '__main__':
    print(bisection_print(lambda x: x**2 - 18, 4, 5))
