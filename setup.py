from setuptools import setup, find_packages

setup(
    name="haven",
    version="0.1.0",
    description="GraTech Haven - Your AI Companion with Arabic Support",
    author="GraTech",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.9",
    install_requires=[
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "rich>=13.7.0",
        "sqlalchemy>=2.0.25",
        "httpx>=0.26.0",
        "python-dotenv>=1.0.0",
    ],
    entry_points={
        "console_scripts": [
            "haven=haven.main:main",
        ],
    },
)
