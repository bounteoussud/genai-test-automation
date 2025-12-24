from crewai import LLM

def get_ollama_llm():
    return LLM(
        model="ollama/llama3:latest",
        temperature=0.1,
        base_url="http://localhost:11434"
    )