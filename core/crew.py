from crewai import Crew
from core.tasks import create_tasks
#from llm.geminiai_llm import llm
from llm.ollama_llm import get_ollama_llm
#import pdb

def run_crew(app_url: str):
    #pdb.set_trace()
    tasks = create_tasks(app_url)
    llm=get_ollama_llm()
    crew = Crew(
        tasks=tasks,
        process="sequential",
        llm=llm,
        verbose=True,
        #manager_llm=llm
    )

    result = crew.kickoff()
    print("Crew Execution Result:",result)
