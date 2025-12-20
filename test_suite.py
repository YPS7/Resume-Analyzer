import processor
import time

# ==========================================
#  TEST DATA REPOSITORY (8 CASES)
# ==========================================

TEST_CASES = [
    {
        "id": 1,
        "name": "Senior Backend (Context Check)",
        "jd": """Senior Backend Engineer (Platform)
We need a seasoned engineer to scale our payments infrastructure.
Requirements:
- 5+ years building distributed systems.
- Experience sharding databases at scale.
- Deep understanding of CAP theorem and consistency models.
- Ability to mentor junior devs.
- Stack: Go, PostgreSQL, Kubernetes.""",
        "resume": """Alex Architect
Experience:
Staff Engineer | Fintech Co.
- Redesigned the core transaction ledger to handle 10k TPS, reducing latency by 40%.
- Split the monolithic database into 4 sharded services to improve availability during peak loads.
- Led the "Engineering Excellence" guild, establishing code review standards for 20+ developers.
- Debugged critical race conditions in the settlement layer.
Skills: System Design, High Availability, Golang, SQL."""
    },
    {
        "id": 2,
        "name": "AI Engineer (AWS vs GCP Transferability)",
        "jd": """AI Engineer (Computer Vision)
Requirements:
- Proficiency in TensorFlow and Keras.
- Experience deploying models on Google Cloud Platform (GCP) using Vertex AI.
- Familiarity with OpenCV.""",
        "resume": """Jordan Vision
Experience:
ML Engineer | SafeCity
- Built and deployed YOLOv8 models for traffic monitoring using PyTorch.
- Automated model training pipelines on AWS SageMaker.
- Optimized inference using TensorRT for edge devices.
Skills: PyTorch, AWS, Docker, Python."""
    },
    {
        "id": 3,
        "name": "Growth Marketing (Domain Mismatch)",
        "jd": """Growth Marketing Manager
Responsibilities:
- Manage $50k/month ad spend on Facebook and Google Ads.
- Run A/B tests on landing pages to improve conversion rates.
- Analyze cohort retention using Mixpanel.""",
        "resume": """Casey Closer
Summary: Top-performing Account Executive with a history of crushing quotas.
Experience:
Sales Manager | SaaS Corp
- Generated $1M in new ARR by closing enterprise deals.
- Managed a pipeline of 50+ prospects in Salesforce.
- Conducted product demos and negotiated contracts.
Skills: CRM, Negotiation, Public Speaking, Salesforce."""
    },
    {
        "id": 4,
        "name": "UI Designer (Generalist vs Expert)",
        "jd": """Senior UI Designer
Requirements:
- Expert in Figma (Components, Auto-layout).
- Strong understanding of iOS Human Interface Guidelines.
- Portfolio demonstrating complex mobile workflows.""",
        "resume": """Sam Sketch
Experience:
Lead Product Designer | AppStudio
- Designed end-to-end mobile apps for 3 startups (iOS & Android).
- Created brand identities, logos, and marketing materials.
- Coded the landing pages using HTML/CSS/Webflow.
- Managed design systems in Sketch and Figma."""
    },
    {
        "id": 5,
        "name": "DevOps (The Proficiency Penalty)",
        "jd": """DevOps Engineer
Requirements:
- Hands-on experience managing K8s in production.
- Infrastructure as Code (Terraform).""",
        "resume": """Riley Rookie
Skills: Kubernetes, Docker, Terraform.
Experience:
Junior Developer | Tech firm
- Learnt Kubernetes by deploying a Hello-World app on Minikube.
- Watched tutorials on Terraform.
- Enthusiastic about DevOps culture."""
    },
    {
        "id": 6,
        "name": "Security (The Dealbreaker - Citizenship)",
        "jd": """Security Analyst
- Must have Top Secret Clearance.
- US Citizenship Required.
- Experience with SIEM tools.""",
        "resume": """Cyber Expert
- 10 years experience with SIEM and Firewalls.
- Citizen of Canada.
- Will require visa sponsorship."""
    },
    {
        "id": 7,
        "name": "Frontend (Acronym Blindness)",
        "jd": """Frontend Dev
- Expertise in SEO (Search Engine Optimization).
- Accessibility (a11y) standards.
- CSR (Client Side Rendering).""",
        "resume": """Web Dev
- Optimized site structure for Google Search rankings.
- Ensured compliance with WCAG 2.1.
- Built Single Page Applications using React."""
    },
    {
        "id": 8,
        "name": "React Dev (Recency Bias)",
        "jd": """Senior React Developer
- Modern React (Hooks, Context API).
- Next.js 13+ (App Router).""",
        "resume": """Dev Manager
- 2020-Present: Engineering Manager (No coding).
- 2016-2018: Senior Dev. Built UI using React.js (Class components).
- 2010-2015: PHP Developer."""
    }
]

# ==========================================
#  TEST RUNNER
# ==========================================

# def run_suite():
#     print("==================================================")
#     print(f"   STARTING AUTOMATED TEST SUITE ({len(TEST_CASES)} CASES)")
#     print("==================================================\n")
    
#     # Pre-load models so we don't reload for every iteration
#     # processor.embedding_model is already loaded on import
    
#     results = []

#     for case in TEST_CASES:
#         print(f"Running Case {case['id']}: {case['name']}...")
        
#         # 1. Run Semantic Analysis
#         embeddings = processor.embedding_model.encode([case['resume'], case['jd']])
#         sem_score = processor.util.cos_sim(embeddings[0], embeddings[1]).item() * 100
        
#         # 2. Run Rule Analysis
#         rule_score, missing = processor.calculate_smart_score(case['jd'], case['resume'])
        
#         # 3. Seniority
#         sen_mult = processor.calculate_seniority_multiplier(case['jd'], case['resume'])
        
#         # 4. Final Score Calc
#         if rule_score > 5:
#             base = (sem_score * 0.3) + (rule_score * 0.7)
#         else:
#             base = sem_score
#         final_score = min(100, round(base * sen_mult, 2))
#         verdict = processor.derive_suitability(final_score)
        
#         results.append({
#             "id": case['id'],
#             "name": case['name'],
#             "score": final_score,
#             "verdict": verdict,
#             "missing": len(missing)
#         })
#         # time.sleep(0.5) # Optional: Pause for readability

#     # ==========================================
#     #  FINAL REPORT CARD
#     # ==========================================
#     print("\n" + "="*80)
#     print(f"{'ID':<4} | {'TEST CASE NAME':<40} | {'SCORE':<8} | {'VERDICT':<20}")
#     print("="*80)
    
#     for r in results:
#         print(f"{r['id']:<4} | {r['name']:<40} | {r['score']:<8} | {r['verdict']:<20}")
    
#     print("="*80)
#     print("Note: Review scores. \n- Case 6 (Dealbreaker) should be LOW (likely failing now).")
#     print("- Case 7 (Acronyms) should be HIGH (likely failing now).")
#     print("- Case 8 (Recency) should be LOW (likely passing now).")

# if __name__ == "__main__":
#     run_suite() 


# ... (imports and TEST_CASES remain same) ...

def run_suite():
    print("==================================================")
    print(f"   STARTING AUTOMATED TEST SUITE ({len(TEST_CASES)} CASES)")
    print("==================================================\n")
    
    results = []

    for case in TEST_CASES:
        print(f"Running Case {case['id']}: {case['name']}...")
        
        # 1. Run Rule Analysis First
        rule_score, missing = processor.calculate_smart_score(case['jd'], case['resume'])
        
        # 2. KILL SWITCH: If dealbreaker, skip semantic entirely
        if "__DEALBREAKER__" in missing:
            final_score = 0.0
            verdict = "Not Suitable (Dealbreaker)"
        else:
            # Only run semantic if dealbreakers passed
            embeddings = processor.embedding_model.encode([case['resume'], case['jd']])
            sem_score = processor.util.cos_sim(embeddings[0], embeddings[1]).item() * 100
            
            sen_mult = processor.calculate_seniority_multiplier(case['jd'], case['resume'])
            
            if rule_score > 5:
                base = (sem_score * 0.3) + (rule_score * 0.7)
            else:
                base = sem_score
            
            final_score = min(100, round(base * sen_mult, 2))
            verdict = processor.derive_suitability(final_score)
        
        results.append({
            "id": case['id'],
            "name": case['name'],
            "score": final_score,
            "verdict": verdict,
            "missing": len(missing)
        })

    print("\n" + "="*80)
    print(f"{'ID':<4} | {'TEST CASE NAME':<40} | {'SCORE':<8} | {'VERDICT':<20}")
    print("="*80)
    for r in results:
        print(f"{r['id']:<4} | {r['name']:<40} | {r['score']:<8} | {r['verdict']:<20}")
    print("="*80)

if __name__ == "__main__":
    run_suite()