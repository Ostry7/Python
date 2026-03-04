import docker
import time
import json
from datetime import datetime

client = docker.from_env()
containers = client.containers.list(all=False)
stats_list = []



def collect_cpu_and_mem():
    while True:
        for container in containers: 
            stats = container.stats(stream=False)         
            cpu_delta = stats["cpu_stats"]["cpu_usage"]["total_usage"] - \
                       stats["precpu_stats"]["cpu_usage"]["total_usage"]
            system_delta = stats["cpu_stats"]["system_cpu_usage"] - \
                          stats["precpu_stats"]["system_cpu_usage"]
            cpu_percent = (cpu_delta / system_delta) * 100.0 if system_delta > 0 else 0
            mem_usage = stats['memory_stats']['usage']      
            mem_limit = stats['memory_stats']['limit']      
            mem_percent = (mem_usage / mem_limit) * 100     
            stats_list.append({
                'timestamp': datetime.now().isoformat(),
                'container': container.name,
                'cpu': f"{cpu_percent:.1f}",
                'memory': f"{mem_percent:.1f}"
            })
            with open ('stats.json', 'w') as f:
                json.dump(stats_list, f, indent=2)            
            time.sleep(1)

def monitor():
    while True:
        try:
            with open ('stats.json', 'r', encoding="utf-8") as f:
                stats = json.load(f)
                for stat in stats:
                    if float(stat['cpu']) > 0.005:
                        print(f"[==== {stat['container']} ==== CPU Usage is higher then selected threshold!")
                    if float(stat["memory"]) > 0.005:
                        print(f"[==== {stat['container']} ==== Memory Usage is higher then selected threshold!")
                    #print(f"{stat['container']}: {stat['timestamp']}")
                
        except FileNotFoundError:
            print("Waiting for stats file")
        time.sleep(5)

#collect_cpu_and_mem()
monitor()
