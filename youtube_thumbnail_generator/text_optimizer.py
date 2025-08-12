import os
import time
from typing import Optional
import google.generativeai as genai
from langdetect import detect


class TextOptimizer:
    """Handles AI-powered text optimization using Gemini."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the text optimizer.
        
        Args:
            api_key: Gemini API key
        """
        self.api_key = api_key
        self.model = None
        
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                self.model = genai.GenerativeModel('gemini-pro')
            except Exception as e:
                print(f"Warning: Failed to initialize Gemini AI: {e}")
                self.model = None
    
    def optimize(
        self,
        text: str,
        source_language: str = "en",
        target_language: str = "en",
        custom_prompt: Optional[str] = None,
        max_length: int = 50,
        style: str = "engaging"
    ) -> str:
        """Optimize text for YouTube thumbnails.
        
        Args:
            text: Original text to optimize
            source_language: Language of input text (en/zh)
            target_language: Target language for output (en/zh)
            custom_prompt: Custom optimization prompt
            max_length: Maximum character length
            style: Style of optimization (engaging/professional/casual/dramatic)
        
        Returns:
            Optimized text or original if optimization fails
        """
        if not self.model:
            return text
        
        try:
            # Build the optimization prompt
            if custom_prompt:
                prompt = custom_prompt.format(text=text)
            else:
                source_lang_name = "English" if source_language == "en" else "Chinese"
                target_lang_name = "English" if target_language == "en" else "Chinese"
                
                # Check if translation is needed
                if source_language != target_language:
                    # Translation + optimization
                    prompt = f"""
                    Translate and optimize this {source_lang_name} text for a YouTube thumbnail.
                    Translate it to {target_lang_name} and make it more {style} and attention-grabbing.
                    
                    Requirements:
                    - Translate from {source_lang_name} to {target_lang_name}
                    - Maximum {max_length} characters
                    - Should be catchy and clickable
                    - Use power words appropriate for {target_lang_name} audience
                    - Keep the core meaning
                    
                    Original text: "{text}"
                    
                    Return ONLY the translated and optimized text in {target_lang_name}, nothing else.
                    """
                else:
                    # Just optimization in the same language
                    prompt = f"""
                    Optimize this {source_lang_name} text for a YouTube thumbnail. 
                    Make it more {style} and attention-grabbing.
                    
                    Requirements:
                    - Keep it in {source_lang_name}
                    - Maximum {max_length} characters
                    - Should be catchy and clickable
                    - Use power words when appropriate
                    - Keep the core meaning
                    
                    Original text: "{text}"
                    
                    Return ONLY the optimized text, nothing else.
                    """
            
            # Generate optimized text
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                optimized = response.text.strip()
                
                # Remove quotes if present
                if optimized.startswith('"') and optimized.endswith('"'):
                    optimized = optimized[1:-1]
                
                # Ensure it's not too long
                if len(optimized) > max_length:
                    # Try to shorten intelligently
                    optimized = self._shorten_text(optimized, max_length)
                
                return optimized
            
        except Exception as e:
            print(f"Warning: Text optimization failed: {e}")
        
        return text
    
    def _shorten_text(self, text: str, max_length: int) -> str:
        """Shorten text to fit within max_length.
        
        Args:
            text: Text to shorten
            max_length: Maximum length
        
        Returns:
            Shortened text
        """
        if len(text) <= max_length:
            return text
        
        # Try to cut at word boundary
        truncated = text[:max_length]
        last_space = truncated.rfind(' ')
        
        if last_space > max_length * 0.7:  # If we have a reasonable cut point
            return truncated[:last_space].strip()
        
        return truncated.strip()
    
    def batch_optimize(self, texts: list, **kwargs) -> list:
        """Optimize multiple texts in batch.
        
        Args:
            texts: List of texts to optimize
            **kwargs: Additional arguments for optimize()
        
        Returns:
            List of optimized texts
        """
        optimized_texts = []
        
        for text in texts:
            optimized = self.optimize(text, **kwargs)
            optimized_texts.append(optimized)
            
            # Add small delay to avoid rate limiting
            time.sleep(0.5)
        
        return optimized_texts