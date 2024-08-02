from setuptools import setup, find_packages
import json


with open("metadata.json", encoding="utf-8") as fp:
    metadata = json.load(fp)


setup(
    name="lexibank_simsrma",
    description=metadata["title"],
    license=metadata.get("license", ""),
    url=metadata.get("url", ""),
    py_modules=["lexibank_simsrma"],
    packages=find_packages(where="."),
    include_package_data=True,
    zip_safe=False,
    entry_points={
        "lexibank.dataset": ["simsrma=lexibank_simsrma:Dataset"],
        "cldfbench.commands": ["simsrma=simsrmacommands"]
        },
    install_requires=["pylexibank>=3.0"],
    extras_require={"test": ["pytest-cldf"]},
)
