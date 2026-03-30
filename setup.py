from setuptools import setup, find_packages

setup(
    name="npltk",
    version="0.3.0",
    description="Nepali Language Processing Toolkit",
    author="Anurag Sharma, Anita Budha Magar, Apeksha Parajuli, Apeksha Katwal",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "sentencepiece>=0.1.90,<0.2.0",
        "torch>=2.0",
        "pytorch-crf>=0.7.2",
    ],
    python_requires=">=3.7",
)
