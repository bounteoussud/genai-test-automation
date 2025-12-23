#from dotenv import load_dotenv
#load_dotenv()  # MUST be first

from core.crew import run_crew

if __name__ == "__main__":
    app_url = "https://www.amazon.in"
    run_crew(app_url)