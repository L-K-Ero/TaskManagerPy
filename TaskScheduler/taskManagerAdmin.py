import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime

class TaskManagerAdmin:
    PASSWORD = "asdf123"  # Replace with your own secure password

    def __init__(self, root):
        self.root = root
        self.root.title("Task Manager Admin")

        self.login()

    def login(self):
        login_window = tk.Toplevel(self.root)
        login_window.title("Login")

        ttk.Label(login_window, text="Enter Password:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        password_var = tk.StringVar()
        ttk.Entry(login_window, textvariable=password_var, show="*").grid(row=0, column=1, padx=10, pady=5)
        ttk.Button(login_window, text="Login", command=lambda: self.authenticate(login_window, password_var.get())).grid(row=1, column=0, columnspan=2, pady=10)

    def authenticate(self, login_window, entered_password):
        if entered_password == self.PASSWORD:
            login_window.destroy()
            self.setup_ui()
        else:
            messagebox.showerror("Error", "Incorrect password. Please try again.")

    def setup_ui(self):
        self.tasks = self.load_tasks()

        self.task_title_var = tk.StringVar()
        self.task_time_var = tk.StringVar()

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.root, text="Task Title:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
        ttk.Entry(self.root, textvariable=self.task_title_var).grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(self.root, text="Task Time (HH:MM):").grid(row=1, column=0, padx=10, pady=5, sticky="e")
        ttk.Entry(self.root, textvariable=self.task_time_var).grid(row=1, column=1, padx=10, pady=5)

        ttk.Button(self.root, text="Add Task", command=self.add_task).grid(row=2, column=0, columnspan=2, pady=10)

        ttk.Label(self.root, text="Task ID to Remove:").grid(row=3, column=0, padx=10, pady=5, sticky="e")
        self.remove_id_var = tk.StringVar()
        ttk.Entry(self.root, textvariable=self.remove_id_var).grid(row=3, column=1, padx=10, pady=5)

        ttk.Button(self.root, text="Remove Task", command=self.remove_task).grid(row=4, column=0, columnspan=2, pady=10)

        # Listbox to display tasks
        self.task_listbox = tk.Listbox(self.root, selectmode=tk.SINGLE, height=10, width=40)
        self.task_listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        self.update_task_listbox()

    def update_task_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task in self.tasks:
            task_str = f"ID: {task['id']}, Title: {task['title']}, Time: {task['time']}"
            self.task_listbox.insert(tk.END, task_str)

    def add_task(self):
        title = self.task_title_var.get()
        time_str = self.task_time_var.get()

        if title and time_str:
            try:
                task_time = datetime.strptime(time_str, "%H:%M").time().strftime("%H:%M")
            except ValueError:
                messagebox.showerror("Error", "Invalid time format. Please use HH:MM.")
                return

            new_task = {"id": len(self.tasks) + 1, "title": title, "time": task_time}

            # Check for duplicates
            if any(task["title"] == new_task["title"] and task["time"] == new_task["time"] for task in self.tasks):
                messagebox.showerror("Error", "Duplicate task. Task not added.")
                return

            self.tasks.append(new_task)
            self.save_tasks()
            messagebox.showinfo("Success", "Task added successfully.")
            self.update_task_listbox()
            self.clear_fields()
        else:
            messagebox.showerror("Error", "Task title and time are required fields.")

    def remove_task(self):
        id_to_remove = self.remove_id_var.get()

        if id_to_remove:
            try:
                id_to_remove = int(id_to_remove)
            except ValueError:
                messagebox.showerror("Error", "Invalid ID. Please enter a valid integer ID.")
                return

            matching_tasks = [task for task in self.tasks if task["id"] == id_to_remove]

            if matching_tasks:
                self.tasks.remove(matching_tasks[0])
                self.save_tasks()
                messagebox.showinfo("Success", "Task removed successfully.")
                self.update_task_listbox()
                self.clear_fields()
            else:
                messagebox.showerror("Error", f"Task with ID {id_to_remove} not found.")
        else:
            messagebox.showerror("Error", "Task ID is required.")

    def clear_fields(self):
        self.task_title_var.set("")
        self.task_time_var.set("")
        self.remove_id_var.set("")

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as file:
                return json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_tasks(self):
        with open("tasks.json", "w") as file:
            json.dump(self.tasks, file, indent=2)

if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerAdmin(root)
    root.mainloop()

