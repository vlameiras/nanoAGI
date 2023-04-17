from collections import deque
import os
import sys
from typing import Dict, List
import pinecone
from chains import TaskCreationChain,TaskExecutionChain, TaskPriorityChain, TaskTodoChain
from tasks import Task


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY environment variable not set")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if PINECONE_API_KEY is None:
    raise ValueError("PINECONE_API_KEY environment variable not set")

pinecone.init(api_key=PINECONE_API_KEY, environment="us-east4-gcp")

# Create Pinecone index
table_name = "test-index"
dimension = 1536
metric = "cosine"
pod_type = "s1.x1"
if table_name not in pinecone.list_indexes():
    pinecone.create_index(
        table_name, dimension=dimension, metric=metric, pod_type=pod_type
    )

# Connect to the index
index = pinecone.Index(table_name)

def get_next_task(
    task_creation_chain: TaskCreationChain,
    result: str,
    task_description: str,
    task_list: List[Task],
    objective: str,
) -> List[Dict]:
    """Get the next task."""
    incomplete_tasks = [t.task_name for t in task_list]
    response = task_creation_chain.chain.llm_chain.run(
        result=result,
        task_description=task_description,
        incomplete_tasks=incomplete_tasks,
        objective=objective,
    )
    new_tasks = response.split("\n")
    new_tasks = [{"task_description": task_description, "task_name": task_description} for task_description in new_tasks if task_description.strip()]
    return new_tasks


def prioritize_tasks(
    task_prioritization_chain: TaskPriorityChain,
    this_task_id: int,
    task_list: List[Task],
    objective: str,
) -> List[Dict]:
    """Prioritize tasks."""
    task_names = [t.task_name for t in task_list]
    next_task_id = int(this_task_id) + 1
    response = task_prioritization_chain.chain.llm_chain.run(
        task_names=task_names, next_task_id=next_task_id, objective=objective
    )
    new_tasks = [t for t in response.split("\n") if t.strip()]
    prioritized_task_list = [
        Task(task_id, task_name, task_name)
        for task_id, task_name in [
            task_string.strip().split(".", maxsplit=1)
            for task_string in new_tasks
        ]
    ]
    return prioritized_task_list

# main
if __name__ == "__main__":
    # get objective from python argument sys argv
    # check if sys.argv is not None else default to "What is the current situation in the United States?"
    OBJECTIVE = sys.argv[1] if len(sys.argv) > 1 else "What is the current situation in the United States?"
    print("Objective: ", OBJECTIVE)

    task_creation_chain = TaskCreationChain("task_creation")
    task_priority_chain = TaskPriorityChain("task_priority")
    task_todo_chain = TaskTodoChain("task_todo")
    task_execution_agent= TaskExecutionChain("task_execution", task_todo_chain.chain.llm_chain)
 
    tasks = deque()
    tasks.append(Task("1", "todo list", "build a todo list"))

    # counter for task ids
    task_id_counter = 1
    while True:
        current_task = tasks.popleft()
        print("Current task: ", current_task.task_id, current_task.task_name)
        # print list of tasks left, one per line
        print("Tasks left:")
        for task in tasks:
            print(task.task_name)

        # print number of tasks left
        print("Number of tasks left: ", len(tasks))   
        print("------------------")
        if current_task is None:
            break

        task_result = task_execution_agent.execute_task(OBJECTIVE, current_task, index)

        new_tasks = get_next_task(task_creation_chain=task_creation_chain, result=task_result, 
                                  task_description=current_task.task_description, task_list=tasks, objective=OBJECTIVE)

        for new_task in new_tasks:        
            new_task.update({"task_id": task_id_counter + 1})
            tasks.append(Task(**new_task))
            
        tasks = deque(
        prioritize_tasks(
            task_priority_chain,
            task_id_counter,
            list(tasks),
            OBJECTIVE,
        ))
        
    # System termination
    print("All tasks completed.")
