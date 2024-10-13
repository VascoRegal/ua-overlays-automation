import os
import sys
import json
import pandas as pd

def load_runs(directory):

    data = {}
    files = os.listdir(directory)

    for f in files:
        with open(f"{directory}/{f}") as fp:
            data[f] = json.load(fp)

    frame = pd.DataFrame.from_dict(data, orient='index')
    return frame

def _pre_process(input_dir, output_dir):
    test_files = os.listdir(input_dir)

    for f in test_files:
        raw_data = {}
        with open(f"{input_dir}/{f}") as test_p:
            raw_data = json.load(test_p)
        
        print(f"[+] Prcoessing {raw_data['building']}...")
        out_object = {
            "rtt": {                        # ms
                "min" : 0,
                "mean" : 0,
                "max" : 0,
            },
            "tcp_throughput": {             # MBytes / s
                "data" : [],
                "mean": 0,
            },
            "jitter": {                     # ms
                "mean": 0
            }
        }


        rtts = []
        throughputs = []

        tcp_streams = raw_data["iperf"]["tcp"]
        udp_streams = raw_data["iperf"]["udp"]

        final_tcp_stream = tcp_streams["end"]["streams"][0]["sender"]
        out_object["rtt"]["min"] = final_tcp_stream["min_rtt"] / 10
        out_object["rtt"]["max"] = final_tcp_stream["max_rtt"] / 10
        out_object["rtt"]["mean"] = final_tcp_stream["mean_rtt"] / 10
        out_object["jitter"]["mean"] = udp_streams["end"]["sum"]["jitter_ms"] 

        for interval in tcp_streams["intervals"]:
            interval_data = interval["streams"][0]
            throughputs.append(interval_data["bits_per_second"] * (1.25 * pow(10, -7)))

        out_object["tcp_throughput"]["data"] = throughputs
        out_object["tcp_throughput"]["mean"] = sum(throughputs) / len(throughputs)

        with open(f"{output_dir}/{f}", "w") as out_p:
            json.dump(out_object, out_p)

if __name__ == '__main__':
    test_dir = sys.agrv[1] if (len(sys.argv) == 2) else "./runs"
    output_dir = "out"

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    _pre_process(test_dir, output_dir)
