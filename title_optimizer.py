#!/usr/bin/env python3
"""
Title Optimizer using Google Gemini API
Optimizes mixed-language titles into single-language, properly formatted titles.
"""

import google.generativeai as genai
import os
import logging
from typing import Optional, Tuple

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# System prompt for title optimization
TITLE_OPTIMIZATION_SYSTEM_PROMPT = """You are a professional YouTube title optimizer. Your task is to convert mixed-language or poorly formatted titles into clean, single-language titles optimized for YouTube thumbnails.

CRITICAL RULES:
1. OUTPUT ONLY THE OPTIMIZED TITLE - No prefixes, suffixes, quotes, or explanations
2. Use SINGLE LANGUAGE ONLY - Pure Chinese OR Pure English OR Pure other language
3. Maintain the original meaning and intent
4. Optimize for YouTube thumbnail readability
5. Length guidelines: Chinese 10-18 characters, English 7-12 words

LANGUAGE DECISION RULES:
- If >60% Chinese characters: Convert to pure Chinese
- If >60% English words: Convert to pure English  
- Otherwise: Choose the dominant language and convert entirely

FORMATTING RULES:
- Remove unnecessary punctuation for thumbnails
- Use title case for English
- No quotation marks, brackets, or special symbols
- Make it catchy and clickable

EXAMPLES:
Input: "AI技术指南 Complete Tutorial 2024"
Output: AI技术完整指南教程

Input: "Learn Python编程 from Zero"  
Output: Learn Python Programming from Zero

Input: "最新科技News今日更新"
Output: 最新科技资讯今日更新

Remember: Output ONLY the optimized title, nothing else."""

class TitleOptimizer:
    """Google Gemini-powered title optimizer"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize title optimizer with Gemini API
        
        Args:
            api_key: Google API key. If None, tries to get from environment
        """
        self.api_key = api_key or os.getenv("GOOGLE_API_KEY")
        self.model = None
        self.is_available = False
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel(
                    "gemini-2.0-flash-exp",
                    system_instruction=TITLE_OPTIMIZATION_SYSTEM_PROMPT
                )
                self.is_available = True
                logger.info("Title optimizer initialized with Gemini API")
            except Exception as e:
                logger.warning(f"Failed to initialize Gemini API: {e}")
                self.is_available = False
        else:
            logger.info("No Google API key provided - title optimization disabled")
    
    def optimize_title(self, title: str) -> Tuple[str, bool]:
        """
        Optimize title using Gemini API
        
        Args:
            title: Original title to optimize
            
        Returns:
            Tuple of (optimized_title, was_optimized)
            - If optimization succeeds: (optimized_title, True)
            - If optimization fails/unavailable: (original_title, False)
        """
        # Return original if API not available
        if not self.is_available:
            logger.info("Gemini API not available - using original title")
            return title, False
        
        # Check if title needs optimization (contains mixed languages)
        if not self._needs_optimization(title):
            logger.info("Title appears to be single language - no optimization needed")
            return title, False
        
        try:
            # Generate optimized title using system instruction
            response = self.model.generate_content(
                title,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,  # Low temperature for consistent results
                    max_output_tokens=50,  # Very short response - just the title
                )
            )
            
            optimized_title = response.text.strip()
            
            # Validate the response
            if optimized_title and len(optimized_title) > 0:
                logger.info(f"Title optimized: '{title}' -> '{optimized_title}'")
                return optimized_title, True
            else:
                logger.warning("Empty response from Gemini - using original title")
                return title, False
                
        except Exception as e:
            logger.error(f"Title optimization failed: {e}")
            return title, False
    
    def _needs_optimization(self, title: str) -> bool:
        """
        Check if title contains mixed languages and needs optimization
        
        Args:
            title: Title to check
            
        Returns:
            True if title needs optimization, False otherwise
        """
        # Count Chinese characters
        chinese_chars = sum(1 for char in title if '\u4e00' <= char <= '\u9fff')
        total_chars = len(title.replace(' ', ''))  # Exclude spaces
        
        if total_chars == 0:
            return False
        
        chinese_ratio = chinese_chars / total_chars
        
        # If it's clearly one language, no optimization needed
        if chinese_ratio >= 0.9 or chinese_ratio <= 0.1:
            return False
        
        # Mixed language detected
        return True
    
    @property
    def system_prompt(self) -> str:
        """Get the system prompt used for optimization"""
        return TITLE_OPTIMIZATION_SYSTEM_PROMPT

def create_title_optimizer(api_key: Optional[str] = None) -> TitleOptimizer:
    """
    Factory function to create title optimizer
    
    Args:
        api_key: Google API key. If None, tries environment variables
        
    Returns:
        TitleOptimizer instance
    """
    return TitleOptimizer(api_key)

# Example usage and testing
if __name__ == "__main__":
    # Test the title optimizer
    optimizer = create_title_optimizer()
    
    test_titles = [
        "AI技术指南 Complete Tutorial 2024",
        "Learn Python编程 from Zero", 
        "最新科技News今日更新",
        "Complete AI Technology Guide",  # Pure English
        "完整人工智能技术指南",  # Pure Chinese
    ]
    
    for title in test_titles:
        optimized, was_optimized = optimizer.optimize_title(title)
        status = "✅ OPTIMIZED" if was_optimized else "➡️ UNCHANGED"
        print(f"{status}: '{title}' -> '{optimized}'")