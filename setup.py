import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Add all the packages to the list that you want to install
packages = ['requests', 'beautifulsoup4', 'nltk', 'scikit-learn', 'joblib', 'json']

for package in packages:
    install(package)