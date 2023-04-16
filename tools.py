from typing import List
from langchain import SerpAPIWrapper
from langchain.agents import Tool
from langchain.chains import LLMMathChain
from langchain.utilities import TextRequestsWrapper, WikipediaAPIWrapper

class Tools:
    def __init__(self, todo_chain, llm):
        self.search = SerpAPIWrapper()
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
            description="useful for when you need to answer concrete questions that would be found on a wikipedia page. Like historic figures, events. Input: a question. Output: a wikipedia page that answers that question. Please be very clear what the question is!",
        ),
        Tool(
            name="Requests",
            func=self.requests.get,
            description="useful when you need to access a website, an API or other web resource. Input: a url. Output: the text on that website. Please be very clear what the url is!",
        ),
        Tool(
            name="Calculator",
            func=self.llm_math_chain.run,
            description="useful for when you need to answer questions about math"
        )
    ]
        self.tool_names = [tool.name for tool in self.tools]

    def get_tool(self, tool_name: str) -> Tool:
        if tool_name not in self.tool_names:
            raise ValueError(f"Invalid tool name: {tool_name}")
        return self.tools[self.tool_names.index(tool_name)]


