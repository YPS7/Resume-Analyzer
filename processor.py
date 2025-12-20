import spacy
from spacy.matcher import Matcher
from sentence_transformers import SentenceTransformer, util
import numpy as np
import re

print("[ML Engine] Loading Embedding Models...")
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
nlp = spacy.load("en_core_web_sm")

# ==========================================
# 1. CONFIGURATION
# ==========================================

ACRONYM_MAP = {
    "k8s": "kubernetes",
    "aws": "amazon web services",
    "gcp": "google cloud platform",
    "seo": "search engine optimization",
    "a11y": "accessibility",
    "ci/cd": "continuous integration",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "ui": "user interface",
    "ux": "user experience",
    "qa": "quality assurance",
    "nlp": "natural language processing",
    "saas": "software as a service",
    "csr": "client side rendering",
    "ssr": "server side rendering",
    "api": "application programming interface"
}

# FORCE KEEP these words regardless of POS tagging (Noun/Verb distinction)
# This fixes "Go" (Case 1) and "React"/"Hooks" (Case 8)
SHORT_TECH = {
    "go", "r", "c#", "f#", "ui", "ux", "ai", "ml", "qa", "ci", "cd", 
    "js", "db", "net", "csr", "ssr", "seo", "api", "llm",
    "react", "vue", "angular", "node", "next", "nuxt", "cloud",
    "hooks", "redux", "context", "docker", "git", "linux", "jenkins", "bash"
}

DEALBREAKER_PATTERNS = {
    "citizenship": ["visa sponsorship", "h1b", "requires sponsorship", "citizen of canada", "citizen of india"],
    "clearance": ["no clearance", "cannot obtain clearance"],
    "us citizen": ["visa", "sponsorship"]
}

STOP_CONCEPTS = {
    'experience', 'requirements', 'responsibilities', 'role', 'candidate',
    'work', 'team', 'communication', 'skills', 'qualification', 'degree',
    'bachelor', 'master', 'phd', 'job', 'description', 'knowledge',
    'understanding', 'proficiency', 'year', 'years', 'employment',
    'strong', 'proven', 'track', 'record', 'ability', 'scientist', 'researcher',
    'engineer', 'developer', 'intern', 'manager', 'lead', 'seasoned',
    'hands-on', 'familiarity', 'grasp', 'way', 'environment', 'tasks',
    'expert', 'code', 'production', 'guidelines', 'workflows', 'auto', 'app',
    'systems', 'models', 'platform', 'backend', 'data', 'google', 'search',
    'building', 'devs', 'standards', 'expertise', 'interface', 'user',
    'stack', 'scale', 'month', 'spend'
}

DEFAULT_ANCHORS = [
    "programming language", "software tool", "computer framework", 
    "database system", "cloud platform", "technical skill", 
    "operating system", "software library", "machine learning model",
    "marketing channel", "design tool", "business software",
    "security tool", "web standard", "certification"
]

SKILL_ANCHORS = DEFAULT_ANCHORS
ANCHOR_EMBEDDINGS = embedding_model.encode(SKILL_ANCHORS, convert_to_tensor=True)

SENIORITY_RANKS = {
    'intern': 1, 'trainee': 1, 'junior': 2, 'entry': 2, 'associate': 2, 
    'mid': 3, 'developer': 3, 'engineer': 3, 'senior': 4, 'lead': 5, 
    'staff': 5, 'principal': 6, 'architect': 6, 'manager': 6, 'head': 7
}

# ==========================================
# 2. ROBUST EXTRACTION
# ==========================================

def normalize_text(text):
    text = text.lower()
    for acronym, expanded in ACRONYM_MAP.items():
        pattern = r'\b' + re.escape(acronym) + r'\b'
        text = re.sub(pattern, expanded, text)
    return text

def check_dealbreakers(jd_text, resume_text):
    jd_lower = jd_text.lower()
    res_lower = resume_text.lower()
    for req_key, bad_flags in DEALBREAKER_PATTERNS.items():
        if req_key in jd_lower:
            for flag in bad_flags:
                if flag in res_lower:
                    print(f"   [Dealbreaker] JD requires '{req_key}' but Resume has '{flag}'.")
                    return True 
    return False

def get_compound_skills(text):
    matcher = Matcher(nlp.vocab)
    patterns = [
        [{"POS": "PROPN"}, {"POS": "PROPN"}], 
        [{"POS": "PROPN"}, {"POS": "NOUN"}],  
        [{"POS": "NOUN"}, {"POS": "NOUN"}],
        # Special catch for things like "Next.js", "Node.js" which split on "."
        [{"TEXT": {"REGEX": r"^[a-zA-Z0-9]+\.js$"}}], 
        [{"TEXT": "Next"}, {"TEXT": "."}, {"TEXT": "js"}],
        [{"TEXT": "Node"}, {"TEXT": "."}, {"TEXT": "js"}],
        [{"LOWER": "c"}, {"TEXT": "++"}], 
        [{"TEXT": "."}, {"LOWER": "net"}],
        [{"POS": "ADJ"}, {"POS": "NOUN"}]
    ]
    matcher.add("TECH_PHRASE", patterns)
    doc = nlp(text)
    matches = matcher(doc)
    compounds = set()
    for match_id, start, end in matches:
        span = doc[start:end]
        clean = re.sub(r'[^\w\s\.\+\#]', '', span.text.lower())
        if any(w in STOP_CONCEPTS for w in clean.split()): continue
        if len(clean) > 2:
            compounds.add(clean)
    return compounds

def is_technical_term(term):
    if term in STOP_CONCEPTS: return False
    if term in SHORT_TECH: return True
    if len(term.split()) > 3: return False 
    
    term_vec = embedding_model.encode(term, convert_to_tensor=True)
    cosine_scores = util.cos_sim(term_vec, ANCHOR_EMBEDDINGS)
    return float(cosine_scores.max()) > 0.35

def extract_entities(text):
    text = normalize_text(text)
    compounds = get_compound_skills(text)
    doc = nlp(text)
    singles = set()
    
    for token in doc:
        clean = token.text.lower().strip()
        # 1. Force Keep Whitelist
        if clean in SHORT_TECH:
            singles.add(clean)
            continue
            
        # 2. Standard Filter
        if token.pos_ in ["PROPN", "NOUN"] and not token.is_stop:
            if len(clean) > 2 and clean not in STOP_CONCEPTS:
                singles.add(clean)

    candidates = compounds.union(singles)
    valid_skills = set()
    for cand in candidates:
        if is_technical_term(cand):
            valid_skills.add(cand)
            
    sorted_skills = sorted(list(valid_skills), key=len, reverse=True)
    final_skills = []
    for i, skill in enumerate(sorted_skills):
        is_substring = False
        for longer_skill in sorted_skills[:i]:
            if skill in longer_skill: 
                is_substring = True
                break
        if not is_substring:
            final_skills.append(skill)
            
    return set(final_skills)

def chunk_resume(resume_text):
    resume_text = normalize_text(resume_text)
    doc = nlp(resume_text)
    return [sent.text.strip() for sent in doc.sents if len(sent.text.strip()) > 5]

def detect_proficiency_penalty(skill, resume_text):
    pattern = r"((learnt|watched|studied|basics of|exposure to).{0,20}" + re.escape(skill) + r")"
    match = re.search(pattern, resume_text.lower())
    if match:
        print(f"   [Proficiency Check] Weak context detected for '{skill}'.")
        return 0.25 
    return 1.0

# ==========================================
# 3. HYBRID SCORING ENGINE
# ==========================================

def calculate_smart_score(jd_text, resume_text):
    # A. Dealbreaker Check (Preserves Case 6)
    if check_dealbreakers(jd_text, resume_text):
        return 0.0, ["__DEALBREAKER__"]

    targets = extract_entities(jd_text)
    if not targets: return 0.0, []
    
    print(f"   [Debug] Targets: {list(targets)[:10]}...")

    resume_lower = resume_text.lower()
    evidence_chunks = chunk_resume(resume_text)
    
    evidence_embeddings = None
    if evidence_chunks:
        evidence_embeddings = embedding_model.encode(evidence_chunks, convert_to_tensor=True)

    matched_score = 0
    missing_items = []
    
    for target in targets:
        # 1. EXACT MATCH
        found_exact = False
        # Use regex for short words to avoid "Go" matching "Google"
        if target in SHORT_TECH or len(target) < 4:
             if re.search(r'\b' + re.escape(target) + r'\b', resume_lower):
                 found_exact = True
        elif target in resume_lower:
            found_exact = True
            
        if found_exact:
            # Check Penalty (Preserves Case 5)
            penalty = detect_proficiency_penalty(target, resume_text)
            matched_score += (1.0 * penalty)
            continue 

        # 2. SEMANTIC MATCH
        if evidence_embeddings is not None:
            target_embedding = embedding_model.encode(target, convert_to_tensor=True)
            cos_scores = util.cos_sim(target_embedding, evidence_embeddings)[0]
            best_match = float(cos_scores.max())
            
            if best_match > 0.65: # Semantic (Optimization ~ Optimized)
                matched_score += 0.8 
                continue
            elif best_match > 0.38: # Transfer (AWS ~ GCP)
                matched_score += 0.5 
                continue

        missing_items.append(target)

    final_score = (matched_score / len(targets)) * 100
    return min(100, final_score), missing_items

# ==========================================
# 4. HELPERS
# ==========================================

def calculate_seniority_multiplier(jd_text, resume_text):
    def get_rank(t):
        r = 0
        for w in t.lower().split():
            cl = w.strip(":,.-")
            if cl in SENIORITY_RANKS: r = max(r, SENIORITY_RANKS[cl])
        return r
    jd = get_rank(jd_text[:500])
    res = get_rank(resume_text[:800])
    if jd == 0: return 1.0
    if res >= jd: return 1.25
    elif res > 0 and res < jd: return 0.85
    return 1.0

def derive_suitability(score, mismatch=False):
    if score == 0: return "Not Suitable (Dealbreaker)"
    if score >= 80: return "Highly Suitable"
    if score >= 60: return "Suitable"
    if score >= 45: return "Potentially Suitable"
    return "Not Suitable"
def update_anchors(x): pass