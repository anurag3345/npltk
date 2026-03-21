from pathlib import Path
from setuptools import setup, find_packages

BASE_DIR = Path(__file__).parent
README_PATH = BASE_DIR / "README.md"

setup(
    name="npltk",
    version="0.1.0",
    description="Nepali Language Processing Toolkit",
    long_description=README_PATH.read_text(encoding="utf-8") if README_PATH.exists() else "",
    long_description_content_type="text/markdown",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    package_data={
        "npltk.stop_word": ["nepali_stopwords.txt"],
    },
    install_requires=[
        "sentencepiece==0.2.0",
    ],
    python_requires=">=3.7",
    author="NPLTK Contributors",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
    ],
)
