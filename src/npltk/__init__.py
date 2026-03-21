"""
npltk - Nepali Language Processing Toolkit
-------------------------------------------
Currently includes:
- NepaliTokenizer: Tokenization for Nepali text

Future modules:
- NepaliStemmer
- NepaliLemmatizer
"""

from .tokenizer.tokenizer import NepaliTokenizer

# Placeholder imports for future tools
try:
    from .stemmer.stemmer import NepaliStemmer
except ImportError:
    class NepaliStemmer:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("NepaliStemmer is not implemented yet.")

try:
    from .lemmatizer.lemmatizer import NepaliLemmatizer
except ImportError:
    class NepaliLemmatizer:
        def __init__(self, *args, **kwargs):
            raise NotImplementedError("NepaliLemmatizer is not implemented yet.")

__all__ = ["NepaliTokenizer", "NepaliStemmer", "NepaliLemmatizer"]

__version__ = "0.1.0"
__author__ = [
    "Anurag Sharma",
    "Anita Budha Magar",
    "Apeksha Parajuli",
    "Apeksha Katwal"
]
__credits__ = [
    "Pukar Karki (Project Supervisor)"
]
