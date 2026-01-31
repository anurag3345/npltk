from npltk.normalizer import build_normalizer
from pathlib import Path

text = "घरमा   नेपाल\u200Bबाट  गएँ"

normalizer = build_normalizer()
result = normalizer.normalize(text)

# Print to console
print("OUT:", result.text)
for t in result.transforms:
    print("-", t.rule, t.meta)

# ---- write output to ROOT (same level as tokenizer_output.txt) ----
root_dir = Path(__file__).resolve().parents[1]
output_file = root_dir / "normalizer_output.txt"

with output_file.open("w", encoding="utf-8") as f:
    f.write("INPUT:\n")
    f.write(text + "\n\n")

    f.write("NORMALIZED OUTPUT:\n")
    f.write(result.text + "\n\n")

    f.write("TRANSFORMATIONS APPLIED:\n")
    for t in result.transforms:
        f.write(f"- {t.rule}: {t.meta}\n")

print(f"\nSaved output to: {output_file}")
