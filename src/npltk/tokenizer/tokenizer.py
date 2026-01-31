# import os
# import sentencepiece as spm


# class NepaliTokenizer:
#     """
#     Nepali Tokenizer using SentencePiece.
#     Provides methods to tokenize (encode) and detokenize (decode) Nepali text.

#     Example:
#         tokenizer = NepaliTokenizer()
#         tokens = tokenizer.tokenize("नेपाल एक सुन्दर देश हो।")
#         text = tokenizer.detokenize(tokens)
#     """

#     def __init__(self, model_path=None):
#         """
#         Initialize the tokenizer.

#         Args:
#             model_path (str, optional): Path to the SentencePiece model file (.model).
#                                         If None, loads from the default models folder.
#         """
#         if model_path is None:
#             # Default model path inside package
#             model_path = os.path.join(os.path.dirname(__file__), "models", "nepali_tokenizer.model")

#         if not os.path.exists(model_path):
#             raise FileNotFoundError(f"SentencePiece model not found at: {model_path}")

#         self.sp = spm.SentencePieceProcessor()
#         self.sp.load(model_path)

#     def tokenize(self, text):
#         """
#         Tokenize Nepali text into subword pieces.

#         Args:
#             text (str): Input text in Nepali.
#         Returns:
#             list[str]: List of subword tokens.
#         """
#         return self.sp.encode(text, out_type=str)

#     def detokenize(self, pieces):
#         """
#         Detokenize a list of subword pieces back into a string.

#         Args:
#             pieces (list[str]): List of subword tokens.
#         Returns:
#             str: Reconstructed text.
#         """
#         return self.sp.decode_pieces(pieces)


from __future__ import annotations

from dataclasses import dataclass
from typing import List

from .sentence_splitter import split_sentences, SentenceSpan
from .types import Token
from .word_tokenizer import tokenize_words


@dataclass
class TokenizedSentence:
    sentence: str
    start: int
    end: int
    tokens: List[Token]


class NepaliTokenizer:
    """
    Public tokenizer class for your toolkit.
    """

    def __init__(self, *, split_into_sentences: bool = True, keep_punct: bool = True):
        self.split_into_sentences = split_into_sentences
        self.keep_punct = keep_punct

    def tokenize(self, text: str) -> List[Token]:
        """Tokenize the full text (no sentence grouping)."""
        return tokenize_words(text, keep_punct=self.keep_punct)

    def tokenize_sentences(self, text: str) -> List[TokenizedSentence]:
        """Split sentences then tokenize each sentence, returning global spans."""
        if not self.split_into_sentences:
            toks = tokenize_words(text, keep_punct=self.keep_punct)
            return [TokenizedSentence(sentence=text, start=0, end=len(text), tokens=toks)]

        spans = split_sentences(text)
        out: List[TokenizedSentence] = []

        for s in spans:
            local_tokens = tokenize_words(s.text, keep_punct=self.keep_punct)

            # shift token spans from sentence-local to global offsets
            global_tokens = [
                Token(t.text, t.start + s.start, t.end + s.start, t.type) for t in local_tokens
            ]

            out.append(TokenizedSentence(sentence=s.text, start=s.start, end=s.end, tokens=global_tokens))

        return out
