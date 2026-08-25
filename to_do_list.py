import os
import csv
import sys

class Task:
    def __init__(self, title, priority='Medium', done=False):
        self.title = title
        self.priority = priority
        if isinstance(done, str):
            self.done = done.lower() in ['1', 'true', 'yes']
        else:
            self.done = bool(done)

class TodoList:
    def __init__(self):
        self.file_name = 'todo.csv'
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        if os.path.exists(self.file_name):
            with open(self.file_name, mode='r', encoding='utf-8') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) >= 3:
                        title, priority, done = row[0], row[1], row[2]
                        task = Task(title, priority, done)
                        self.tasks.append(task)

    def save_tasks(self):
        with open(self.file_name, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            for task in self.tasks:
                done_val = 1 if task.done else 0
                writer.writerow([task.title, task.priority, done_val])

    def create_task(self, title, priority='Medium', done=False):
        new_task = Task(title, priority, done)
        self.tasks.append(new_task)
        self.save_tasks()
        print(f'Task "{title}" created successfully.')

    def list_tasks(self):
        if not self.tasks:
            print("No tasks found.")
            return

        print("Task List:")
        print("{:<6} {:<15} {:<10} {:<10}".format("Index", "Title", "Priority", "Done"))
        
        for index, task in enumerate(self.tasks, start=1):
            done_val = 1 if task.done else 0
            print("{:<6} {:<15} {:<10} {:<10}".format(index, task.title, task.priority, done_val))
    
    def update_task(self, title, field, edit):
        for task in self.tasks:
            if task.title == title:
                if field == 'title':
                    task.title = edit
                elif field == 'priority':
                    task.priority = edit
                elif field == 'done':
                    task.done = edit.lower() in ['1', 'true', 'yes']
                else:
                    print("Invalid field.")
                    return
                self.save_tasks()
                print(f'Task "{title}" updated successfully.')
                return
        print("Invalid title.")

    def delete_task(self, title):
        for task in self.tasks:
            if task.title == title:
                self.tasks.remove(task)
                self.save_tasks()
                print(f'Task "{title}" deleted successfully.')
                return
        print("Invalid title.")
    
    def clear_list(self):
        self.tasks.clear()
        self.save_tasks()
        print("To-do list cleared successfully.")

    def get_task(self, title):
        for task in self.tasks:
            if task.title == title:
                done_val = 1 if task.done else 0
                print("{:<15} {:<10} {:<10}".format("Title", "Priority", "Done"))
                print("{:<15} {:<10} {:<10}".format(task.title, task.priority, done_val))
                return


def main():
    if len(sys.argv) < 2:
        print("Invalid command.")
        return
    todo = TodoList()
    command = sys.argv[1].lower()

    if command == 'create':
        if len(sys.argv) < 3:
            print("Invalid command.")
            return
            
        title = sys.argv[2]
        priority = 'Medium'
        done = False

        if len(sys.argv) >= 4:
            priority = sys.argv[3]
            
        if len(sys.argv) >= 5:
            done = sys.argv[4]

        todo.create_task(title, priority, done)

    elif command == 'list':
        todo.list_tasks()

    elif command == 'update':
        if len(sys.argv) < 5:
            print("Invalid command.")
            return
        title = sys.argv[2]
        field = sys.argv[3]
        edit = sys.argv[4]
        todo.update_task(title, field, edit)

    elif command == 'delete':
        if len(sys.argv) < 3:
            print("Invalid command.")
            return
        title = sys.argv[2]
        todo.delete_task(title)

    elif command == 'clear':
        todo.clear_list()

    elif command == 'search':
        if len(sys.argv) < 3:
            print("Invalid command.")
            return
        title = sys.argv[2]
        todo.get_task(title)

    else:
        print("Invalid command.")

if __name__ == "__main__":
    main()