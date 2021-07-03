from copy import deepcopy
from operator import itemgetter

from colorama import init
from termcolor import colored
from terminaltables import SingleTable

init()


def round_robin(jobs, quantum):
    jobs = sorted(jobs, key=itemgetter('arrival'))
    curr_time = 0
    total_wait_time = 0
    total_resp_time = 0
    total_turn_time = 0
    sum_time = 0
    timeline = []
    process_details = {}

    for process in jobs:
        process_details[process['name']] = {
            'arrival': process['arrival'],
            'burst': process['burst'],
            'wait_time': 0,
            'turn_time': 0,
            'resp_time': 0,
        }

    process_queue = []
    for orig_process in jobs:
        process = deepcopy(orig_process)
        process['time_given'] = 0
        process['last_time'] = 0
        process['wait_time'] = 0
        process['turn_time'] = 0
        process['resp_time'] = 0
        process_queue.append(process)

    i = 0
    while process_queue:
        process = process_queue[i]

        if curr_time < process['arrival']:
            timeline += [{
                'name': 'Idle',
                'start': curr_time,
                'end': process['arrival'],
                'queue': []
            }]

            curr_time = process['arrival']

        if (process['burst'] - process['time_given']) > quantum:
            time_added = quantum
            process['time_given'] += quantum
        else:
            time_added = process['burst'] - process['time_given']
            process['time_given'] = process['burst']
            process['completed'] = True

        if process['last_time'] == 0:
            process['start_time'] = curr_time
            process['resp_time'] = curr_time - process['arrival']
            process['wait_time'] += curr_time - process['arrival']
        else:
            process['first_start'] = False
            process['wait_time'] += curr_time - process['last_time']

        timeline += [{
            'name': process['name'],
            'completed': process.get('completed', False),
            'first_start': process.get('first_start', True),
            'start': curr_time,
            'end': curr_time + time_added,
            'queue': [
                p['name']
                for p in filter(lambda e: e['arrival'] < curr_time and e['name'] != process['name'], process_queue)
            ]
        }]

        curr_time += time_added
        process['last_time'] = curr_time

        if process['time_given'] == process['burst']:  # Process has finished execution
            process['turn_time'] = curr_time - process['arrival']

            process_details[process['name']]['wait_time'] = process['wait_time']
            process_details[process['name']]['turn_time'] = process['turn_time']
            process_details[process['name']]['resp_time'] = process['resp_time']

            total_wait_time += process['wait_time']
            total_turn_time += process['turn_time']
            total_resp_time += process['resp_time']
            sum_time += process['burst']

            process_queue.remove(process)

            if i >= len(process_queue):
                i = 0
        else:
            i = get_next_process(i, curr_time, process_queue)

    stats = {
        'Total time': '%7.2f' % float(sum_time),
        'Average waiting time': '%7.2f' % (float(total_wait_time) / len(jobs)),
        'Average response time': '%7.2f' % (float(total_resp_time) / len(jobs)),
        'Average turn-around time': '%7.2f' % (float(total_turn_time) / len(jobs)),
        'Average throughput': '%7.2f' % (len(jobs) / float(curr_time)),
        'CPU utilization': str('%7.2f' % (float(sum_time) * 100 / float(curr_time))) + '%'
    }

    return timeline, stats, process_details


def print_timeline(timeline):
    data = [['Start-End Time', 'Active Job', 'Queue']]

    for job in timeline:
        job_color = 'white'
        job_title = job['name']

        if job['name'] == 'Idle':
            job_color = 'grey'
        elif job.get('first_start', False) and job.get('completed', False):
            job_color = 'green'
        elif job.get('first_start', False):
            job_color = 'blue'
        elif job.get('completed', False):
            job_color = 'red'

        data.append([
            colored(f"{job['start']}-{job['end']}", 'cyan'),
            colored(job_title, job_color),
            ', '.join(job['queue'])
        ])

    table = SingleTable(data)
    print('\n\n Process execution timeline')
    print(table.table)


def print_process_details(processes):
    table = SingleTable([
        ['Name', 'Arrival Time', 'Burst Time', 'Waiting Time', 'Turn-around Time', 'Response Time'],
        *(
            [
                colored(k, 'green'),
                colored(p['arrival'], 'cyan'),
                colored(p['burst'], 'cyan'),
                colored(p['wait_time'], 'cyan'),
                colored(p['turn_time'], 'cyan'),
                colored(p['resp_time'], 'cyan'),
            ]
            for k, p in processes.items()
        )
    ])
    table.justify_columns = {0: 'left', 1: 'right', 2: 'right', 3: 'right', 4: 'right', 5: 'right'}
    print('\n\n Individual process details')
    print(table.table)


def print_stats(stats):
    table = SingleTable([[colored(k, 'green'), colored(v, 'cyan')] for k, v in stats.items()])
    table.outer_border = True
    table.inner_heading_row_border = False
    table.inner_column_border = False
    print('\n\n Overall stats')
    print(table.table)


def get_next_process(robin_idx, curr_time, process_queue):
    next_idx = (robin_idx + 1) % len(process_queue)
    while next_idx != robin_idx:
        if process_queue[next_idx]['arrival'] < curr_time:
            return next_idx
        else:
            next_idx = (next_idx + 1) % len(process_queue)
    return robin_idx


if __name__ == '__main__':
    quantum = 4

    timeline, stats, process_details = round_robin([
        {'name': 'p1', 'arrival': 11, 'burst': 6},
        {'name': 'p2', 'arrival': 5, 'burst': 4},
        {'name': 'p3', 'arrival': 3, 'burst': 8},
        {'name': 'p4', 'arrival': 13, 'burst': 5},
        {'name': 'p5', 'arrival': 3, 'burst': 4},
        {'name': 'p6', 'arrival': 2, 'burst': 9},
        {'name': 'p7', 'arrival': 9, 'burst': 3},
        {'name': 'p8', 'arrival': 7, 'burst': 9},
    ], quantum)

    print_timeline(timeline)
    print_process_details(process_details)
    print_stats(stats)
