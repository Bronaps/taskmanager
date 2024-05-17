import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# List to hold our tasks with start time, duration, and description
daily_tasks = []

def add_task(start_time, duration, task_description, is_quick_task=False):
    """Adds a task to the daily schedule."""
    start_datetime = datetime.strptime(start_time, '%H:%M')
    end_datetime = start_datetime + timedelta(minutes=duration)
    daily_tasks.append((task_description, start_datetime, end_datetime, is_quick_task))

def plot_daily_tasks():
    """Plots tasks using rectangles of different colors to enhance visibility."""
    # Create figure and plot settings
    plt.figure(figsize=(6, 6))  # Adjust figure size
    plt.xlabel('Tasks')
    plt.ylabel('Time of Day')

    # Define a list of colors for the tasks
    colors = ['skyblue', 'lightgreen', 'salmon', 'gold', 'violet']

    # Calculate the horizontal position for the task
    x_pos = 1  # Single x position for all tasks

    # Plot each task as a rectangle with different colors
    for i, (desc, start, end, quick) in enumerate(daily_tasks):
        # Convert datetimes to float hours for plotting
        start_num = (start - datetime.combine(start.date(), datetime.min.time())).total_seconds() / 3600
        end_num = (end - datetime.combine(end.date(), datetime.min.time())).total_seconds() / 3600
        color = colors[i % len(colors)]  # Cycle through colors list
        plt.barh((start_num + end_num) / 2, width=0.8, height=end_num - start_num, left=x_pos - 0.4, align='center',
                 color=color, edgecolor='blue', label=f"{desc} ({'Quick' if quick else 'Normal'})")
        plt.text(x_pos, start_num, desc, horizontalalignment='center', verticalalignment='bottom')

    # Enhance y-axis to display time
    plt.ylim(6, 21)  # Limiting y-axis from 6 AM to 9 PM
    plt.yticks([i for i in range(6, 22)], [f"{i}:00" for i in range(6, 22)])  # Hourly ticks from 6 AM to 9 PM

    plt.xticks([x_pos], ["Tasks"])  # Simplified x-axis
    plt.grid(True)  # Enable grid
    plt.legend(loc='upper right', bbox_to_anchor=(1, 1.1))  # Place legend to the right of the plot
    plt.tight_layout()
    plt.show()

# Example tasks
add_task('09:00', 30, 'Emails')
add_task('09:30', 60, 'Team Meeting')
add_task('10:30', 15, 'Coffee Break', True)
add_task('10:45', 45, 'Project Work')
add_task('18:00', 30, 'Evening Run')

# Plotting the tasks
plot_daily_tasks()
