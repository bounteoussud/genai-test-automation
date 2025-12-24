#from dotenv import load_dotenv
#load_dotenv()  # MUST be first
import os

os.environ["LITELLM_LOG"] = "ERROR"
os.environ["LITELLM_DISABLE_TELEMETRY"] = "true"
os.environ["LITELLM_MODE"] = "NONE"   # 👈 important

from core.crew import run_crew

if __name__ == "__main__":
    app_url = "https://www.amazon.in"
    run_crew(app_url)