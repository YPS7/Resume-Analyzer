import shutil
import os
import tempfile
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
import processor
import tools
import llm_client
import pdf_utils

load_dotenv()
app = FastAPI(title="AI Resume Engine")

class AnalysisResponse(BaseModel):
    score: float
    verdict: str
    missing_skills: list[str]
    summary: str
    dealbreaker: bool

@app.get("/")
def health_check():
    return {"status": "online", "engine": "v8.0"}

@app.post("/analyze", response_model=AnalysisResponse)
async def analyze_resume(
    jd_text: str = Form(...), 
    resume_file: UploadFile = File(None),
    resume_text_raw: Optional[str] = Form(None)
):
    try:
        final_resume_text = ""
        if resume_file:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
                shutil.copyfileobj(resume_file.file, tmp)
                tmp_path = tmp.name
            print(f"[API] Processing PDF: {resume_file.filename}")
            final_resume_text = pdf_utils.extract_text_from_pdf(tmp_path)
            os.remove(tmp_path)
        elif resume_text_raw:
            final_resume_text = resume_text_raw
        
        if not final_resume_text or len(final_resume_text) < 50:
            raise HTTPException(status_code=400, detail="Resume text empty/unreadable")

        job_role = jd_text.split('\n')[0][:50]
        dynamic_anchors = tools.get_market_anchors(job_role)
        processor.update_anchors(dynamic_anchors)

        embeddings = processor.embedding_model.encode([final_resume_text, jd_text])
        sem_score = processor.util.cos_sim(embeddings[0], embeddings[1]).item() * 100
        rule_score, missing_skills = processor.calculate_smart_score(jd_text, final_resume_text)

        is_dealbreaker = False
        final_score = 0.0
        verdict = "Not Suitable"
        summary_text = "Analysis complete."

        if "__DEALBREAKER__" in missing_skills:
            final_score = 0.0
            verdict = "Not Suitable (Dealbreaker)"
            is_dealbreaker = True
            missing_skills = ["Critical Dealbreaker (Citizenship/Clearance)"]
            summary_text = "Candidate rejected due to mandatory dealbreaker violations."
        else:
            if missing_skills:
                recovered = llm_client.verify_missing_skills(final_resume_text, missing_skills)
                if recovered:
                    boost = min(15.0, len(recovered) * 2.5)
                    rule_score = min(100, rule_score + boost)
                    missing_skills = [s for s in missing_skills if s not in recovered]

            sen_mult = processor.calculate_seniority_multiplier(jd_text, final_resume_text)
            if rule_score > 5:
                base = (sem_score * 0.3) + (rule_score * 0.7)
            else:
                base = sem_score
            final_score = min(100, round(base * sen_mult, 2))
            verdict = processor.derive_suitability(final_score)

            try:
                stream = llm_client.generate_human_summary(final_resume_text, jd_text, final_score, missing_skills)
                summary_text = ""
                if isinstance(stream, str):
                    summary_text = stream
                else:
                    for chunk in stream:
                        content = chunk.choices[0].delta.content
                        if content: summary_text += content
            except Exception:
                summary_text = "AI Summary unavailable."

        return {
            "score": final_score,
            "verdict": verdict,
            "missing_skills": missing_skills,
            "summary": summary_text,
            "dealbreaker": is_dealbreaker
        }
    except Exception as e:
        print(f"[API Error] {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))