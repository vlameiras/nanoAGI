from collections import deque
import os
from typing import Dict, List
from langchain.vectorstores import FAISS
from langchain.docstore import InMemoryDocstore
from langchain.embeddings import OpenAIEmbeddings
import faiss
from chains import TaskCreationChain,TaskExecutionChain, TaskPriorityChain, TaskTodoChain
from tasks import Task

# Define your embedding model
embeddings_model = OpenAIEmbeddings()
# Initialize the vectorstore as empty
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model.embed_query, index, InMemoryDocstore({}), {})

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if OPENAI_API_KEY is None:
    raise ValueError("OPENAI_API_KEY environment variable not set")
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
if PINECONE_API_KEY is None:
    raise ValueError("PINECONE_API_KEY environment variable not set")

# implement get_next_task
# def get_next_task(task_creation_chain, result, objective):
#     new_task = task_creation_chain.create_task(result, objective)
#     return new_task

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
    new_tasks = response.split("\n")
    prioritized_task_list = []
    for task_string in new_tasks:
        if not task_string.strip():
            continue
        task_parts = task_string.strip().split(".", 1)
        if len(task_parts) == 2:
            task_id = task_parts[0].strip()
            task_name = task_parts[1].strip()
            prioritized_task_list.append(Task(task_id, task_name, task_name))
    return prioritized_task_list


# main
if __name__ == "__main__":
    OBJECTIVE = "Build a hello world Flask application."

    task_creation_chain = TaskCreationChain("task_creation")
    task_priority_chain = TaskPriorityChain("task_priority")
    task_todo_chain = TaskTodoChain("task_todo")
    task_execution_chain = TaskExecutionChain("task_execution", task_todo_chain.chain.llm_chain)
 
    tasks = deque()
    tasks.append(Task("1", "todo list", "Make a concise todo list"))

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

        task_result = task_execution_chain.execute_task(OBJECTIVE, current_task, vectorstore)
        vectorstore.add_texts(
            texts=[task_result],
            metadatas=[{"task": current_task.task_name}],
            ids=[current_task.task_id],
        )

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
