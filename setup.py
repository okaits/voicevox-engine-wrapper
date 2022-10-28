""" setup.py """

import setuptools
with open("README.md", "r", encoding="utf-8") as file:
    readme = file.read()
setuptools.setup(
    name="voicevox.py",
    version="0.0.1",
    install_requires=[
        "pygame"
    ],
    author="okaits7534",
    author_email="okaits7534@gmail.com",
    description="VOICEVOX Engine Wrapper for Python3",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/okaits/voicevox-engine-wrapper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: GPU :: NVIDIA CUDA :: 11.8",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Natural Language :: Japanese",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Sound/Audio :: Sound Synthesis",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
