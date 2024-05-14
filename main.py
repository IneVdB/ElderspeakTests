from collections import Counter
import spacy
import re
import os

with open('geen_verkleinwoorden.txt', 'r', encoding='utf-8') as f:
    geen_verkleinwoorden = f.read().splitlines()

with open('nietszeggendewoorden.txt', 'r', encoding='utf-8') as f:
    nietzeggendewoorden = f.read().splitlines()

with open('tussenwerpsels.txt', 'r', encoding='utf-8') as f:
    tussenwerpels_woorden = f.read().splitlines()

with open('new_tussenwerpsels.txt', 'r', encoding='utf-8') as f:
    new_tussenwerpsels = f.read().splitlines()


def pos_count(text):

    nlp = spacy.load("nl_core_news_lg")

    doc = nlp(text)

    tussenwerpsels = []
    verkleinwoorden = []
    collectieve_voornaamwoorden = []

    for token in doc:
        if "dim" in token.tag_ and token.text not in geen_verkleinwoorden:
            verkleinwoorden.append(token.text.lower())
        elif "TSW" in token.tag_ or token.text.lower() in new_tussenwerpsels:
            tussenwerpsels.append(token.text.lower())
        elif "VNW" in token.tag_ and "1|mv" in token.tag_:
            collectieve_voornaamwoorden.append(token.text.lower())

    dimdict = dict(Counter(verkleinwoorden))
    twdict = dict(Counter(tussenwerpsels))
    cvdict = dict(Counter(collectieve_voornaamwoorden))


    print(dimdict)
    print(twdict)
    print(cvdict)



def make_array_words(text):
    text = re.sub(r'\s{2,}', '', text.lower())
    text = re.sub(r'[^\w\s]', '', text)
    words = text.split()
    return words


def old_verkleinwoorden(text):
    verkleinwoorden_array = []
    words = make_array_words(text)
    for word in words:
        if word is not None:
            if (len(word) > 3 and word not in geen_verkleinwoorden) and (
                    word.endswith('je') or word.endswith('ke') or word.endswith('kes') or word.endswith('jes')):
                verkleinwoorden_array.append(word)
    dimdict = dict(Counter(verkleinwoorden_array))
    return dimdict


def old_tussenwerpsels(text):
    tussenwerpsels_array = []
    words = make_array_words(text)
    for word in words:
        if word is not None and word in tussenwerpels_woorden:
            tussenwerpsels_array.append(word)
    c = dict(Counter(tussenwerpsels_array))
    return c


def old_collectieve_voornaamwoorden(text):
    collectieve_voornaamwoorden_array = []
    words = make_array_words(text)
    for word in words:
        if word is not None and word == "we":
            collectieve_voornaamwoorden_array.append(word)
    c = dict(Counter(collectieve_voornaamwoorden_array))
    return c


def compare_all_files():
    directory = 'transcripties'

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)

        if os.path.isfile(f):
            with open(f, "r", encoding="utf-8") as file:
                text = file.read()
                print("BESTAND:", f)
                print('---------------- NIEUW ----------------')
                pos_count(text)
                print('----------------- OUD -----------------')
                print(old_verkleinwoorden(text))
                print(old_tussenwerpsels(text))
                print(old_collectieve_voornaamwoorden(text))
                print("-----------------------------------------------------------------")


if __name__ == '__main__':
    compare_all_files()
