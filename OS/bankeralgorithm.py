from operator import sub, add

from colorama import init
from termcolor import colored
from terminaltables import SingleTable

init()


def banker_algorithm(p_table, total_resources):
    safe_sequence = []
    available = total_resources

    for p in p_table:
        available = list(map(sub, available, p['allocated']))
        p['need'] = list(map(sub, p['max'], p['allocated']))
        p['done'] = False

    while True:
        for p in p_table:
            if all(a >= n for a, n in zip(available, p['need'])) and not p['done']:
                safe_sequence.append(p['i'])
                available = list(map(add, available, p['allocated']))
                p['done'] = True
                break
        else:
            break

    return safe_sequence, p_table


if __name__ == '__main__':
    total = [10, 5, 7]
    processes = [
        {'i': 0, 'allocated': [0, 1, 0], 'max': [7, 5, 3]},
        {'i': 1, 'allocated': [2, 0, 0], 'max': [3, 2, 2]},
        {'i': 2, 'allocated': [3, 0, 2], 'max': [9, 0, 2]},
        {'i': 3, 'allocated': [2, 1, 1], 'max': [2, 2, 2]},
        {'i': 4, 'allocated': [0, 0, 2], 'max': [4, 3, 3]},
    ]

    seq, processes = banker_algorithm(processes, total)

    table = SingleTable([
        ['Process', 'Allocated', 'Max', 'Need'],
        *(
            [
                colored(f'P{p["i"]}', 'green'),
                colored(', '.join(map(str, p['allocated'])), 'cyan'),
                colored(', '.join(map(str, p['max'])), 'cyan'),
                colored(', '.join(map(str, p['need'])), 'cyan'),
            ]
            for p in processes
        )
    ])
    print('\n\n Process Table')
    print(table.table)

    if len(seq) != len(processes):
        print(f'\n\n {colored("No safe sequence found.", "red")} Following process can be executed:')
    else:
        print(f'\n\n {colored("Following is the safe sequence of process execution:", "blue")}')

    print(' ' + ' -> '.join(colored(f'P{i}', 'green') for i in seq))
