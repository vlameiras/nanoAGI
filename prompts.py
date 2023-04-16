from langchain.agents import ZeroShotAgent

from tools import Tools

TASK_PRIORITIZATION_PROMPT= (
    "You are an task prioritization AI tasked with cleaning the formatting of and reprioritizing"
    " the following tasks: {task_names}."
    " Consider the ultimate objective of your team: {objective}."
    " Do not remove any tasks. Return the result as a numbered list, like:"
    " #. First task"
    " #. Second task"
    " Start the task list with number {next_task_id}."
)

TASK_CREATION_PROMPT= (
    "You are an task creation AI that uses the result of an execution agent"
    " to create new tasks with the following objective: {objective},"
    " The last completed task has the result: {result}."
    " This result was based on this task description: {task_description}."
    " These are incomplete tasks: {incomplete_tasks}."
    " Based on the result, create new tasks to be completed"
    " by the AI system that do not overlap with incomplete tasks."
    " Return the tasks as an array."
)
    
TASK_TODO_PROMPT= (
    "You are a planner who is an expert at coming up with a todo list for a given objective. Come up with a todo list for this objective: {objective}. If there is already an extensive task list, only change it or include new tasks if needed."
)

templates = {
    "task_creation": {
        "template": TASK_CREATION_PROMPT,
        "input_variables": ["objective", "result", "task_description", "incomplete_tasks"],
    },
    "task_priority": {
        "template": TASK_PRIORITIZATION_PROMPT,
        "input_variables": ["task_names", "next_task_id", "objective"],
    },
    "task_todo": {
        "template": TASK_TODO_PROMPT,
        "input_variables": ["objective"]
    }
}

def get_execution_prompt_template(tools: Tools):
    prefix = """You are an AI who performs one task based on the following objective: {objective}. Take into account these previously completed tasks: {context}."""
    suffix = """Question: {task}
    {agent_scratchpad}"""
    prompt = ZeroShotAgent.create_prompt(
        tools.tools,
        prefix=prefix,
        suffix=suffix,
        input_variables=["objective", "task", "context", "agent_scratchpad"],
    )
    return prompt