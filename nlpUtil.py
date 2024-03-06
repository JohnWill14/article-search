import os
from os import listdir

import nltk
from PyPDF2 import PdfReader
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk.collocations import BigramCollocationFinder

import re
import string

import hashlib

from rank_bm25 import BM25Okapi

import numpy

from extractInfoUtil import extractReferences, extractObjective, extractProblem, \
    extractMethodologyByTerms, extractContributes
from fileUtil import readPdf


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


def article(title,numberPages, most_common, objective, problem, method, contributes, references, path):
    h = hashlib.shake_256(title.encode())
    id = h.hexdigest(20)
    return {"id": id, "title": title,"pages":numberPages, "most_common": most_common, "objective": objective, "problem": problem, "method": method,
     "references": references, "contributes":contributes, "path":path}

def prepareTextFromPath(path):
    text = readPdf(path)
    return prepareText(text)

def prepareText(text):
    # token
    tokens = tokenizeText(text)

    # remove stop words
    words_really_importants = removeStopWords(tokens)

    # lemmatize
    lemma = lemmatize(words_really_importants)

    return lemma

def perform(path):
    nltk.download('punkt')
    nltk.download('wordnet')
    print(path)

    # info
    title, numberPages = extractInfoFromPdf(path)

    # read
    text = readPdf(path)
    references = extractReferences(text)
    text = text.replace(references, "")

    # token
    tokens = tokenizeText(text)

    # remove stop words
    words_really_importants = removeStopWords(tokens)

    # freq
    freq = extractFreq(words_really_importants)

    most_common10 = freq.most_common(20)

    # objective
    objective = extractObjective(text)

    # problem
    problem = extractProblem(text)

    # method
    method = extractMethodologyByTerms(text)

    # contributes
    contributes = extractContributes(text)

    return article(title, numberPages, most_common10,objective,problem, method, contributes, references, path)

def process_papers(listdir):
    nltk.download('stopwords')

    cont = 1
    datas = []
    for path in listdir:
        if path.endswith(".pdf"):
            l = perform(path)
            datas.append(l)
    return datas


def searchBm25(query, tokens):
    query = prepareText(query)

    bm25 = BM25Okapi(tokens)
    return list(numpy.array(bm25.get_scores(query)))


def extractInfoFromPdf(path):
    reader = PdfReader(path)
    title = reader.metadata.title
    if title==None or title== "untitled":
        title = clean_text(os.path.basename(path).replace(".pdf",""))
    sizePages = len(reader.pages)
    return title, sizePages
