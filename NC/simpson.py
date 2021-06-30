from decimal import Decimal

from sympy import ln, symbols, lambdify, latex

from utils import r
from trapezoidal import trapezoidal_single

def simpson_single(a, b, vals, h, i):
    outstr = f'\n$a={r(a)}$, $b={r(b)}$, $h={r(h)}$\n'
    outstr += f'$$ I_{i} = \\frac{{b-a}}{{6}}\\left(f(a) + 4f(\\frac{{a+b}}{{2}}) + f(b)\\right) $$\n'
    outstr += f'$$ I_{i} = \\frac{{{r(b-a)}}}{{6}}\\left(f({r(a)}) + 4f({r((a+b)/2)}) + f({b})\\right) $$\n'
    outstr += f'$$ I_{i} = {r((b-a)/6)}\\left({r(vals[0])} + 4\\times{vals[1]} + {r(vals[-1])}\\right) $$\n'
    
    ans = (b-a)/6 * Decimal(vals[0] + 4*vals[1] + vals[-1])
    outstr += f'$$ I_{i} = {r(ans)} $$\n'
    return outstr, ans


def simpson_multi(a, b, vals, h, i, n):
    outstr = f'\n$a={r(a)}$, $b={r(b)}$, $n={n}$, $h={r(h)}$\n'
    outstr += f'$$ I_{i} = \\frac{{b-a}}{{3n}}\\left(f(a) + 4\\sum_{{\\substack{{i=1\\\\i = odd}}}}^{{n-1}}f(x_i) + 2\\sum_{{\\substack{{i=2\\\\i = even}}}}^{{n-2}}f(x_i) + f(b)\\right) $$\n'
    outstr += f'$$ I_{i} = \\frac{{{r(b-a)}}}{{3\\times{n}}}\\left(f({r(a)}) + 4\\sum_{{\\substack{{i=1\\\\i = odd}}}}^{{{n-1}}}f(x_i) + 2\\sum_{{\\substack{{i=2\\\\i = even}}}}^{{{n-1}}}f(x_i) + f({r(b)})\\right) $$\n'
    outstr += f'$$ I_{i} = {r((b-a)/(3*n))}\\left({r(vals[0])} + 4\\sum_{{\\substack{{i=1\\\\i = odd}}}}^{{{n-1}}}f(x_i) + 2\\sum_{{\\substack{{i=2\\\\i = even}}}}^{{{n-1}}}f(x_i) + {r(vals[-1])}\\right) $$\n'
    
    odd_sum = sum(vals[i] for i in range(1, n) if i % 2 != 0)
    even_sum = sum(vals[i] for i in range(2, n-1) if i % 2 == 0)
    
    outstr += f'$$ I_{i} = {r((b-a)/(3*n))}\\left({r(vals[0])} + 4\\times{r(odd_sum)} + 2\\times{r(even_sum)} + {r(vals[-1])}\\right) $$\n'
    outstr += f'$$ I_{i} = {r((b-a)/(3*n))}\\left({r(vals[0])} + {r(4*odd_sum)} + {r(2*even_sum)} + {r(vals[-1])}\\right) $$\n'
    outstr += f'$$ I_{i} = {r((b-a)/(3*n))}\\left({r(vals[0] + 4*odd_sum + 2*even_sum + vals[-1])}\\right) $$\n'
    
    ans = (b-a)/(3*n) * Decimal((vals[0] + 4*odd_sum + 2*even_sum + vals[-1]))
    outstr += f'$$ I_{i} = {r(ans)} $$\n'
    return outstr, ans


def simpson(points, vals=None, fn=None, n=2):
    outstr = ''
    x = symbols('x')
    
    points = [Decimal(p) for p in points]
    if len(points) == 2:
        h = (points[-1] - points[0])/n
        points = [Decimal(points[0] + h * i) for i in range(0, n+1)]
    
    if vals is None and fn is None:
        raise ValueError('vals or fn should be provided')
    
    if vals is not None and len(vals) != len(points):
        raise ValueError('values and points have different lengths')
    
    if vals is None:
        vals = [lambdify(x, fn)(float(p)) for p in points]
    
    intervals = [{'start': 0, 'end': 1, 'diff': points[1] - points[0], 'n': 1}]
    for i, el in enumerate(points[2:]):
        i = i+2
        diff = points[i] - points[i-1]
        if diff == intervals[-1]['diff']:
            intervals[-1]['end'] = i
            intervals[-1]['n'] += 1
        else:
            intervals.append({
                'start': i-1,
                'end': i,
                'diff': points[i] - points[i-1],
                'n': 1,
            })
    
    if fn is not None:
        outstr += f'$$ f(x) = {latex(fn)} $$\n'
        for i, p in enumerate(points):
            outstr += f'$$ f({r(p)}) = {r(vals[i])} $$\n'
            
    ans = 0
    for j, i in enumerate(intervals):
        s, o = '', 0
        if i['n'] == 1:
            s, o = trapezoidal_single(
                points[i['start']], points[i['end']],
                vals[i['start']: i['end']+1],
                i['diff'], j+1
            )
        elif i['n'] == 2:
            s, o = simpson_single(
                points[i['start']], points[i['end']],
                vals[i['start']: i['end']+1],
                i['diff'], j+1
            )
        elif i['n'] > 2:
            s, o = simpson_multi(
                points[i['start']], points[i['end']],
                vals[i['start']: i['end']+1],
                i['diff'], j+1, i['n'] 
            )
        else:
            raise ValueError('')
        outstr += s
        ans += o
        
    outstr += f'\n$$ I = sum(I) = {r(ans)} $$\n'
    
    return outstr


if __name__ == '__main__':
    x = symbols('x')
    # print(simpson([8, 30], fn=2000*ln(140000/(140000-2100*x))-9.8*x))
    print(simpson([8, 30], fn=2000*ln(140000/(140000-2100*x))-9.8*x, n=4))
