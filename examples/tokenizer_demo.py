import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from npltk import NepaliTokenizer

tokenizer = NepaliTokenizer()

sentences = [
    "नेपाल एक सुन्दर देश हो।",
    "काठमाडौं नेपालको राजधानी हो।",
    "घरहरूमा धेरै मान्छे बस्छन्।"
]

output_path = "tokenizer_output.txt"

with open(output_path, "w", encoding="utf-8") as f:
    for sent in sentences:
        tokens = tokenizer.tokenize(sent)
        reconstructed = tokenizer.detokenize(tokens)

        f.write(f"SENTENCE: {sent}\n")
        f.write(f"TOKENS:   {tokens}\n")
        f.write(f"RECON:    {reconstructed}\n\n")

print(f"Output saved to {output_path}")
