## npltk

Nepali Language Processing Toolkit for Python.

This package provides core building blocks for Nepali text processing:

- text normalization pipeline
- sentence and token-level tokenization (rule + hybrid)
- lemmatization (dictionary + suffix-rule based)
- stop-word removal using a Nepali stopword list

## Installation

```bash
pip install npltk
```

For local development:

```bash
pip install -e .
```

## Quick Start

```python
from npltk import create_tokenizer, Lemmatizer
from npltk.stop_word.remover import StopWordRemover

text = "नेपाल एक सुन्दर देश हो।"

tokenizer = create_tokenizer(mode="hybrid")
tokens = tokenizer.tokenize(text)

remover = StopWordRemover()
filtered_tokens, info = remover.remove(tokens)

lemmatizer = Lemmatizer()
lemmas = [lemmatizer.lemmatize(t.text) for t in filtered_tokens]

print([t.text for t in tokens])
print([t.text for t in filtered_tokens])
print(lemmas)
print(info)
```

## Tokenizer Methods

Main constructor:

- `create_tokenizer(mode="hybrid" | "rule", split_into_sentences=True, keep_punct=True, model_path=None, subword=True, preprocess=None, fallback_to_rule=True)`

Main methods:

- `tokenize(text)`
- `tokenize_sentences(text)`
- `detokenize(tokens)`

Hybrid mode uses the packaged SentencePiece model file in:

- `src/npltk/tokenizer/models/nepali_tokenizer.model`

If hybrid initialization fails and `fallback_to_rule=True`, it automatically falls back to the rule tokenizer.

## Normalization Example

```python
from npltk.normalizer import build_normalizer

raw = "  नेपाल।।  "
result = build_normalizer().normalize(raw)

print(result.text)
for t in result.transforms:
    print(t.rule, t.before, "->", t.after)
```

## Lemmatizer Methods

Main class:

- `Lemmatizer(dictionary_path=None, cache_size=4096, min_root_len=2)`

Main methods:

- `lemmatize(word)`
- `lemmatize_many(words)`

Compatibility alias:

- `HybridLemmatizer`

## Stopword Methods

Class:

- `StopWordRemover(stopword_file=None)`

Method:

- `remove(tokens)`

## Requirements

- Python 3.7+
- sentencepiece

## License

MIT
