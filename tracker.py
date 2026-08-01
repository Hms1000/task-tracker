
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
        return f"title: {self.title}, priority: {self.priority}, done: {self.done}"
        pass

    def __repr__(self):
        super().__str__()
        pass

    @property # creating a dictionary 
    def to_dict(self):
        base = f"title: {self.title}, priority: {self.priority}, done: {self.done}"
        return base
        
class Deadline(Task):  # deadline class
    def __init__(self, title, priority, done, due_date):
        super().__init__(title, priority, done)
        self.due_date = due_date

    def __str__(self):
        return super().__str__(self.due_date)

    @property
    def to_dict(self):
        base = super().to_dict()
        base["due_date"] = self.due_date
        return base

class Recurring(Task): # recurring class
    def __init__(self, title, priority, done, frequency):
        super().__init__(title, priority, done)
        self.frequency = frequency

    def __str__(self):
        return super().__str__(self.frequency)

    @property
    def to_dict(self):
        base = super().to_dict()
        base["frequency"] = self.frequency
        return base

class TaskManager(): # list of Tasks class 
    def __init__(self):
        self.tasks = []
        pass

    @property 
    def add_tasks(self, task):
        self.tasks.append(task)

    def __str__(self):
        return "List of Tasks"

    @property       # task dictionary list
    def to_dict_list(self):
        task_dic_list = []
        for task in self.tasks:
            task_dic_list.append(task.to_dict())
        return task_dic_list


def main():

    # command getting command line arguments 
    parser = argparse.ArgumentParser(description="task manager application")
    parser.add_argument("--list", action="store_value", help="list all tasks")
    parser.add_argument("--add", action="store_value", help="add task")
    parser.add_argument("--title", help="title of task")
    parser.add_argument("--priority", help="priority level of task e.g low")
    parser.add_argument("--done", bool, help="return 'True/False'")
    parser.add_argument("--due_date", help="last date")
    parser.add_argument("--frequency", help="the number a task is perfomed")

    args = parser.parse_args()

    # checking if the filename exists and if its not empty before reading the json file
    filename = "tracker.json"
    if os.path.exists(filename) and os.path.getsize(filename) != 0:
        with open(filename, "r") as f:
            task_dic_list = json.load(f)

    print(f"{filename} does not exist")


    # writing to a json file
    with open("filename", "w") as f:
        json.dump(task_dic_list, f)

if __name__=="__main__()":
    main()