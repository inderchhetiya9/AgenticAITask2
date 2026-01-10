from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from tools import tools
from models import ResponseFromLLM
import os
model = ChatOpenAI(model = "gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))



def get_agent_response(user_query: str):

    agent = create_agent(
    model=model,
    tools=tools,
    system_prompt="You are a helpful assistant",
    response_format=ResponseFromLLM,
)
    
    response = agent.invoke(
        {"messages": [{"role": "user", "content": user_query}]}
    )
    return response["structured_response"]
# Run the agent
# response = agent.invoke(
#     {"messages": [{"role": "user", "content": "what is the company's policy on remote work?"}]}
# )

# response["structured_response"]