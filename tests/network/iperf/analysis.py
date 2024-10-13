import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt

def _load_runs(directory):
    
    data = {}
    files = os.listdir(directory)
    
    for f in files:
        with open(f"{directory}/{f}") as fp:
            data[f.split("_")[0]] = json.load(fp)

    return data


def _to_tex(data):
    for building in data.keys():
        b_data = data[building]
        print(f"{building} & {round(b_data['rtt']['min'], 2)} & {round(b_data['rtt']['mean'], 2)} & {round(b_data['rtt']['max'],2)} & {round(b_data['tcp_throughput']['mean'],2)} & {b_data['jitter']['mean']}  \\\\ \\hline")

def _throughput_overhead(data):
    buildings = [x for x in data.keys() if "IRIS" in x]
    colors = ["red", "blue"]
    means = []
    ts = list(range(600))
    color_index = 0
    for b in buildings:
        means.append(data[b]['tcp_throughput']['mean'])
        plt.plot(ts, data[b]['tcp_throughput']['data'], color=colors[color_index], marker='o', linestyle='-', linewidth=1)
        color_index += 1
    
    plt.title(f"IRIS Lab's TCP Throughput on Internal and Overlay connections")
    plt.legend(["overlay", "internal"])
    plt.xlabel("Time (seconds)")
    plt.ylabel("MBytes per Second (MB/s)")
    plt.grid(True)
    plt.show()

    print(f"\n>>> Throughput % loss: {_percent_loss(means[1], means[0])}")

def _rtt_box_plot(data):
    buildings = [x for x in data.keys() if "IRIS" in x]
    mins = []
    means = []
    maxs = []

    for b in buildings:
        mins.append(data[b]['rtt']['min'])
        means.append(data[b]['rtt']['mean'])
        maxs.append(data[b]['rtt']['max'])

    box_data = [[mins[0], maxs[0]], [mins[1], maxs[1]]]
    print(box_data)
    fig, ax = plt.subplots()
    ax.boxplot(box_data, vert=True, patch_artist=True, showmeans=False, whis=[0,100], widths=0.5)
    ax.scatter([1,2], means, color='red', label='Mean', zorder=3)
    plt.show()

def _percent_loss(avg1, avg2):
    return ((avg1 - avg2) / avg1) * 100

def percent_gain(avg1, avg2):
    return ((avg2 - avg1) / avg1) * 100

if __name__ == '__main__':

    test_dir = sys.agrv[1] if (len(sys.argv) == 2) else "./out"
    data = _load_runs(test_dir)
    #_to_tex(data)
    #_throughput_overhead(data)
    _rtt_box_plot(data)
