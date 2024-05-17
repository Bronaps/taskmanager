import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np

class Subtask:
    def __init__(self, description, duration):
        self.description = description
        self.duration = int(duration)  # Duration in minutes, ensure it's an integer

class Task:
    def __init__(self, title, start_time, subtasks=None):
        self.title = title
        self.start_time = datetime.strptime(start_time, '%H:%M')
        self.subtasks = subtasks if subtasks else []
    
    def add_subtask(self, subtask):
        self.subtasks.append(subtask)
    
    def get_end_time(self):
        total_duration = sum(subtask.duration for subtask in self.subtasks)
        return self.start_time + timedelta(minutes=total_duration)
    
    def get_total_duration(self):
        return sum(subtask.duration for subtask in self.subtasks)

def collect_tasks():
    tasks = []
    while True:
        title = input("Enter task title: ")
        start_time = input("Enter the start time of the task (HH:MM): ")
        task = Task(title, start_time)
        while True:
            subtask_desc = input("Enter subtask description: ")
            subtask_duration = input("Enter subtask duration (in minutes): ")
            subtask = Subtask(subtask_desc, subtask_duration)
            task.add_subtask(subtask)
            if input("Add another subtask? (yes/no): ").lower() != 'yes':
                break
        tasks.append(task)
        if input("Add another task? (yes/no): ").lower() != 'yes':
            break
    # Sort tasks by start time
    tasks.sort(key=lambda x: x.start_time)
    return tasks

def adjust_lightness(color, amount=1.2):
    import matplotlib.colors as mc
    import colorsys
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])

def plot_tasks(tasks):
    plt.figure(figsize=(10, 6))
    plt.ylabel('Tasks')
    plt.xlabel('Time of Day')
    
    # List of base colors for tasks
    base_colors = ['skyblue', 'lightgreen', 'salmon', 'gold', 'violet']
    
    for i, task in enumerate(tasks):
        start = task.start_time
        color = base_colors[i % len(base_colors)]
        for j, subtask in enumerate(task.subtasks):
            shade = adjust_lightness(color, 1 - j * 0.1)  # Lighten the color for each subtask
            start_num = (start - datetime.combine(start.date(), datetime.min.time())).total_seconds() / 3600
            end_num = (start + timedelta(minutes=subtask.duration) - datetime.combine(start.date(), datetime.min.time())).total_seconds() / 3600
            plt.barh(i, end_num - start_num, left=start_num, height=0.8, color=shade, edgecolor='blue')
            plt.text(start_num, i, f"{subtask.description}", horizontalalignment='left', verticalalignment='center', rotation=270)
            start += timedelta(minutes=subtask.duration)

    plt.xlim(6, 21)
    hour_ticks = np.arange(6, 21.1, 1)  # Major ticks at every full hour
    minute_ticks = np.arange(6, 21.1, 1/12)  # Minor ticks at every 5 minutes
    plt.xticks(hour_ticks, [f"{int(h)}:00" for h in hour_ticks])  # Label only full hours
    plt.gca().xaxis.set_minor_locator(plt.MultipleLocator(1/12))  # Minor ticks every 5 minutes
    plt.yticks(range(len(tasks)), [task.title for task in tasks])
    plt.gca().invert_yaxis()  # Inverts the y-axis
    plt.grid(True, which='both', linestyle='-', linewidth=0.5)
    plt.tight_layout()
    plt.show()

tasks = collect_tasks()
plot_tasks(tasks)
