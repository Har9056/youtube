from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
from pathlib import Path
import os

# Import your services and logic
from backend.crew.crew_runner import run_growth_agent_if_same_domain, run_agents_on_channel
from backend.services.youtube_service import get_channel_analysis
from backend.utils.pdf_generator import generate_pdf

app = FastAPI()

# Enable CORS (adjust `allow_origins` for production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Use your frontend domain in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------- Models ---------
class ChannelRequest(BaseModel):
    channel_url: str

class CompareRequest(BaseModel):
    channels: List[str]

# --------- Routes ---------
@app.get("/")
def health_check():
    return {"status": "Backend running"}

@app.post("/analyze_channel")
def analyze_channel(request: ChannelRequest):
    try:
        channel_data = get_channel_analysis(request.channel_url)
        ai_result = run_agents_on_channel(channel_data)

        if isinstance(ai_result, dict):
            content_analysis = ai_result.get("content_analysis", "No analysis found.")
            strategy_recommendations = ai_result.get("strategy_recommendation", "No recommendations found.")
        elif isinstance(ai_result, list) and len(ai_result) >= 2:
            content_analysis = ai_result[0]
            strategy_recommendations = ai_result[1]
        else:
            content_analysis = str(ai_result)
            strategy_recommendations = "No strategy generated."

        pdf_path = generate_pdf(channel_data, {
            "content_analysis": content_analysis,
            "strategy_recommendations": strategy_recommendations
        })

        print(f"[✅] PDF Path Generated: {pdf_path}")
        return {
            "channel_stats": channel_data,
            "ai_recommendations": {
                "content_analysis": content_analysis,
                "strategy_recommendation": strategy_recommendations
            },
            "pdf_path": f"/download_pdf/{os.path.basename(pdf_path)}"  # 🔁 Return relative path for frontend
        }

    except Exception as e:
        print("[❌] Exception in analyze_channel:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/compare_channels")
def compare_channels(request: CompareRequest):
    try:
        if len(request.channels) != 2:
            raise ValueError("Please provide exactly two channel URLs.")

        ch1_data = get_channel_analysis(request.channels[0])
        ch2_data = get_channel_analysis(request.channels[1])
        growth_output = run_growth_agent_if_same_domain(ch1_data, ch2_data)

        if isinstance(growth_output, str):
            growth_output = {"summary": growth_output, "recommendations": ""}
        elif growth_output is None:
            growth_output = {"summary": "No growth opportunity.", "recommendations": ""}

        return {
            "comparisons": [ch1_data, ch2_data],
            "growth_advice": growth_output
        }

    except Exception as e:
        print("❌ Compare error:", e)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download_pdf/{filename}")
def download_pdf(filename: str):
    pdf_path = Path("assets/pdfs") / filename
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found")
    return FileResponse(
        path=pdf_path,
        media_type='application/pdf',
        filename=filename
    )
