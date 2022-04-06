import argparse
import matplotlib.pyplot as plt
import json
import itertools
import numpy as np
from pprint import pprint as pp
from datetime import datetime as dt
# import pprint.pprint as pp

MARKER = itertools.cycle(('s', '*', 'p', 'v', 'X', '^', 'D', 'o', 'P', '1', '8'))

def read_json(path_file):
    with open(path_file) as f:
        data = json.load(f)
        return data

def process_data(json_data):
    data = {'CHASELEV': {'times': [], 'graph': None, 'puts': [], 'takes': [], 'steals': []},
            'CILK': {'times': [], 'graph': None, 'puts': [], 'takes': [], 'steals': []},
            'IDEMPOTENT_FIFO': {'times': [], 'graph': None, 'puts': [], 'takes': [], 'steals': []},
            'IDEMPOTENT_LIFO': {'times': [], 'graph': None, 'puts': [], 'takes': [], 'steals': []},
            'IDEMPOTENT_DEQUE': {'times': [], 'graph': None, 'puts': [], 'takes': [], 'steals': []},
            'WS_NC_MULT': {'times': [], 'graph': None, 'puts': [], 'takes': [], 'steals': []},
            'B_WS_NC_MULT': {'times': [], 'graph': None, 'puts': [], 'takes': [], 'steals': []}
            }
    for result in json_data:
        algorithm = result['algorithm']
        time = result['executionTime']
        graph = result['graphType']
        puts = result['puts']
        takes = result['takes']
        steals = result['steals']
        data[algorithm]['times'].append(time)
        data[algorithm]['graph'] = graph
        data[algorithm]['puts'].append(puts)
        data[algorithm]['takes'].append(takes)
        data[algorithm]['steals'].append(steals)
    return data

def draw_chart_times(data, size):
    algs = list(data.keys())
    graph = data[algs[0]]['graph']
    plt.margins(0, 0)
    major_ticks = np.arange(0, size, 8)
    minor_ticks = np.arange(0, size, 1)
    nrange = np.arange(0, size)
    fig, axes = plt.subplots()
    axes.set_ylabel('Time in nanoseconds')
    axes.set_xlabel('Processors')
    axes.set_xticks(major_ticks, major=True)
    axes.set_yticks(minor_ticks, minor=True)
    axes.grid(which='both', axis='both')
    axes.grid(which='minor', alpha=0.2)
    axes.grid(which='major', alpha=0.5)
    fig.suptitle('Time to calculate spanning tree of a graph {} of 1,000,000 of vertices'.format(graph))
    for alg in algs:
        axes.plot(nrange, data[alg]['times'], marker=next(MARKER), ls='--', label=alg)
    axes.legend()
    current_time = dt.now().strftime('%H:%M:%S')
    plt.gcf().set_size_inches(19.2, 10.8)
    plt.savefig('time-measurment-{}-{}.png'.format(graph, current_time))


def chartGen(path_file):
    json_data = read_json(path_file)
    # print(json_data)
    processed_data = process_data(json_data['values'])
    draw_chart_times(processed_data, 64)
    # pp(processed_data.keys())


def main():
    desc="""Tools to make charts of experiments of work-stealing"""
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '--new',
        dest='chartGen',
        help="""Plot the chart of the given json file."""
    )
    args = parser.parse_args()
    if args.chartGen:
        chartGen(args.chartGen)

if __name__ == '__main__':
    main()
