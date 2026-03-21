## npltk

Nepali Language Processing Toolkit for Python.

This package provides core building blocks for Nepali text processing:

- text normalization pipeline
- sentence and token-level tokenization
- stop-word removal using a Nepali stopword list

## Installation

```bash
pip install npltk
```

## Quick Start

```python
from npltk.tokenizer.tokenizer import NepaliTokenizer
from npltk.stop_word.remover import StopWordRemover

text = "नेपाल एक सुन्दर देश हो।"

tokenizer = NepaliTokenizer()
tokens = tokenizer.tokenize(text)

remover = StopWordRemover()
filtered_tokens, info = remover.remove(tokens)

print(tokens)
print(filtered_tokens)
print(info)
```

## Normalization Example

```python
from npltk.normalizer import build_normalizer

raw = "  नेपाल।।  "
result = build_normalizer().normalize(raw)

print(result.text)
for t in result.transforms:
	print(t.rule, t.before, "->", t.after)
```

## Requirements

- Python 3.7+
- sentencepiece==0.2.0

## License

MIT
