import re

def load_keywords(keywordFile):
    if keywordFile is None:
        return []
    with open(keywordFile, "r", encoding="utf-8") as f:
        return [line.strip().lower() for line in f if line.strip()]
    
def check_success(response_text, keywords):
    if not keywords:
        return None
    
    response_lower = response_text.lower()
    response_clean = re.sub(r'[^a-z0-9]', '', response_lower)
    
    for kw in keywords:
        kw_clean = re.sub(r'[^a-z0-9]', '', kw)
        if kw in response_lower or kw_clean in response_clean:
            return kw
    return None