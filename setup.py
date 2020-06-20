import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lehd", # Replace with your own username
    version="0.0.1",
    author="Jeff Allen",
    author_email="jeff.allen@utoronto.ca",
    description="a library for downloading LEHD data",
    long_description="a Python library for downloading LEHD data into pandas DataFrames",
    long_description_content_type="text/markdown",
    url="https://github.com/jamaps/lehd",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'pandas>=1.0',
        'urllib3>1.25'
    ]
)
