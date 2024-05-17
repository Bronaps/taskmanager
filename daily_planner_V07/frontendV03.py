import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pandas as pd

class TaskManagerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager CSV Editor")

        self.tree = ttk.Treeview(root, columns=('Task Title', 'Start Time', 'Subtask Description', 'Duration'), show='headings', height=15)
        self.tree.grid(row=0, column=0, columnspan=4, sticky='nsew')
        self.tree.heading('Task Title', text='Task Title')
        self.tree.heading('Start Time', text='Start Time')
        self.tree.heading('Subtask Description', text='Subtask Description')
        self.tree.heading('Duration', text='Duration')
        self.tree.bind('<Double-1>', self.on_double_click)

        ttk.Button(root, text="Load CSV", command=self.load_csv).grid(row=1, column=0)
        ttk.Button(root, text="Save to CSV", command=self.save_to_csv).grid(row=1, column=1)
        ttk.Button(root, text="Add Task", command=self.add_task).grid(row=1, column=2)
        ttk.Button(root, text="Delete Task", command=self.delete_task).grid(row=1, column=3)

        self.editing_cell = None

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
        self.entry = tk.Entry(self.tree, width=width)
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

    def add_task(self):
        self.tree.insert('', 'end', values=("Enter Task Title", "Start Time", "Description", "Duration"))

    def delete_task(self):
        selected_item = self.tree.selection()
        if selected_item:
            self.tree.delete(selected_item)

    def load_csv(self):
        """Load tasks from a CSV file."""
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if file_path:
            df = pd.read_csv(file_path)
            self.clear_treeview()
            for index, row in df.iterrows():
                self.tree.insert('', 'end', values=(row['Task Title'], row['Start Time'], row['Subtask Description'], row['Duration']))

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

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerGUI(root)
    root.mainloop()
