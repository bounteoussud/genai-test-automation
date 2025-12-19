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

Ensure these extensions are installed:

Python

Pylance

GitHub Copilot

GitHub Copilot Chat

**PHASE 2 — GitHub Repository Setup**
4️⃣ Create Repository

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

Create repo in git bash  Clone locally:

git clone https://github.com/bounteoussud/genai-test-automation.git

cd genai-test-automation


