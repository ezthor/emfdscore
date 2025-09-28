# Enhanced eMFDscore: Extended Moral Foundation Dictionary Scoring with PDF/OCR Support

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/) [![Open Source Love png2](https://badges.frapsoft.com/os/v2/open-source.png?v=103)](https://github.com/ellerbrock/open-source-badges/)

**Enhanced eMFDscore** is an extended version of the original eMFDscore library that adds comprehensive text extraction capabilities including PDF processing with OCR support. It provides a complete pipeline from document processing to moral framework analysis.

## New Features

### 🔍 Text Extraction Support
- **PDF Processing**: Extract text from PDF documents using multiple extraction methods
- **OCR Support**: Fallback OCR support for image-based PDFs (requires tesseract)
- **Extensible Architecture**: Easy to add support for new file formats
- **Multiple Extraction Methods**: Automatic fallback between pdfplumber, PyPDF2, and OCR

### 📊 Enhanced Moral Analysis
- **Complete Workflow**: From file input to moral framework scores
- **Batch Processing**: Analyze multiple documents at once
- **Rich Metadata**: File information, text statistics, and analysis parameters
- **Human-Readable Summaries**: Interpret moral foundation scores in natural language

### 🛠️ New Command Line Tools
- **`moral_analyzer`**: New comprehensive CLI tool for document analysis
- **Original `emfdscore`**: Original CLI tool remains available

### 📚 Programmatic API
- **Simple Functions**: Easy-to-use convenience functions
- **Class-Based API**: Full-featured analyzer classes for advanced usage
- **Extensible Design**: Create custom extractors and analyzers

## Installation

### Basic Installation
```bash
pip install https://github.com/medianeuroscience/emfdscore/archive/master.zip
```

### With OCR Support
```bash
pip install https://github.com/medianeuroscience/emfdscore/archive/master.zip[ocr]
# Also install tesseract OCR engine on your system
```

### Development Installation
```bash
git clone https://github.com/medianeuroscience/emfdscore.git
cd emfdscore
pip install -e .[ocr,dev]
```

### Prerequisites
- Python 3.7+
- spaCy English model: `python -m spacy download en_core_web_sm`
- For OCR: Tesseract OCR engine installed on your system

## Quick Start

### Command Line Usage

```bash
# Analyze a text file
moral_analyzer input.txt --show-summary

# Analyze a PDF document  
moral_analyzer document.pdf --output results.json

# Batch process multiple files
moral_analyzer file1.pdf file2.txt file3.pdf --output batch_results.json

# Use different moral foundation dictionary
moral_analyzer input.txt --dict-type mfd --show-summary

# List supported file types
moral_analyzer --list-supported
```

### Python API Usage

```python
from emfdscore.moral_analysis import analyze_file_moral_framework

# Analyze a file (PDF, TXT, etc.)
result = analyze_file_moral_framework('document.pdf')

print(f"Dominant moral foundation: {result['moral_summary']['dominant_foundation']['name']}")
print(f"Moral content density: {result['moral_summary']['moral_density']['interpretation']}")

# Print all foundation scores
for foundation, data in result['moral_summary']['moral_foundations'].items():
    print(f"{foundation}: {data['probability']:.3f} ({data['strength']})")
```

### Simple Text Analysis

```python
from emfdscore.moral_analysis import analyze_text_moral_framework

text = """The volunteers showed great compassion, helping victims 
of the disaster with food, shelter, and medical care."""

scores = analyze_text_moral_framework(text)
print(f"Care foundation score: {scores['care_p']:.3f}")
print(f"Moral-to-nonmoral ratio: {scores['moral_nonmoral_ratio']:.3f}")
```

## Example Output

### Command Line Output
```bash
$ moral_analyzer example.pdf --show-summary

============================================================
MORAL FRAMEWORK ANALYSIS SUMMARY
============================================================
File: example.pdf
  Text length: 1,250 characters
  Word count: 195 words
  Dominant moral foundation: care (0.143)
  Moral content density: high_moral_content (ratio: 1.234)
  Moral foundations:
    care: 0.143 (very_high)
    fairness: 0.089 (moderate)
    loyalty: 0.076 (moderate)
    authority: 0.065 (moderate)
    sanctity: 0.054 (moderate)
```

### JSON Output
```json
{
  "file_path": "example.pdf",
  "file_metadata": {
    "file_size": 15420,
    "file_type": "pdf",
    "page_count": 3
  },
  "text_length": 1250,
  "word_count": 195,
  "moral_scores": {
    "care_p": 0.143,
    "fairness_p": 0.089,
    "loyalty_p": 0.076,
    "authority_p": 0.065,
    "sanctity_p": 0.054,
    "care_sent": 0.032,
    "fairness_sent": -0.012,
    "moral_nonmoral_ratio": 1.234
  },
  "moral_summary": {
    "dominant_foundation": {
      "name": "care",
      "probability": 0.143
    },
    "moral_density": {
      "ratio": 1.234,
      "interpretation": "high_moral_content"
    }
  }
}
```

## Supported File Formats

- **Text Files**: `.txt`, `.text`
- **PDF Files**: `.pdf` (with automatic OCR fallback)
- **Extensible**: Easy to add support for new formats

## Moral Foundation Dictionaries

The enhanced version supports all original eMFDscore dictionaries:

- **eMFD (Extended Moral Foundation Dictionary)**: Most comprehensive, includes probability and sentiment scores
- **MFD (Moral Foundation Dictionary)**: Original dictionary with virtue/vice categories  
- **MFD2**: Updated version of the original dictionary

## Advanced Usage

### Custom Text Extraction

```python
from emfdscore.text_extraction import TextExtractionManager, PDFExtractor

# Create custom extraction manager
manager = TextExtractionManager()

# Extract text with specific options
text = manager.extract_text('document.pdf', use_ocr_fallback=True)

# Get file metadata
metadata = manager.get_file_metadata('document.pdf')
print(f"PDF has {metadata['page_count']} pages")
```

### Batch Processing

```python
from emfdscore.moral_analysis import MoralFrameworkAnalyzer

analyzer = MoralFrameworkAnalyzer()

# Process multiple files
file_paths = ['doc1.pdf', 'doc2.txt', 'doc3.pdf']
results = analyzer.analyze_batch(file_paths)

for result in results:
    if 'error' not in result:
        summary = analyzer.get_moral_summary(result['moral_scores'])
        dominant = summary['dominant_foundation']
        print(f"{result['file_path']}: {dominant['name']} ({dominant['probability']:.3f})")
```

### Different Dictionaries and Methods

```python
# Use MFD dictionary
result = analyze_file_moral_framework(
    'document.pdf',
    dict_type='mfd',
    score_method='bow'
)

# Use different probability mapping for eMFD
result = analyze_file_moral_framework(
    'document.pdf', 
    dict_type='emfd',
    prob_map='single',  # vs 'all'
    output_metrics='vice-virtue'  # vs 'sentiment'
)
```

## Command Line Reference

### moral_analyzer

```bash
usage: moral_analyzer [-h] [-o OUTPUT] [--show-summary] [--dict-type {emfd,mfd,mfd2}]
                     [--prob-map {all,single}] [--score-method {bow,wordlist,gdelt.ngrams,pat}]
                     [--output-metrics {sentiment,vice-virtue}] [--encoding ENCODING]
                     [--no-ocr] [-v] [--list-supported]
                     input_files [input_files ...]

Enhanced Moral Framework Analyzer with PDF/OCR support

positional arguments:
  input_files           Input file(s) to analyze (PDF, TXT)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        Output JSON file for results (default: print to stdout)
  --show-summary        Show human-readable summary of results
  --dict-type {emfd,mfd,mfd2}
                        Dictionary for scoring (default: emfd)
  --prob-map {all,single}
                        Probability mapping for eMFD (default: all)
  --score-method {bow,wordlist,gdelt.ngrams,pat}
                        Scoring method (default: bow)
  --output-metrics {sentiment,vice-virtue}
                        Output metrics for eMFD (default: sentiment)
  --encoding ENCODING   Text encoding for TXT files (default: utf-8)
  --no-ocr              Disable OCR fallback for PDF files
  -v, --verbose         Enable verbose logging
  --list-supported      List supported file extensions and exit
```

## Error Handling

The system includes comprehensive error handling:

- **File Not Found**: Clear error messages for missing files
- **Unsupported Formats**: Helpful suggestions for unsupported file types
- **PDF Processing Errors**: Automatic fallback between extraction methods
- **Encoding Issues**: Automatic detection and handling of text encodings
- **OCR Failures**: Graceful degradation when OCR is not available

## Performance Notes

- **PDF Processing**: Large PDFs may take longer to process, especially with OCR
- **Batch Processing**: Files are processed sequentially; consider splitting large batches
- **Memory Usage**: Large documents are processed in memory; monitor usage for very large files

## Extending the System

### Adding New File Format Support

```python
from emfdscore.text_extraction import TextExtractorBase, TextExtractionManager

class CustomExtractor(TextExtractorBase):
    def extract(self, file_path: str, **kwargs) -> str:
        # Your extraction logic here
        return extracted_text
    
    def supports_file(self, file_path: str) -> bool:
        return file_path.lower().endswith('.custom')

# Register the new extractor
manager = TextExtractionManager()
manager.register_extractor(CustomExtractor())
```

## Citation

When using the enhanced eMFDscore, please cite the original paper:

Hopp, F. R., Fisher, J. T., Cornell, D., Huskey, R., & Weber, R. (2020). The extended Moral Foundations Dictionary (eMFD): Development and applications of a crowd-sourced approach to extracting moral intuitions from text. _Behavior Research Methods_, https://doi.org/10.3758/s13428-020-01433-0

## License

Enhanced eMFDscore is dual-licensed under GNU GENERAL PUBLIC LICENSE 3.0, which permits the non-commercial use, distribution, and modification of the eMFDscore package. Commercial use requires an [application](https://forms.gle/RSKzZ2DvDyaprfeE8).

## Support

For questions about the enhanced features, please create an issue on GitHub. For questions about the original eMFDscore functionality, connect with **Musa Malik** via [LinkedIn](https://www.linkedin.com/in/musainayatmalik/).

## Original Features

All original eMFDscore features remain available and unchanged:

- Fast spaCy-based text processing
- Multiple moral foundation dictionaries
- Various scoring methods (bag-of-words, wordlist, PAT extraction)
- Original command-line interface (`emfdscore`)

For original documentation and usage, see the main README.md file.