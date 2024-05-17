import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import numpy as np
import matplotlib.colors as mc
import colorsys

def adjust_lightness(color, amount=1.2):
    try:
        c = mc.cnames[color]
    except:
        c = color
    c = colorsys.rgb_to_hls(*mc.to_rgb(c))
    return colorsys.hls_to_rgb(c[0], max(0, min(1, amount * c[1])), c[2])



class Subtask:
    def __init__(self, description, duration):
        self.description = description
        self.duration = int(duration)

class Task:
    def __init__(self, title, start_time):
        self.title = title
        self.start_time = datetime.strptime(start_time, '%H:%M')
        self.subtasks = []
    
    def add_subtask(self, subtask):
        self.subtasks.append(subtask)

def load_tasks_from_csv(filename):
    df = pd.read_csv(filename)
    tasks = {}
    for _, row in df.iterrows():
        task_title = row['Task Title']
        if task_title not in tasks:
            tasks[task_title] = Task(task_title, row['Start Time'])
        tasks[task_title].add_subtask(Subtask(row['Subtask Description'], row['Duration']))
    return list(tasks.values())

def plot_tasks(tasks):
    plt.figure(figsize=(10, 6))
    plt.ylabel('Tasks')
    plt.xlabel('Time of Day')
    base_colors = ['skyblue', 'lightgreen', 'salmon', 'gold', 'violet']
    for i, task in enumerate(sorted(tasks, key=lambda x: x.start_time)):
        start = task.start_time
        color = base_colors[i % len(base_colors)]
        for j, subtask in enumerate(task.subtasks):
            shade = adjust_lightness(color, 1 + j * 0.1)
            start_num = (start - datetime.combine(start.date(), datetime.min.time())).total_seconds() / 3600
            end_num = (start + timedelta(minutes=subtask.duration) - datetime.combine(start.date(), datetime.min.time())).total_seconds() / 3600
            plt.barh(i, end_num - start_num, left=start_num, height=0.8, color=shade, edgecolor='blue')
            plt.text(start_num, i, f"{subtask.description}", horizontalalignment='left', verticalalignment='center', rotation=270)
            start += timedelta(minutes=subtask.duration)
    plt.xlim(0, 24)
    plt.xticks(np.arange(0, 24, 1), [f"{h}:00" for h in np.arange(0, 24, 1)])
    plt.yticks(range(len(tasks)), [task.title for task in tasks])
    plt.gca().invert_yaxis()
    plt.grid(True, which='both', linestyle='-', linewidth=0.5)
    plt.tight_layout()
    plt.show()

# Example usage:
tasks = load_tasks_from_csv('daily_planner_V06\planning.csv')
plot_tasks(tasks)
