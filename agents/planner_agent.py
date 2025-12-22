from crewai import Agent

planner_agent = Agent(
    role="Test Planner",
    goal="Convert natural language requirements into test scenarios",
    backstory="Senior QA architect with UI and API automation expertise",
    verbose=True
)
