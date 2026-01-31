from setuptools import setup, find_packages

setup(
    name="npltk",
    version="0.1.0",
    description="Nepali Language Processing Toolkit",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "sentencepiece==0.2.0",
    ],
    python_requires=">=3.7",
)
