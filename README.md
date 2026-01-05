AI-Enabled QA Automation Framework
📌 Problem Statement
The objective of this project is to build an AI-driven QA automation framework where multiple intelligent agents collaborate to automate the complete testing lifecycle.

The framework will:
Accept user requirements or user stories as input
Automatically generate manual test cases using a Generative AI model
Store generated manual test cases in an Excel file
Read manual test cases from Excel and generate automation test scripts
Execute automation scripts using Python, Playwright, and Pytest

Use Ollama (LLM engine) locally to ensure:
Faster execution
Offline capability
No dependency on cloud APIs
Secure data handling
The framework is designed to be modular, scalable, lightweight, and fast.

🧠 Agent Responsibilities
Agent	Responsibility
Requirement Agent	Converts user requirements into manual test cases
Automation Agent	Converts manual test cases (Excel) into automation scripts
Execution Agent	Executes automation scripts and generates reports

🛠 STEP-BY-STEP SETUP GUIDE
STEP 1: Install System Prerequisites
1.1 Install Python 3.11
Download:
https://www.python.org/downloads/release/python-311/

During installation:
✅ Check Add Python to PATH
✅ Install pip

Verify:
python --version

1.2 Install Git
Download:
https://git-scm.com/downloads

Verify:
git --version

STEP 2: Install & Configure Ollama (LLM Engine)
2.1 Install Ollama
Download:
https://ollama.com/download

Verify:
ollama --version

2.2 Pull AI Models
ollama pull llama3

(Optional – lightweight model)
ollama pull mistral

2.3 Start Ollama Service
ollama run llama3


Verify API:
curl http://localhost:11434

STEP 3: Create Project Workspace
mkdir ai-qa-framework
cd ai-qa-framework

STEP 4: Install Poetry (Dependency Manager)
4.1 Install Poetry
pip install poetry


Verify:
poetry --version

4.2 Configure Python Version
poetry env use python3.11

4.3 Initialize Project
poetry init


(Press Enter to accept defaults)

STEP 5: Install Dependencies
Core Libraries
poetry add requests pandas openpyxl python-dotenv

Testing & Automation
poetry add pytest pytest-html playwright pytest-json-report

Install Playwright Browsers
poetry run playwright install

STEP 6: Create Project Structure
mkdir agents llm utils logs reports testcases
mkdir testcases/manual testcases/automation


Create files:

touch main.py
touch llm/ollama_client.py
touch agents/requirement_agent.py
touch agents/automation_agent.py
touch agents/execution_agent.py
touch utils/excel_utils.py
touch utils/excel_writer.py
touch utils/excel_validator.py
touch utils/logger.py
touch utils/requirement_hash.py
touch .env
touch .gitignore

STEP 7: Run the Framework
poetry run python main.py

🧰 Tech Stack
Layer	Technology
Language	Python 3.11
AI Model	Ollama (LLaMA 3)
Automation	Playwright (Sync API)
Test Runner	Pytest
Test Storage	Excel (Pandas)
Logging	Python Logging
Dependency Management	Poetry
📁 Project Structure
ai-qa-framework/
│
├── agents/
│   ├── requirement_agent.py
│   ├── automation_agent.py
│   └── execution_agent.py
│
├── llm/
│   └── ollama_client.py
│
├── testcases/
│   ├── manual/
│   │   └── testcases.xlsx
│   │
│   └── automation/
│       ├── test_TC_1.py
│       ├── test_TC_2.py
│       └── ...
│
├── utils/
│   ├── excel_utils.py
│   ├── excel_writer.py
│   ├── excel_validator.py
│   ├── logger.py
│   └── requirement_hash.py
│
├── logs/
│   └── framework.log
│
├── reports/
│   └── report.html
│
├── main.py
├── pyproject.toml
├── poetry.lock
├── .env
└── .gitignore

✅ Outcome
This framework delivers:
End-to-end AI-powered QA automation
Automatic test case generation
Automatic script generation
Local, fast, and secure LLM execution
Scalable agent-based architecture