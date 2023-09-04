import psutil
import time
import multiprocessing

def cpu_bound_task():
    while True:
        pass  # This task will consume CPU resources

def monitor_system_stats(duration_seconds):
    start_time = time.time()

    while time.time() - start_time < duration_seconds:
        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        
        # Get RAM usage
        ram_usage = psutil.virtual_memory()

        # Yield real-time stats
        yield {
            'CPU Usage': cpu_percent,
            'RAM Usage': ram_usage.percent
        }

if __name__ == "__main__":
    duration = int(input("Enter the duration of the stress test (in seconds): "))

    # Create multiple processes to load the CPU
    num_processes = multiprocessing.cpu_count()
    processes = [multiprocessing.Process(target=cpu_bound_task) for _ in range(num_processes)]

    print("Starting stress test...")
    for process in processes:
        process.start()

    print("\nMonitoring system stats during stress test...")

    # Create a generator to yield real-time stats
    stats_generator = monitor_system_stats(duration)

    # Loop to display real-time stats
    for stats in stats_generator:
        print(stats)

    # Terminate the CPU-bound processes when done
    for process in processes:
        process.terminate()
