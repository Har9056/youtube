#backend/crew/tasks.py
from crewai import Task
from backend.crew.agents import content_analyst_agent, strategy_advisor_agent,growth_recommendation_agent

def generate_growth_task(weaker_channel, stronger_channel):
    return Task(
        description=(
            f"Analyze the performance of '{weaker_channel['channel_name']}' and compare it to the stronger channel "
            f"'{stronger_channel['channel_name']}'. Based on content, frequency, video types, and audience engagement, "
            f"provide clear growth recommendations for the weaker channel to reach or surpass the success of the stronger one."
        ),
        expected_output="A detailed strategy for growth tailored to the weaker channel.",
        agent=growth_recommendation_agent,
    )
def content_analysis_task(channel_data):
    return Task(
        description=f"""
        You are a YouTube Content Analyst.

        Analyze the following YouTube channel data:

        {channel_data}

        **Provide your output in this structured format:**

        1. **Key Topics & Niches:** Top topics covered and emerging areas within the channel's videos.
        2. **Audience Type:** Beginner, Intermediate, Advanced, or Mixed.
        3. **Title Style Analysis:** Common patterns, length, use of emojis, strong words, hashtags.
        4. **Thumbnail Style Analysis:** Colors, text overlay, face inclusion, minimalism vs. detail.
        5. **Video Length Patterns:** Average length of top performing videos (if data available).
        6. **Publishing Time Patterns:** Days or times that perform best (if data available).
        7. **Engagement Metrics Summary:** View-to-like ratio, comments frequency, shares if available.
        8. **Key Success Factors:** 3-5 bullet points summarizing why these videos succeeded.

        Your analysis will guide a growth strategist to design content strategies.
        """,
        agent=content_analyst_agent,
        expected_output="A structured detailed analysis report as described above."
    )


def strategy_recommendation_task(analysis_summary):
    return Task(
        description=f"""
        You are a YouTube Growth Strategist.

        Based on this **channel analysis**:

        {analysis_summary}

        **Provide your recommendations in this structured format:**

        1. **Content Strategy:**
           - 3-5 specific video topics to publish next (titles + 1-line descriptions).
           - Suggested frequency (videos per week).

        2. **SEO Improvements:**
           - Keyword strategy for titles, descriptions, hashtags.

        3. **Thumbnail Strategy:**
           - Recommended style, colors, text overlay tips.

        4. **Community Engagement:**
           - Comment prompts, polls, or challenges to increase interaction.

        5. **Additional Growth Tactics:**
           - Collaborations, shorts strategy, live sessions, playlists structuring.

        Focus on **practical, realistic, actionable next steps** to grow this channel by at least 2x in the next 6 months.
        """,
        agent=strategy_advisor_agent,
        expected_output="A clear, practical, structured growth plan as described above."
    )
