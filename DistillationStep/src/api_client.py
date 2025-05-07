"""
This module handles all interactions with the Together API for processing hadith texts.
It includes prompt templates and response processing.
"""

from typing import Dict, Any, Optional
from together import Together
from .utils import estimate_tokens, get_fixed_questions

class TogetherAPIClient:
    """
    Handles all interactions with the Together API including prompt creation,
    API calls, and response processing.
    """

    PROMPT_TEMPLATE = """
You are an expert in analyzing Prophetic Hadiths and Islamic jurisprudence.
Your task is to analyze an Arabic Hadith using the provided explanation to extract knowledge, jurisprudential rulings, and practical applications.

== INPUT ==
You will receive:
- 'hadith': Text of the Prophetic Hadith in Arabic (with diacritics).
- 'explanation': Detailed explanation of the Hadith (Arabic text).

== TASK ==
Based on the provided Hadith, explanation, and your knowledge, answer the following questions in JSON format.

== FIXED QUESTIONS ==
Answer ONLY these questions without repeating the question text:
1. What are the main messages, lessons learned, and benefits derived from the Hadith?
2. How can the Hadith be applied in daily life?
3. What is the importance of the Hadith in Islamic jurisprudence?
4. What is the reason or context behind the narration of the Hadith?

== RULES ==
- Use Modern Standard Arabic with full diacritics in your answers.
- Base your answers on the provided explanation and your knowledge of authentic Hadiths.
- Ensure each answer accurately reflects the content and meaning of the Hadith without incorporating personal interpretations or conclusions.
- Verify the authenticity of all information before preparing your response.
- Return ONLY a JSON array with your answers as shown below, without any additional comments or explanations.

== Expected Input ==
{{
  "hadith": "{hadith}",
  "sharh": "{sharh}"
}}

== Expected Output (JSON Array) ==
[
  "الإجابة الأولى مع التشكيل الكامل...",
  "الإجابة الثانية مع التشكيل الكامل...",
  "الإجابة الثالثة مع التشكيل الكامل...",
  "الإجابة الرابعة مع التشكيل الكامل..."
]
"""

    def __init__(self, api_key: str):
        """
        Initialize the API client.
        
        Args:
            api_key (str): The Together API key
        """
        self.client = Together(api_key=api_key)
        self.fixed_questions = get_fixed_questions()

    def process_hadith(self, hadith: str, sharh: str) -> Optional[Dict[str, Any]]:
        """
        Process a single hadith through the Together API.

        Args:
            hadith (str): The hadith text
            sharh (str): The explanation text

        Returns:
            Optional[Dict[str, Any]]: Processed data including tokens and answers,
                                    or None if processing failed
        """
        try:
            # Format prompt
            prompt = self.PROMPT_TEMPLATE.format(
                hadith=hadith,
                sharh=sharh
            )
            
            # Estimate tokens before generation
            tokens_before = estimate_tokens(prompt)
            
            # Get API response
            response = self.client.chat.completions.create(
                model="deepseek-ai/DeepSeek-V3",
                messages=[{"role": "user", "content": prompt}],
                stream=True
            )
            
            # Collect streaming response
            output_text = ""
            for token in response:
                if hasattr(token, 'choices') and token.choices[0].delta.content:
                    output_text += token.choices[0].delta.content
            
            # Clean and parse response
            answers = self._parse_response(output_text)
            if not answers:
                return None
            
            # Calculate tokens after
            tokens_after = estimate_tokens(output_text)
            
            # Create QA pairs
            qa_pairs = []
            for i, answer in enumerate(answers[:4]):
                qa_pair = {
                    "question": self.fixed_questions[i]["question"],
                    "answer": answer
                }
                qa_pairs.append(qa_pair)
            
            return {
                "tokens_before": tokens_before,
                "tokens_after": tokens_after,
                "answers": answers,
                "qa_pairs": qa_pairs
            }
            
        except Exception as e:
            print(f"Error processing hadith: {str(e)}")
            return None

    def _parse_response(self, response_text: str) -> Optional[list]:
        """
        Parse and clean the API response text.
        
        Args:
            response_text (str): Raw response from the API
            
        Returns:
            Optional[list]: List of answers or None if parsing failed
        """
        try:
            # Clean the response text
            text = response_text.strip()
            if text.startswith("```json"):
                text = text[7:]
            if text.endswith("```"):
                text = text[:-3]
            text = text.strip()
            
            # Parse JSON and validate
            import json
            answers = json.loads(text)
            
            if not isinstance(answers, list):
                return None
                
            # Ensure we have exactly 4 answers
            while len(answers) < 4:
                answers.append("")
                
            return answers[:4]
            
        except Exception as e:
            print(f"Error parsing response: {str(e)}")
            return None