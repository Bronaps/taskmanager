import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime, timedelta
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
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

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager CSV Editor with Plotting")
        self.root.configure(bg='white')

        style = ttk.Style()
        style.configure("Treeview", font=('Arial', 12), rowheight=25)
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))

        self.tree = ttk.Treeview(root, columns=('Task Title', 'Start Time', 'Subtask Description', 'Duration'), show='headings', height=15)
        self.tree.grid(row=0, column=0, columnspan=4, sticky='nsew', padx=10, pady=10)
        self.tree.heading('Task Title', text='Task Title')
        self.tree.heading('Start Time', text='Start Time')
        self.tree.heading('Subtask Description', text='Subtask Description')
        self.tree.heading('Duration', text='Duration')
        self.tree.column('Task Title', width=200)
        self.tree.column('Start Time', width=100)
        self.tree.column('Subtask Description', width=200)
        self.tree.column('Duration', width=100)
        self.tree.bind('<Double-1>', self.on_double_click)

        button_frame = ttk.Frame(root, padding=10)
        button_frame.grid(row=1, column=0, columnspan=4, sticky='nsew')
        ttk.Button(button_frame, text="Load CSV", command=self.load_csv).grid(row=0, column=0, padx=5)
        ttk.Button(button_frame, text="Save to CSV", command=self.save_to_csv).grid(row=0, column=1, padx=5)
        ttk.Button(button_frame, text="Add Task", command=self.add_task).grid(row=0, column=2, padx=5)
        ttk.Button(button_frame, text="Add Subtask", command=self.add_subtask).grid(row=0, column=3, padx=5)  # Add Subtask Button
        ttk.Button(button_frame, text="Delete Task", command=self.delete_task).grid(row=0, column=4, padx=5)

        self.editing_cell = None

        # Create a frame for the plot
        self.plot_frame = ttk.Frame(root, padding=10)
        self.plot_frame.grid(row=0, column=10, rowspan=5, sticky='nsew', padx=10, pady=10)

        # Initialize the plot
        self.figure = plt.Figure(figsize=(17, 12), dpi=110)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

    def on_double_click(self, event):
        """Handle double-click to enable cell editing."""
        region = self.tree.identify("region", event.x, event.y)
        if region == "cell":
            column = self.tree.identify_column(event.x)
            item = self.tree.selection()[0]
            self.editing_cell = (item, column)
            value = self.tree.item(item, 'values')[int(column[1:]) - 1]
            self.edit_cell(item, column, value)

    def edit_cell(self, item, column, value):
        """Edit the content of a cell in place."""
        x, y, width, height = self.tree.bbox(item, column)
        self.entry = tk.Entry(self.tree, font=('Arial', 12))
        self.entry.place(x=x, y=y, width=width, height=height)
        self.entry.insert(0, value)
        self.entry.icursor(tk.END)  # Move cursor to the end of the text
        self.entry.focus()
        self.entry.bind("<Return>", self.save_edit)
        self.entry.bind("<FocusOut>", self.save_edit)

    def save_edit(self, event):
        """Save the edited value back to the treeview and move to the next column."""
        if self.editing_cell:
            item, column = self.editing_cell
            new_value = self.entry.get()
            self.tree.set(item, column, new_value)
            self.entry.destroy()
            self.editing_cell = None
            self.update_plot()

    def add_task(self):
        self.tree.insert('', 'end', values=("Enter Task Title", "Start Time", "Description", "Duration"))
        self.update_plot()

    def add_subtask(self):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item)['values']
            task_title, start_time, _, duration = item_values
            start_datetime = datetime.strptime(start_time, '%H:%M')
            end_datetime = start_datetime + timedelta(minutes=int(duration))
            self.tree.insert('', 'end', values=(task_title, end_datetime.strftime('%H:%M'), "Enter Description", "0"))
            self.update_plot()

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)
            self.update_plot()

    def load_csv(self):
        """Load tasks from a CSV file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            df = pd.read_csv(file_path)
            self.clear_treeview()
            for index, row in df.iterrows():
                self.tree.insert('', 'end', values=(row['Task Title'], row['Start Time'], row['Subtask Description'], row['Duration']))
            self.update_plot()

    def save_to_csv(self):
        """Save tasks to a CSV file."""
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            tasks = [self.tree.item(item)['values'] for item in self.tree.get_children()]
            df = pd.DataFrame(tasks, columns=['Task Title', 'Start Time', 'Subtask Description', 'Duration'])
            df.to_csv(file_path, index=False)
            messagebox.showinfo("Success", "Data saved to CSV!")

    def clear_treeview(self):
        """Clear all items from the Treeview."""
        for item in self.tree.get_children():
            self.tree.delete(item)

    def update_plot(self):
        """Update the plot based on the current tasks in the Treeview."""
        self.ax.clear()
        
        tasks = [self.tree.item(item)['values'] for item in self.tree.get_children()]
        if not tasks:
            self.canvas.draw()
            return
        
        # Process tasks into Task and Subtask classes
        df = pd.DataFrame(tasks, columns=['Task Title', 'Start Time', 'Subtask Description', 'Duration'])
        task_dict = {}
        for _, row in df.iterrows():
            task_title = row['Task Title']
            if task_title not in task_dict:
                task_dict[task_title] = Task(task_title, row['Start Time'])
            task_dict[task_title].add_subtask(Subtask(row['Subtask Description'], row['Duration']))
        task_list = list(task_dict.values())

        # Plot tasks
        self.plot_tasks(task_list)
        self.canvas.draw()

    def plot_tasks(self, tasks):
        self.ax.clear()
        base_colors = ['skyblue', 'lightgreen', 'salmon', 'gold', 'violet']
        for i, task in enumerate(sorted(tasks, key=lambda x: x.start_time)):
            start = task.start_time
            color = base_colors[i % len(base_colors)]
            for j, subtask in enumerate(task.subtasks):
                shade = adjust_lightness(color, 1 + j * 0.05)
                start_num = (start - datetime.combine(start.date(), datetime.min.time())).total_seconds() / 3600
                end_num = (start + timedelta(minutes=subtask.duration) - datetime.combine(start.date(), datetime.min.time())).total_seconds() / 3600
                self.ax.barh(i, end_num - start_num, left=start_num, height=0.8, color=shade, edgecolor='white')
                self.ax.text(start_num, i, f"{subtask.description}", horizontalalignment='left', verticalalignment='center', rotation=270,size= 'xx-large' if subtask.duration > 60 else 'x-small')
                start += timedelta(minutes=subtask.duration)
        self.ax.set_xlim(0, 24)
        self.ax.set_xticks(np.arange(0, 24, 1))
        self.ax.set_xticklabels([f"{h}:00" for h in np.arange(0, 24, 1)])
        self.ax.set_yticks(range(len(tasks)))
        self.ax.set_yticklabels([task.title for task in tasks])
        self.ax.invert_yaxis()
        self.ax.grid(True, which='both', linestyle='solid', linewidth=0.5)
        self.figure.tight_layout()

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
