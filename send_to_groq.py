import requests
import json
from legal_ner_script import process_entities
from send_to_roxie import send_to_api, extract_text_from_response
import sys

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

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python send_to_groq.py '<text>' '<user_prompt>'")
        sys.exit(1)

    input_text = sys.argv[1]

    ner_output = process_entities(input_text)

    api_url1 = "http://university-roxie.us-hpccsystems-dev.azure.lnrsg.io:8002/WsEcl/json/query/roxie/roxie_index_search_2"
    combined_texts = ""

    while not combined_texts:
        roxie_response = send_to_api(ner_output, api_url1)
        combined_texts = extract_text_from_response(roxie_response)

    user_prompt = sys.argv[2]
    api_url2 = "https://api.groq.com/openai/v1/chat/completions"
    
    groq_response = send_to_groq(combined_texts, user_prompt, api_url2)

    print(json.dumps({"response": groq_response}, indent=4))
