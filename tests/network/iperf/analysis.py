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


def latency_histogram(df, save=True, compare=False):

    if compare:
        df = df.loc[df["building"].isin(["IRIS-INTERNAL", "IRIS-TS"])]

    avg_latencies = [x['average (ms)'] for x in df["latency"]]
    plt.bar(df["building"], avg_latencies)
    plt.xlabel("Building")
    plt.ylabel("Average Latency (ms)")
    title = "Average Latency from IRIS-Lab to UA Buildings through Tailscale"


    if compare:
        title = "Average latency comparison on Internal vs Tailscale connections"

    plt.title(title)

    for idx, val in enumerate(avg_latencies):
        plt.annotate(str(val), (idx, val), ha='center', va='bottom')
    if save:
        if compare:
            fname = "./plots/latency_overhead.png"
        else:
            fname = "./plots/building_latency.png"

        plt.savefig(fname)
    plt.show()

def jitter_histogram(df, save=True):
    jitters = [j['sum']['jitter_ms'] for j in [x['udp']['end'] for x in df['iperf']]]
    
    plt.bar(df["building"], jitters)
    plt.xlabel("Building")
    plt.ylabel("Jitter (ms)")
    plt.title("Average jitter")

    for idx, val in enumerate(jitters):
        plt.annotate(str(val), (idx, val), ha="center", va="bottom")

    if save:
        plt.savefig("./plots/building_jitter.png")
    plt.show()


def throughput_over_time(df, building, protocol="tcp"):
    print(f"Throughput for building {building}")

    building_df = df.loc[df["building"] == building]
    tcp_streams = [x[protocol] for x in  building_df["iperf"]][0]
    ts = []
    throughput = []

    for interval in tcp_streams['intervals']:
        data = interval['sum']
        ts.append(data['end'])
        throughput.append(data['bits_per_second'] / 1000000)

    print(f"{building} Avg TCP Throughput: {avg(throughput)}")
    #plt.plot(ts, throughput, color='blue', marker='o', linestyle='-', linewidth=1)
    plt.title(f'MBits Transmitted Per Second Over 120 Seconds - {building}')
    plt.xlabel('Time (seconds)')
    plt.ylabel('MBits per Second (Mbit/s)')
    plt.grid(True)

    if protocol != "tcp":
        ax = plt.gca()
        ax.set_ylim([1, 1.2])
    
    #plt.savefig(f"./plots/throughput/{protocol}/{building}.png")
    plt.close()
    plt.cla()
    plt.clf()

def throughput_all_buildings(df, protocol="tcp"):
    buildings = [ x for x in df['building'].unique() if "IRIS" not in x]
    
    for b in buildings:
        if "INTERNAL" not in b:
            if b == "IRIS-TS":
                b = "IRIS"
            throughput_over_time(df, b, protocol)
    

def throughput_internal_vs_tailscale(df, protocol="tcp"):
    dfs = [ df.loc[df["building"] == "IRIS-INTERNAL"], df.loc[df["building"] == "IRIS-TS"]]
    colors = ["blue", "red"]
    frame_id = 0
    
    tp_loss = 0.0
    tp_vals = {}
    tp_loss_avgs = []

    for frame in dfs:
        streams = [x[protocol] for x in frame["iperf"]][0]
        ts = []
        throughput = []

        for interval in streams['intervals']:
            data = interval['sum']
            ts.append(data['end'])
            tp_mbits = data['bits_per_second'] / 1000000
            throughput.append(tp_mbits)
            if frame_id not in tp_vals.keys():
                tp_vals[frame_id] = [tp_mbits]
            else:
                tp_vals[frame_id].append(tp_mbits)

        plt.plot(ts, throughput, color=colors[frame_id], marker='o', linestyle='-', linewidth=1)
        frame_id = frame_id + 1

    plt.title(f"{protocol.upper()} Throughput - Internal vs Tailscale connection (IRIS)")
    plt.legend(["internal", "tailscale"])
    plt.xlabel('Time (seconds)')
    plt.ylabel('MBits per Second (Mbit/s)')
    plt.grid(True)
    #plt.show()
    #plt.savefig(f"./plots/throughput/{protocol}/overhead.png")
    print(f"Throughput % loss: {percent_loss(avg(tp_vals[0]), avg(tp_vals[1]))}")
    #print(f"Latency % increase: {percent_gain(8.629, 11.671)}")

def percent_loss(avg1, avg2):
    return ((avg1 - avg2) / avg1) * 100

def percent_gain(avg1, avg2):
    return ((avg2 - avg1) / avg1) * 100

def avg(data):
    return sum(data) / len(data)

if __name__ == '__main__':

    test_dir = sys.agrv[1] if (len(sys.argv) == 2) else "./runs"
    df = load_runs(test_dir)
    
    #latency_histogram(df, compare=True)
    throughput_all_buildings(df, "tcp")
    #jitter_histogram(df)
    #throughput_internal_vs_tailscale(df)
    #percent_loss(df)
