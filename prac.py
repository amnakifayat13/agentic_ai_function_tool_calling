import os
from dotenv import load_dotenv
from agents import Agent, AsyncOpenAI,  Runner, OpenAIChatCompletionsModel
from agents.run import RunConfig
import asyncio


load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")


external_client = AsyncOpenAI(
    api_key = gemini_api_key,
    base_url= "https://generativelanguage.googleapis.com/v1beta/openai/"
)


model = OpenAIChatCompletionsModel(
    model = "gemini-2.0-flash",
    openai_client= external_client,
)

config = RunConfig(
    model = model,
    model_provider= external_client,
    tracing_disabled = True,
)


async def main():
    user_input = input("ask your question: ")
    agent = Agent(
        name = "Assistant",
        instructions = "You are a helpful Assistant",
        model = model,
    )
    
    
    result =  await Runner.run(agent, user_input, run_config= config)
    print(result.final_output)
    
    
if __name__ == "__main__":
    asyncio.run(main())    