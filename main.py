import argparse
import matplotlib.pyplot as plt
import json
import itertools
import numpy as np

from datetime import datetime
from pprint import pprint

def read_json(path_file):
    """Read the json from the `path_file`"""
    with open(path_file) as f:
        data = json.load(f)
        return data

def plot_llic(path_file):
    marker = itertools.cycle(('s', '*', 'p', 'v', 'X', '^', 'D', 'o', 'P', '1'))
    json_data = read_json(path_file)
    pprint(json_data)
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
    axes.plot(nrange, cas, marker=next(marker), ls='--', label='LL/IC CAS')
    axes.plot(nrange, rw, marker=next(marker), ls='-', label='LL/IC without False Sharing')
    axes.plot(nrange, rwnc, marker=next(marker), ls='-', label='LL/IC with False Sharing')
    axes.plot(nrange, fai, marker=next(marker), ls=':', label='Fetch&Inc')
    axes.legend()
    current_time = datetime.now().strftime("%H:%M:%S")
    plt.gcf().set_size_inches(19.2, 10.8)
    plt.savefig('time-measurment-{}.png'.format(current_time))


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
    args = parser.parse_args()
    if args.llicest:
        plot_llic(args.llicest)

if __name__ == '__main__':
    main()
