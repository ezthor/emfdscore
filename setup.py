from setuptools import setup

setup(name='emfdscore',
      version='0.0.2',
      description='Extended Moral Foundation Dictionary Scoring for Python with PDF/OCR support',
      url='https://github.com/medianeuroscience/emfdscore',
      author='Anonymized.',
      author_email='fhopp@ucsb.edu',
      license='MIT',
      packages=['emfdscore'],
      scripts=['bin/emfdscore', 'bin/moral_analyzer'],
      include_package_data=True, 
      install_requires=[
          'pandas',
          'progressbar2',
          'nltk',
          'numpy',
          'spacy>=3.0.0',
          'scikit-learn',
          # Text extraction dependencies
          'pdfplumber>=0.5.0',
          'PyPDF2>=3.0.0',
      ],
      extras_require={
          'ocr': [
              'pytesseract>=0.3.0',
              'Pillow>=8.0.0',
              'PyMuPDF>=1.18.0'  # fitz module for PDF to image conversion
          ],
          'dev': [
              'reportlab>=3.0.0'  # for creating test PDFs
          ]
      },
      classifiers=[
          'Development Status :: 4 - Beta',
          'Intended Audience :: Researchers',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'Programming Language :: Python :: 3.10',
          'Programming Language :: Python :: 3.11',
          'Programming Language :: Python :: 3.12',
          'Topic :: Scientific/Engineering :: Artificial Intelligence',
          'Topic :: Text Processing :: Linguistic',
      ],
      python_requires='>=3.7',
      zip_safe=False)
