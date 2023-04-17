from typing import List
from langchain.agents import Tool
from langchain.chains import LLMMathChain
from langchain.utilities import GoogleSerperAPIWrapper, TextRequestsWrapper, WikipediaAPIWrapper

class Tools:
    def __init__(self, todo_chain, llm):
        self.search = GoogleSerperAPIWrapper()
        self.wikipedia = WikipediaAPIWrapper()
        self.requests = TextRequestsWrapper()
        self.llm_math_chain = LLMMathChain(llm=llm, verbose=True)

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
        Tool(
            name="Wikipedia",
            func=self.wikipedia.run,
            description="Useful for finding information about a specific topic. You cannot use this tool to ask questions, only to find information about a specific topic.",
        ),
        Tool(
            name="Requests",
            func=self.requests.get,
            description="useful when you need to access a website or API. Input: Valid URL.Please be very clear what the URL is! Output: The text of the website or API. ",
        ),
        Tool(
            name="Calculator",
            func=self.llm_math_chain.run,
            description="useful for when you need to answer questions about mathematical operations"
        )
    ]
        self.tool_names = [tool.name for tool in self.tools]

    def get_tool(self, tool_name: str) -> Tool:
        if tool_name not in self.tool_names:
            raise ValueError(f"Invalid tool name: {tool_name}")
        return self.tools[self.tool_names.index(tool_name)]


