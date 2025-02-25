import tkinter as tk
import time
import csv
from datetime import datetime, timedelta

# Global variables to store the start time, elapsed time, and running status
start_time = 0
running = False
elapsed_time = 0

# Function to start the stopwatch
def start():
    global start_time, running
    if not running:
        start_time = time.time() - elapsed_time  # Start from the last time (or 0 if new start)
        running = True
        update_time()  # Update the time immediately when starting the stopwatch

# Function to stop the stopwatch
def stop():
    global running, elapsed_time
    if running:
        elapsed_time = time.time() - start_time  # Calculate the elapsed time
        running = False

# Function to reset the stopwatch
def reset():
    global start_time, running, elapsed_time
    running = False
    elapsed_time = 0
    start_time = 0
    time_label.config(text="00:00:00")  # Reset the time display to 00:00:00

# Function to update the time on the label
def update_time():
    if running:
        current_time = time.time() - start_time  # Calculate elapsed time
        time_str = format_time(current_time)  # Format the time as hh:mm:ss
        time_label.config(text=time_str)  # Update the display
        time_label.after(1000, update_time)  # Update every second

# Function to format the time as hh:mm:ss (without milliseconds)
def format_time(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}"  # Format as hh:mm:ss

# Function to save the time to a CSV file
def save_time():
    global elapsed_time
    current_time = format_time(elapsed_time)
    current_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Replace this with your directory
    with open('C:/Users/aakas/OneDrive/Documents/stopwatch_times.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([current_date, current_time])
    
    # Display a message indicating that the time has been saved
    save_message.config(text=f"Saved: {current_date} - {current_time}")

# Function to show the total time recorded in the last N days
def show_last_n_days():
    try:
        # Ask the user to input the number of days
        n_days = int(n_days_entry.get())
        current_date = datetime.now()
        total_seconds = 0
        

        with open('C:/Users/aakas/OneDrive/Documents/stopwatch_times.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                # Parse the date from the CSV row
                entry_date = datetime.strptime(row[0], "%Y-%m-%d %H:%M:%S")
                # Check if the entry is within the last N days
                if current_date - entry_date <= timedelta(days=n_days):
                    # Convert the time from hh:mm:ss format to seconds
                    time_str = row[1]
                    hours, minutes, seconds = map(int, time_str.split(":"))
                    total_seconds += hours * 3600 + minutes * 60 + seconds

        # Convert the total time in seconds to hh:mm:ss format
        total_hours = int(total_seconds // 3600)
        total_minutes = int((total_seconds % 3600) // 60)
        total_seconds = int(total_seconds % 60)
        total_time = f"{total_hours:02}:{total_minutes:02}:{total_seconds:02}"
        
        # Display the result
        result_label.config(text=f"Total time worked in last {n_days} days: {total_time}")
    
    except ValueError:
        result_label.config(text="Please enter a valid number for N.")

# Create the main window
window = tk.Tk()
window.title("Stopwatch Application")
window.geometry("450x450")
window.config(bg="#212121")

# Label to display the time
time_label = tk.Label(window, text="00:00:00", font=("Helvetica", 40), bg="#212121", fg="white")
time_label.pack(pady=50)

# Button to start the stopwatch
start_button = tk.Button(window, text="Start", font=("Helvetica", 16), command=start, bg="#4CAF50", fg="white", width=10)
start_button.pack(pady=10)

# Button to stop the stopwatch
stop_button = tk.Button(window, text="Stop", font=("Helvetica", 16), command=stop, bg="#FF5722", fg="white", width=10)
stop_button.pack(pady=10)

# Button to reset the stopwatch
reset_button = tk.Button(window, text="Reset", font=("Helvetica", 16), command=reset, bg="#FFC107", fg="white", width=10)
reset_button.pack(pady=10)

# Button to save the time to CSV
save_button = tk.Button(window, text="Save", font=("Helvetica", 16), command=save_time, bg="#2196F3", fg="white", width=10)
save_button.pack(pady=10)

# Entry for inputting the number of days
n_days_label = tk.Label(window, text="Enter number of days:", font=("Helvetica", 12), bg="#212121", fg="white")
n_days_label.pack(pady=5)

n_days_entry = tk.Entry(window, font=("Helvetica", 14), bg="#424242", fg="white")
n_days_entry.pack(pady=5)

# Button to show the total time in last N days
show_button = tk.Button(window, text="Show Last N Days", font=("Helvetica", 16), command=show_last_n_days, bg="#9C27B0", fg="white", width=15)
show_button.pack(pady=10)

# Label to show the result for total time in last N days
result_label = tk.Label(window, text="", font=("Helvetica", 14), bg="#212121", fg="white")
result_label.pack(pady=20)

# Label to show save message
save_message = tk.Label(window, text="", font=("Helvetica", 12), bg="#212121", fg="white")
save_message.pack(pady=10)

# Run the main loop
window.mainloop()
