from PyPDF2 import PdfReader

import os
from os import listdir

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.collocations import BigramCollocationFinder

import re
import string

import json

def readPdf(path):
    reader = PdfReader(path)

    number_of_pages = len(reader.pages)

    text = ""
    for i in range(number_of_pages):
        page = reader.pages[i]
        text += page.extract_text()

    return text.strip()

def extractInfoFromPdf(path):
    reader = PdfReader(path)
    title = reader.metadata.title
    if(title==None or title=="untitled"):
        title = clean_text(os.path.basename(path).replace(".pdf",""))
    return title



def tokenizeText(text):
    return word_tokenize(text.lower())


def removeStopWords(tokens):
    english_stopwords = stopwords.words('english')
    wordsWithoutStopWords = [t for t in tokens if t not in english_stopwords]
    wordsClear = [clean_text(w) for w in wordsWithoutStopWords]
    return [w for w in wordsClear if w != '']


def clean_text(text):
    # remove numbers
    text_nonum = re.sub(r'\d+', '', text)
    # remove punctuations and convert characters to lower case
    text_nopunct = "".join([char for char in text_nonum if char not in string.punctuation])
    return text_nopunct.strip()


def stemming(tokens):
    ans = []
    ps = PorterStemmer()
    for w in tokens:
        ans.append(ps.stem(w))
    return ans


def lemmatize(tokens):
    ans = []
    wnl = WordNetLemmatizer()
    for w in tokens:
        ans.append(wnl.lemmatize(w))
    return ans


def extractFreq(tokens):
    return nltk.FreqDist(tokens)


def extractReferences(text):
    refrences = "".join(re.findall("(?s)REFERENCES(.*)", text)).strip()
    index = refrences.rfind(".")
    return refrences[0:index + 1]

def extractAbstract(text):
    find_abstract = text.find("Abstract")
    find_keywords = text.find("I.")
    return text[find_abstract:find_keywords]

def extractIntro(text):
    find_abstract = text.find("I.")
    find_keywords = text.find("II.")
    return text[find_abstract:find_keywords]
def extractObjectiveByTerms(text):
    word_keys =[
        'this work',
        'paper describe',
        'This paper explain',
        'This article explain',
        "This paper describe",
        'article describe',
        'This work explain',
        'work describe',
        'This work propose',
        'This paper propose',
        'This article propose',
        'This study',
        'In this paper'
    ]
    word_keys = [w.lower() for w in word_keys]
    sent_text = nltk.sent_tokenize(text.lower())
    for sentence in sent_text:
        s = sentence.replace('\n', "")
        if any(substring in s for substring in word_keys):
            return s
    return "not found"

def extractObjective(text):
    abstract = extractAbstract(text)
    objective = extractObjectiveByTerms(abstract).replace("abstract", "")

    if objective == "not found":
        intro = extractIntro(text)
        return  extractObjectiveByTerms(intro).replace("abstract", "")

    return objective

def extractProblemByTerms(text):
    word_keys =[
        'this issue',
        'this problem',
        'issue',
        'problem',
        'Challenge',
        'Dilemma',
        'Impasse',
        'Difficulty',
        'Barrier',
        'Hurdle',
        'Conundrum'
    ]
    word_keys = [w.lower() for w in word_keys]
    sent_text = nltk.sent_tokenize(text.lower())
    for sentence in sent_text:
        s = sentence.replace('\n', "")
        if any(substring in s for substring in word_keys):
            return s
    return "not found"

def extractProblem(text):
    abstract = extractAbstract(text)
    problem = extractProblemByTerms(abstract).replace("abstract", "")

    if problem == "not found":
        intro = extractIntro(text)
        return  extractProblemByTerms(intro).replace("abstract", "")

    return problem


def extractMethodologyByTerms(text):
    word_keys =[
        'Based on',
        'approach is'
        'method',
        'methodology',
        'interviews',
        'survey',
        'content',
        'analysis'
    ]
    word_keys = [w.lower() for w in word_keys]
    sent_text = nltk.sent_tokenize(text.lower())
    for sentence in sent_text:
        s = sentence.replace('\n', "")
        if any(substring in s for substring in word_keys):
            return s
    return "not found"

def extractMethodology(text):
    return  extractMethodologyByTerms(text)

def article(title, most_common, objective, problem, method, references):
    return {"title": title, "most_common": most_common, "objective": objective, "problem": problem, "method": method,
     "references": references}
def perform(path):
    print(path)

    # info
    title = extractInfoFromPdf(path)
    print(title)
    # read
    text = readPdf(path)
    references = extractReferences(text)  # import
    text = text.replace(references, "")

    # token
    tokens = tokenizeText(text)

    # remove stop words
    words_really_importants = removeStopWords(tokens)

    # lemmatize
    lemma = lemmatize(words_really_importants)

    # stemming
    ws = stemming(lemma)

    # freq
    freq = extractFreq(ws)

    most_common10 = freq.most_common(20)  # import

    # bigrama
    bigram_measures = nltk.collocations.BigramAssocMeasures()
    finder_bigram = BigramCollocationFinder.from_words(ws)

    # print(finder_bigram.nbest(bigram_measures.pmi, 10))

    # objective

    objective = extractObjective(text)

    # problem

    problem = extractProblem(text)

    # method
    method = extractMethodologyByTerms(text)

    return article(title, most_common10,objective,problem, method, references)

if __name__ == '__main__':
    nltk.download('stopwords')

    pathDir = "/home/johnwill14/PycharmProjects/pythonProject/papers/Artigos IEEE - Forense"
    listdir = listdir(pathDir)

    cont = 1
    infos = []
    for filename in listdir:

        if filename.endswith(".pdf"):
            path = pathDir + os.sep + filename

            l = perform(path)
            output = json.dumps(l)
            infos.append(output)
    FILE_PATH = './data.txt'

    with open(FILE_PATH, 'w') as output_file:
            json.dump(infos, output_file, indent=2)