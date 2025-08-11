import os
import sentencepiece as spm


class NepaliTokenizer:
    """
    Nepali Tokenizer using SentencePiece.
    Provides methods to tokenize (encode) and detokenize (decode) Nepali text.

    Example:
        tokenizer = NepaliTokenizer()
        tokens = tokenizer.tokenize("नेपाल एक सुन्दर देश हो।")
        text = tokenizer.detokenize(tokens)
    """

    def __init__(self, model_path=None):
        """
        Initialize the tokenizer.

        Args:
            model_path (str, optional): Path to the SentencePiece model file (.model).
                                        If None, loads from the default models folder.
        """
        if model_path is None:
            # Default model path inside package
            model_path = os.path.join(os.path.dirname(__file__), "models", "nepali_tokenizer.model")

        if not os.path.exists(model_path):
            raise FileNotFoundError(f"SentencePiece model not found at: {model_path}")

        self.sp = spm.SentencePieceProcessor()
        self.sp.load(model_path)

    def tokenize(self, text):
        """
        Tokenize Nepali text into subword pieces.

        Args:
            text (str): Input text in Nepali.
        Returns:
            list[str]: List of subword tokens.
        """
        return self.sp.encode(text, out_type=str)

    def detokenize(self, pieces):
        """
        Detokenize a list of subword pieces back into a string.

        Args:
            pieces (list[str]): List of subword tokens.
        Returns:
            str: Reconstructed text.
        """
        return self.sp.decode_pieces(pieces)
