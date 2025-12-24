from crewai import Task
from agents.planner_agent import planner_agent
from agents.ui_agent import ui_agent

def create_tasks(app_url: str):

    planning_task = Task(
        description=f"""
        Analyze the website {app_url}.
        Generate key UI test cases focusing on:
        - Homepage validation
        - Search functionality
        - Product navigation
        """,
        expected_output="A list of UI test cases",
        agent=planner_agent
    )

    ui_execution_task = Task(
        description=f"""
        Execute UI automation for {app_url}
        using Playwright based on the generated test cases.
        """,
        expected_output="Automation results and screenshots",
        agent=ui_agent
    )

    return [planning_task, ui_execution_task]
