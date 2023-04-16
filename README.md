
# 🤖💡📚 nanoAGI

## 🌐 Introduction

`nanoAGI` is an implementation of popular autonomous task management systems like [BabyAGI](https://github.com/yoheinakajima/babyagi/tree/main) and [Auto-GPT](https://github.com/Significant-Gravitas/Auto-GPT). It also takes a lot of inspiration from [LangChain Agent examples](https://python.langchain.com/en/latest/use_cases/agents/baby_agi_with_agent.html)

For a more detailed overview of the approach, please refer to BabyAGI's "generated paper" [here](https://yoheinakajima.com/task-driven-autonomous-agent-utilizing-gpt-4-pinecone-and-langchain-for-diverse-applications/).

## ⚠️ Disclaimer

- This project is not intended to be used in production. It was build for learning purposes and should not be used for any other purpose.
- Still under development, so it might not work as expected.
- Tested with GPT-3.5, I still don't have GPT-4 API access 😥
- Please beware of costs when using OpenAI's APIs. While Pinecone has a free tier that should be enough for the purpose of testing this tool, this is not the - - case for OpenAI's APIs.

## 🔧 Requirements

- Python 3.8+
- [Pinecone API Key](https://docs.pinecone.io/getting-started/quickstart/)
- [OpenAI API Key](https://openai.com/docs/developer-quickstart/api-key-creation)
- [SERP API Key](https://serpapi.com/)

## 🛠 Installation

Setup a virtual environment and install the requirements:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Setup the environment variables:

```bash
export PINECONE_API_KEY=<your_pinecone_api_key>
export OPENAI_API_KEY=<your_openai_api_key>
export SERP_API_KEY=<your_serp_api_key>
```

## 🚀 Usage

Run the main module and pass the objective as an argument:

```bash
python main.py "I want to build an Helo world Flask app."
```

## Known Issues

- It tends to keep adding tasks to the todo list, changing priorities and "rambling" over small details. The algorithm needs to be improved to avoid this behavior.
- The execution between iterations takes longer than expected. Needs to be understood and improved.
