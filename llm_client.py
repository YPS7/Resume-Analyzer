import os
import json
from dotenv import load_dotenv
from openai import OpenAI

# 1. Load Environment Variables
load_dotenv()
api_key = os.getenv("OPENROUTER_API_KEY")

if not api_key:
    # Fail gracefully if no key, but warn the user
    print("[Warning] OPENROUTER_API_KEY not found in .env. LLM features will fail.")
    api_key = "dummy_key" 

# 2. Initialize Client
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key
)

# Using Mistral Devstral (Free) or similar high-reasoning model
MODEL_NAME = "mistralai/devstral-2512:free"

def verify_missing_skills(resume_text, missing_skills_list):
    """
    Role-Agnostic Verifier.
    Checks if 'missing' keywords are actually implied in the text.
    """
    if not missing_skills_list:
        return []

    print(f"   [AI Verifier] Double-checking gaps: {missing_skills_list}...")

    prompt = f"""
    You are an Expert Resume Validator. 
    The automated parser failed to detect the following specific requirements in the candidate's text: 
    {missing_skills_list}

    RESUME / CV CONTENT:
    {resume_text[:3000]}

    TASK:
    Analyze the text deeply. Does the candidate actually possess these requirements?
    Look for synonyms, conceptual descriptions, tool usage, or project implications.
    (e.g., if 'Sales' is missing, look for 'Revenue Growth'. If 'Figma' is missing, look for 'UI Design').

    OUTPUT:
    Return ONLY a JSON list of the specific requirements found. 
    Example: ["requirement_1", "requirement_2"]
    If none are found, return [].
    """

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json_object"}
        )
        content = completion.choices[0].message.content
        
        if "[" in content and "]" in content:
            start = content.find("[")
            end = content.rfind("]") + 1
            return json.loads(content[start:end])
        return []

    except Exception as e:
        print(f"   [LLM Error] Verification failed: {e}")
        return []

def generate_human_summary(resume_text, jd_text, final_score, missing_skills):
    """
    Generates a high-level executive summary using the 'Senior Authority' Context Prompt.
    """
    
    # --- THE SUPER PROMPT ---
    prompt = f"""
    You are a senior hiring authority responsible for evaluating a candidate’s resume against a job description in a realistic, industry-accurate manner.

    Your task is to assess true role fit, not keyword overlap.

    --- 1. DOMAIN & PERSONA DETECTION (Mandatory) ---
    First, analyze the Job Description (JD) and classify it into one or more of the following domains.
    Adopt the corresponding persona(s):

    * **Engineering & Technology:**
        * Backend / Systems → CTO / Principal Engineer
        * Frontend / UI → Frontend Architect
        * Full-Stack → Engineering Manager
        * Mobile → Mobile Tech Lead
        * DevOps / Cloud → Head of Platform Engineering
    * **Data & AI:**
        * Data Engineering → Head of Data Infrastructure
        * ML / AI → AI Engineering Lead
    * **Product & Strategy:**
        * Product Management → Product Director
    * **Design & Creative:**
        * UI / UX / Product Design → Creative Director
    * **Marketing & Growth:**
        * Performance / Growth → Growth Lead
        * Brand / Content → CMO

    (If the JD spans multiple domains, apply a weighted, cross-functional perspective.)

    --- 2. CORE EVALUATION PHILOSOPHY ---
    Evaluate the candidate using:
    1.  Resume content
    2.  The real intent of the JD, not surface terminology
    3.  Computed Data: (Match Score: {final_score}%, Gaps: {missing_skills})

    *Perform semantic equivalence matching:*
    * Tools, platforms, or frameworks may differ; concepts matter more.
    * Examples: AWS ↔ GCP ↔ Azure | React ↔ Vue | TensorFlow ↔ PyTorch.
    * Prioritize depth of experience and impact over list of buzzwords.

    --- 3. JUDGMENT & FIT CLASSIFICATION ---
    Identify:
    * **Strong Matches:** Directly aligned with core JD needs.
    * **Transferable Strengths:** Adjacent experience that scales quickly.
    * **Critical Gaps:** Missing essentials that materially impact success.

    *Red Flags to Watch For (Domain Specific):*
    * Engineering: Only tutorial-level projects for senior roles.
    * Data/AI: Overreliance on prebuilt models without explanation.
    * Design: Aesthetic focus without usability reasoning.
    * Product: Execution without strategic reasoning.

    --- 4. OUTPUT STRUCTURE (Strict) ---
    Produce output in the following order (Plain Text, No Markdown Headers):

    1.  **Persona & Domain Assumed**: (e.g., "Acting as CTO / Senior Engineering Manager")
    2.  **Overall Fit Summary**: Clear and decisive executive summary (1-2 paragraphs).
    3.  **Key Strengths vs JD**: Bullet points of real strengths.
    4.  **Gaps / Risks**: Honest assessment of what is missing.
    5.  **Final Verdict**: (Strong Fit / Good Fit / Partial Fit / Weak Fit)
    6.  **Optional**: Targeted Improvement Suggestions.

    *Tone:* Professional, Hiring-panel realistic, Honest, Non-inflated.

    --- INPUT DATA ---
    
    JOB DESCRIPTION:
    {jd_text[:2000]}

    CANDIDATE RESUME:
    {resume_text[:2500]}
    """
    
    try:
        stream = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            stream=True 
        )
        return stream
        
    except Exception as e:
        return f"Summary unavailable: {e}"