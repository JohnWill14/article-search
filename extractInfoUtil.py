import re

import nltk


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


