"""Dynamic package setup configuration file."""

# Import standard modules
import setuptools

__author__ = "Vitali Lupusor"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cmc_data",
    version="0.0.1",
    author="Vitali Lupusor",
    author_email="nacho-banana-nacho@protonmail.com",
    description="Coinmarketcap data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BarryFoye/coinmarketcap-scraper",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=[
        "SQLAlchemy>=1.4.26",
        "click>=8.0.3",
        "python-dotenv>=0.19.1",
        "psycopg2>=2.9.1",
        "requests>=2.26.0",
        "urllib3>=1.26.7",
    ],
)
