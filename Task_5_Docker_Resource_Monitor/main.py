from docker_monitoring import monitor, collect_cpu_and_mem
import threading 
import time

if __name__ == "__main__":
    cpu_threshold = 10
    mem_threshold = 2
    monitoring_interval = 5

    collector_thread = threading.Thread(
        target=collect_cpu_and_mem, 
        daemon=True  
    )
    collector_thread.start()
    print("🚀 Collector started in background!")
    time.sleep(3)  # Daj czas na zebranie pierwszych danych

    monitor(cpu_threshold, mem_threshold, monitoring_interval)