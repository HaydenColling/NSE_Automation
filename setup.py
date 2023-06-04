import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

packages = ['requests', 'beautifulsoup4', 'nltk', 'scikit-learn', 'joblib', 'json']

for package in packages:
    install(package)

import nltk
nltk.download('stopwords')
nltk.download('punkt')
