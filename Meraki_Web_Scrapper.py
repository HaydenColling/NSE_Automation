import requests
from bs4 import BeautifulSoup as bs
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
import re
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

appliance = input("Enter Appliance: ")

appliacne = appliance.upper()

url = "https://documentation.meraki.com/" + appliacne

response = requests.get(url)

print(response)

soup = bs(response.content, 'html.parser')

webpages = []

for link in soup.find_all('a'):
    if "/MX/" in link.get('href'): 
        webpages.append(link.get('href'))
        #print(link.get('href'))

subWebPages = []
for url in webpages:
    response = requests.get(url)
    soup = bs(response.content, 'html.parser')
    for link in soup.find_all('a'):
        if "/MX/" in link.get('href') and link.get('href') not in subWebPages and "jp"  not in link.get('href') and "CH"  not in link.get('href') and "https" in link.get('href') and "china" not in link.get('href'):
            subWebPages.append(link.get('href'))

# Go through each Page and collect all the words 
Words = []
for link in subWebPages:
    print(link)
    response = requests.get(link)
    soup = bs(response.content,'html.parser')
    Words.append(soup.get_text())


stemmer = PorterStemmer()

# Define the stop words
stop_words = set(stopwords.words('english'))

# Clean the text, tokenize it, remove stop words, and stem 

for x in range(len(Words)):
    print("Starting on webpage\n")
    # Remove non-alphabetic characters and convert to lower
    Words[x] = re.sub('a-zA-Z',' ',Words[x].lower())

    # Tokenize
    tokens = word_tokenize(Words[x])

    # Remove stop words and stem the words 
    tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]

    # Join the tokens back into a single string 
    Words[x] = ' '.join(tokens)

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(Words)

question = "My DHCP is not working on my MX Device"

question_vector = vectorizer.transform([question])

cosine_similarity = cosine_similarity(question_vector, X).flatten()

top_doc_indices = cosine_similarity.argsort()[::-1]
top_matches = [subWebPages[x] for x in top_doc_indices]

print(top_matches[:5])