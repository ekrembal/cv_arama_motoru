from transformers import pipeline, AutoModelForTokenClassification, AutoTokenizer

model = AutoModelForTokenClassification.from_pretrained("savasy/bert-base-turkish-ner-cased")

tokenizer = AutoTokenizer.from_pretrained("savasy/bert-base-turkish-ner-cased")

ner=pipeline('ner', model=model, tokenizer=tokenizer)


def extract_entities(text):
    results = ner(text)
    entitites = []
    for result in results:
        if(result['entity'][0] == 'B'):
            entitites.append(result['word'])
        else:
            entitites[-1] += result['word']
    return entitites

if __name__ == "__main__":
    print(extract_entities("Mustafa Kemal Atatürk 19 Mayıs 1919'da Samsun'a ayak bastı."))