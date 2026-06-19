from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="doc-verification-agent",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A document verification agent that fetches, parses, and scores documents using LLM APIs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/doc-verification-agent",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "doc-verify=doc_verification_agent.cli:main",
        ],
    },
)
