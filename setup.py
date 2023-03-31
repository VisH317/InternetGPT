from setuptools import setup, find_packages

VERSION = '0.0.1'
DESCRIPTION = "Internet-augmented ChatGPT"
LONG_DESCRIPTION = "A package that connects ChatGPT to the internet with recursive search in complex internet search spaces"

setup(
    name="internet-gpt",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    author="Vishrut Thoutam",
    author_email="vt201916384@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "selenium", 
        "openai", 
        "webdriver-manager",
        "fastapi[all]",
        "pytest",
        "nltk",
        "python-dotenv",
        "matplotlib",
        "plotly",
        "pandas",
        "scipy",
        "numpy",
        "scikit-learn",
        "tiktoken"
    ],
    classifiers= [
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        'License :: OSI Approved :: MIT License',
        "Programming Language :: Python :: 3",
    ]
)