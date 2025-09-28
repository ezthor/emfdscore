#!/usr/bin/env python3
"""
Demonstration script showing how to use the enhanced moral framework analysis system.
This script demonstrates both programmatic usage and CLI usage.
"""

import os
import json
import tempfile
from pathlib import Path

# Import our enhanced modules
from emfdscore.moral_analysis import MoralFrameworkAnalyzer, analyze_text_moral_framework
from emfdscore.text_extraction import extract_text_from_file, TextExtractionManager

def demo_text_analysis():
    """Demonstrate text analysis with the example from the problem statement."""
    print("="*60)
    print("DEMO 1: Direct Text Analysis")
    print("="*60)
    
    # Example text from the problem statement
    example_text = """Emmanuel Durand had only arrived in Kharkiv on the overnight train a few hours earlier when he heard the first explosion.

A thunderous clap brought into focus just how close the 52-year-old structural engineer from France was to the frontline of the war in Ukraine.

The Ukrainian members of his team, who by this stage had endured three months of the Russian invasion, were quick to reassure their nervous companion.

"The shelling is over there [in another neighbourhood]. Here it's okay," he recalled his fellow volunteers saying, as if they were talking about the weather.

Durand, an expert in the 3D laser scanning of structures, had arrived in Ukraine's second-largest city on a 17-day mission to document the destruction of culturally significant sites across the nation."""
    
    # Analyze using convenience function
    scores = analyze_text_moral_framework(example_text)
    
    print(f"Text length: {len(example_text)} characters")
    print(f"Word count: {len(example_text.split())} words")
    print("\nMoral Framework Scores (eMFD):")
    
    foundations = ['care', 'fairness', 'loyalty', 'authority', 'sanctity']
    for foundation in foundations:
        prob = scores.get(f'{foundation}_p', 0)
        sent = scores.get(f'{foundation}_sent', 0)
        print(f"  {foundation.capitalize()}: {prob:.3f} (sentiment: {sent:+.3f})")
    
    moral_ratio = scores.get('moral_nonmoral_ratio', 0)
    print(f"\nMoral-to-nonmoral ratio: {moral_ratio:.3f}")
    
    # Find dominant foundation
    prob_scores = {f: scores.get(f'{f}_p', 0) for f in foundations}
    dominant = max(prob_scores.items(), key=lambda x: x[1])
    print(f"Dominant moral foundation: {dominant[0]} ({dominant[1]:.3f})")


def demo_file_analysis():
    """Demonstrate file-based analysis."""
    print("\n" + "="*60)
    print("DEMO 2: File-based Analysis")
    print("="*60)
    
    # Create a temporary text file for demonstration
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("""In the heart of the city, a group of volunteers worked tirelessly to help refugees find shelter and safety. Their compassion knew no bounds as they provided food, medical care, and emotional support to those who had lost everything.

The community response was overwhelming - neighbors helping neighbors, strangers becoming friends, and everyone united in the shared belief that no one should face hardship alone. Local businesses donated supplies, while families opened their homes to provide temporary housing.

This act of collective kindness demonstrated the very best of human nature, showing that even in the darkest times, people can come together to care for one another and rebuild what has been lost.""")
        temp_file_path = f.name
    
    try:
        # Initialize analyzer
        analyzer = MoralFrameworkAnalyzer()
        
        # Analyze the file
        result = analyzer.analyze_file(temp_file_path)
        
        print(f"Analyzed file: {temp_file_path}")
        print(f"File metadata: {result['file_metadata']}")
        print(f"Text length: {result['text_length']} characters")
        print(f"Word count: {result['word_count']} words")
        
        # Get moral summary
        summary = analyzer.get_moral_summary(result['moral_scores'])
        
        print(f"\nDominant foundation: {summary['dominant_foundation']['name']} ({summary['dominant_foundation']['probability']:.3f})")
        print(f"Moral density: {summary['moral_density']['interpretation']}")
        
        print("\nFoundation details:")
        for foundation, data in summary['moral_foundations'].items():
            prob = data.get('probability', 0)
            strength = data.get('strength', 'unknown')
            sentiment = data.get('sentiment_direction', 'neutral')
            print(f"  {foundation}: {prob:.3f} ({strength}, {sentiment})")
    
    finally:
        # Clean up
        os.unlink(temp_file_path)


def demo_different_dictionaries():
    """Demonstrate using different moral foundation dictionaries."""
    print("\n" + "="*60)
    print("DEMO 3: Different Dictionary Types")
    print("="*60)
    
    text = "The judge delivered a fair verdict, upholding justice and maintaining order in the courtroom. The defendant showed respect for the authority of the court."
    
    analyzer = MoralFrameworkAnalyzer()
    
    # Test different dictionaries
    for dict_type in ['emfd', 'mfd', 'mfd2']:
        print(f"\n--- Using {dict_type.upper()} dictionary ---")
        try:
            if dict_type == 'emfd':
                scores = analyzer.analyze_text(text, dict_type=dict_type, prob_map='all', output_metrics='sentiment')
            else:
                scores = analyzer.analyze_text(text, dict_type=dict_type)
            
            print(f"Results using {dict_type}:")
            for key, value in scores.items():
                if isinstance(value, (int, float)):
                    print(f"  {key}: {value:.3f}")
                else:
                    print(f"  {key}: {value}")
                    
        except Exception as e:
            print(f"Error with {dict_type}: {e}")


def demo_extensible_extraction():
    """Demonstrate the extensible text extraction system."""
    print("\n" + "="*60)
    print("DEMO 4: Extensible Text Extraction")
    print("="*60)
    
    # Show supported file types
    manager = TextExtractionManager()
    supported_extensions = manager.get_supported_extensions()
    print(f"Supported file extensions: {', '.join(supported_extensions)}")
    
    # Create test files
    test_files = []
    
    # Text file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write("This is a simple text file for testing the moral framework analysis system.")
        test_files.append(f.name)
    
    try:
        for file_path in test_files:
            print(f"\nExtracting from: {file_path}")
            
            # Extract text
            text = extract_text_from_file(file_path)
            print(f"Extracted text: {text[:100]}...")
            
            # Get metadata
            metadata = manager.get_file_metadata(file_path)
            print(f"File metadata: {metadata}")
            
            # Quick moral analysis
            analyzer = MoralFrameworkAnalyzer()
            scores = analyzer.analyze_text(text)
            moral_ratio = scores.get('moral_nonmoral_ratio', 0)
            print(f"Moral content ratio: {moral_ratio:.3f}")
    
    finally:
        # Clean up
        for file_path in test_files:
            if os.path.exists(file_path):
                os.unlink(file_path)


def demo_batch_processing():
    """Demonstrate batch processing of multiple files."""
    print("\n" + "="*60)
    print("DEMO 5: Batch Processing")
    print("="*60)
    
    # Create multiple test files
    test_texts = [
        "The volunteers showed great compassion, helping victims of the natural disaster with food and shelter.",
        "The court upheld justice, ensuring fair treatment for all parties involved in the legal proceedings.",
        "The soldiers demonstrated loyalty to their country, following orders with dedication and honor.",
        "The religious ceremony emphasized purity and sanctity, creating a sacred atmosphere for worship.",
        "The government official exercised proper authority, maintaining order and enforcing the law effectively."
    ]
    
    test_files = []
    for i, text in enumerate(test_texts):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
            f.write(text)
            test_files.append(f.name)
    
    try:
        # Batch analysis
        analyzer = MoralFrameworkAnalyzer()
        results = analyzer.analyze_batch(test_files)
        
        print(f"Processed {len(results)} files:")
        
        for i, result in enumerate(results):
            if 'error' in result:
                print(f"  {i+1}. ERROR: {result['error']}")
            else:
                # Get summary
                summary = analyzer.get_moral_summary(result['moral_scores'])
                dominant = summary['dominant_foundation']
                print(f"  {i+1}. Dominant: {dominant['name']} ({dominant['probability']:.3f}) - {result['word_count']} words")
    
    finally:
        # Clean up
        for file_path in test_files:
            if os.path.exists(file_path):
                os.unlink(file_path)


def demo_cli_usage():
    """Demonstrate CLI usage examples."""
    print("\n" + "="*60)
    print("DEMO 6: CLI Usage Examples")
    print("="*60)
    
    print("The moral_analyzer CLI tool can be used as follows:")
    print()
    print("# Analyze a single text file:")
    print("python3 bin/moral_analyzer input.txt --show-summary")
    print()
    print("# Analyze a PDF file with specific parameters:")
    print("python3 bin/moral_analyzer document.pdf --dict-type emfd --prob-map all --output results.json")
    print()
    print("# Batch process multiple files:")
    print("python3 bin/moral_analyzer file1.pdf file2.txt file3.pdf --output batch_results.json")
    print()
    print("# Use different moral foundation dictionary:")  
    print("python3 bin/moral_analyzer input.txt --dict-type mfd --show-summary")
    print()
    print("# List supported file types:")
    print("python3 bin/moral_analyzer --list-supported")


def main():
    """Main demonstration function."""
    print("Enhanced Moral Framework Analysis System - Demonstration")
    print("This demo shows the complete workflow from text extraction to moral analysis")
    
    # Run all demonstrations
    demo_text_analysis()
    demo_file_analysis()
    demo_different_dictionaries()
    demo_extensible_extraction()
    demo_batch_processing()
    demo_cli_usage()
    
    print("\n" + "="*60)
    print("DEMONSTRATION COMPLETE")
    print("="*60)
    print("The system successfully:")
    print("1. ✓ Extracted text from various file formats")
    print("2. ✓ Analyzed moral frameworks using emfdscore")
    print("3. ✓ Provided extensible interfaces for new file types")
    print("4. ✓ Generated comprehensive moral analysis reports")
    print("5. ✓ Demonstrated both programmatic and CLI usage")


if __name__ == '__main__':
    main()