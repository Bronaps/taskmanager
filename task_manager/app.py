from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mc
import colorsys
from datetime import datetime, timedelta
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

UPLOAD_FOLDER = os.path.join(app.root_path, 'uploads')
PLOT_FOLDER = os.path.join(app.root_path, 'static', 'plots')

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
if not os.path.exists(PLOT_FOLDER):
    os.makedirs(PLOT_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PLOT_FOLDER'] = PLOT_FOLDER

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file:
        filename = os.path.join(app.config['UPLOAD_FOLDER'], 'tasks.csv')
        file.save(filename)
        return redirect(url_for('display_tasks'))

@app.route('/tasks', methods=['GET', 'POST'])
def display_tasks():
    if request.method == 'POST':
        data = request.json
        df = pd.DataFrame(data)
        df.to_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'tasks.csv'), index=False)
        return jsonify({'status': 'success'})

    tasks = load_tasks_from_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'tasks.csv'))
    return render_template('tasks.html', tasks=tasks)

@app.route('/plot')
def plot_tasks():
    tasks = load_tasks_from_csv(os.path.join(app.config['UPLOAD_FOLDER'], 'tasks.csv'))

    if not tasks:
        return "No tasks to plot", 400

    plt.figure(figsize=(20, 11))
    plt.ylabel('Tasks')
    plt.xlabel('Time of Day')
    base_colors = ['skyblue', 'lightgreen', 'salmon', 'gold', 'violet']

    # Determine the time range for the x-axis based on task times
    min_time = 24
    max_time = 0
    for task in tasks:
        start_time_num = (task.start_time - datetime.combine(task.start_time.date(), datetime.min.time())).total_seconds() / 3600
        end_time_num = start_time_num + sum(subtask.duration for subtask in task.subtasks) / 60
        if start_time_num < min_time:
            min_time = start_time_num
        if end_time_num > max_time:
            max_time = end_time_num

    # Add some padding to the time range
    time_padding = 0.5
    min_time = max(0, min_time)
    max_time = min(24, max_time + time_padding)

    print(f"Plotting tasks from {min_time} to {max_time} hours")

    for i, task in enumerate(sorted(tasks, key=lambda x: x.start_time)):
        start = task.start_time
        color = base_colors[i % len(base_colors)]
        for j, subtask in enumerate(task.subtasks):
            shade = adjust_lightness(color, 1 + j * 0.075)
            start_num = (start - datetime.combine(start.date(), datetime.min.time())).total_seconds() / 3600
            end_num = (start + timedelta(minutes=subtask.duration) - datetime.combine(start.date(), datetime.min.time())).total_seconds() / 3600
            plt.barh(i, end_num - start_num, left=start_num, height=0.8, color=shade, edgecolor='white', linewidth=0.5)
            if subtask.duration >= 60:
                sized = 'large'
            elif subtask.duration >= 30:
                sized = 'medium'
            elif subtask.duration >= 15:
                sized = 'small'
            else:
                sized = 'x-small'
            plt.text(start_num, i, f"{subtask.description}", horizontalalignment='left', verticalalignment='center', rotation=270, size=sized)
            start += timedelta(minutes=subtask.duration)

    plt.xlim(min_time, max_time)
    plt.xticks(np.arange(np.floor(min_time), np.ceil(max_time) + 1, 1), [f"{int(h)}:00" for h in np.arange(np.floor(min_time), np.ceil(max_time) + 1, 1)])
    plt.yticks(range(len(tasks)), [task.title for task in tasks])
    plt.gca().invert_yaxis()
    plt.grid(True, which='both', linestyle='--', linewidth=0.25)
    plt.tight_layout()

    plot_filename = os.path.join(app.config['PLOT_FOLDER'], 'plot.png')
    try:
        plt.savefig(plot_filename)
    except Exception as e:
        print(f"Error saving plot: {e}")
        return str(e), 500
    finally:
        plt.close()  # Close the figure to prevent memory leaks
    return send_file(plot_filename, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
