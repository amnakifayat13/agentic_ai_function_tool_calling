import os
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
import asyncio
import json
# Load the environment variables from the .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

# Check if the API key is present; if not, raise an error
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please ensure it is defined in your .env file.")


external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# @function_tool
# def list_todos()->str:
#     """list all todos"""
#     with open("todo.json", "r") as f:
#         data = json.load(f)
#     return str(data)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)



# query = input("insert your query: ")
async def main():
    agent = Agent(
        name="Todo's Assistant",
        instructions="You are a todos you can add,list, and complete todos.",
        model=model,
        # tools=[list_todos]
    )

    result = await Runner.run(agent, "who is the founder of Pakistan", run_config=config)
    print(result.final_output)
   

if __name__ == "__main__":
    asyncio.run(main())