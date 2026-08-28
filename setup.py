from setuptools import setup, find_packages
from pathlib import Path

# Lecture du README pour la description longue
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8")

setup(
    name="catar-software",
    version="1.0.0",
    description="Logiciel d'alignement cognitif pour sécuriser le comportement des IA complexes.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="QuatreCATAR",
    url="https://github.com/QuatreCATAR/CATAR-software",
    packages=find_packages(where="src"),
    package_dir={"": "src"},

    # Inclusion des fichiers JSON du protocole
    package_data={
        "protocol": [
            "phase1.json",
            "phase2.json",
            "phase3.json",
            "scoring.json"
        ]
    },

    include_package_data=True,

    install_requires=[
        "fastapi",
        "uvicorn",
        "pytest"
    ],

    python_requires=">=3.10",

    entry_points={
        "console_scripts": [
            "catar-cli=interface.cli:main"
        ]
    },

    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
)
