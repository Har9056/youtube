# backend/test.py

from crewai import Agent, Task, Crew
import litellm
import os
from dotenv import load_dotenv

load_dotenv()

# Set your Gemini API key for LiteLLM
litellm.api_key = os.getenv("GEMINI_API_KEY")

# Define the Gemini model string
llm_model = "gemini/gemini-1.5-pro"

# ✅ Define a simple agent for testing
test_agent = Agent(
    role="Test Agent",
    goal="Say hello and confirm Gemini is working.",
    backstory="You are a simple testing agent to validate LLM connectivity.",
    verbose=True,
    llm=llm_model
)

# ✅ Define a simple task
test_task = Task(
    description="Say a short greeting message to confirm Gemini API call works.",
    expected_output="A short greeting message.",
    output_format="raw",
    agent=test_agent
)

# ✅ Create the Crew
crew = Crew(
    agents=[test_agent],
    tasks=[test_task],
    verbose=True
)

# ✅ Run the crew and print result
if __name__ == "__main__":
    result = crew.kickoff()

    if isinstance(result, dict) and "raw" in result:
        print("✔ Test Result:", result["raw"].strip())
    else:
        print("✔ Test Result:", str(result).strip())
