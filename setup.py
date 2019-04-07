import setuptools
import os

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="blackjack",
    version=os.environ.get("VERSION", "0.0.0"),
    author="Anderson Frailey",
    author_email="andersonfrailey@gmail.org",
    description="Library for running blackjack simulations",
    long_description=long_description,
    url="https://github.com/andersonfrailey/blackjack",
    packages=["blackjack"],
    install_requires=["tqdm", "paramtools"],
    tests_require=["pytest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Opperating Sytem :: OS Independent"
    ],
    include_package_data=True
)
