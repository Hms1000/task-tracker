import os
import json
import argparse

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

    def add_tasks(self, task):
        self.tasks.append(task)

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
    parser.add_argument("--filter", help="filter tasks")
    parser.add_argument("--priority", help="priority level of task e.g low")
    parser.add_argument("--done", action="store_true", help="return 'True/False'")
    parser.add_argument("--due_date", help="last date")
    parser.add_argument("--frequency", help="the number a task is perfomed")

    args = parser.parse_args()

    # checking if the filename exists and if its not empty before reading the json file
    filename = "tracker.json"
    if os.path.exists(filename) and os.path.getsize(filename) != 0:
        with open(filename, "r") as f:
            task_dic_list = json.load(f)

    else:
        task_dic_list = []

     # rebuilding every saved task into a real object
    for d in task_dic_list:
        if "due_date" in d:
            rebuilt = Deadline(d["title"], d["priority"], d["done"], d["due_date"])
        elif "frequency" in d:
            rebuilt = Recurring(d["title"], d["priority"], d["done"], d["frequency"])
        else:
            rebuilt = Task(d["title"], d["priority"], d["done"])
        manager.tasks.append(rebuilt)

    # what the user asks for
    if args.add:
        if args.due_date:
            new_task = Deadline(args.title, args.priority, args.done, args.due_date)
        elif args.frequency:
            new_task = Recurring(args.title, args.priority, args.done, args.frequency)
        else:
            new_task = Task(args.title, args.priority, args.done)

        manager.tasks.append(new_task)

        updated_data = manager.to_dict_list()
        with open(filename, "w") as f:
            json.dump(updated_data, f)
        print("Task Added")
            
    
if __name__=="__main__":
    main()