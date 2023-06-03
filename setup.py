import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# All the packages that are required
packages = ['requests', 'beautifulsoup4', 'nltk', 'scikit-learn', 'joblib', 'json']

for package in packages:
    install(package)
