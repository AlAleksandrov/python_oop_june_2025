from project.task import Task


class Section:
    def __init__(self, name:str):
        self.name = name
        self.tasks:list = []

    def add_task(self, new_task: Task) -> str:
        if new_task in self.tasks:
            return f"Task is already in the section {self.name}"
        self.tasks.append(new_task)
        return f"Task {new_task.details()} is added to the section"

    def complete_task(self, task_name: str) -> str:
        t = next((t for t in self.tasks if task_name == t.name),None)
        if t:
            t.completed = True
            return f"Completed task {task_name}"
        return f"Could not find task with the name {task_name}"

    def clean_section(self) -> str:
        len_curr_tasks = len(self.tasks)
        self.tasks = [t for t in self.tasks if not t.completed]
        return f"Cleared {len_curr_tasks - len(self.tasks)} tasks."

    def view_section(self) -> str:
        task_details = '\n'.join(t.details() for t in self.tasks)
        return f"Section {self.name}:\n{task_details}"