import sys
from datetime import datetime
import subprocess
import json
import time

TEST_DURATION=60
MAX_PING_REPS=50

def iperf_base(host):
    return f"iperf3 -c {host} --json -t {TEST_DURATION}"

def test_iperf_tcp(host):
    return run(iperf_base(host))

def test_iperf_udp(host):
    return run(iperf_base(host) + f"--udp ")

def test_latency(host):
    return float(run(f"ping -c {MAX_PING_REPS} www.stackoverflow.com | tail -1| awk '{{print $4}}' | cut -d '/' -f 2", False))

def run(command, as_json=True):
    res = subprocess.check_output(command, shell=True).decode("utf-8")

    if as_json:
        return json.loads(res)
    return res    

def run_tests(host, building):
    

    print("\t[-] Running IPERF TCP tests...")
    tcp = test_iperf_tcp(host)
    print("\t[-] Done!")
    print()

    print("\t[-] Running IPERF UDP tests...")
    udp = test_iperf_udp(host)
    print("\t[-] Done!")
    print()

    print("\t[-] Calculating latencies...")
    lat = test_latency(host)
    print(f"\t[-] Done! ({lat} ms)")
    print() 

    results = {
        "iperf" : {
            "tcp": tcp,
            "udp": udp
        },
        "latency": {
            "average (ms)": lat,
            "max_replies": MAX_PING_REPS
        },
        "test_duration": 0,
        "building": building,
        "host": host
    }
    return results

if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print("python3 run.py [IPERF_HOST] [BUILDING]")
        sys.exit(1)

    iperf_host = sys.argv[1]
    building = sys.argv[2]
    
    test_name = f"{building}_{datetime.now().strftime('%d-%m-%y_%H-%M-%S')}"

    print(f"[+] Starting tests from {building}...")
    print(f"[+] Exporting runs to {test_name}.json")

    with open(f"runs/{test_name}.json", "w") as fp:
        json.dump(run_tests(iperf_host, building), fp)


