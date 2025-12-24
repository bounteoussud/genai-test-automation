from crewai import Agent
from llm.ollama_llm import get_ollama_llm

planner_agent = Agent(
    role="Test Planning Agent",
    goal="Analyze the application URL and generate UI test cases",
    backstory="Senior QA architect with expertise in e-commerce testing",
    llm=get_ollama_llm(),
    verbose=True
)
