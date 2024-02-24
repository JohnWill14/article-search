from PyPDF2 import PdfReader

import os
from os import listdir

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.stem import 	WordNetLemmatizer

import re
import string


def readPdf(path):
    reader = PdfReader(path)

    number_of_pages = len(reader.pages)

    text = ""

    for i in range(number_of_pages):
        page = reader.pages[i]
        text += page.extract_text()

    return text.strip()


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
    return text_nopunct

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
    return refrences[0:index+1]

if __name__ == '__main__':
    nltk.download('stopwords')

    pathDir = "/home/johnwill14/PycharmProjects/pythonProject/papers/Artigos IEEE - Forense"
    listdir = listdir(pathDir)
    path = pathDir + os.sep + listdir[3]

    # # read
    # text = readPdf(path)
    # references = extractReferences(text)
    # text = text.replace(references, "")
    #
    # # token
    # tokens = tokenizeText(text)
    #
    # # remove stop words
    # words_really_importants = removeStopWords(tokens)
    #
    # # lemmatize
    # lemma = lemmatize(words_really_importants)
    #
    # # stemming
    # ws = stemming(lemma)
    #
    # # freq
    # freq = extractFreq(ws)
    #
    # most_common10 = freq.most_common(10)
    #
    # for key in most_common10:
    #     print(key)

    cont = 1
    for filename in listdir:

        if filename.endswith(".pdf"):
            path = pathDir +os.sep+ filename

            # read
            text = readPdf(path)
            references = extractReferences(text)
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

            most_common10 = freq.most_common(10)

            print("PDF: ", cont)
            cont+=1
            for key in most_common10:
                print(key)
