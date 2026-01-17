# 🤖 Sales Manager AI Agent

**An autonomous AI team that drafts, reviews, and sends cold sales emails.**

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![OpenAI](https://img.shields.io/badge/OpenAI-Agents_SDK-green)
![SendGrid](https://img.shields.io/badge/SendGrid-API-orange)

## 💡 What is this?

Most AI tools just write generic text. This project builds a **virtual sales team** on your computer.

Instead of one AI trying to do everything, this system uses **5 different AI Agents** working together:
1.  **3 Writer Agents:** They compete to write the best email (one is aggressive, one is helpful, one is casual).
2.  **1 Manager Agent:** It reviews the drafts and picks the "Winner" based on who we are emailing.
3.  **1 Execution Agent:** It formats the winning email and sends it via SendGrid.



## 🏗️ How It Works

When you run the script, the "Sales Manager" follows this logic:

1.  **Drafting Phase:** It commands the three writers (`Challenger`, `Consultant`, `Networker`) to write drafts in parallel.
2.  **Decision Phase:** The Manager acts as a judge. It evaluates the drafts against the prospect's profile (e.g., "This is a CEO, so keep it short").
3.  **Handoff Phase:** The winning draft is passed to the `Email Manager`.
4.  **Execution Phase:** The Email Manager generates a subject line, converts the text to HTML, and triggers the SendGrid API.

## 🛠️ The Tech Stack

* **Python:** Core logic and async orchestration.
* **OpenAI Agents SDK:** For managing the "Swarm" of agents and handoffs.
* **GPT-4o-mini:** The brain behind the agents (chosen for speed and low cost).
* **SendGrid:** The delivery infrastructure to send the actual emails.

## 🚀 How to Run This

### 1. Clone the Repository

git clone [https://github.com/sagar-dhawane/Sales-Manager-Email-Agent.git](https://github.com/sagar-dhawane/Sales-Manager-Email-Agent.git)
cd Sales-Manager-Email-Agent

### 2.Set up Virtual Environment
It's best to keep dependencies clean.
Mac/Linux
python3 -m venv venv
source venv/bin/activate

Windows
python -m venv venv
venv\Scripts\activate

### 3. Install Dependencies
pip install openai sendgrid python-dotenv

### 4. Configure Your Keys (Important!)
Create a file named .env in the root folder. Do not upload this file to GitHub. Add your keys inside it:
OPENAI_API_KEY=sk-proj-your-key-here
SENDGRID_API_KEY=SG.your-sendgrid-key-here

### 5. Run the Agent
python main.py
📂 Project Structure
main.py: The entry point. Initializes the agents and runs the workflow.

agents.py: Contains the instructions and definitions for the 3 writer personas.

tools.py: Connects to the SendGrid API.

.env: Stores your private API keys (make sure this is in .gitignore!).

## Author: Sagar Dhawane Built with ❤️ using Python & OpenAI

