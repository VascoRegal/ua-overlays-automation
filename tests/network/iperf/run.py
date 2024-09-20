import sys
from datetime import datetime
import subprocess
import json
import time

TEST_DURATION=600
MAX_PING_REPS=100

def iperf_base(host):
    return f"iperf3 -c {host} --json -t {TEST_DURATION} "

def test_iperf(host, udp=False):
    command = iperf_base(host)
    if udp:
        command += "-u"
    results = run(command)
    time.sleep(2)
    return results

def test_latency(host):
    results = run(f"ping -c {MAX_PING_REPS} {host} | tail -1| awk '{{print $4}}'", False)
    results = [float(x.strip()) for x in results.split("/")]
    rtts = {
        'min': results[0],
        'avg': results[1],
        'max': results[2],
        'dev': results[3]
    }
    return rtts

def run(command, as_json=True):
    res = subprocess.check_output(command, shell=True).decode("utf-8")

    if as_json:
        return json.loads(res)
    return res    

def run_tests(host, building):
    

    print("\t[-] Running IPERF TCP tests...")
    tcp = test_iperf(host)
    print("\t[-] Done!")
    print()

    print("\t[-] Running IPERF UDP tests...")
    udp = test_iperf(host,udp=True)
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
        "rtt": lat,
        "test_duration": 0,
        "building": building,
        "host": host,
        "date": {
            "day": None,
            "time": None
        }
    }
    return results

if __name__ == '__main__':
    
    if len(sys.argv) != 3:
        print("python3 run.py [IPERF_HOST] [BUILDING]")
        sys.exit(1)

    iperf_host = sys.argv[1]
    building = sys.argv[2]
    day = datetime.today().strftime('%d-%m-%y')
    hours = datetime.now().time().strftime('%H-%M-%S')

    test_name = f"{building}_{day}_{hours}"

    print(f"[+] Starting tests from {building}...")
    print(f"[+] Exporting runs to {test_name}.json")

    res = run_tests(iperf_host, building)
    res['date']['day'] = day
    res['date']['time'] = hours

    with open(f"runs/{test_name}.json", "w") as fp:
        json.dump(res, fp, indent=4)



