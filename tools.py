from typing import List
from langchain import SerpAPIWrapper
from langchain.agents import Tool

class Tools:
    def __init__(self, todo_chain):
        self.search = SerpAPIWrapper()
        self.tools = [
        Tool(
            name="Search",
            func=self.search.run,
            description="useful for when you need to answer questions about current events",
        ),
        Tool(
            name="TODO",
            func=todo_chain.run,
            description="useful for when you need to come up with todo lists. Input: an objective to create a todo list for. Output: a todo list for that objective. Please be very clear what the objective is!",
        ),
    ]
        self.tool_names = [tool.name for tool in self.tools]

    def get_tool(self, tool_name: str) -> Tool:
        if tool_name not in self.tool_names:
            raise ValueError(f"Invalid tool name: {tool_name}")
        return self.tools[self.tool_names.index(tool_name)]


