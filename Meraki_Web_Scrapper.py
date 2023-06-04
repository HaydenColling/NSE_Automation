import requests
from bs4 import BeautifulSoup as bs
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.metrics.pairwise import cosine_similarity as cs
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump, load
import json

appliancesDic = {"MX" : 0,"MR" : 0,"MS" : 0,"MG" : 0,"MV" : 0,"MT" : 0,"SM" : 0,"MI" : 0,"Go" : 0,"Firmware" : 0}
synonymsDic = {"MS" : ["Meraki Switch","Switch"], "MV" : ["Meraki Vision","Camera"], "MR" : ["Meraki Router","Router"]}

question = input("Question: ")

for appliance in appliancesDic.keys():
    m = re.search(rf'\b{appliance}',question,re.I)
    if m: 
        print(m.group())
        appliancesDic[appliance] += 1
    else:
        print("No Match")
    
    if appliance in synonymsDic:
        for synonym in synonymsDic[appliance]:
            m = re.search(f'{synonym}',question,re.I)
            if m: 
                appliancesDic[appliance] += 1

for appliance, count in appliancesDic.items():
    if count >= 1:
        print(f"\n{appliance} occurs {count} times")
        with open(f'{appliance}_subWebPages.json','r') as f:
            subWebPages = json.load(f)
        
        # X is a representation of all the subwebsites in each appliance 
        vectorizer = load(f'{appliance}_vectorizer.joblib')
        X = load(f'{appliance}_tfidf_matrix.joblib')

        # Vectorize the question 
        question_vector = vectorizer.transform([question])

        # Get the cosine similarity between the question and Webpages 

        cosine_similarity = cs(question_vector, X).flatten()

        top_doc_indices = cosine_similarity.argsort()[::-1]
        top_matches = [subWebPages[x] for x in top_doc_indices]

        for x in range(0,5):
            print(top_matches[x] + '\n')
