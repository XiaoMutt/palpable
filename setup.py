import pathlib

from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

# This call to setup() does all the work
setup(
    name="palpable",
    version="0.0.11",
    description="A multiprocessing task server",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/XiaoMutt/palpable",
    author="Xiao",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    package_dir={"": "src"},
    packages=find_packages("src"),
    include_package_data=True,
    install_requires=["dill", "sortedcontainers", "psutil"],
)
