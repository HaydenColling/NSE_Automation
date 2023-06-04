import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])
    if package is "nltk":
        import nltk
        nltk.download('stopwords')

packages = ['requests', 'beautifulsoup4', 'nltk', 'scikit-learn', 'joblib', 'json']

for package in packages:
    install(package)

import nltk
nltk.download('stopwords')
