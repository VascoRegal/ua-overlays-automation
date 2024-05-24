import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt

def load_runs(directory):
    
    data = {}
    files = os.listdir(directory)
    
    for f in files:
        with open(f"{directory}/{f}") as fp:
            data[f] = json.load(fp)

    frame = pd.DataFrame.from_dict(data, orient='index')
    return frame


def latency_histogram(df, save=True):
    avg_latencies = [x['average (ms)'] for x in df["latency"]]
    plt.bar(df["building"], avg_latencies)
    plt.xlabel("Building")
    plt.ylabel("Average Latency (ms)")
    plt.title("Average Latency from IRIS-Lab to UA Buildings through Tailscale")

    for idx, val in enumerate(avg_latencies):
        plt.annotate(str(val), (idx, val), ha='center', va='bottom')
    if save:
        plt.savefig("./plots/building_latency.png")
    plt.show()

if __name__ == '__main__':

    test_dir = sys.agrv[1] if (len(sys.argv) == 2) else "./runs"
    df = load_runs(test_dir)
    
    latency_histogram(df)
