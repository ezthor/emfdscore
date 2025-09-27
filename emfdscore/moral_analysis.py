"""
Moral Analysis module that integrates text extraction with emfdscore moral framework scoring.
"""

import pandas as pd
import tempfile
import os
from typing import Dict, Any, Optional, List, Union
import logging

from .text_extraction import TextExtractionManager, extract_text_from_file
from .scoring import score_docs

logger = logging.getLogger(__name__)


class MoralFrameworkAnalyzer:
    """Main class for analyzing moral frameworks in text documents."""
    
    def __init__(self):
        """Initialize the analyzer with text extraction capabilities."""
        self.text_manager = TextExtractionManager()
    
    def analyze_file(self, 
                    file_path: str, 
                    dict_type: str = 'emfd',
                    prob_map: str = 'all',
                    score_method: str = 'bow',
                    output_metrics: str = 'sentiment',
                    **extraction_kwargs) -> Dict[str, Any]:
        """
        Analyze moral frameworks in a document file.
        
        Args:
            file_path: Path to input file (PDF, TXT, etc.)
            dict_type: Dictionary type ('emfd', 'mfd', 'mfd2')
            prob_map: Probability mapping ('all', 'single') - only for emfd
            score_method: Scoring method ('bow', 'wordlist', 'gdelt.ngrams', 'pat')
            output_metrics: Output metrics ('sentiment', 'vice-virtue') - only for emfd
            **extraction_kwargs: Additional arguments for text extraction
            
        Returns:
            Dictionary containing analysis results and metadata
        """
        # Extract text from file
        logger.info(f"Extracting text from {file_path}")
        try:
            text = self.text_manager.extract_text(file_path, **extraction_kwargs)
        except Exception as e:
            logger.error(f"Text extraction failed: {e}")
            raise
        
        # Get file metadata
        file_metadata = self.text_manager.get_file_metadata(file_path)
        
        # Analyze moral frameworks in the text
        moral_scores = self.analyze_text(
            text, 
            dict_type=dict_type,
            prob_map=prob_map,
            score_method=score_method,
            output_metrics=output_metrics
        )
        
        return {
            'file_path': file_path,
            'file_metadata': file_metadata,
            'extracted_text': text,
            'text_length': len(text),
            'word_count': len(text.split()),
            'moral_scores': moral_scores,
            'analysis_parameters': {
                'dict_type': dict_type,
                'prob_map': prob_map,
                'score_method': score_method,
                'output_metrics': output_metrics
            }
        }
    
    def analyze_text(self, 
                    text: str,
                    dict_type: str = 'emfd',
                    prob_map: str = 'all',
                    score_method: str = 'bow',
                    output_metrics: str = 'sentiment') -> Dict[str, Any]:
        """
        Analyze moral frameworks in raw text.
        
        Args:
            text: Input text to analyze
            dict_type: Dictionary type ('emfd', 'mfd', 'mfd2')
            prob_map: Probability mapping ('all', 'single') - only for emfd
            score_method: Scoring method ('bow', 'wordlist', 'gdelt.ngrams', 'pat')
            output_metrics: Output metrics ('sentiment', 'vice-virtue') - only for emfd
            
        Returns:
            Dictionary containing moral framework scores
        """
        if not text.strip():
            raise ValueError("Input text is empty")
        
        # Create temporary CSV file with the text
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as tmp_file:
            # Properly escape the text for CSV
            escaped_text = text.replace('"', '""')
            tmp_file.write(f'"{escaped_text}"')
            tmp_csv_path = tmp_file.name
        
        try:
            # Load the CSV into a pandas DataFrame
            csv_data = pd.read_csv(tmp_csv_path, header=None)
            num_docs = len(csv_data)
            
            logger.info(f"Analyzing text with {dict_type} dictionary using {score_method} method")
            
            # Call the emfdscore scoring function
            if dict_type == 'emfd':
                df = score_docs(csv_data, dict_type, prob_map, score_method, output_metrics, num_docs)
            else:
                # For mfd and mfd2, prob_map and output_metrics are not used
                # But we still need to pass them to maintain the function signature
                df = score_docs(csv_data, dict_type, '', score_method, '', num_docs)
            
            # Convert DataFrame to dictionary
            if len(df) > 0:
                scores_dict = df.iloc[0].to_dict()
                return scores_dict
            else:
                logger.warning("No scores returned from emfdscore")
                return {}
                
        except Exception as e:
            logger.error(f"Moral framework analysis failed: {e}")
            raise
        finally:
            # Clean up temporary file
            if os.path.exists(tmp_csv_path):
                os.unlink(tmp_csv_path)
    
    def analyze_batch(self, 
                     file_paths: List[str],
                     dict_type: str = 'emfd',
                     prob_map: str = 'all',
                     score_method: str = 'bow',
                     output_metrics: str = 'sentiment',
                     **extraction_kwargs) -> List[Dict[str, Any]]:
        """
        Analyze multiple files in batch.
        
        Args:
            file_paths: List of file paths to analyze
            dict_type: Dictionary type ('emfd', 'mfd', 'mfd2')
            prob_map: Probability mapping ('all', 'single') - only for emfd
            score_method: Scoring method ('bow', 'wordlist', 'gdelt.ngrams', 'pat')
            output_metrics: Output metrics ('sentiment', 'vice-virtue') - only for emfd
            **extraction_kwargs: Additional arguments for text extraction
            
        Returns:
            List of analysis results for each file
        """
        results = []
        for file_path in file_paths:
            try:
                result = self.analyze_file(
                    file_path,
                    dict_type=dict_type,
                    prob_map=prob_map,
                    score_method=score_method,
                    output_metrics=output_metrics,
                    **extraction_kwargs
                )
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to analyze {file_path}: {e}")
                results.append({
                    'file_path': file_path,
                    'error': str(e),
                    'moral_scores': {}
                })
        return results
    
    def get_moral_summary(self, scores: Dict[str, Any], dict_type: str = 'emfd') -> Dict[str, Any]:
        """
        Generate a human-readable summary of moral framework scores.
        
        Args:
            scores: Moral framework scores dictionary
            dict_type: Dictionary type used for scoring
            
        Returns:
            Dictionary with interpreted results
        """
        summary = {
            'dictionary_used': dict_type,
            'moral_foundations': {}
        }
        
        if dict_type == 'emfd':
            foundations = ['care', 'fairness', 'loyalty', 'authority', 'sanctity']
            
            # Extract probability scores
            prob_scores = {}
            sent_scores = {}
            
            for foundation in foundations:
                prob_key = f"{foundation}_p"
                sent_key = f"{foundation}_sent"
                
                if prob_key in scores:
                    prob_scores[foundation] = scores[prob_key]
                if sent_key in scores:
                    sent_scores[foundation] = scores[sent_key]
            
            # Find dominant moral foundation
            if prob_scores:
                dominant_foundation = max(prob_scores.items(), key=lambda x: x[1])
                summary['dominant_foundation'] = {
                    'name': dominant_foundation[0],
                    'probability': dominant_foundation[1]
                }
            
            # Summarize each foundation
            for foundation in foundations:
                foundation_summary = {}
                if foundation in prob_scores:
                    foundation_summary['probability'] = prob_scores[foundation]
                    foundation_summary['strength'] = self._categorize_score(prob_scores[foundation])
                
                if foundation in sent_scores:
                    foundation_summary['sentiment'] = sent_scores[foundation]
                    foundation_summary['sentiment_direction'] = 'positive' if sent_scores[foundation] > 0 else 'negative' if sent_scores[foundation] < 0 else 'neutral'
                
                if foundation_summary:
                    summary['moral_foundations'][foundation] = foundation_summary
            
            # Add additional metrics
            if 'moral_nonmoral_ratio' in scores:
                summary['moral_density'] = {
                    'ratio': scores['moral_nonmoral_ratio'],
                    'interpretation': self._interpret_moral_density(scores['moral_nonmoral_ratio'])
                }
        
        elif dict_type in ['mfd', 'mfd2']:
            # Handle MFD and MFD2 results
            foundations = ['care.virtue', 'fairness.virtue', 'loyalty.virtue',
                          'authority.virtue', 'sanctity.virtue',
                          'care.vice', 'fairness.vice', 'loyalty.vice',
                          'authority.vice', 'sanctity.vice']
            
            for foundation in foundations:
                if foundation in scores:
                    summary['moral_foundations'][foundation] = {
                        'score': scores[foundation],
                        'strength': self._categorize_score(scores[foundation])
                    }
            
            if 'moral_nonmoral_ratio' in scores:
                summary['moral_density'] = {
                    'ratio': scores['moral_nonmoral_ratio'],
                    'interpretation': self._interpret_moral_density(scores['moral_nonmoral_ratio'])
                }
        
        return summary
    
    def _categorize_score(self, score: float) -> str:
        """Categorize a score into strength levels."""
        if score >= 0.15:
            return 'very_high'
        elif score >= 0.10:
            return 'high'
        elif score >= 0.05:
            return 'moderate'
        elif score >= 0.01:
            return 'low'
        else:
            return 'very_low'
    
    def _interpret_moral_density(self, ratio: float) -> str:
        """Interpret the moral-to-nonmoral word ratio."""
        if ratio >= 1.0:
            return 'very_high_moral_content'
        elif ratio >= 0.5:
            return 'high_moral_content'
        elif ratio >= 0.2:
            return 'moderate_moral_content'
        elif ratio >= 0.1:
            return 'low_moral_content'
        else:
            return 'very_low_moral_content'


# Convenience functions for simple use cases
def analyze_file_moral_framework(file_path: str, **kwargs) -> Dict[str, Any]:
    """Analyze moral frameworks in a file (convenience function)."""
    analyzer = MoralFrameworkAnalyzer()
    return analyzer.analyze_file(file_path, **kwargs)


def analyze_text_moral_framework(text: str, **kwargs) -> Dict[str, Any]:
    """Analyze moral frameworks in text (convenience function)."""
    analyzer = MoralFrameworkAnalyzer()
    return analyzer.analyze_text(text, **kwargs)