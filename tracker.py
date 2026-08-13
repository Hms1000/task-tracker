import sqlite3, argparse

# task base class
class Task:
    def __init__(self, title, priority, done):
        self. title = title
        self.priority = priority
        self.done = done
        pass

    def __str__(self): # printing the string
        return f"{self.title} {self.priority} {self.done}"
        pass

    def __repr__(self):
        return self.__str__()
        pass
    
    # creating a dictionary 
    def to_dict(self):
        return {
            "title": self.title,
            "priority": self.priority,
            "done": self.done
        }
        
class Deadline(Task):  # deadline class
    def __init__(self, title, priority, done, due_date):
        super().__init__(title, priority, done)
        self.due_date = due_date

    def __str__(self):
        return f"{self.title} {self.priority} {self.done} {self.due_date}"

    def to_dict(self):
        base = super().to_dict()
        base["due_date"] = self.due_date
        return base

    def __repr__(self):
        return super().__repr__()
    
class Recurring(Task): # recurring class
    def __init__(self, title, priority, done, frequency):
        super().__init__(title, priority, done)
        self.frequency = frequency

    def __str__(self):
        return f"{self.title} {self.priority} {self.done} {self.frequency}"

    def to_dict(self):
        base = super().to_dict()
        base["frequency"] = self.frequency
        return base
class TaskManager(): # list of Tasks class 
    def __init__(self):
        self.tasks = []
        pass

    def add_tasks(self, task): #add a task to the list only if it doesn't exist
        for t in self.tasks:
            if t.title == task.title:
                print(f"{task.title} already in the list")
                return False
        else:
            self.tasks.append(task)
            return True
        

    def __str__(self):
        return "List of Tasks"

     # task dictionary list
    def to_dict_list(self):
        task_dic_list = []
        for task in self.tasks:
            task_dic_list.append(task.to_dict())
        return task_dic_list


def main():

    manager = TaskManager()

    # command getting command line arguments 
    parser = argparse.ArgumentParser(description="task manager application")
    parser.add_argument("--list", action="store_true", help="list all tasks")
    parser.add_argument("--add", action="store_true", help="add task")
    parser.add_argument("--title", help="title of task")
    parser.add_argument("--filter", help="filter by priority")
    parser.add_argument("--priority", help="priority level of task e.g low")
    parser.add_argument("--done", action="store_true", help="return 'True/False'")
    parser.add_argument("--due_date", help="last date")
    parser.add_argument("--frequency", help="the number a task is perfomed")

    args = parser.parse_args()

    with sqlite3.connect("tracker.db") as conn:
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        # creating a database table
        cursor.execute(""" 
            CREATE TABLE IF NOT EXISTS tasks (
                title TEXT UNIQUE,
                priority TEXT,
                done BOOLEAN,
                due_date TEXT,
                frequency TEXT
            )
        """)
        conn.commit()

        cursor.execute("SELECT * FROM tasks") # selecting tasks to print
        rows = cursor.fetchall()

        for row in rows:
            title = row["title"]
            priority = row["priority"]
            done = row["done"]
            due_date = row["due_date"]
            frequency = row["frequency"]

            if due_date is not None:
                rebuilt = Deadline(title, priority, done, due_date)
            elif frequency is not None:
                rebuilt = Recurring(title, priority, done, frequency)
            else:
                rebuilt = Task(title, priority, done)

            manager.add_tasks(rebuilt)
    
        # what the user asks for
        if args.add:
            if args.due_date:
                new_task = Deadline(args.title, args.priority, args.done, args.due_date)
            elif args.frequency:
                new_task = Recurring(args.title, args.priority, args.done, args.frequency)
            else:
                new_task = Task(args.title, args.priority, args.done)

            added = manager.add_tasks(new_task)
            if added:
                due_date_value = getattr(new_task, "due_date", None)
                frequency_value = getattr(new_task, "frequency", None)

                cursor.execute(
                    "INSERT INTO tasks (title, priority, done, due_date, frequency) VALUES (?, ?, ?, ?, ?)",
                    (new_task.title, new_task.priority, new_task.done, due_date_value, frequency_value)
                )
                conn.commit()
                print("Task Added")

        if args.filter: # filtering by priority
            for task in manager.tasks:
                if task.priority == args.filter:
                    print(task)            

if __name__=="__main__":
    main()