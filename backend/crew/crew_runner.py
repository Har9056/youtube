from crewai import Crew
from backend.crew.tasks import (
    content_analysis_task,
    strategy_recommendation_task,
    generate_growth_task  # ✅ new import
)
from backend.crew.agents import (
    content_analyst_agent,
    strategy_advisor_agent,
  
    growth_recommendation_agent
)


# def run_agents_on_channel(channel_data):
#     # 1️⃣ Create and run content analysis
#     content_task = content_analysis_task(channel_data)
#     analysis_output = Crew(
#         agents=[content_task.agent],
#         tasks=[content_task],
#         verbose=True
#     ).kickoff()

#     # 2️⃣ Create strategy task using the raw analysis text
#     strategy_task = strategy_recommendation_task(analysis_output.raw)

#     # 3️⃣ Run strategy task
#     strategy_output = Crew(
#         agents=[strategy_task.agent],
#         tasks=[strategy_task],
#         verbose=True
#     ).kickoff()

#     # ✅ Return only .raw as JSON-serializable text
#     return {
#         "content_analysis": analysis_output.raw,
#         "strategy_recommendation": strategy_output.raw
#     }

def run_agents_on_channel(channel_data):
    print("[DEBUG] 🚀 Starting run_agents_on_channel")

    # 1️⃣ Content Analysis Task
    print("[DEBUG] Creating content analysis task...")
    content_task = content_analysis_task(channel_data)

    print("[DEBUG] Running content analysis Crew kickoff...")
    analysis_output = Crew(
        agents=[content_task.agent],
        tasks=[content_task],
        verbose=True
    ).kickoff()

    print("[DEBUG] 🧠 Content Analysis Output:\n", analysis_output.raw)

    # 2️⃣ Strategy Recommendation Task
    print("[DEBUG] Creating strategy recommendation task...")
    strategy_task = strategy_recommendation_task(analysis_output.raw)

    print("[DEBUG] Strategy task description:", strategy_task.description)

    print("[DEBUG] Running strategy recommendation Crew kickoff...")
    strategy_output = Crew(
        agents=[strategy_task.agent],
        tasks=[strategy_task],
        verbose=True
    ).kickoff()

    print("[DEBUG] 🚀 Strategy Recommendation Output:\n", strategy_output.raw)

    # ✅ Final structured return
    result = {
        "content_analysis": analysis_output.raw,
        "strategy_recommendation": strategy_output.raw
    }

    print("[DEBUG] ✅ Final AI results to return:", result)
    return result

# ✅ Fixed version
def run_growth_agent_if_same_domain(channel1, channel2):
    from backend.crew.tasks import generate_growth_task
    from backend.crew.agents import growth_recommendation_agent
    from crewai import Crew

    # Rough similarity check using description keyword overlap
    desc1 = set(channel1.get("description", "").lower().split())
    desc2 = set(channel2.get("description", "").lower().split())
    common = desc1.intersection(desc2)

    if len(common) >= 5:  # Adjust threshold if needed
        try:
            subs1 = int(str(channel1.get("subscribers", "0")).replace(",", ""))
            subs2 = int(str(channel2.get("subscribers", "0")).replace(",", ""))
        except (ValueError, AttributeError):
            return None  # Skip if data isn't clean

        stronger, weaker = (channel1, channel2) if subs1 > subs2 else (channel2, channel1)

        growth_task = generate_growth_task(weaker, stronger)
        crew = Crew(
            agents=[growth_recommendation_agent],
            tasks=[growth_task],
            verbose=True
        )
        output = crew.kickoff()

        # ✅ Normalize output to structured dict for frontend
        if isinstance(output, dict):
            # Already structured, return as is
            return output

        elif isinstance(output, str):
            # If string, treat first line as summary, rest as recommendations
            lines = output.strip().split("\n")
            summary = lines[0] if lines else "Growth Opportunity Generated"
            recommendations = "\n".join(lines[1:]) if len(lines) > 1 else ""

            return {
                "summary": summary,
                "recommendations": recommendations
            }

        else:
            # Unexpected output type
            return {
                "summary": "Growth analysis completed.",
                "recommendations": str(output)
            }

    # If not similar domains, return None to skip growth suggestion
    return None
