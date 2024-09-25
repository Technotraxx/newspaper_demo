#!/bin/bash

# Install Python packages
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt')"
