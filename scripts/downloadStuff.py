import nltk
import nltk, re, pprint
from nltk import word_tokenize
import requests
import urllib
import sys

def getSubjects(phrase):
    phrase="\""+phrase+"\""
    query="""PREFIX dbr: <http://dbpedia.org/resource/>
    PREFIX bif:<>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX dbo: <http://dbpedia.org/ontology/>
    PREFIX rdf:<http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX dbpedia-owl: <http://dbpedia.org/ontology/>
    PREFIX foaf: <http://xmlns.com/foaf/0.1/> 
    SELECT DISTINCT * WHERE 
    {
     ?s rdfs:label ?label .
     ?sub ?p ?s .
     FILTER (CONTAINS(lcase(?label),"""+phrase+"""))
    }"""
    q=urllib.pathname2url(query)
    return queryLocalDB(q)

def queryLocalDB(q):
    predicateList=[]
    with open(r'/home/anantgupta/Documents/Programming/Projects/situationalAwareness/SAProject/data/predicateList.txt') as f:
        content = f.readlines()
    for x in content:
        x=x[1:-2]
        #print(x)
        predicateList.append(x)
    #predicateList = [x.strip() for x in content] 
    #print(predicateList)
    url = "http://172.16.131.14:3030/da/query"
    #print(q)
    
    payload = "query="+q
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'cache-control': "no-cache",
        'Postman-Token': "681d8312-7fab-40ab-b91d-e1926ad703cd"
        }

    response = requests.request("POST", url, data=payload, headers=headers)
#     print(response.text)
#     print(response.json().keys())
#     print(response.json()['results']['bindings'])
#     print('I am in query function')
#     print(len(response.json()['results']['bindings']))
    subjects=[]
    superSubjects=[]
    for i in response.json()['results']['bindings']:
        #print('here we go')
        #print(i['s']['value'])
        #print(i['sub']['value'])
        #print(i['p']['value'])
        if i['p']['value'] in predicateList:
            #print('hello, hi')
            #print(i['p']['value'])
            subjects.append(i['s']['value'])
            superSubjects.append(i['sub']['value'])
    #print('subjects')
    #print(subjects)
    return subjects,superSubjects

#to preprocess query :
# stop words removal
# NER
#Nouns phrases
#nouns
#verbs

def parseChunking(parser, postags):
    chunked = parser.parse(postags)
#     print(type(chunked))
#     print(type(postags))
    for subtree in chunked.subtrees():
        print(subtree)
    phrases=[]
    for subtree in chunked.subtrees(filter=lambda t: t.label() == 'Chunk'):
        np=''
#         print(subtree)
        for s in subtree:
#             print(s[0], s[1])
            np=np+s[0]+' '
        phrases.append(np.rstrip())    
    return phrases
    

def queryPreprocessing(query):
    phraseList=[]
    tokens = word_tokenize(query)
    postags=nltk.pos_tag(tokens)
#     print(postags)
    #chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
    chunkGram = r"""Chunk: {<RB.?>*<VB.?>*<NN>+<NNS>?}"""
    chunkGram2 = r"""Chunk: {<RB.?>*<VB.?>*<NNP>+<NN>?}"""
    chunkParser = nltk.RegexpParser(chunkGram)
    chunkParser2 = nltk.RegexpParser(chunkGram2)
    phraseList.extend(parseChunking(chunkParser,postags))
    phraseList.extend(parseChunking(chunkParser2,postags))
    return phraseList
        
    
def main():
    phrases =queryPreprocessing('services industry in america')
    subjects=[]
    print(phrases)
    for phrase in phrases:
        if len(phrase)>3:
            print(phrase)
            subjects, superSubjects=getSubjects(phrase.lower())
        #subjects.append(getSubjects(phrase.lower()))
    print(len(set(subjects)))
    print(len(set(superSubjects)))
