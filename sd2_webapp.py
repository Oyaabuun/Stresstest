import sched
from flask import Flask, render_template, request, redirect, url_for, jsonify
import multiprocessing
import time
import psutil

app = Flask(__name__)
app.scheduler = sched.scheduler(time.time, time.sleep)

# Global variable to control when to stop the CPU-bound tasks
stop_cpu_tasks = False

def cpu_bound_task(duration):
    global stop_cpu_tasks
    start_time = time.time()
    while not stop_cpu_tasks and (time.time() - start_time) < duration:
        pass  # This task will consume CPU resources

# ... (other code)

@app.route("/", methods=["GET", "POST"])
def index():
    global stop_cpu_tasks
    if request.method == "POST":
        duration = int(request.form["duration"])
        num_processes = multiprocessing.cpu_count()
        processes = [multiprocessing.Process(target=cpu_bound_task, args=(duration,)) for _ in range(num_processes)]

        for process in processes:
            process.start()

        # Set a flag to stop CPU-bound tasks after the duration
        stop_cpu_tasks = True

        # Schedule a function to stop the CPU-bound tasks after the specified duration
        def stop_tasks():
            global stop_cpu_tasks
            stop_cpu_tasks = True

        # Use the Flask scheduler to stop the tasks
        app.scheduler.enter(duration, 1, stop_tasks)

        return redirect(url_for("monitor_stats", duration=duration))

    return render_template("index.html")

@app.route("/monitor/<int:duration>")
def monitor_stats(duration):
    def stats_generator(duration):
        start_time = time.time()
        while time.time() - start_time < duration:
            # Get CPU usage
            cpu_percent = psutil.cpu_percent(interval=1)
            
            # Get RAM usage
            ram_usage = psutil.virtual_memory()

            yield jsonify({
                'CPU Usage': cpu_percent,
                'RAM Usage': ram_usage.percent
            })

    return render_template("stats.html", duration=duration)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
