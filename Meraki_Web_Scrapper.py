import requests
from bs4 import BeautifulSoup as bs
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump, load
import json

appliances = ["Getting_Started_with_Meraki","General_Administration","MX","MR","MS","MG","MV","MT","SM","MI","Architectures_and_Best_Practices","Go","CiscoPlusSecureConnect","Firmware_Features","Cloud_Monitoring_for_Catalys"]

appliance = input("Enter appliance: ")
with open(f'{appliance}_subWebPages.json','r') as f:
    subWebPages = json.load(f)

vectorizer = load(f'{appliance}_vectorizer.joblib')
X = load(f'{appliance}_tfidf_matrix.joblib')

# Enter Question and Vectorize it 
question = "What are the highlights of the MV93 camera? What are the specifications? What is the datasheets?"

question_vector = vectorizer.transform([question])

# Get the cosine similarity between the question and Webpages 

cosine_similarity = cosine_similarity(question_vector, X).flatten()

top_doc_indices = cosine_similarity.argsort()[::-1]
top_matches = [subWebPages[x] for x in top_doc_indices]

print(top_matches[:5])