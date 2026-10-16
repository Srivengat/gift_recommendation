import json
import requests
import re

def rank_gifts_with_llm(user_preferences: dict, gifts: list):
    # Shorten gift list for prompt clarity if needed, but here we only have a few
    gift_list_str = json.dumps(gifts, indent=2)
    
    prompt = f"""
    You are an intelligent gifting recommendation AI.
    
    USER PREFERENCES:
    {json.dumps(user_preferences)}

    AVAILABLE GIFTS DATABASE:
    {gift_list_str}

    TASK:
    Select the 3 most relevant gifts from the AVAILABLE GIFTS DATABASE based on the USER PREFERENCES (relation, occasion, category, budget).
    
    CRITICAL INSTRUCTIONS:
    1. Return ONLY a JSON array of gift_id strings.
    2. Do not include any conversational text, headers, or explanations.
    3. If you can't find 3 perfect matches, pick the closest ones.
    4. Ensure the output is precisely like this: ["id1", "id2", "id3"]
    """

    url = "http://127.0.0.1:11434/api/generate"
    payload = {
        "model": "llama3.1:latest",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.1,
            "num_predict": 100
        }
    }

    try:
        print(f"DEBUG: Calling Ollama with preferences: {user_preferences}")
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()
        content = data.get("response", "").strip()
        print(f"DEBUG: Ollama raw response: {content}")

        # Robust extraction
        match = re.search(r'\[\s*".*?"(?:\s*,\s*".*?")*\s*\]', content, re.DOTALL)
        if match:
             ids = json.loads(match.group(0))
        else:
             # Try simple split if it returned identifiers without brackets
             ids = re.findall(r'[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}', content)
        
        if not ids:
            print("WARNING: No IDs extracted from LLM response.")
            return []
            
        return ids[:3]
             
    except Exception as e:
        print(f"Ollama API Error: {e}")
        return []
