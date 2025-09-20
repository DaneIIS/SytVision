# setup.py
from pathlib import Path
from setuptools import setup, find_packages

ROOT = Path(__file__).parent
README = (ROOT / "README.md").read_text(encoding="utf-8")

# Optional: read pinned deps from requirements.txt
req_file = ROOT / "requirements.txt"
install_requires = []
if req_file.exists():
    # Keep it simple: ignore comments/empty lines
    for line in req_file.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            install_requires.append(line)

setup(
    name="SytVision",                         # ← rebranded project name
    version="0.1.0",                          # ← set your versioning scheme
    description="SytVision – Network Video Recorder with AI/Computer Vision backend",
    long_description=README,
    long_description_content_type="text/markdown",
    author="DaneIIS",                         # ← update as you like
    url="https://github.com/DaneIIS/SytVision",
    license="MIT",                            # ← match your repo license
    packages=find_packages(include=["viseron", "viseron.*"]),
    python_requires=">=3.10",
    install_requires=install_requires,
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.10",
    ],
    # Optional: CLI entry points (uncomment/adjust if you have a main script)
    # entry_points={
    #     "console_scripts": [
    #         "sytvision=viseron.__main__:main",
    #     ]
    # },
)
