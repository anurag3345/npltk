import sys
import os
import pytest

# Add src folder to path for local run
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from npltk import NepaliTokenizer

def test_tokenizer_basic():
    tokenizer = NepaliTokenizer()
    text = "नेपाल एक सुन्दर देश हो।"
    tokens = tokenizer.tokenize(text)
    reconstructed = tokenizer.detokenize(tokens)

    assert isinstance(tokens, list)
    assert len(tokens) > 0
    assert reconstructed == text

if __name__ == "__main__":
    pytest.main([__file__])
