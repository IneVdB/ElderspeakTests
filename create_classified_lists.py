import spacy
import pandas
import os

with open('geen_verkleinwoorden.txt', 'r', encoding='utf-8') as f:
    geen_verkleinwoorden = f.read().splitlines()

with open('nietszeggendewoorden.txt', 'r', encoding='utf-8') as f:
    nietzeggendewoorden = f.read().splitlines()

with open('tussenwerpsels.txt', 'r', encoding='utf-8') as f:
    tussenwerpels_woorden = f.read().splitlines()

with open('new_tussenwerpsels.txt', 'r', encoding='utf-8') as f:
    new_tussenwerpsels = f.read().splitlines()

def new_tag_words(text):
    nlp = spacy.load("nl_core_news_lg")

    doc = nlp(text)

    classified = []

    for token in doc:
        if token.text is not None:
            if "dim" in token.tag_ and token.text not in geen_verkleinwoorden:
                classified.append([token.text, "VKW"])
            elif "TSW" in token.tag_ or token.text.lower() in new_tussenwerpsels:
                classified.append([token.text, "TSW"])
            elif "VNW" in token.tag_ and "1|mv" in token.tag_:
                classified.append([token.text, "CVNW"])
            else:
                classified.append([token.text, "NONE"])

        else:
            classified.append([token.text, "NONE"])

    return classified


def old_tag_words(text):
    nlp = spacy.load("nl_core_news_lg")
    doc = nlp(text)
    classified = []
    for token in doc:
        word = token.text
        if word is not None:
            if (len(word) > 3 and word not in geen_verkleinwoorden) and (
                    word.endswith('je') or word.endswith('ke') or word.endswith('kes') or word.endswith('jes')):
                classified.append([word, "VKW"])
            elif word in tussenwerpels_woorden:
                classified.append([word, "TSW"])
            elif word == "we":
                classified.append([word, "CVNW"])
            else:
                classified.append([word, "NONE"])
        else:
            classified.append([word, "NONE"])

    return classified


if __name__ == '__main__':

    directory = 'transcripties'

    #clear files first
    open('tagged_csv/predict_new.csv', 'w').close()
    open('tagged_csv/predict_old.csv', 'w').close()

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        if os.path.isfile(f):
            with open(f, "r", encoding="utf-8") as file:
                text = file.read()
            print("processing file ", f)
            pd = pandas.DataFrame(new_tag_words(text))
            pd.to_csv("tagged_csv/predict_new.csv", mode='a', index=False, header=False)

            pd = pandas.DataFrame(old_tag_words(text))
            pd.to_csv("tagged_csv/predict_old.csv", mode='a', index=False, header=False)
