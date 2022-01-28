import argparse
import matplotlib.pyplot as plt
import json
import itertools
import numpy as np

from datetime import datetime
from pprint import pprint

MARKER = itertools.cycle(('s', '*', 'p', 'v', 'X', '^', 'D', 'o', 'P', '1', '8'))

def read_json(path_file):
    """Read the json from the `path_file`"""
    with open(path_file) as f:
        data = json.load(f)
        return data

def plot_llic(path_file):
    json_data = read_json(path_file)
    cas = json_data['CAS']
    fai = json_data['FAI']
    rw = json_data['RW']
    rwnc = json_data['RWNC']
    size = len(cas)
    nrange = np.arange(1, size + 1)
    versions = ['LLIC-CAS', 'LLIC-RW wo FS', 'LLIC-RW w FS', 'Fetch&Inc']
    major_ticks = np.arange(0, size+1, 8)
    minor_ticks = np.arange(0, size+1, 1)
    plt.margins(0,0)
    fig, axes = plt.subplots()
    axes.set_ylabel('Time in ms')
    axes.set_xlabel('Processors')
    axes.set_xticks(major_ticks, major=True)
    axes.set_xticks(minor_ticks, minor=True)
    axes.grid(which='both', axis='both')
    axes.grid(which='minor', alpha=0.2)
    axes.grid(which='major', alpha=0.5)
    fig.suptitle('Time to perform 500,000,000 of interspersed LL/IC')
    axes.plot(nrange, cas, marker=next(MARKER), ls='--', label='LL/IC CAS')
    axes.plot(nrange, rw, marker=next(MARKER), ls='-', label='LL/IC without False Sharing')
    axes.plot(nrange, rwnc, marker=next(MARKER), ls='-', label='LL/IC with False Sharing')
    axes.plot(nrange, fai, marker=next(MARKER), ls=':', label='Fetch&Inc')
    axes.legend()
    current_time = datetime.now().strftime("%H:%M:%S")
    plt.gcf().set_size_inches(19.2, 10.8)
    plt.savefig('time-measurment-{}.png'.format(current_time))

def plot_llic_iters(path_file, iters):
    json_data = read_json(path_file)
    algs = ['RW', 'RWNC', 'RW16', 'RW32', 'RW128', 'RWWC', 'CAS', 'FAI', 'FAIDELAY', 'FAIRANDOM', 'RWNS']
    alg_names = [
        {'name': 'LL/IC without False Sharing', 'ls': '-'},
        {'name': 'LL/IC with False Sharing', 'ls': '-'},
        {'name': 'LL/IC 16 bits without False Sharing', 'ls': '--'},
        {'name': 'LL/IC 32 bits without False Sharing', 'ls': '--'},
        {'name': 'LL/IC 128 bits without False Sharing', 'ls': '--'},
        {'name': 'LL/IC without False Sharing and no cycle in IC', 'ls': '--'},
        {'name': 'LL/IC CAS', 'ls': ':'},
        {'name': 'Fetch & Inc', 'ls': ':'},
        {'name': 'Fetch & Inc Delay', 'ls': ':'},
        {'name': 'Fetch & Inc Random', 'ls': ':'},
        {'name': 'LL/IC new Solution', 'ls': '-'}
    ]
    data = {alg: [] for alg in algs}
    for i in range(iters):
        iter_vals = json_data['iter-{}'.format(i)]
        data = {alg: data[alg] + [iter_vals[alg]] for alg in algs}
    data = {alg: np.mean(data[alg], axis = 0) for alg in algs}
    print(data)
    size = len(data[algs[0]])
    nrange = np.arange(1, size + 1)
    major_ticks = np.arange(0, size+1, 8)
    minor_ticks = np.arange(0, size+1, 1)
    plt.margins(0,0)
    fig, axes = plt.subplots()
    axes.set_ylabel('Time in ns')
    axes.set_xlabel('Processors')
    axes.set_xticks(major_ticks, major=True)
    axes.set_xticks(minor_ticks, minor=True)
    axes.grid(which='both', axis='both')
    axes.grid(which='minor', alpha=0.2)
    axes.grid(which='major', alpha=0.5)
    fig.suptitle('Time to perform 500,000,000 of interspersed LL/IC')
    for idx, alg in enumerate(algs):
        axes.plot(nrange, data[alg], marker=next(MARKER),
                  ls=alg_names[idx]['ls'], label=alg_names[idx]['name'])
    axes.legend()
    current_time = datetime.now().strftime("%H:%M:%S")
    plt.gcf().set_size_inches(19.2, 10.8)
    plt.savefig('[MEAN-{}]time-measurment-{}.png'.format(iters, current_time))


def plot_latency(path_file):
    json_data = read_json(path_file)
    # pprint(json_data)
    latfai = json_data['LAT_FAI']
    latllic = json_data['LAT_LLIC']
    size = len(latfai)
    nrange = np.arange(1, size + 1)
    versions = ['Fetch&Inc', 'LLIC-CAS']
    major_ticks = np.arange(0, size+1, 8)
    minor_ticks = np.arange(0, size+1, 1)
    plt.margins(0,0)
    fig, axes = plt.subplots()
    axes.set_ylabel('Operation Latency [ns/op]')
    axes.set_xlabel('Concurrent Threads')
    axes.set_xticks(major_ticks, major=True)
    axes.set_xticks(minor_ticks, minor=True)
    axes.grid(which='both', axis='both')
    axes.grid(which='minor', alpha=0.2)
    axes.grid(which='major', alpha=0.5)
    axes.plot(nrange, latfai, marker=next(MARKER), ls='--', label='Fetch & Increment')
    axes.plot(nrange, latllic, marker=next(MARKER), ls='-', label='LL/IC CAS')
    axes.legend()
    current_time = datetime.now().strftime("%H:%M:%S")
    plt.gcf().set_size_inches(19.2, 10.8)
    plt.savefig('operations-latency-{}.png'.format(current_time))


def plot_latency_iters(path_file, iters):
    json_data = read_json(path_file)
    types = ['LAT_FAI', 'LAT_LLICCAS']
    type_names = [
        {'name': 'Fetch & Increment', 'ls': '--'},
        {'name': 'LL/IC CAS', 'ls': '-'}
    ]
    data = {t: [] for t in types}
    for i in range(iters):
        iter_vals = json_data['iter-{}'.format(i)]
        data = {t: data[t] + [iter_vals[t]] for t in types}
    data = {t: np.mean(data[t], axis = 0) for t in types}
    size = len(data[types[0]])
    nrange = np.arange(1, size + 1)
    major_ticks = np.arange(0, size+1, 8)
    minor_ticks = np.arange(0, size+1, 1)
    plt.margins(0,0)
    fig, axes = plt.subplots()
    axes.set_ylabel('Operation Latency [ns/op]')
    axes.set_xlabel('Concurrent Threads')
    axes.set_xticks(major_ticks, major=True)
    axes.set_xticks(minor_ticks, minor=True)
    axes.grid(which='both', axis='both')
    axes.grid(which='minor', alpha=0.2)
    axes.grid(which='major', alpha=0.5)
    for idx, t in enumerate(types):
        axes.plot(nrange, data[t], marker=next(MARKER),
                  ls=type_names[idx]['ls'], label=type_names[idx]['name'])
    axes.legend()
    current_time = datetime.now().strftime("%H:%M:%S")
    plt.gcf().set_size_inches(19.2, 10.8)
    plt.savefig('[MEAN-{}]operations-latency-{}.png'.format(iters, current_time))



def main():
    desc = """
    Tools to made the charts for queues experiments.
    """
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument(
        '--llic',
        dest='llicest',
        help='''Plot the chart for llic tests'''
    )
    parser.add_argument(
        '--lat',
        dest='lat',
        help='''Plot the chart for latency tests'''
    )
    parser.add_argument(
        '--iters',
        dest='iters',
        help='''Iterations number'''
    )
    parser.add_argument(
        '--llicm',
        dest='llicm',
        help='''Plot the chart for llic tests'''
    )
    parser.add_argument(
        '--latm',
        dest='latm',
        help='''Plot the chart for latency tests'''
    )
    args = parser.parse_args()
    if args.llicest:
        plot_llic(args.llicest)
    elif args.lat:
        plot_latency(args.lat)
    elif args.latm:
        plot_latency_iters(args.latm, int(args.iters))
    elif args.llicm:
        plot_llic_iters(args.llicm, int(args.iters))

if __name__ == '__main__':
    main()
