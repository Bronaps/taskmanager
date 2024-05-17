import matplotlib.pyplot as plt
from datetime import datetime, timedelta

class Subtask:
    def __init__(self, description, duration):
        self.description = description
        self.duration = duration  # Duration in minutes

class Task:
    def __init__(self, start_time, subtasks=None):
        self.start_time = datetime.strptime(start_time, '%H:%M')
        self.subtasks = subtasks if subtasks else []
    
    def add_subtask(self, subtask):
        self.subtasks.append(subtask)
    
    def get_end_time(self):
        total_duration = sum(subtask.duration for subtask in self.subtasks)
        return self.start_time + timedelta(minutes=total_duration)
    
    def get_total_duration(self):
        return sum(subtask.duration for subtask in self.subtasks)

tasks = [
    Task('09:00', [Subtask('Emails', 30), Subtask('Quick Review', 10)]),
    Task('10:00', [Subtask('Team Meeting', 60)]),
    Task('11:30', [Subtask('Coffee Break', 15), Subtask('Casual Chat', 15)]),
    Task('14:00', [Subtask('Project Work', 120)]),
    Task('17:00', [Subtask('Evening Run', 30), Subtask('Stretching', 10)])
]

def plot_tasks():
    plt.figure(figsize=(10, 6))
    plt.ylabel('Tasks')
    plt.xlabel('Time of Day')
    colors = ['skyblue', 'lightgreen', 'salmon', 'gold', 'violet']
    
    for i, task in enumerate(tasks):
        start_num = (task.start_time - datetime.combine(task.start_time.date(), datetime.min.time())).total_seconds() / 3600
        end_num = (task.get_end_time() - datetime.combine(task.get_end_time().date(), datetime.min.time())).total_seconds() / 3600
        plt.barh(i, end_num - start_num, left=start_num, height=0.8, color=colors[i % len(colors)], edgecolor='blue')
        plt.text(start_num, i, f"{task.subtasks[0].description}...", horizontalalignment='left', verticalalignment='center')

    plt.xlim(6, 21)
    plt.xticks([i for i in range(6, 22)], [f"{i}:00" for i in range(6, 22)])
    plt.yticks(range(len(tasks)), [f"Task {i+1}" for i in reversed(range(len(tasks)))])
    plt.gca().invert_yaxis()  # Inverts the y-axis
    plt.grid(True)
    plt.tight_layout()
    plt.show()

plot_tasks()
