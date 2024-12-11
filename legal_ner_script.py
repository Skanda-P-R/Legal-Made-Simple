import spacy
import re
import warnings
import sys

warnings.filterwarnings("ignore")

nlp = spacy.load('en_legal_ner_trf')

def apply_ner(text):
    chunk_size = 50000
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]

    result = []

    for chunk in chunks:
        doc = nlp(chunk)
        for ent in doc.ents:
            result.append({'text': ent.text, 'label': ent.label_})

    return result

def process_entities(text):
    result = apply_ner(text)
    combined_entities = []
    i = 0

    while i < len(result):
        current_entity = result[i]
        if (current_entity['label'] == 'PROVISION' and
            i + 1 < len(result) and
            result[i + 1]['label'] == 'STATUTE'):

            statute_text = re.sub(r'\b\d{4}\b', '', result[i + 1]['text']).strip()
            combined_text = f"{current_entity['text']} {statute_text}"
            combined_entities.append({'text': combined_text, 'label': 'PROVISION_STATUTE'})
            i += 2
        else:
            combined_entities.append(current_entity)
            i += 1

    extracted_string = ''
    for entity in combined_entities:
        if entity['label'] in ['PROVISION_STATUTE', 'STATUTE', 'COURT', 'PRECEDENT', 'PROVISION']:
            extracted_string += entity['text'] + '/'

    return extracted_string

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python legal_ner_script.py '<text>'")
        sys.exit(1)

    input_text = sys.argv[1]
    result = process_entities(input_text)
    print(result)
