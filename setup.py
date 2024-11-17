from setuptools import setup, find_packages

setup(
    name="travel_planner",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=[
        "openai>=1.0.0",
        "requests>=2.31.0",
        "pydantic>=2.5.0",
        "python-dotenv>=1.0.0",
        "agentops>=0.1.0",
        "structlog>=24.1.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.23.0",
            "pytest-cov>=4.1.0",
            "black>=24.1.0",
            "isort>=5.13.0",
            "flake8>=7.0.0",
        ]
    },
    author="Pinaki Guha",
    author_email="pinaki.guha@gmail.com",
    description="A travel planning system using LLMs and weather data. Built to test agenops.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
)