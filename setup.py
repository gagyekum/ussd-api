from setuptools import setup, find_packages

setup(
    name="ussd-api",
    version="0.1.0",
    packages=find_packages(),
    description="A versatile framework-agnostic USSD API for Python",
    author="Gideon Agyekum",
    author_email="gide2005@gmail.com",
    url="https://github.com/gagyekum/ussd-api",
    keywords=["ussd", "telecom", "session", "menu", "navigation", "api"],
    install_requires=[],
    extras_require={
        "dev": ["pytest", "fakeredis", "black"],
    },
    python_requires=">=3.7",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
