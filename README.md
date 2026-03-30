# npltk

Nepali Language Processing Toolkit for tokenization, normalization, lemmatization, POS tagging, and NER.

## Public Top-Level API

- `create_tokenizer`
- `Lemmatizer`
- `POSTagger`
- `NERTagger`

## Package Layout

- `src/npltk/tokenizer/`: rule and hybrid tokenizer engines
- `src/npltk/normalizer/`: configurable normalization pipeline
- `src/npltk/lemmatizer/`: dictionary + rule-based lemmatizer
- `src/npltk/pos/`: BiLSTM-CRF POS tagger and model assets
- `src/npltk/ner/`: BiLSTM-CRF NER tagger and model assets
- `src/npltk/stop_word/`: stopword remover

## Installation

```bash
pip install -e .
```

or

```bash
pip install .
```

## Dependencies

- `sentencepiece` for hybrid tokenizer mode
- `torch` for POS/NER inference
- `pytorch-crf` for CRF decoding in POS/NER models

## Quick Start

```python
from npltk import create_tokenizer, Lemmatizer, POSTagger, NERTagger

text = "नेपालको प्रधानमन्त्री काठमाडौं गए।"

# Tokenizer
tok = create_tokenizer(mode="hybrid", fallback_to_rule=True)
tokens = [t.text for t in tok.tokenize(text)]
print(tokens)

# Lemmatizer
lem = Lemmatizer()
print(lem.lemmatize("गयो"))

# POS Tagger
pos = POSTagger()
print(pos.tag_with_tokens(tokens))

# NER Tagger
ner = NERTagger(tokenizer_mode="hybrid")
print(ner.tag(text))
print(ner.extract(text))
```

## Formatted Examples

### 1) Lemmatizer Example

```python
from npltk import Lemmatizer

lemmatizer = Lemmatizer()
words = ["गयो", "घरहरूमा", "किताबबाट"]
lemmas = lemmatizer.lemmatize_many(words)

print("Lemmatizer Output")
print("-----------------")
for w, l in zip(words, lemmas):
    print(f"{w:12} -> {l}")
```

### 2) Stop Word Removal Example

```python
from npltk import create_tokenizer
from npltk.stop_word.remover import StopWordRemover

text = "नेपाल सुन्दर देश हो र यहाँ धेरै हिमाल छन् ।"
tokenizer = create_tokenizer(mode="rule")
tokens = tokenizer.tokenize(text)

remover = StopWordRemover()
filtered, info = remover.remove(tokens)

print("Original Tokens:", [t.text for t in tokens])
print("Filtered Tokens:", [t.text for t in filtered])
print("Info:", info)
```

### 3) POS Tagger Example

```python
from npltk import create_tokenizer, POSTagger

text = "नेपालको प्रधानमन्त्री काठमाडौं गए।"
tokenizer = create_tokenizer(mode="hybrid", fallback_to_rule=True)
tokens = [t.text for t in tokenizer.tokenize(text)]

pos = POSTagger()
pairs = pos.tag_with_tokens(tokens)

print("POS Output")
print("----------")
for token, tag in pairs:
    print(f"{token:12} {tag}")
```

### 4) NER Tagger Example

```python
from pprint import pprint
from npltk import NERTagger

text = "शेरबहादुर देउवा काठमाडौं पुगे।"
ner = NERTagger(tokenizer_mode="hybrid")
result = ner.predict(text)

print("Token-Tag Pairs:")
for token, tag in zip(result["tokens"], result["tags"]):
    print(f"{token:12} {tag}")

print("\nExtracted Entities:")
pprint(result["entities"], width=100)
```

### 5) Normalizer Example

```python
from npltk.normalizer import build_normalizer

raw = "  नेपाल।।  "
result = build_normalizer().normalize(raw)

print("Normalized:", result.text)
print("Transforms:")
for tr in result.transforms:
    print(f"- {tr.rule}: {tr.before!r} -> {tr.after!r}")
```

## API Summary

### 1) Tokenizer

Factory:

```python
create_tokenizer(
    *,
    mode: Literal["hybrid", "rule"] = "hybrid",
    split_into_sentences: bool = True,
    keep_punct: bool = True,
    model_path: str | None = None,
    subword: bool = True,
    preprocess: Callable[[str], str] | None = None,
    fallback_to_rule: bool = True,
)
```

Common methods on tokenizer instances:

```python
tokenize(text: str) -> list[Token]
tokenize_sentences(text: str) -> list[TokenizedSentence]
detokenize(tokens: list[Token]) -> str
```

### 2) Lemmatizer

```python
Lemmatizer(
    dictionary_path: str | Path | None = None,
    *,
    cache_size: int = 4096,
    min_root_len: int = 2,
)
```

Methods:

```python
lemmatize(word: str) -> str
lemmatize_many(words: list[str]) -> list[str]
```

### 3) POS Tagger

```python
POSTagger(model_path: str | None = None, device: str | None = None)
```

Methods:

```python
tag(tokens: Sequence[str]) -> list[str]
tag_with_tokens(tokens: Sequence[str]) -> list[tuple[str, str]]
```

### 4) NER Tagger

```python
NERTagger(
    model_path: str | None = None,
    device: str | None = None,
    tokenizer: Any | None = None,
    tokenizer_mode: Literal["hybrid", "rule"] = "hybrid",
)
```

Methods:

```python
predict(text: str) -> dict[str, Any]
tag(text: str) -> list[tuple[str, str]]
extract(text: str) -> list[dict[str, Any]]
```

### 5) Normalizer

Builder:

```python
build_normalizer(cfg: NormalizerConfig | None = None) -> Normalizer
```

Main method:

```python
normalize(text: str) -> NormResult
```

Result fields:

```python
NormResult.text
NormResult.transforms
```

### 6) Stop Word Remover

Constructor:

```python
StopWordRemover(stopword_file: str | None = None)
```

Main method:

```python
remove(tokens: list[Token]) -> tuple[list[Token], dict[str, Any]]
```

Returned info keys typically include:

- removed_words
- removed_count
- changed

## Notes

- If hybrid tokenizer initialization fails and `fallback_to_rule=True`, it falls back to rule tokenizer.
- POS/NER require corresponding model files in `src/npltk/pos/models/` and `src/npltk/ner/models/`.

## Full Package Information

`npltk` is a complete Nepali NLP package that combines preprocessing and sequence tagging tools under one interface.

Included capabilities:

- Tokenization: rule-based and hybrid (SentencePiece-assisted)
- Sentence splitting and detokenization
- Normalization pipeline with configurable rules
- Lemmatization (dictionary + suffix-rule hybrid approach)
- Stop-word removal for Nepali tokens
- POS tagging (BiLSTM-CRF)
- Named Entity Recognition (BiLSTM-CRF)

Suggested workflow in applications:

1. Normalize raw text
2. Tokenize text
3. Optionally remove stop-words
4. Lemmatize remaining tokens
5. Run POS tagging
6. Run NER for entity extraction

### Tokenizer Methods (Detailed)

Factory:

```python
create_tokenizer(
        *,
        mode: Literal["hybrid", "rule"] = "hybrid",
        split_into_sentences: bool = True,
        keep_punct: bool = True,
        model_path: str | None = None,
        subword: bool = True,
        preprocess: Callable[[str], str] | None = None,
        fallback_to_rule: bool = True,
)
```

Method behavior:

- `tokenize(text)`
    - Returns a flat list of `Token` objects.
    - Each token includes text span information (`start`, `end`) and token type.

- `tokenize_sentences(text)`
    - Splits text into sentence blocks and tokenizes each block.
    - Returns `TokenizedSentence` objects with sentence-level boundaries.

- `detokenize(tokens)`
    - Reconstructs string text from token sequence.
    - Useful when building pipelines that temporarily transform tokens.

Hybrid mode notes:

- Uses the packaged SentencePiece model by default.
- If model loading fails and `fallback_to_rule=True`, rule tokenizer is used automatically.

### Full Feature Demonstration

```python
from pprint import pprint

from npltk import create_tokenizer, Lemmatizer, POSTagger, NERTagger
from npltk.normalizer import build_normalizer
from npltk.stop_word.remover import StopWordRemover

text = "  शेरबहादुर देउवा काठमाडौं पुगे र नेपालको बारेमा बोले।  "

print("1) Normalize")
normalizer = build_normalizer()
norm = normalizer.normalize(text)
print("Normalized:", norm.text)

print("\n2) Tokenize")
tokenizer = create_tokenizer(mode="hybrid", fallback_to_rule=True)
tokens = tokenizer.tokenize(norm.text)
token_texts = [t.text for t in tokens]
print(token_texts)

print("\n3) Stop-word removal")
filtered_tokens, info = StopWordRemover().remove(tokens)
filtered_texts = [t.text for t in filtered_tokens]
print(filtered_texts)
print(info)

print("\n4) Lemmatize")
lemmatizer = Lemmatizer()
lemmas = [lemmatizer.lemmatize(t) for t in filtered_texts]
for original, lemma in zip(filtered_texts, lemmas):
        print(f"{original:12} -> {lemma}")

print("\n5) POS")
pos_pairs = POSTagger().tag_with_tokens(token_texts)
for tok, tag in pos_pairs:
        print(f"{tok:12} {tag}")

print("\n6) NER")
ner_result = NERTagger(tokenizer_mode="hybrid").predict(norm.text)
for tok, tag in zip(ner_result["tokens"], ner_result["tags"]):
        print(f"{tok:12} {tag}")

print("\nEntities:")
pprint(ner_result["entities"], width=100)
```

## Version

Current package version: `0.3.0`

## Contributors

This project was started by:

- Anurag Sharma
- Anita Budha Magar
- Apeksha Parajuli
- Apeksha Katwal

Supervisor:

- Pukar Karki

Affiliation:

- Department of Electronics and Computer Engineering
- Institute of Engineering, Purwanchal Campus
