from collections import deque
from typing import List


class Task:
    def __init__(self, task_id: str, task_name: str, task_description: str):
        self.task_id = task_id
        self.task_description = task_description
        self.task_name = task_name

def get_top_tasks(vectorstore, query: str, k: int) -> List[str]:
    """Get the top k tasks based on the query."""
    results = vectorstore.similarity_search_with_score(query, k=k)
    if not results:
        return []
    sorted_results, _ = zip(*sorted(results, key=lambda x: x[1], reverse=True))
    return [str(item.metadata["task"]) for item in sorted_results]
