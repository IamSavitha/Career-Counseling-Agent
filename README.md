## Career Counseling Agent
AI-powered Career Planning Assistant using Ollama, LangChain, and Streamlit

This project implements an intelligent Career Counseling Agent that assists users with career planning, skill development, salary expectations, resume improvement, and interview preparation.

The agent uses Ollama (llama3.2) as the local LLM, LangChain for agent/tool orchestration, and Streamlit for the chat-based frontend UI.

## Features
### 1. Skills Gap Analyzer

Compares user skills with target job requirements

Identifies strong skills, partial matches, and missing skills

Generates a detailed learning roadmap

Suggests resources & project ideas

###  2. Resume Scorer

Evaluates resume content for a target role

Provides a score out of 10

Gives actionable improvements

Suggests rewrites & strong bullet samples

### 3. Salary Estimator

Estimates realistic salary ranges based on:

Job title

Location

Years of experience

Notes influential factors & market variations

Provides external references users can verify with

### 4. Interview Question Generator

Generates technical and behavioral interview questions

Groups questions by category

Tags difficulty levels

Provides hints on what interviewers expect

### Conversation Memory

The agent maintains context using LangChain ConversationBufferMemory, allowing natural multi-turn conversations.

### Tool-Aware Intelligent Agent

Thanks to LangChain’s agent architecture, the model automatically:

Chooses the correct tool

Executes tool functions

Returns structured, helpful responses

###  Streamlit UI

Includes:

Sidebar for configuration

Model selection

Temperature control

Tool enabling/disabling

Chat history with memory

Project Structure
career_counseling_agent/
│── app.py
│── requirements.txt
│── README.md

Installation
1. Install Ollama

Download & install from:
https://ollama.com/download

2. Pull the model
ollama pull llama3.2

3. Install Python dependencies
pip install -r requirements.txt

▶️ Running the App
streamlit run app.py


Your browser will open the Streamlit app automatically.

Example Queries
Skills Gap
I want to become a Data Engineer at a FAANG company.
My current skills: Python, pandas, SQL, Airflow, Linux.
Target JD: Spark, AWS, data modeling, advanced SQL, pipelines.
Analyze my gap and build me a 3-month roadmap.

Resume Scoring
Target Role: ML Engineer
Resume:
- MS in Data Analytics
- Projects: LSTM stock prediction, Airflow-dbt pipeline
- Skills: Python, ML, SQL
Score my resume out of 10 and give concrete improvements.

Salary Estimate
Job Title: Data Scientist
Location: San Francisco Bay Area
YOE: 1
Estimate realistic salary ranges.

Interview Questions
Role: Backend Engineer
Level: Entry
Focus: APIs, SQL, concurrency
Generate 12 technical + behavioral questions.

Technologies Used
Component	Technology
LLM	Ollama (llama3.2)
Agent framework	LangChain
Tools	Custom Python functions
UI	Streamlit
Memory	LangChain ConversationBufferMemory

Author
Savitha Vijayarangan
MS Data Analytics | SJSU
Tech: Data Science • ML • AI • Data Engineering