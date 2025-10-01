from setuptools import find_packages, setup

setup(
    name="primai-shared",
    version="0.1.0",
    description="Shared Pydantic models and utilities for PrimAI API and Workers",
    author="PrimAI",
    packages=find_packages(),
    install_requires=[
        "pydantic>=2.8.2",
        "pydantic-settings>=2.3.4",
    ],
    python_requires=">=3.11",
)
