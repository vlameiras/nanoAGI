from typing import List, Optional

class Task:
    def __init__(self, task_id: str, task_description: str):
        self.task_id = task_id
        self.task_description = task_description

class SimpleTaskManagerAgent:
    def __init__(self):
        self.task_list = []

    def add_tasks(self, tasks: List[Task]) -> None:
        self.task_list.extend(tasks)

    def get_next_task(self) -> Optional[Task]:
        if len(self.task_list) == 0:
            return None
        return self.task_list.pop(0)

class SimpleTaskExecutorAgent:
    def process_task(self, task: Task) -> str:
        # Execute the task and return the result
        # This is a placeholder for the actual task execution logic
        task_result = f"Result for {task.task_description}"
        return task_result


# Initialize and configure simplified agents for the MVP
task_manager_agent = SimpleTaskManagerAgent()
task_executor_agent = SimpleTaskExecutorAgent()

# Define a list of sample tasks for the MVP
sample_tasks = [
    Task("t1", "Perform task A"),
    Task("t2", "Perform task B"),
    Task("t3", "Perform task C"),
]

# Add the sample tasks to the task manager agent
task_manager_agent.add_tasks(sample_tasks)

# Main loop for the MVP system operation
while True:
    # Task Manager Agent gets the next task in the task list
    current_task = task_manager_agent.get_next_task()

    # If there are no more tasks, break the loop and terminate the system
    if current_task is None:
        break

    # Task Executor Agent processes the current task
    task_result = task_executor_agent.process_task(current_task)

    # Optional: Store the task result or perform further actions based on the result
    print(f"Task {current_task.task_id} completed with result: {task_result}")

# System termination
print("All tasks completed.")
