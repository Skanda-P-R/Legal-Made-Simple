from flask import Flask, request, jsonify, send_from_directory, render_template
from legal_ner_script import process_entities
from send_to_groq import send_to_groq
import mysql.connector

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1803",
    database="legal"
)

cursor = mydb.cursor()

app = Flask(__name__)

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

        cursor.execute(f"delete from test_words")
        cursor.execute(f"delete from relevant_text_id")

        extracted_list = extracted_string.split("/")
        
        for i in extracted_list:
            cursor.execute(f"insert into test_words values ('{i}')")

        cursor.execute(f"insert into relevant_text_id select legal_words.text_id, count(legal_words.words) as words_count from legal_words inner join test_words on legal_words.words = test_words.words group by legal_words.text_id order by words_count DESC limit 10")
        cursor.execute(f"select cases.text from cases inner join relevant_text_id on relevant_text_id.text_id = cases.text_id")
        text = cursor.fetchall()
        count = 1
        texts = []
        for i in text:
            texts.append(f"({count}) {i[0][:5000]}\n")
            count+=1
        
        case_statements = " ".join(texts)

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

        cursor.execute(f"delete from test_words")
        cursor.execute(f"delete from relevant_text_id")

        extracted_list = ner_output.split("/")
        
        for i in extracted_list:
            cursor.execute(f"insert into test_words values ('{i}')")

        cursor.execute(f"insert into relevant_text_id select legal_words.text_id, count(legal_words.words) as words_count from legal_words inner join test_words on legal_words.words = test_words.words group by legal_words.text_id order by words_count DESC limit 10")
        cursor.execute(f"select cases.text from cases inner join relevant_text_id on relevant_text_id.text_id = cases.text_id")
        text = cursor.fetchall()
        count = 1
        texts = []
        for i in text:
            texts.append(f"({count}) {i[0][:1000]}\n")
            count+=1
        
        case_statements = " ".join(texts)

        groq_response = send_to_groq(case_statements, user_prompt, GROQ_API_URL)

        return jsonify({"response": groq_response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/static/<path:path>')
def send_static(path):
    return send_from_directory('static', path)

if __name__ == '__main__':
    app.run(debug=True)
