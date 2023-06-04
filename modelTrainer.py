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
from concurrent.futures import ThreadPoolExecutor

appliances = ["Getting_Started_with_Meraki", "General_Administration", "MX", "MR", "MS", "MG", "MV", "MT", "SM", "MI",
              "Architectures_and_Best_Practices", "Go", "CiscoPlusSecureConnect", "Firmware_Features",
              "Cloud_Monitoring_for_Catalys"]


def process_appliance(appliance):
    url = "https://documentation.meraki.com/" + appliance

    response = requests.get(url)
    if response.status_code == 404:
        return

    print(response)

    soup = bs(response.content, 'html.parser')

    webpages = []

    for link in soup.find_all('a'):
        if f"/{appliance}/" in link.get('href'):
            webpages.append(link.get('href'))

    subWebPages = []
    for url in webpages:
        response = requests.get(url)
        soup = bs(response.content, 'html.parser')
        for link in soup.find_all('a'):
            href = link.get('href')
            if href is not None and f"/{appliance}/" in href and href not in subWebPages and "jp" not in href and "CH" not in href and "https" in href and "china" not in href:
                subWebPages.append(link.get('href'))

    # Go through each Page and collect all the words 
    Words = []
    for link in subWebPages:
        print(link)
        response = requests.get(link)
        soup = bs(response.content, 'html.parser')
        Words.append(soup.get_text())

    stemmer = PorterStemmer()

    # Define the stop words
    stop_words = set(stopwords.words('english'))

    # Clean the text, tokenize it, remove stop words, and stem 
    for x in range(len(Words)):
        #print("Starting on webpage\n")
        # Remove non-alphabetic characters and convert to lower
        Words[x] = re.sub('a-zA-Z', ' ', Words[x].lower())

        # Tokenize
        tokens = word_tokenize(Words[x])

        # Remove stop words and stem the words 
        tokens = [stemmer.stem(token) for token in tokens if token not in stop_words]

        # Join the tokens back into a single string 
        Words[x] = ' '.join(tokens)

    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(Words)

    # Dump Subweb pages to refrence later 
    with open(f'{appliance}_subWebPages.json', 'w') as f:
        json.dump(subWebPages, f)

    # Save the Vectorizer and the TF-IDF matrix
    dump(vectorizer, f'{appliance}_vectorizer.joblib')
    dump(X, f'{appliance}_tfidf_matrix.joblib')


numThreads = input("Enter number of threads [Higher is faster = More resources]: ")

with ThreadPoolExecutor(max_workers=int(numThreads)) as executor:
    executor.map(process_appliance, appliances)