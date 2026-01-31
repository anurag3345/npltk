# import sys
# import os

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

# from npltk import NepaliTokenizer

# tokenizer = NepaliTokenizer()

# sentences = [
#     "नेपाल एक सुन्दर देश हो।",
#     "काठमाडौं नेपालको राजधानी हो।",
#     "घरहरूमा धेरै मान्छे बस्छन्।"
# ]

# output_path = "tokenizer_output.txt"

# with open(output_path, "w", encoding="utf-8") as f:
#     for sent in sentences:
#         tokens = tokenizer.tokenize(sent)
#         reconstructed = tokenizer.detokenize(tokens)

#         f.write(f"SENTENCE: {sent}\n")
#         f.write(f"TOKENS:   {tokens}\n")
#         f.write(f"RECON:    {reconstructed}\n\n")

# print(f"Output saved to {output_path}")


from __future__ import annotations

from pathlib import Path

from npltk.normalizer import build_normalizer
from npltk.tokenizer import NepaliTokenizer


OUT_PATH = Path("tokenizer_output.txt")


def main() -> None:
    text = "घरमा नेपालबाट गएँ। अनि school गएँ! मिति २०२६/०१/३१ हो 🙂"

    # --- Normalization ---
    normalizer = build_normalizer()
    norm_result = normalizer.normalize(text)
    norm_text = norm_result.text

    # --- Tokenization ---
    tokenizer = NepaliTokenizer(
        split_into_sentences=True,
        keep_punct=True
    )
    tokenized = tokenizer.tokenize_sentences(norm_text)

    # --- Output formatting ---
    lines = []
    lines.append(f"IN   : {text}")
    lines.append(f"NORM : {norm_text}")
    lines.append("")

    for idx, sent in enumerate(tokenized, start=1):
        lines.append(f"[SENT {idx}] {sent.sentence}  (span={sent.start}:{sent.end})")
        for t in sent.tokens:
            lines.append(f"  - {t.text}\t{t.type.value}\t({t.start},{t.end})")
        lines.append("")

    OUT_PATH.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote: {OUT_PATH}")


if __name__ == "__main__":
    main()
