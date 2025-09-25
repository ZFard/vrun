#!/usr/bin/env python3
"""
Setup script for VASP DOS Plotter
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="vasp-dos-plotter",
    version="1.0.0",
    author="Zeinab H. Fard",
    author_email="zfard@iastate.edu",
    description="A professional GUI application for plotting VASP Density of States data",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/zeinabfard/vasp-dos-plotter",
    project_urls={
        "Bug Reports": "https://github.com/zeinabfard/vasp-dos-plotter/issues",
        "Source": "https://github.com/zeinabfard/vasp-dos-plotter",
        "Documentation": "https://github.com/zeinabfard/vasp-dos-plotter#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "Environment :: X11 Applications :: Qt",
        "Environment :: Win32 (MS Windows)",
        "Environment :: MacOS X",
    ],
    python_requires=">=3.7",
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=6.0",
            "pytest-cov>=2.0",
            "black>=21.0",
            "flake8>=3.8",
            "mypy>=0.800",
        ],
        "docs": [
            "sphinx>=4.0",
            "sphinx-rtd-theme>=0.5",
            "myst-parser>=0.15",
        ],
    },
    entry_points={
        "console_scripts": [
            "vasp-dos-plotter=vasp_dos_plotter.gui:main",
            "vasp-dos-plot=vasp_dos_plotter.gui:main",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["*.png", "*.jpg", "*.ico", "*.txt", "*.md", "*.bat"],
    },
    keywords=[
        "vasp",
        "density-of-states",
        "dos",
        "materials-science",
        "computational-chemistry",
        "visualization",
        "gui",
        "plotting",
        "dft",
        "electronic-structure",
    ],
    zip_safe=False,
)
