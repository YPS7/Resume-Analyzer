import sys
import os
import tools
import processor
import llm_client
import pdf_utils

def get_user_input(prompt_type):
    """
    Handles input for either Resume (PDF/Text) or JD (Text).
    """
    if prompt_type == "resume":
        print("\n--- RESUME INPUT ---")
        choice = input("Enter path to PDF file (or press Enter to paste text): ").strip()
        
        # Option C: PDF Support
        if choice and choice.lower().endswith(".pdf"):
            # Remove quotes if user dragged-and-dropped file
            clean_path = choice.replace('"', '').replace("'", "")
            print(f"[System] Reading PDF: {clean_path}...")
            text = pdf_utils.extract_text_from_pdf(clean_path)
            if text: return text
            print("[System] Fallback to manual paste mode.")
    
    # Default: Text Paste
    print(f"\nPASTE {prompt_type.upper()} TEXT:")
    print("Type 'END' on a new line when finished:")
    lines = []
    while True:
        try:
            line = input()
        except EOFError: break
        if line.strip() == 'END': break
        lines.append(line)
    return "\n".join(lines)

def run_pipeline():
    print("================================================")
    print("   AI RESUME ANALYZER v9.0 (PDF + LLM + ML)")
    print("================================================")
    
    # 1. INPUTS
    jd_text = get_user_input("job description")
    resume_text = get_user_input("resume")

    if not jd_text or not resume_text:
        print("\n[Error] Missing input. Exiting.")
        return

    # 2. MARKET CONTEXT (Dynamic Anchors)
    print("\n[Search Agent] Identifying domain context...")
    job_role = jd_text.split('\n')[0][:50]
    dynamic_anchors = tools.get_market_anchors(job_role)
    processor.update_anchors(dynamic_anchors)
    
    # 3. ML ANALYSIS (The Core Processor)
    print("\n[ML Engine] Running Semantic Audit...")
    
    # A. Semantic Score
    embeddings = processor.embedding_model.encode([resume_text, jd_text])
    sem_score = processor.util.cos_sim(embeddings[0], embeddings[1]).item() * 100
    
    # B. Rule Score (Logic + Penalties)
    rule_score, missing_skills = processor.calculate_smart_score(jd_text, resume_text)
    
    # Dealbreaker Check
    is_dealbreaker = False
    if "__DEALBREAKER__" in missing_skills:
        final_score = 0.0
        verdict = "Not Suitable (Dealbreaker)"
        is_dealbreaker = True
    else:
        # 4. OPTION A: LLM VERIFICATION
        # Only check if there are actual gaps to verify
        if missing_skills and len(missing_skills) > 0:
            print(f"\n[AI Verifier] Double-checking {len(missing_skills)} gaps with LLM...")
            recovered = llm_client.verify_missing_skills(resume_text, missing_skills)
            
            if recovered:
                print(f"   [AI Correction] Recovered skills: {recovered}")
                # Boost score for recovered skills (0.5 points each, capped)
                boost = min(15.0, len(recovered) * 2.5)
                rule_score = min(100, rule_score + boost)
                # Remove from missing list for clarity
                missing_skills = [s for s in missing_skills if s not in recovered]

        # Final Calc
        sen_mult = processor.calculate_seniority_multiplier(jd_text, resume_text)
        if rule_score > 5:
            base = (sem_score * 0.3) + (rule_score * 0.7)
        else:
            base = sem_score
        final_score = min(100, round(base * sen_mult, 2))
        verdict = processor.derive_suitability(final_score)

    # 5. REPORT GENERATION
    print("\n" + "="*50)
    print(f"       ANALYSIS REPORT: {job_role.strip()}")
    print("="*50)
    print(f"Score:   {final_score}%")
    print(f"Verdict: {verdict}")
    if not is_dealbreaker:
        print(f"Gaps:    {missing_skills}")
    print("-" * 50)
    
    # LLM Executive Summary
    if not is_dealbreaker:
        print("\n[AI Agent] Generating Executive Summary...")
        stream = llm_client.generate_human_summary(resume_text, jd_text, final_score, missing_skills)
        
        print("\nEXECUTIVE SUMMARY:\n")
        # Handle both stream and string returns
        if isinstance(stream, str):
            print(stream)
        else:
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    sys.stdout.write(content)
                    sys.stdout.flush()
    print("\n" + "="*50)

if __name__ == "__main__":
    run_pipeline()