import os

from flask import Flask, request, render_template

from ner import extract_entities
from pdf_operations import get_text_from_pdf

api = Flask(__name__)

cv_texts = []

def get_cv_texts():
    for file in os.listdir("cv_ler"):
        if file.endswith(".pdf"):
            filename = os.path.join("cv_ler", file)
            cv_texts.append((filename, get_text_from_pdf(filename)))


@api.route("/search", methods=['POST', 'GET'])
def search():
    question = request.args.get('search')
    entities = extract_entities(question)
    entities = [entity.replace('#', '') for entity in entities]
    print(entities)
    # print(entities)
    cv_scores = []
    for cv_name, cv_text in cv_texts:
        score = 0
        for entity in entities:
            if(entity.lower() in cv_text):
                score += 1
        cv_scores.append(( int(100*score/len(entities)), cv_name))
    return render_template('result.html', cv_scores=cv_scores)

@api.route('/')
def main_page():
    return render_template('index.html')

if __name__ == "__main__":
    get_cv_texts()
    api.run(debug=True, port=8080)
