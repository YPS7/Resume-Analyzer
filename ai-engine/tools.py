from duckduckgo_search import DDGS
import re

def get_market_anchors(job_role):
    """
    Fetches a list of 5-10 high-level skill categories for the given role.
    Used to dynamically populate SKILL_ANCHORS.
    """
    if not job_role: return []
    
    print(f"[Search API] Fetching dynamic domain anchors for: {job_role.strip()}...")
    query = f"top technical skill categories keywords for {job_role}"
    
    anchors = set()
    try:
        with DDGS() as ddgs:
            # We look for short lists or bullet points in snippets
            results = ddgs.text(query, max_results=4)
            
            for r in results:
                # Simple extraction: split by commas or newlines
                text = r['body'].lower()
                # Clean up and split
                tokens = re.split(r'[,|;]', text)
                for t in tokens:
                    clean = t.strip()
                    # Keep short phrases (likely skills)
                    if 3 < len(clean) < 25 and "experience" not in clean:
                        anchors.add(clean)
                        
    except Exception as e:
        print(f"[Search API] Error fetching anchors: {e}")
        return []
    
    # Return top 10 distinct anchors to keep it fast
    return list(anchors)[:12]