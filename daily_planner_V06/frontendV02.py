import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import pandas as pd

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")

        self.tasks = []  # Data structure to hold all tasks
        self.current_task = None
        self.last_end_time = None

        # Task entry fields
        self.title_var = tk.StringVar()
        self.start_time_var = tk.StringVar()
        self.subtask_desc_var = tk.StringVar()
        self.duration_var = tk.StringVar()

        # Create UI elements
        tk.Label(root, text="Task Title:").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.title_var).grid(row=0, column=1)

        tk.Label(root, text="Start Time (HH:MM):").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.start_time_var).grid(row=1, column=1)

        tk.Label(root, text="Subtask Description:").grid(row=2, column=0)
        tk.Entry(root, textvariable=self.subtask_desc_var).grid(row=2, column=1)

        tk.Label(root, text="Duration (minutes):").grid(row=3, column=0)
        tk.Entry(root, textvariable=self.duration_var).grid(row=3, column=1)

        # Buttons
        tk.Button(root, text="Add Subtask", command=self.add_subtask).grid(row=4, column=0)
        tk.Button(root, text="Finish Task & Add New", command=self.finish_task).grid(row=4, column=1)
        tk.Button(root, text="Save to CSV", command=self.save_to_csv).grid(row=5, column=0, columnspan=2)

        # Treeview for displaying tasks
        self.tree = ttk.Treeview(root, columns=('Task Title', 'Start Time', 'Subtask Description', 'Duration', 'End Time'), show='headings')
        self.tree.grid(row=6, column=0, columnspan=2, sticky='nsew')
        self.tree.heading('Task Title', text='Task Title')
        self.tree.heading('Start Time', text='Start Time')
        self.tree.heading('Subtask Description', text='Subtask Description')
        self.tree.heading('Duration', text='Duration')
        self.tree.heading('End Time', text='End Time')

    def add_subtask(self):
        start_time = self.start_time_var.get()
        if not self.current_task or self.current_task != self.title_var.get():
            self.current_task = self.title_var.get()
            self.last_end_time = datetime.strptime(start_time, '%H:%M') if start_time else datetime.now()

        duration = int(self.duration_var.get())
        end_time = self.last_end_time + timedelta(minutes=duration)
        subtask = {
            'Task Title': self.current_task,
            'Start Time': self.last_end_time.strftime('%H:%M'),
            'Subtask Description': self.subtask_desc_var.get(),
            'Duration': duration
        }
        self.tasks.append(subtask)
        self.tree.insert('', 'end', values=(subtask['Task Title'], subtask['Start Time'], subtask['Subtask Description'], subtask['Duration'], end_time.strftime('%H:%M')))

        self.last_end_time = end_time  # Update last_end_time for the next subtask
        self.subtask_desc_var.set('')
        self.duration_var.set('')

    def finish_task(self):
        self.current_task = None
        self.title_var.set('')
        self.start_time_var.set('')
        self.subtask_desc_var.set('')
        self.duration_var.set('')

    def save_to_csv(self):
        if self.tasks:
            df = pd.DataFrame(self.tasks)
            df.to_csv('daily_planner_V06\planning.csv', index=False)
            messagebox.showinfo("Save Successful", "Tasks saved to CSV successfully!")
            self.tasks.clear()
            self.tree.delete(*self.tree.get_children())
        else:
            messagebox.showinfo("No Data", "No tasks to save.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
