from fpdf import FPDF
from datetime import datetime
from pathlib import Path

PDF_DIR = Path("assets/pdfs")
PDF_DIR.mkdir(parents=True, exist_ok=True)

def clean_text(text):
    return text.encode('latin-1', 'ignore').decode('latin-1')

def generate_pdf(channel_data, agents_output):
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "YouTube Channel Report", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, clean_text(f"Channel: {channel_data.get('channel_name', '-')}"), ln=True)

    pdf.set_font("Arial", "", 11)
    pdf.cell(0, 8, f"Subscribers: {channel_data.get('subscribers', '-')}", ln=True)
    pdf.cell(0, 8, f"Total Views: {channel_data.get('total_views', '-')}", ln=True)
    pdf.cell(0, 8, f"Total Videos: {channel_data.get('video_count', '-')}", ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Top Videos:", ln=True)
    pdf.set_font("Arial", "", 11)

    for video in channel_data.get("top_videos", []):
        text = f"- {video['title']} | Views: {video['views']} | Likes: {video['likes']} | Comments: {video['comments']}"
        pdf.multi_cell(0, 8, clean_text(text))

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Content Analysis (AI):", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, clean_text(agents_output.get("content_analysis", "No analysis.")))

    pdf.ln(5)
    pdf.set_font("Arial", "B", 12)
    pdf.cell(0, 10, "Strategy Recommendations (AI):", ln=True)
    pdf.set_font("Arial", "", 11)
    pdf.multi_cell(0, 8, clean_text(agents_output.get("strategy_recommendations", "No recommendations.")))

    pdf.ln(10)

    filename = f"{channel_data.get('channel_name', 'report').replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = PDF_DIR / filename
    pdf.output(str(filepath))

    print("✅ PDF Generated:", filepath)
    return str(filepath)
