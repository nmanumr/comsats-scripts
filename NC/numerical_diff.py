from utils import r
from sympy import lambdify, symbols, sin, sqrt


formulas = {
    'forward': [
        # First Derivative
        [
            [
                'f\'(x_i)',
                '\\frac{f(x_{i+1})+f(x_i)}{h}+O(h)',
                [0, 1],
                lambda y, h: (y[1] + y[0])/h,
                '1st derivative forward divided differential with $O(h)$'
            ],
            [
                'f\'(x_i)',
                '\\frac{-f(x_{i+2})+4f(x_{i+1})-3f(x_i)}{2h}+O(h^2)',
                [0, 1, 2],
                lambda y, h: (-1*y[2] + 4*y[1] - 3*y[0])/(2*h),
                '1st derivative forward divided differential with $O(h^2)$'
            ],
        ],
        # Second Derivative
        [
            [
                'f\'\'(x_i)',
                '\\frac{f(x_{i+2})-2f(x_{i+1})+f(x_i)}{h^2}+O(h)',
                [0, 1, 2],
                lambda y, h: (y[2]-2*y[1]+y[0])/h**2,
                '2nd derivative forward divided differential with $O(h)$'
            ],
            [
                'f\'\'(x_i)',
                '\\frac{-f(x_{i+3})+4f(x_{i+2})-5f(x_{i+1})+2f(x_i)}{h^2}+O(h^2)',
                [0, 1, 2, 3],
                lambda y, h: (-1*y[3]+4*y[2]-5*y[1]+2*y[0])/(h**2),
                '2nd derivative forward divided differential with $O(h^2)$'
            ],
        ],
    ],
    'backward': [
        # First Derivative
        [
            [
                'f\'(x_i)',
                '\\frac{f(x_{i})-f(x_{i-1})}{h}+O(h)',
                [-1, 0],
                lambda y, h: (y[0] - y[-1])/h,
                '1st derivative backward divided differential with $O(h)$'
            ],
            [
                'f\'(x_i)',
                '\\frac{3f(x_i)-4f(x_{i-1})+f(x_{i-2})}{2h}+O(h^2)',
                [-2, -1, 0],
                lambda y, h: (y[-2] - 4*y[-1] + 3*y[0])/(2*h),
                '1st derivative backward divided differential with $O(h^2)$'
            ],
        ],
        # Second Derivative
        [
            [
                'f\'\'(x_i)',
                '\\frac{f(x_i)-2f(x_{i-1})+f(x_{i-2})}{h^2}+O(h)',
                [-2, -1, 0],
                lambda y, h: (y[0]-2*y[-1]+y[-2])/h**2,
                '2nd derivative backward divided differential with $O(h)$'
            ],
            [
                'f\'\'(x_i)',
                '\\frac{2f(x_i)-5f(x_{i-1})+4f(x_{i-2})-f(x_{i-3})}{h^2}+O(h^2)',
                [-3, -2, -1, 0],
                lambda y, h: (-1*y[-3]+4*y[-2]-5*y[-1]+2*y[0])/(h**2),
                '2nd derivative backward divided differential with $O(h^2)$'
            ],
        ],
    ],
    'center': [
        # First Derivative
        [
            [
                'f\'(x_i)',
                '\\frac{f(x_{i+1})-f(x_{i-1})}{2h}+O(h^2)',
                [-1, 1],
                lambda y, h: (y[1] - y[-1])/h,
                '1st derivative centered divided differential with $O(h^2)$'
            ],
            [
                'f\'(x_i)',
                '\\frac{-f(x_{i+2})+8f(x_{i+1})-8f(x_{i-1}+f(x_{i-2}))}{12h}+O(h^4)',
                [-2, -1, 1, 2],
                lambda y, h: (-1*y[2] + 8*y[1] - 8*y[-1] + y[-2])/(12*h),
                '1st derivative centered divided differential with $O(h^4)$'
            ],
        ],
        # Second Derivative
        [
            [
                'f\'\'(x_i)',
                '\\frac{f(x_{i+1})-2f(x_{i})+f(x_{i-1})}{h^2}+O(h^2)',
                [-1, 0, 1],
                lambda y, h: (y[1] - 2*y[0] + y[-1])/h**2,
                '2nd derivative centered divided differential with $O(h^2)$'
            ],
            [
                'f\'\'(x_i)',
                '\\frac{-f(x_{i+2})+16f(x_{i+1})-30f(x_i)+16f(x_{i-1})-f(x_{i-2})}{12h^2}+O(h^4)',
                [-2, -1, 0, 1, 2],
                lambda y, h: (-1*y[2] + 16*y[1] - 30*y[0] + 16*y[-1] - y[-2])/(12*h**2),
                '2nd derivative centered divided differential with $O(h^4)$'
            ],
        ],
    ],
}


def numerical_differentiation(x_vals, y_vals, e=None, i_vals=None, methods=None, d=None, o=None):
    out_str = ''
    
    if (i_vals == None and e == None) or (i_vals == None and x_vals.index(e) == -1):
        raise ValueError('value value of i_vals or e should be provided')
        
    if i_vals == None:
        i = x_vals.index(e)
        i_vals = list(range(-1*i, len(x_vals)-i))
        
    if methods == None:
        if i_vals[0] == 0:
            methods = ['forward']
        elif i_vals[-1] == 0:
            methods = ['backward']
        else:
             methods = ['center']
            
    if type(methods) is str:
        methods = [methods]
    
    if d == None:
        d = [0, 1]
    if type(d) is int:
        d = [d]
        
    if o == None:
        o = [0, 1]
    if type(o) is int:
        o = [o]
        
    h = x_vals[1] - x_vals[0]
        
    
    out_str += f"\\begin{{center}}\n\\begin{{tabular}}{{ c |{' c' * len(i_vals)} }}\n"
    out_str += f" $i$ & ${'$ & $'.join([str(i) for i in i_vals])}$ \\\\\n \\hline\n"
    out_str += f" $x_i$ & ${'$ & $'.join([str(i) for i in x_vals])}$ \\\\\n"
    out_str += f" $f(x_i)$ & ${'$ & $'.join([str(r(i)) for i in y_vals])}$ \\\\\n"
    out_str += "\\end{tabular}\n\\end{center}\n\n"
    
    for method in methods:
        derivatives = [e for i, e in enumerate(formulas[method]) if i in d]
        for derivative in derivatives:
            orders = [e for i, e in enumerate(derivative) if i in o]
            for order in orders:
                if len(set(order[2])-set(i_vals)) < 1:
                    out_str += f'\\textbf{{{order[4]}}}\n\n'
                    out_str += f'$$ {order[0]} = {order[1]} $$ \n'
                    out_str += f'$$ {order[0]} = {r(order[3](dict(zip(i_vals, y_vals)), h))} $$ \n\n'
        
    return out_str


def numerical_differentiation_fn(f, x, h, method, derivative, order):
    i_vals = formulas[method][derivative-1][order-1][2]
    x_vals = [x + i * h for i in range(i_vals[0], i_vals[-1]+1)]
    y_vals = [f(x) for x in x_vals]
    
    return numerical_differentiation(x_vals, y_vals, h, x, i_vals)


if __name__ == '__main__':
    x = symbols('x')

    t = [0, 25, 50, 75, 100, 125]
    v = [0, 32, 58, 78, 92, 100]

    t = [.4, .6, .8, 1]
    v = [lambdify((x,), sin(0.5*sqrt(x))/x)(i) for i in t]

    print(numerical_differentiation(t, v, e=1))

    # for ti in t:
    #     print(f'\n\n\\textbf{{At $t={ti}$}}\n\n')
    #     print(numerical_differentiation(t, y, e=ti))
