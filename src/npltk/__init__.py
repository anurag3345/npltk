"""
npltk - Nepali Language Processing Toolkit
-------------------------------------------
Public API entry points:
- create_tokenizer
- Lemmatizer
- POSTagger
- NERTagger
"""
from .tokenizer.factory import create_tokenizer
from .lemmatizer import Lemmatizer
from .pos import POSTagger
from .ner import NERTagger

__all__ = ["create_tokenizer", "Lemmatizer", "POSTagger", "NERTagger"]

__version__ = "0.3.0"
__author__ = [
    "Anurag Sharma",
    "Anita Budha Magar",
    "Apeksha Parajuli",
    "Apeksha Katwal"
]
__credits__ = [
    "Pukar Karki (Project Supervisor)"
]
