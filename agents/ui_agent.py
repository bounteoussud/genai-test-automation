from crewai import Agent
from llm.ollama_llm import get_ollama_llm
from tools.playwright_tool import PlaywrightTool


ui_agent = Agent(
    role="UI Automation Agent",
    goal="Execute UI automation using Playwright based on test cases.",
    backstory="Senior QA automation engineer specializing in Playwright.",
    llm=get_ollama_llm(),
    verbose=True,
    tools=[PlaywrightTool()]   # ✅ Tool instance
)
