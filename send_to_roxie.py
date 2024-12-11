import requests
import json
from legal_ner_script import process_entities
import sys

def send_to_api(ner_output, api_url):

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic c2thbmRhcHI6RWFWNG5NREFDbUxtYXhRcg=="
    }

    payload = {
        "roxie_index_search_2": {
            "Enter_Words_separated_by_forward_slash": ner_output
        }
    }

    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}

def extract_text_from_response(response):
    texts = []

    try:
        rows = response.get("roxie_index_search_2Response", {}).get("Results", {}).get("result_1", {}).get("Row", [])
        for i, row in enumerate(rows, start=1):
            text = row.get("text", "").strip()
            if text:
                texts.append(f"({i}) {text}\n")
    except AttributeError:
        return "Invalid response format"

    return " ".join(texts)

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Usage: python send_to_api.py '<text>'")
        sys.exit(1)

    input_text = sys.argv[1]

    ner_output = process_entities(input_text)

    api_url = "http://university-roxie.us-hpccsystems-dev.azure.lnrsg.io:8002/WsEcl/json/query/roxie/roxie_index_search_2"

    combined_texts = ''

    while not combined_texts:
        response = send_to_api(ner_output, api_url)
        combined_texts = extract_text_from_response(response)

    print(combined_texts)
