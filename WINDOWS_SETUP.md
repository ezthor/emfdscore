# Windows Setup Guide for Enhanced eMFDscore

This guide helps Windows users set up and run the enhanced eMFDscore system with PDF/OCR support.

## Quick Start

### Option 1: Automated Setup (Recommended)
1. Download the repository
2. Open Command Prompt or PowerShell as Administrator
3. Navigate to the emfdscore directory
4. Run: `start_windows.bat`

The script will automatically:
- Create a conda environment named `emfd`
- Install all dependencies
- Handle spaCy model installation issues
- Test the installation

### Option 2: Manual Setup

#### Prerequisites
- Windows 10/11
- Anaconda or Miniconda installed
- Internet connection

#### Step-by-Step Instructions

1. **Create and activate conda environment:**
```cmd
conda create -n emfd python=3.11 -y
conda activate emfd
```

2. **Install dependencies:**
```cmd
pip install pandas progressbar2 nltk numpy spacy scikit-learn pdfplumber PyPDF2
```

3. **Install eMFDscore:**
```cmd
pip install -e .
```

4. **Install spaCy model (see troubleshooting if this fails):**
```cmd
python -m spacy download en_core_web_sm
```

## Common Issues and Solutions

### Issue 1: spaCy Model Download Fails

**Error:** `ERROR: Wheel 'en-core-web-sm' located at ... is invalid.`

**Solutions (try in order):**

#### Solution A: Clear pip cache and retry
```cmd
pip cache purge
python -m spacy download en_core_web_sm
```

#### Solution B: Manual download
```cmd
# Download the wheel file manually
curl -L -o en_core_web_sm-3.8.0-py3-none-any.whl https://github.com/explosion/spacy-models/releases/download/en_core_web_sm-3.8.0/en_core_web_sm-3.8.0-py3-none-any.whl

# Install from local file
pip install en_core_web_sm-3.8.0-py3-none-any.whl
```

#### Solution C: Use alternative mirror
```cmd
pip install -i https://pypi.tuna.tsinghua.edu.cn/simple spacy
python -m spacy download en_core_web_sm
```

#### Solution D: Install from conda-forge
```cmd
conda install -c conda-forge spacy-model-en_core_web_sm
```

### Issue 2: KeyError 'moral_summary'

**Error:** `KeyError: 'moral_summary'`

**Problem:** The basic `analyze_file()` method doesn't include moral summary by default.

**Solutions:**

#### Solution A: Use the enhanced method (Recommended)
```python
from emfdscore.moral_analysis import MoralFrameworkAnalyzer

analyzer = MoralFrameworkAnalyzer()
result = analyzer.analyze_file_with_summary('your_file.txt')  # Note: with_summary
print(f"Dominant foundation: {result['moral_summary']['dominant_foundation']['name']}")
```

#### Solution B: Generate summary manually
```python
from emfdscore.moral_analysis import MoralFrameworkAnalyzer

analyzer = MoralFrameworkAnalyzer()
result = analyzer.analyze_file('your_file.txt')
moral_summary = analyzer.get_moral_summary(result['moral_scores'])
print(f"Dominant foundation: {moral_summary['dominant_foundation']['name']}")
```

#### Solution C: Use convenience function
```python
from emfdscore.moral_analysis import analyze_file_moral_framework_with_summary

result = analyze_file_moral_framework_with_summary('your_file.txt')
print(f"Dominant foundation: {result['moral_summary']['dominant_foundation']['name']}")
```

### Issue 3: Import Errors

**Error:** `ModuleNotFoundError: No module named 'emfdscore'`

**Solutions:**
1. Make sure you're in the correct conda environment: `conda activate emfd`
2. Reinstall in development mode: `pip install -e .`
3. Check your Python path: `python -c "import sys; print(sys.path)"`

### Issue 4: Permission Errors

**Error:** `PermissionError` or `Access denied`

**Solutions:**
1. Run Command Prompt as Administrator
2. Check if files are not read-only
3. Make sure no antivirus is blocking file operations

## Usage Examples

### Basic Text Analysis
```python
# start.py - Fixed version that handles the KeyError
from emfdscore.moral_analysis import MoralFrameworkAnalyzer

text = "Your text here..."
analyzer = MoralFrameworkAnalyzer()

# Method 1: Get scores only
moral_scores = analyzer.analyze_text(text)
moral_summary = analyzer.get_moral_summary(moral_scores)  # Generate summary separately

# Method 2: Analyze file with summary included
result = analyzer.analyze_file_with_summary('input.txt')
print(f"Dominant foundation: {result['moral_summary']['dominant_foundation']['name']}")
```

### Command Line Usage
```cmd
# Activate environment first
conda activate emfd

# Analyze a text file with summary
python bin\moral_analyzer input.txt --show-summary

# Analyze a PDF file
python bin\moral_analyzer document.pdf --output results.json

# Batch process multiple files
python bin\moral_analyzer file1.pdf file2.txt --output batch_results.json

# Use different dictionary
python bin\moral_analyzer input.txt --dict-type mfd --show-summary
```

### Running the Demo
```cmd
conda activate emfd
python demo_moral_analysis.py
```

### Running the Fixed Startup Script
```cmd
conda activate emfd
python start.py
```

## Testing Your Installation

Run this test script to verify everything works:

```python
# test_installation.py
try:
    import emfdscore
    print("✓ eMFDscore imported successfully")
    
    import spacy
    nlp = spacy.load('en_core_web_sm')
    print("✓ spaCy model loaded successfully")
    
    from emfdscore.moral_analysis import MoralFrameworkAnalyzer
    analyzer = MoralFrameworkAnalyzer()
    
    text = "The volunteers showed great compassion."
    result = analyzer.analyze_file_with_summary_from_text(text)
    print("✓ Moral analysis working correctly")
    
    print("\nInstallation successful! 🎉")
    
except Exception as e:
    print(f"✗ Error: {e}")
    print("Please check the troubleshooting section above.")
```

## Performance Tips for Windows

1. **Use SSD storage** for better PDF processing performance
2. **Add exclusions** in Windows Defender for the conda environment folder
3. **Use Windows Terminal** instead of Command Prompt for better display
4. **Close unnecessary applications** when processing large PDFs

## Getting Help

If you continue to have issues:

1. Check the main README_ENHANCED.md for general documentation
2. Run the diagnostic script: `python bin\moral_analyzer --list-supported`
3. Enable verbose logging: `python bin\moral_analyzer input.txt --verbose`
4. Create an issue on GitHub with your error message and Windows version

## Environment Management

### Reactivating the environment later:
```cmd
conda activate emfd
```

### Updating the installation:
```cmd
conda activate emfd
git pull
pip install -e . --upgrade
```

### Removing the environment:
```cmd
conda deactivate
conda remove -n emfd --all
```