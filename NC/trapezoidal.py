from decimal import Decimal
import math

from sympy import lambdify, symbols, cos, ln, latex

from utils import r


def trapezoidal_single(a, b, vals, h, i):
    outstr = f'\n$a={r(a)}$, $b={r(b)}$\n'
    outstr += f'$$ I_{i} = (b-a)\\left(\\frac{{f(a) + f(b)}}{{2}}\\right) $$\n'
    outstr += f'$$ I_{i} = ({r(b)}-{r(a)})\\left(\\frac{{f({r(a)}) + f({r(b)})}}{{2}}\\right) $$\n'
    outstr += f'$$ I_{i} = ({r(b-a)})\\left(\\frac{{{r(vals[0])} + {r(vals[1])}}}{{2}}\\right) $$\n'
    ans = (b-a)*Decimal(((vals[0]+vals[1])/2))
    outstr += f'$$ I_{i} = {r(ans)} $$\n'
    return outstr, ans


def trapezoidal_multi(a, b, vals, h, i, n):
    outstr = f'\n$a={r(a)}$, $b={r(b)}$, $n={n}$, $h={r(h)}$\n'
    outstr += f'$$ I_{i} = \\frac{{b-a}}{{2n}}\\left[f(a) + 2\\left(\\sum^{{n-1}}_{{i=1}}f(a+ih)\\right) + f(b)\\right] $$\n'
    outstr += f'$$ I_{i} = \\frac{{{r(b)}-{r(a)}}}{{2({n})}}\\left[f({r(a)}) + 2\\left(\\sum^{{{n-1}}}_{{i=1}}f({r(a)}+{r(h)}i)\\right) + f({r(b)})\\right] $$\n'
    fns = sum(vals[1:n])
    
    outstr += f'$$ I_{i} = \\frac{{{r(b-a)}}}{{{2*n}}}\\left[{r(vals[0])} + 2*{r(fns)} + {r(vals[-1])}\\right] $$\n'
    outstr += f'$$ I_{i} = {r((b-a)/(2*n))}({r(vals[0] + fns*2 + vals[-1])}) $$\n'
    ans = (b-a)/(2*n)*Decimal(vals[0] + fns*2 + vals[-1])
    outstr += f'$$ I_{i} = {r(ans)} $$\n'
    return outstr, ans


def trapezoidal(points, vals=None, fn=None):
    outstr = ''
    if vals is None and fn is None:
        raise ValueError('vals or fn should be provided')
    
    if vals is not None and len(vals) != len(points):
        raise ValueError('values and points have different lengths')
    
    if vals is None:
        x = symbols('x')
        vals = [lambdify(x, fn)(float(p)) for p in points]
    
    points = [Decimal(p) for p in points]
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
        elif i['n'] > 1:
            s, o = trapezoidal_multi(
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

    # print(trapezoidal(['1990', '1992', '1994', '1996', '1998'], [2, 5, 8, 11, 13]))
    # print(trapezoidal(['0', '.1', '.2', '.3', '.4', '.5'], [1, 8, 4, 3.5, 5, 1]))
    print(trapezoidal([0, math.pi/2], fn=6+3*cos(x)))
    # print(trapezoidal([math.pi/10 * i for i in range(6)], fn=6+3*cos(x)))
    # print(trapezoidal(['8', '30'], fn=2000*ln(140000/(140000-2100*x))-9.8*x))