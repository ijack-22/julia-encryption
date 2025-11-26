from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="julia-encryption",
    version="1.0.0",
    author="ijack-22",
    description="A secure file encryption tool with GUI and CLI interfaces",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ijack-22/julia-encryption",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7+",
    ],
    python_requires=">=3.7",
    install_requires=[
        "cryptography>=3.4.0",
        "customtkinter>=5.0.0",
    ],
        entry_points={
        "console_scripts": [
            "julia-encrypt=src.julia_main:main",
        ],
    },
