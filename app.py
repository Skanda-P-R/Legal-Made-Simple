from flask import Flask, request, jsonify, send_from_directory, render_template, session
from legal_ner_script import process_entities
from send_to_roxie import send_to_api, extract_text_from_response
from send_to_groq import send_to_groq
import os

app = Flask(__name__)

# Secret key for session management
app.secret_key = os.urandom(24)

ROXIE_API_URL = "http://university-roxie.us-hpccsystems-dev.azure.lnrsg.io:8002/WsEcl/json/query/roxie/roxie_index_search_2"
GROQ_API_URL = "https://api.groq.com/openai/v1/chat/completions"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/extract', methods=['POST'])
def extract_case_statements():
    try:
        data = request.get_json()
        input_text = data.get('sampleCase', '')

        if not input_text:
            return jsonify({"error": "Sample case input is required"}), 400

        extracted_string = process_entities(input_text)

        case_statements = ''
        while not case_statements:
            roxie_response = send_to_api(extracted_string, ROXIE_API_URL)
            case_statements = extract_text_from_response(roxie_response)

        session['case_statements'] = case_statements

        return jsonify({
            "extracted": extracted_string,
            "caseStatements": case_statements
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/submit', methods=['POST'])
def submit_prompt():
    try:
        data = request.get_json()
        input_text = data.get('sampleCase', '')
        user_prompt = data.get('userPrompt', '')

        if not input_text or not user_prompt:
            return jsonify({"error": "Sample case and user prompt inputs are required"}), 400

        ner_output = process_entities(input_text)

        combined_texts = ''

        while not combined_texts:
            response = send_to_api(ner_output, ROXIE_API_URL)
            combined_texts = extract_text_from_response(response)

        groq_response = send_to_groq(combined_texts, user_prompt, GROQ_API_URL)

        return jsonify({"response": groq_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
