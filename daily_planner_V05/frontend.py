import tkinter as tk
from tkinter import messagebox, simpledialog
import pandas as pd

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager")
        
        # Data structure to hold all tasks
        self.tasks = []
        
        # Task entry fields
        self.title_var = tk.StringVar()
        self.start_time_var = tk.StringVar()
        self.subtask_desc_var = tk.StringVar()
        self.duration_var = tk.StringVar()

        # Task Title
        tk.Label(root, text="Task Title:").grid(row=0, column=0)
        tk.Entry(root, textvariable=self.title_var).grid(row=0, column=1)
        
        # Start Time
        tk.Label(root, text="Start Time (HH:MM):").grid(row=1, column=0)
        tk.Entry(root, textvariable=self.start_time_var).grid(row=1, column=1)
        
        # Subtask Description
        tk.Label(root, text="Subtask Description:").grid(row=2, column=0)
        tk.Entry(root, textvariable=self.subtask_desc_var).grid(row=2, column=1)
        
        # Duration
        tk.Label(root, text="Duration (minutes):").grid(row=3, column=0)
        tk.Entry(root, textvariable=self.duration_var).grid(row=3, column=1)
        
        # Buttons
        tk.Button(root, text="Add Subtask", command=self.add_subtask).grid(row=4, column=0)
        tk.Button(root, text="Finish Task & Add New", command=self.finish_task).grid(row=4, column=1)
        tk.Button(root, text="Save to CSV", command=self.save_to_csv).grid(row=5, column=0, columnspan=2)

        # Display area
        self.display = tk.Text(root, height=10, width=50)
        self.display.grid(row=6, column=0, columnspan=2)
        self.display.insert(tk.END, "Tasks will appear here.\n")

    def add_subtask(self):
        subtask = {
            'Task Title': self.title_var.get(),
            'Start Time': self.start_time_var.get(),
            'Subtask Description': self.subtask_desc_var.get(),
            'Duration': self.duration_var.get()
        }
        self.tasks.append(subtask)
        self.display.insert(tk.END, f"Added subtask: {subtask['Subtask Description']} for task {subtask['Task Title']}\n")
            # Clear subtask description and duration fields after adding a subtask
        self.subtask_desc_var.set('')
        self.duration_var.set('')

    def finish_task(self):
        self.title_var.set('')
        self.start_time_var.set('')
        self.subtask_desc_var.set('')
        self.duration_var.set('')
        self.display.insert(tk.END, "Finished current task, ready for a new task.\n")
    
    def save_to_csv(self):
        if self.tasks:
            df = pd.DataFrame(self.tasks)
            df.to_csv('tasks.csv', index=False)
            messagebox.showinfo("Save Successful", "Tasks saved to CSV successfully!")
            self.tasks = []  # Clear tasks after saving
            self.display.insert(tk.END, "Tasks saved and cleared.\n")
        else:
            messagebox.showinfo("No Data", "No tasks to save!")

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
