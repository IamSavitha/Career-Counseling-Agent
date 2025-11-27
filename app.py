import streamlit as st
from langchain_community.chat_models import ChatOllama
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool
from langchain.memory import ConversationBufferMemory

# -----------------------------
# Tool factory functions
# -----------------------------

def make_skills_gap_tool(llm):
    """Tool 1: Skills Gap Analyzer"""

    def _skills_gap_analyzer(input_text: str) -> str:
        """
        Expected input format (free-form is OK, but this works best):

        Target Role: <role title>
        Location: <city/country> (optional)
        Years of Experience: <X> (optional)
        User Skills:
        - skill 1
        - skill 2
        - ...
        Target Job Description:
        <paste JD or bullets here>
        """
        prompt = f"""
You are a senior career coach and technical mentor.

Task: Compare the user's current skills against the target job and identify:
1. Strong matches
2. Partial matches
3. Clear gaps
4. A step-by-step learning path (ordered roadmap) to close the gaps.
5. Recommended resources or practice project ideas.

Be concrete and structured. Use short sections and bullet points.

User & Job Info:
{input_text}
"""
        resp = llm.invoke(prompt)
        return resp.content

    return Tool(
        name="skills_gap_analyzer",
        func=_skills_gap_analyzer,
        description=(
            "Analyze the gap between a user's current skills and a target job's requirements "
            "and generate a structured learning path. Use when user asks about skill gaps, "
            "learning roadmap, or how to reach a specific role."
        ),
    )


def make_resume_scorer_tool(llm):
    """Tool 2: Resume Scorer (0–10)"""

    def _resume_scorer(input_text: str) -> str:
        """
        Expected input format:

        Target Role: <role>
        Resume:
        <paste resume text or bullet points>
        """
        prompt = f"""
You are an expert resume reviewer for top tech companies.

Task:
1. Score the resume out of 10 for the specified target role.
2. Briefly explain the score.
3. List concrete, actionable improvements:
   - content (projects, impact, metrics)
   - structure & clarity
   - keywords & ATS-friendliness
4. Provide a revised sample bullet or small section as an example.

Be concise but specific.

Input:
{input_text}
"""
        resp = llm.invoke(prompt)
        return resp.content

    return Tool(
        name="resume_scorer",
        func=_resume_scorer,
        description=(
            "Score a resume out of 10 for a target role and provide detailed, actionable feedback. "
            "Use when user asks to evaluate, review, or improve a resume or CV."
        ),
    )


def make_salary_estimator_tool(llm):
    """Tool 3: Salary Estimator"""

    def _salary_estimator(input_text: str) -> str:
        """
        Expected input format:

        Job Title: <title>
        Location: <city/country>
        Years of Experience: <X>
        Notes: <industry / company type / remote etc.> (optional)
        """
        prompt = f"""
You are a career and compensation advisor.

Task:
1. Estimate a realistic **base salary range** for this profile (low, median, high).
2. Specify the assumed currency clearly.
3. Mention factors that affect the range:
   - company size (startup vs big tech),
   - cost of living at the location,
   - skills & specialization,
   - remote vs on-site.
4. Add a short note on how the user can validate/adjust this range using public sources.

Be explicit that this is an approximate estimate, not official or guaranteed.

Profile:
{input_text}
"""
        resp = llm.invoke(prompt)
        return resp.content

    return Tool(
        name="salary_estimator",
        func=_salary_estimator,
        description=(
            "Estimate a realistic salary range based on job title, location, and years of experience. "
            "Use when user asks about expected salary, salary range, or compensation."
        ),
    )


def make_interview_question_tool(llm):
    """Tool 4: Interview Question Generator"""

    def _interview_question_generator(input_text: str) -> str:
        """
        Expected input format:

        Role: <e.g., Data Scientist, Backend Engineer>
        Level: <e.g., junior / mid / senior / intern>
        Focus Areas (optional): <e.g., SQL, Python, system design, ML basics>
        Question Types: <technical / behavioral / both>
        Number of Questions: <e.g., 10>
        """
        prompt = f"""
You are an expert interviewer.

Task:
1. Generate interview questions for the given role and level.
2. Include the requested mix of technical and/or behavioral questions.
3. Group questions by category (e.g., Technical - Python, Technical - SQL, Behavioral).
4. For each question, optionally add:
   - a short hint or what the interviewer is looking for,
   - difficulty tag (easy/medium/hard).

Input:
{input_text}
"""
        resp = llm.invoke(prompt)
        return resp.content

    return Tool(
        name="interview_question_generator",
        func=_interview_question_generator,
        description=(
            "Generate technical and behavioral interview questions for a given role and difficulty. "
            "Use when user wants practice questions or mock interview preparation."
        ),
    )


def build_tools(llm, enabled_tool_names):
    """Return tools filtered by user selection in the sidebar."""
    all_tools = {
        "Skills Gap Analyzer": make_skills_gap_tool(llm),
        "Resume Scorer": make_resume_scorer_tool(llm),
        "Salary Estimator": make_salary_estimator_tool(llm),
        "Interview Question Generator": make_interview_question_tool(llm),
    }
    return [all_tools[name] for name in enabled_tool_names]


# -----------------------------
# Streamlit UI
# -----------------------------

st.set_page_config(page_title="Career Counseling Agent", page_icon="🎯", layout="wide")

st.title("🎯 Career Counseling Agent")
st.write(
    "Ask me about skill gaps, resumes, salaries, and interview prep. "
    "I'll automatically use the right tools for you."
)

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")

    model_name = st.text_input("Ollama model name", value="llama3.2")
    temperature = st.slider("Temperature", 0.0, 1.5, 0.7, 0.1)

    st.markdown("**Enabled Tools**")
    default_tools = [
        "Skills Gap Analyzer",
        "Resume Scorer",
        "Salary Estimator",
        "Interview Question Generator",
    ]
    enabled_tools = st.multiselect(
        "Select which tools the agent can use:",
        default_tools,
        default=default_tools,
    )

    clear_chat = st.button("🧹 Clear Conversation")

# Session state initialization
if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "memory" not in st.session_state:
    st.session_state["memory"] = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True,
    )

if clear_chat:
    st.session_state["messages"] = []
    st.session_state["memory"].clear()
    st.experimental_rerun()

# Display previous chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Create LLM and Agent (per run, reusing memory)
llm = ChatOllama(
    model=model_name,
    temperature=temperature,
)

tools = build_tools(llm, enabled_tools)

agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,  # shows tool reasoning/logs in terminal
    memory=st.session_state["memory"],
    handle_parsing_errors=True,
)

# Chat input
user_input = st.chat_input("How can I help with your career today?")

if user_input:
    # Show user message
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Agent response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = agent.run(user_input)
            except Exception as e:
                response = f"Oops, something went wrong: {e}"
            st.markdown(response)

    st.session_state["messages"].append({"role": "assistant", "content": response})
