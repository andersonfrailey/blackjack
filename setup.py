import setuptools
import os

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="py21",
    version=os.environ.get("VERSION", "1.6.0"),
    author="Anderson Frailey",
    author_email="andersonfrailey@gmail.org",
    description="Library for running blackjack simulations",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andersonfrailey/blackjack",
    packages=["py21"],
    install_requires=["tqdm", "paramtools", "pandas"],
    tests_require=["pytest"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License"
    ],
    include_package_data=True,
    entry_points= {
        "console_scripts": ["blackjack=py21.cli:cli_main"]
    }
)
