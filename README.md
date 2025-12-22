# genai-test-automation

**PHASE 1 — Local Machine Setup (Windows 11)**

1️⃣ Install Python 3.11

Download Python 3.11.x

👉 https://www.python.org/downloads/windows/

During install:

✅ Add Python to PATH

✅ Install pip

After install go to cmd and verify:

python --version

2️⃣ Install Git from https://git-scm.com/download/win (if not already)

After install go to cmd and verify:


git --version

3️⃣ VS Code Setup

Ensure these extensions are installed, make sure to install the tool having maxmimum ratings and download count:

Python

Pylance

GitHub Actions 

GitHub Copilot

GitHub Copilot Chat

Allure Support

Playwright Test For VS Code

**PHASE 2 — GitHub Repository Setup**
4️⃣ Create Repository and Clone

On GitHub portal → New Repository

Name: genai-test-automation

Add Python .gitignore

Install git bash if not installed

Do the ssh setup through https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent

create ssh key using following command in git bash (if key not generated yet)

 ssh-keygen -t ed25519 -C "sudershan.singh@bounteous.com"

 In git bash go to the id_ed25519.pub file location and copy the key using following command:
 
 cat ~/.ssh/id_ed25519.pub > /dev/clipboard

 Now Go to Github portal > Your account > Settings > SSH and GPG Keys > New SSH Key > Provide Title > Paste the Key > Click Add SSH Key

In your windoes 11 machine create a folder vscode_workstation > go to folder properties> Security > Edit
Provide Full Control to Users and Authenticated Users.

In git bash change directory and go inside vscode_workstation and Create repo  by cloning locally :

git clone https://github.com/bounteoussud/genai-test-automation.git

cd genai-test-automation


**PHASE 3 — Poetry Setup**
5️⃣ Go to cmd and Install Poetry (GLobal) using below command (make sure Python desired version should be installed)

pip install poetry

Verify:

poetry --version

Configure Poetry - Recommended, it ensures .venv stays inside project (portable for team):

poetry config virtualenvs.in-project true



**PHASE 3 - Create Project Skeleton**

Step 1.1 — Create Base Project 

In git bash change directory and go inside vscode_workstation and run below command:

poetry new genai-test-automation-qathan

Go inside the folder:

cd genai-test-automation-qathan

Open the current folder in VS-Code:

code .


Step 1.2 — Remove Default Package Folder (Recommended)

Poetry creates a library-style folder genai-test-automation-qathan inside genai-test-automation-qathan we don’t need it hence remove it:

rmdir genai-test-automation-qathan /s /q

now below folder structure should exist:

genai-test-automation-qathan/
├── tests/
│   └── __init__.py
├── pyproject.toml
└── README.md


Step 1.3 — Create Framework Folder Structure

In VS Code > Terminal> Git Bash - Run from project root (genai-test-automation-qathan), following creates the folder structure:

mkdir -p agents llm core tests/ui tests/api test_data reports/allure-results .github/workflows

Step 1.4 — Add __init__.py for Imports

Now run below commands to create __init__.py in required folders:

touch agents/__init__.py
touch llm/__init__.py
touch core/__init__.py
touch tests/ui/__init__.py
touch tests/api/__init__.py


Step 1.5 — Create Required Files using below commands:

touch agents/planner_agent.py
touch agents/ui_agent.py
touch agents/api_agent.py

touch llm/gemini_client.py

touch core/config.py
touch core/executor.py

touch tests/ui/test_login_ui.py
touch tests/api/test_user_api.py

touch test_data/test_cases.yaml



Resulting Folder Structure should like as follows: 
genai-test-automation-qathan/
│
├── agents/
│   ├── __init__.py   ← ✅
│   ├── planner_agent.py
│   ├── ui_agent.py
│
├── llm/
│   ├── __init__.py   ← ✅
│   └── gemini_client.py
│
├── core/
│   ├── __init__.py   ← ✅
│   ├── executor.py
│
├── tests/
│   ├── ui/
│   │   ├── __init__.py   ← ✅
│   │   └── test_login_ui.py
│   │
│   ├── api/
│   │   ├── __init__.py   ← ✅
│   │   └── test_user_api.py
├── test_data/
│   ├── test_cases.yaml



CLUE: Why NOT Add __init__.py in Root?
Root is not a Python package. Poetry uses root as project context. Adding it may confuse imports.


**PHASE 2 — Dependency Installation (Poetry)**
Step 2.1 — Add Dependencies using following command:

poetry add pytest playwright httpx allure-pytest crewai google-generativeai

Step 2.2 — Install Playwright Browsers

poetry run playwright install


Step 2.3 — Verify Virtual Environment (.venv folder should exist inside project)

poetry env info



**PHASE 3 — LLM & Agent Wiring (Minimal Baseline)**

Step 3.1 — Environment Variables

Create .env file (DO NOT COMMIT):

GEMINI_API_KEY=your_api_key_here


Add to .gitignore:

Step 3.2 — Gemini Client (llm/gemini_client.py)


import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def ask_gemini(prompt: str) -> str:
    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt)
    return response.text


Step 3.3 — CrewAI Agent Example (agents/planner_agent.py)


from crewai import Agent

planner_agent = Agent(
    role="Test Planner",
    goal="Convert natural language requirements into test scenarios",
    backstory="Senior QA architect with UI and API automation expertise",
    verbose=True
)



**PHASE 4 — UI & API Automation (Execution Ready)**

Step 4.1 — UI Test Example (tests/ui/test_login_ui.py)

def test_sample_ui(page):
    page.goto("https://example.com")
    assert "Example" in page.title()


Step 4.2 — API Test Example (tests/api/test_user_api.py)

import httpx

def test_sample_api():
    response = httpx.get("https://api.github.com")
    assert response.status_code == 200



**PHASE 5 — Allure Reporting**

Step 5.1 — Run Tests with Allure

poetry run pytest --alluredir=reports/allure-results


Step 5.2 — View Report

allure serve reports/allure-results


**PHASE 6 — GitHub Setup (Single Source of Truth)**

Step 6.1 — Initialize Git

git init

git branch -M main

git add .

git commit -m "Initial GenAI test automation framework for QATHAN Team setup"

Step 6.2 — Create GitHub Repo

Create empty repo in GitHub and Copy repo URL and paste in 

git remote add origin <repo_url>

git push -u origin main



Step 6.3 — GitHub Actions Workflow

Create .github/workflows/automation.yml

name: Automation Tests

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install poetry
      - run: poetry install
      - run: poetry run playwright install
      - run: poetry run pytest --alluredir=reports/allure-results





**PHASE 7 — Team Onboarding (MOST IMPORTANT)**

✅ This Is What Team Members Must Do (ONLY)

git clone <repo_url>
cd genai-test-automation
pip install poetry
poetry install
poetry run playwright install

