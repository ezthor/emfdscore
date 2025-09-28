"""
Text extraction module with support for various file formats including PDF with OCR.
This module provides an extensible interface for extracting text from different sources.
"""

import abc
import os
from typing import List, Optional, Dict, Any
import logging

# PDF processing imports
try:
    import pdfplumber
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False

try:
    from PyPDF2 import PdfReader
    PYPDF2_AVAILABLE = True
except ImportError:
    PYPDF2_AVAILABLE = False

# OCR imports (optional)
try:
    import pytesseract
    from PIL import Image
    import io
    OCR_AVAILABLE = True
except ImportError:
    OCR_AVAILABLE = False

logger = logging.getLogger(__name__)


class TextExtractorBase(abc.ABC):
    """Base class for text extractors providing extensible interface."""
    
    @abc.abstractmethod
    def extract(self, file_path: str, **kwargs) -> str:
        """Extract text from the given file."""
        pass
    
    @abc.abstractmethod
    def supports_file(self, file_path: str) -> bool:
        """Check if this extractor supports the given file type."""
        pass
    
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Get metadata about the file (optional)."""
        return {}


class TxtExtractor(TextExtractorBase):
    """Text extractor for plain text files."""
    
    def extract(self, file_path: str, encoding: str = 'utf-8', **kwargs) -> str:
        """Extract text from a text file."""
        try:
            with open(file_path, 'r', encoding=encoding) as f:
                return f.read()
        except UnicodeDecodeError:
            # Try with different encodings
            for enc in ['latin-1', 'cp1252', 'iso-8859-1']:
                try:
                    with open(file_path, 'r', encoding=enc) as f:
                        logger.warning(f"Using encoding {enc} for {file_path}")
                        return f.read()
                except UnicodeDecodeError:
                    continue
            raise ValueError(f"Unable to decode text file {file_path}")
    
    def supports_file(self, file_path: str) -> bool:
        """Check if file is a text file."""
        return file_path.lower().endswith(('.txt', '.text'))
    
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Get basic file metadata."""
        if os.path.exists(file_path):
            stat = os.stat(file_path)
            return {
                'file_size': stat.st_size,
                'file_type': 'text',
                'modified_time': stat.st_mtime
            }
        return {}


class PDFExtractor(TextExtractorBase):
    """Text extractor for PDF files with fallback OCR support."""
    
    def __init__(self, use_ocr_fallback: bool = True):
        """Initialize PDF extractor.
        
        Args:
            use_ocr_fallback: Whether to use OCR when text extraction fails
        """
        self.use_ocr_fallback = use_ocr_fallback and OCR_AVAILABLE
        if not PDF_AVAILABLE and not PYPDF2_AVAILABLE:
            raise ImportError("Neither pdfplumber nor PyPDF2 is available for PDF processing")
    
    def extract(self, file_path: str, **kwargs) -> str:
        """Extract text from PDF file."""
        text = ""
        
        # Try pdfplumber first (better text extraction)
        if PDF_AVAILABLE:
            try:
                text = self._extract_with_pdfplumber(file_path)
                if text.strip():  # If we got meaningful text
                    return text
            except Exception as e:
                logger.warning(f"pdfplumber extraction failed for {file_path}: {e}")
        
        # Fallback to PyPDF2
        if PYPDF2_AVAILABLE:
            try:
                text = self._extract_with_pypdf2(file_path)
                if text.strip():  # If we got meaningful text
                    return text
            except Exception as e:
                logger.warning(f"PyPDF2 extraction failed for {file_path}: {e}")
        
        # If no text extracted and OCR is available, try OCR
        if self.use_ocr_fallback and not text.strip():
            try:
                text = self._extract_with_ocr(file_path)
            except Exception as e:
                logger.warning(f"OCR extraction failed for {file_path}: {e}")
        
        if not text.strip():
            raise ValueError(f"Unable to extract text from PDF: {file_path}")
        
        return text
    
    def _extract_with_pdfplumber(self, file_path: str) -> str:
        """Extract text using pdfplumber."""
        text_parts = []
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return '\n'.join(text_parts)
    
    def _extract_with_pypdf2(self, file_path: str) -> str:
        """Extract text using PyPDF2."""
        text_parts = []
        with open(file_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            for page in pdf_reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return '\n'.join(text_parts)
    
    def _extract_with_ocr(self, file_path: str) -> str:
        """Extract text using OCR (requires tesseract)."""
        if not OCR_AVAILABLE:
            raise ImportError("OCR dependencies not available")
        
        # Convert PDF pages to images and OCR them
        text_parts = []
        try:
            import fitz  # PyMuPDF for converting PDF to images
            pdf_document = fitz.open(file_path)
            for page_num in range(pdf_document.page_count):
                page = pdf_document[page_num]
                pix = page.get_pixmap()
                img_data = pix.tobytes("png")
                img = Image.open(io.BytesIO(img_data))
                
                # Perform OCR
                page_text = pytesseract.image_to_string(img)
                if page_text.strip():
                    text_parts.append(page_text)
            
            pdf_document.close()
        except ImportError:
            logger.warning("PyMuPDF not available, OCR extraction may be limited")
            raise
        
        return '\n'.join(text_parts)
    
    def supports_file(self, file_path: str) -> bool:
        """Check if file is a PDF."""
        return file_path.lower().endswith('.pdf')
    
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """Get PDF metadata."""
        metadata = {}
        if not os.path.exists(file_path):
            return metadata
        
        # Basic file info
        stat = os.stat(file_path)
        metadata.update({
            'file_size': stat.st_size,
            'file_type': 'pdf',
            'modified_time': stat.st_mtime
        })
        
        # Try to get PDF-specific metadata
        if PDF_AVAILABLE:
            try:
                with pdfplumber.open(file_path) as pdf:
                    metadata.update({
                        'page_count': len(pdf.pages),
                        'pdf_metadata': pdf.metadata or {}
                    })
            except Exception as e:
                logger.warning(f"Could not extract PDF metadata: {e}")
        
        return metadata


class TextExtractionManager:
    """Manager class that handles different file types using appropriate extractors."""
    
    def __init__(self):
        """Initialize with default extractors."""
        self.extractors: List[TextExtractorBase] = []
        self.register_default_extractors()
    
    def register_default_extractors(self):
        """Register the default set of extractors."""
        self.extractors.append(TxtExtractor())
        try:
            self.extractors.append(PDFExtractor())
        except ImportError as e:
            logger.warning(f"PDF extraction not available: {e}")
    
    def register_extractor(self, extractor: TextExtractorBase):
        """Register a custom extractor."""
        self.extractors.append(extractor)
    
    def extract_text(self, file_path: str, **kwargs) -> str:
        """Extract text from file using appropriate extractor."""
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        
        for extractor in self.extractors:
            if extractor.supports_file(file_path):
                try:
                    return extractor.extract(file_path, **kwargs)
                except Exception as e:
                    logger.error(f"Extraction failed with {extractor.__class__.__name__}: {e}")
                    continue
        
        raise ValueError(f"No suitable extractor found for file: {file_path}")
    
    def get_file_metadata(self, file_path: str) -> Dict[str, Any]:
        """Get metadata for file."""
        for extractor in self.extractors:
            if extractor.supports_file(file_path):
                return extractor.get_metadata(file_path)
        return {}
    
    def get_supported_extensions(self) -> List[str]:
        """Get list of supported file extensions."""
        extensions = []
        # This is a simple implementation - could be improved
        for extractor in self.extractors:
            if isinstance(extractor, TxtExtractor):
                extensions.extend(['.txt', '.text'])
            elif isinstance(extractor, PDFExtractor):
                extensions.append('.pdf')
        return extensions


# Convenience function for simple use cases
def extract_text_from_file(file_path: str, **kwargs) -> str:
    """Extract text from any supported file type."""
    manager = TextExtractionManager()
    return manager.extract_text(file_path, **kwargs)