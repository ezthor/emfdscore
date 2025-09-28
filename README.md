# Windows Quick Start Guide

## 🚀 For Windows Users - Fast Setup

### Option 1: Automated Setup (Recommended)
1. Download this repository
2. Open Command Prompt or PowerShell **as Administrator**
3. Navigate to the emfdscore directory
4. Run: `start_windows.bat`

The script will automatically create a conda environment named `emfd`, install all dependencies, and handle spaCy model installation issues.

### Option 2: Manual Setup

**⚠️ Conda Environment Warning:** Always create a dedicated conda environment to avoid conflicts with other Python packages.

```cmd
# Create and activate conda environment
conda create -n emfd python=3.11 -y
conda activate emfd

# Install dependencies
pip install pandas progressbar2 nltk numpy spacy scikit-learn pdfplumber PyPDF2

# Install eMFDscore
pip install -e .

# Install spaCy model (if this fails, see WINDOWS_SETUP.md for troubleshooting)
python -m spacy download en_core_web_sm
```

### Quick Usage
```cmd
# Activate environment
conda activate emfd

# Analyze a text file
python bin\moral_analyzer input.txt --show-summary

# Analyze a PDF file  
python bin\moral_analyzer document.pdf --output results.json
```

**For detailed Windows troubleshooting and advanced usage, see [WINDOWS_SETUP.md](WINDOWS_SETUP.md)**

---

## eMFDscore: Extended Moral Foundation Dictionary Scoring for Python 
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Open Source Love png2](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

**eMFDscore** is a library for the fast and flexible extraction of various moral information metrics from textual input data. eMFDscore is built on [spaCy](https://github.com/explosion/spaCy) for faster execution and performs minimal preprocessing consisting of tokenization, syntactic dependency parsing, lower-casing, and stopword/punctuation/whitespace removal. eMFDscore lets users score documents with multiple Moral Foundations Dictionaries and provides various metrics for analyzing moral information. We also encourage users to check out [eMACDscore](https://github.com/medianeuroscience/eMACDscore), an alternative moral mining tool from our lab that adopts the theoretical perspective of [Morality as Cooperation](https://link.springer.com/chapter/10.1007/978-3-319-19671-8_2).

When using eMFDscore, please consider giving this repository a star (top right corner) and citing the following article: 

Hopp, F. R., Fisher, J. T., Cornell, D., Huskey, R., & Weber, R. (2020). The extended Moral Foundations Dictionary (eMFD): Development and applications of a crowd-sourced approach to extracting moral intuitions from text. _Behavior Research Methods_, https://doi.org/10.3758/s13428-020-01433-0 

eMFDscore is dual-licensed under GNU GENERAL PUBLIC LICENSE 3.0, which permits the non-commercial use, distribution, and modification of the eMFDscore package. Commercial use of the eMFDscore requires an [application](https://forms.gle/RSKzZ2DvDyaprfeE8).

If you have any questions and/or require additional assistance with running the package, feel free to connect directly with the current package maintainer, **Musa Malik**, via their [LinkedIn](https://www.linkedin.com/in/musainayatmalik/). 

## Install 
**eMFDscore** requires a Python installation (v3.11+). If your machine does not have Python installed, we recommend installing Python by downloading and installing either [Anaconda or Miniconda](https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/index.html) for your OS.

For best practises, we recommend installing eMFDscore into a virtual conda environment. Hence, you should first create a virtual environment by executing the following command in your terminal:

```
$ conda create -n emfd python=3.11
```

Once Anaconda/Miniconda is installed activate the env via:

```
$ source activate emfd
```

Next, you must install spaCy, which is the main natural language processing backend that eMFDscore is built on:

```
$ conda install -c conda-forge spacy
$ python -m spacy download en_core_web_sm
``` 

Finally, you can install eMFDscore by copying, pasting, and executing the following command: 

`
pip install https://github.com/medianeuroscience/emfdscore/archive/master.zip
`

### eMFDscore in Google Colaboratory

eMFDscore can also be run in [google colab](https://colab.research.google.com/notebooks/intro.ipynb). All you need to do is add these lines to the beginning of your notebook, execute them, and then restart your runtime:

```
!pip install https://github.com/medianeuroscience/emfdscore/archive/master.zip
```

You can then use eMFDscore as a regular python library.
