from llm.ollama_llm import get_ollama_llm

def generate_ui_test_cases(app_url: str) -> str:
    prompt = f"""
    You are a senior QA engineer.

    Generate UI test cases for the website:
    {app_url}

    Focus on:
    - Homepage validation
    - Search flow
    - Product navigation

    Return numbered test cases.
    """
    return get_ollama_llm(prompt)
