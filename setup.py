from setuptools import setup, find_packages

setup(
    name="SytVision",
    version="0.1.0",
    description="SytVision – Network Video Recorder with AI/Computer Vision backend",
    author="Dane",
    url="https://github.com/DaneIIS/SytVision",
    packages=find_packages(include=["viseron", "viseron.*"]),  # keep code import path
    python_requires=">=3.10",
    install_requires=[
        # your deps, or use requirements.txt parsing
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
