#!/usr/bin/env python3
"""
Simple startup script for eMFDscore analysis
Demonstrates basic usage and fixes the KeyError issue mentioned in the comment.
"""

from emfdscore.moral_analysis import MoralFrameworkAnalyzer

def main():
    # Example text for analysis
    text = """Emmanuel Durand had only arrived in Kharkiv on the overnight train a few hours earlier when he heard the first explosion.

A thunderous clap brought into focus just how close the 52-year-old structural engineer from France was to the frontline of the war in Ukraine.

The Ukrainian members of his team, who by this stage had endured three months of the Russian invasion, were quick to reassure their nervous companion.

"The shelling is over there [in another neighbourhood]. Here it's okay," he recalled his fellow volunteers saying, as if they were talking about the weather.

Durand, an expert in the 3D laser scanning of structures, had arrived in Ukraine's second-largest city on a 17-day mission to document the destruction of culturally significant sites across the nation."""

    print("=== eMFDscore Analysis Demo ===")
    print(f"Analyzing text of {len(text)} characters...")
    print()

    # Create analyzer
    analyzer = MoralFrameworkAnalyzer()
    
    # Method 1: Analyze text directly (this is what was causing the KeyError)
    print("[Method 1] Direct text analysis:")
    try:
        # NEW: Use the enhanced method that includes summary
        result = analyzer.analyze_text_with_summary(text)
        print(f"✓ Analysis completed. Found {len(result['moral_scores'])} moral scores.")
        print(f"Dominant moral foundation: {result['moral_summary']['dominant_foundation']['name']}")
        print(f"Probability: {result['moral_summary']['dominant_foundation']['probability']:.3f}")
        print()
        
    except Exception as e:
        print(f"✗ Error in text analysis: {e}")
        return

    # Method 2: Using the enhanced analyze_file_with_summary function
    print("[Method 2] Using enhanced file analysis:")
    
    # Save text to a temporary file
    import tempfile
    import os
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False, encoding='utf-8') as f:
        f.write(text)
        temp_file = f.name
    
    try:
        # Use the enhanced analysis that includes summary
        result = analyzer.analyze_file_with_summary(temp_file)
        
        print(f"✓ File analysis completed!")
        print(f"File: {result['file_path']}")
        print(f"Text length: {result['text_length']} characters")
        print(f"Word count: {result['word_count']} words")
        print(f"Dominant moral foundation: {result['moral_summary']['dominant_foundation']['name']}")
        print(f"Moral density: {result['moral_summary']['moral_density']['interpretation']}")
        
        print("\nMoral foundations breakdown:")
        for foundation, data in result['moral_summary']['moral_foundations'].items():
            prob = data.get('probability', 0)
            strength = data.get('strength', 'unknown')
            sentiment = data.get('sentiment_direction', 'neutral')
            print(f"  {foundation}: {prob:.3f} ({strength}, {sentiment})")
            
    except Exception as e:
        print(f"✗ Error in file analysis: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up temp file
        if os.path.exists(temp_file):
            os.unlink(temp_file)

    print("\n=== Analysis Complete ===")
    print("To avoid KeyError issues in the future:")
    print("1. Use analyzer.analyze_file_with_summary() instead of analyze_file()")
    print("2. Or manually call analyzer.get_moral_summary(moral_scores)")
    print("3. Or use the CLI tool: python bin/moral_analyzer input.txt --show-summary")

if __name__ == '__main__':
    main()