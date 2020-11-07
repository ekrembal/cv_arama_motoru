import os

from flask import Flask, request, render_template, make_response

from ner import extract_entities
from pdf_operations import get_text_from_pdf

api = Flask(__name__)

cv_texts = []

def get_cv_texts():
    for file in os.listdir("cv_ler"):
        if file.endswith(".pdf"):
            filename = os.path.join("cv_ler", file)
            cv_texts.append((filename, get_text_from_pdf(filename)))
            print(cv_texts[-1], '\n\n\n')



@api.route("/cv_goruntule", methods=['POST', 'GET'])
def cv_goruntule():
    filename = request.args.get('cv')
    if id is not None:
        print(os.path.join('cv_ler', filename))
        binary_pdf = open(os.path.join('cv_ler', filename), 'rb').read()
        print(binary_pdf)
        response = make_response(binary_pdf)
        response.headers['Content-Type'] = 'application/pdf'
        response.headers['Content-Disposition'] = \
            'inline; filename=%s.pdf' % 'yourfilename'
        return response

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
        found_entities = []
        cant_found_entities = []
        for entity in entities:
            if(entity.lower() in cv_text):
                score += 1
                found_entities.append(entity)
            else:
                cant_found_entities.append(entity)
        cv_scores.append(( int(100*score/len(entities)), cv_name, found_entities, cant_found_entities))
        # print(found_entities)
    cv_scores = reversed(sorted(cv_scores))
    return render_template('result.html', cv_scores=cv_scores, soru=question)

@api.route('/')
def main_page():
    return render_template('index.html')

if __name__ == "__main__":
    get_cv_texts()
    api.run(debug=True, port=8080)
