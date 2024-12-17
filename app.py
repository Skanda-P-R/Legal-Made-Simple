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

@app.route('/extractwords', methods=['POST'])
def extract_words():
    try:
        cursor.execute(f"DELETE FROM test_words")
        cursor.execute(f"DELETE FROM relevant_text_id")
        mydb.commit()
        data = request.get_json()
        input_text = data.get('sampleCase', '')

        if not input_text:
            return jsonify({"error": "Sample case input is required"}), 400

        extracted_string = process_entities(input_text)

        extracted_list = extracted_string.split("/")
        
        for i in extracted_list:
            cursor.execute(f"INSERT INTO test_words VALUES ('{i}')")
        
        # mydb.commit()

        return jsonify({
            "extracted": extracted_string
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route('/extract', methods=['POST'])
def extract_case_statements():
    try:
        data = request.get_json()
        input_text = data.get('sampleCase', '')

        if not input_text:
            return jsonify({"error": "Sample case input is required"}), 400

        cursor.execute(f"INSERT INTO relevant_text_id SELECT legal_words.text_id, COUNT(legal_words.words) AS words_count FROM legal_words INNER JOIN test_words ON legal_words.words = test_words.words GROUP BY legal_words.text_id ORDER BY words_count DESC LIMIT 10")
        cursor.execute(f"SELECT cases.text FROM cases INNER JOIN relevant_text_id ON relevant_text_id.text_id = cases.text_id")
        text = cursor.fetchall()
        count = 1
        texts = []
        for i in text:
            texts.append(f"({count}) {i[0][:5000]}\n")
            count+=1
        
        case_statements = " ".join(texts)

        return jsonify({
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

        cursor.execute(f"SELECT cases.text FROM cases INNER JOIN relevant_text_id ON relevant_text_id.text_id = cases.text_id")
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
