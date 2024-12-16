import requests
from legal_ner_script import process_entities

def send_to_groq(roxie_output, user_prompt, api_url):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer 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"
    }

    payload = {
        "model": "llama3-8b-8192",
        "messages": [
            {"role": "system", "content": "You are an AI that answers questions based on the given Legal article."},
            {"role": "user", "content": "Legal article : " + roxie_output},
            {"role": "user", "content": "Question : " + user_prompt}
        ]
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        response_json = response.json()
        
        content = response_json.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        return content
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

