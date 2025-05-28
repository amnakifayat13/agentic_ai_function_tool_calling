import os
import asyncio
import requests
from dotenv import load_dotenv
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel, function_tool
from agents.run import RunConfig
import math 
import calendar
from datetime import date, timedelta

# Load environment variables from .env file
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")
weather_api_key = os.getenv("WEATHER_API_KEY")

if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set.")
if not weather_api_key:
    raise ValueError("WEATHER_API_KEY is not set.")
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

@function_tool
async def get_weather(city: str = "karachi") -> str:
    url = f"http://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={city}&aqi=no"
    response = requests.get(url)
    data = response.json()
    if "error" in data:
        return f"Sorry, couldn't find weather info for '{city}'."
    condition = data["current"]["condition"]["text"]
    temp = data["current"]["temp_c"]
    return f"The current weather in {city.title()} is {condition} and {temp}°C."

@function_tool
async def add(*args) ->int:
    """ add all numbers
    
    """
    add = sum(args)
    return add

@function_tool
async def subtract(a:int, b:int)->int:
    """ subtract two numbers"""
    return a - b

@function_tool
async def multiply(*args)->int:
    """ multliply all numbers"""
    multiple = 1
    for num in args:
        multiple *= num
    return multiple

@function_tool
async def divide(a: int, b: int) -> float:
    """divide two numbers"""
    try:
        return a / b
    except ZeroDivisionError:
        return "Cannot divide by zero."
    
@function_tool
async def pi()-> int:
    """provide the value of pi
    """
    
    return math.pi

@function_tool
async def power(a:int, b:int) -> int:
    """ provide powers of number""" 
    return a ** b 

@function_tool
async def squareRoot(a:int)->int:
    """square root of the number"""
    return math.sqrt(a) 

@function_tool
async def log(a:int)->int:
    """log of the number"""
    return math.log(a)

@function_tool
async def log10(a:int)->int:
    """log10 of the numeber"""
    return math.log10(a)
@function_tool
async def sin(a:int)->int:
    """sin of number"""
    return math.sin(a)

@function_tool
async def cos(a:int)->int:
    """cos of number"""
    return math.cos(a)

@function_tool
async def tan(a:int)->int:
    """tan of number"""
    return math.tan(a)

@function_tool
async def table(a: int) -> str:
    """make the table for the number"""
    lines = []
    for i in range(1, 11):
        lines.append(f"{a} x {i} = {a*i}")
    return "\n".join(lines)



@function_tool
def show_calendar(year: int, month: int) -> str:
    """
    provide year and month
    """
    return calendar.month(year, month)

@function_tool
def today_date() -> str:
    """
    Today's date.
    """
    return f"today is: {date.today()}"

@function_tool
def tomorrow_date() -> str:
    """
    tomorrow date.
    """
    return f"tomorrow date will be: {date.today() + timedelta(days=1)}"

@function_tool
def yesterday_date() -> str:
    """
    yesterday date.
    """
    return f"yesterday day was: {date.today() - timedelta(days=1)}"

async def main():
    user_input = input("Ask your question: ")

    agent = Agent(
        name="Assistant",
        instructions=(
            "You are a helpful assistant. "
            "If the user asks about the weather, use the get_weather tool. "
            "For all other questions, answer directly using your own knowledge."
            # "if user asks add however how many numbers are given by the user, use the add tool and add all numbers "
           
        ),
        model=model,
        tools=[get_weather, add, subtract,multiply, divide,pi,power,squareRoot,log, log10,sin,cos,tan,table,show_calendar, today_date, tomorrow_date,yesterday_date]
    )
    result = await Runner.run(agent, user_input, run_config=config)
    print("\nAI Response:")
    print(result.final_output)

asyncio.run(main())