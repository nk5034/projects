"""LLM-based document scoring."""

from typing import Dict, Any, Optional
from loguru import logger
from .config import settings


class LLMScorer:
    """Scores documents using LLM APIs."""

    def __init__(self, api_provider: Optional[str] = None):
        """
        Initialize the LLM scorer.

        Args:
            api_provider: LLM provider to use (openai, anthropic)
        """
        self.provider = api_provider or settings.llm_provider
        self._initialize_client()

    def _initialize_client(self):
        """Initialize the appropriate LLM client."""
        if self.provider == "openai":
            try:
                import openai
                self.client = openai.OpenAI(api_key=settings.openai_api_key)
                self.model = settings.openai_model
                logger.info(f"Initialized OpenAI client with model {self.model}")
            except ImportError:
                logger.error("OpenAI package not installed")
                raise
        elif self.provider == "anthropic":
            try:
                import anthropic
                self.client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
                self.model = settings.anthropic_model
                logger.info(f"Initialized Anthropic client with model {self.model}")
            except ImportError:
                logger.error("Anthropic package not installed")
                raise
        else:
            raise ValueError(f"Unsupported LLM provider: {self.provider}")

    def score_document(
        self,
        document_content: str,
        template_content: str,
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Score a document using LLM.

        Args:
            document_content: The document to score
            template_content: The template to compare against
            additional_context: Additional context for scoring

        Returns:
            Scoring results including score and feedback
        """
        logger.info(f"Scoring document using {self.provider}")

        prompt = self._build_scoring_prompt(
            document_content,
            template_content,
            additional_context,
        )

        try:
            if self.provider == "openai":
                response = self._score_with_openai(prompt)
            elif self.provider == "anthropic":
                response = self._score_with_anthropic(prompt)

            return self._parse_llm_response(response)
        except Exception as e:
            logger.error(f"Failed to score document: {e}")
            raise

    def _build_scoring_prompt(
        self,
        document: str,
        template: str,
        context: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Build the scoring prompt for the LLM."""
        context_str = ""
        if context:
            context_str = f"\n\nAdditional Context:\n{context}"

        return f"""You are a document quality and readiness assessor. 

Please evaluate the following document against the template provided. Score it from 1-10 based on:
1. Completeness: Does it cover all required sections?
2. Clarity: Is the writing clear and professional?
3. Structure: Does it follow the template structure?
4. Accuracy: Is the information accurate?
5. Consistency: Is the style and tone consistent?

Document to evaluate:
---
{document}
---

Template to compare against:
---
{template}
---
{context_str}

Please provide:
1. A score from 1-10
2. A brief summary of strengths (2-3 bullet points)
3. A brief summary of areas for improvement (2-3 bullet points)
4. Specific action items to improve the document

Format your response as JSON with keys: score, summary, strengths, improvements, action_items
"""

    def _score_with_openai(self, prompt: str) -> str:
        """Score using OpenAI API."""
        logger.debug("Calling OpenAI API for scoring")

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        # Note: This assumes messages API - adjust if using completions
        return message.content[0].text

    def _score_with_anthropic(self, prompt: str) -> str:
        """Score using Anthropic API."""
        logger.debug("Calling Anthropic API for scoring")

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": prompt}
            ],
        )

        return message.content[0].text

    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """Parse LLM response and extract scoring data."""
        logger.info("Parsing LLM response")

        try:
            import json
            import re

            # Try to extract JSON from response
            json_match = re.search(r"\{.*\}", response, re.DOTALL)
            if json_match:
                data = json.loads(json_match.group())
                # Ensure score is within valid range
                score = int(data.get("score", 5))
                score = max(settings.min_score, min(settings.max_score, score))
                data["score"] = score
                return data
        except (json.JSONDecodeError, ValueError) as e:
            logger.warning(f"Failed to parse LLM response as JSON: {e}")

        # Fallback: extract score from text
        import re
        score_match = re.search(r"(\d+)\s*(?:/10|out of 10)", response)
        score = int(score_match.group(1)) if score_match else 5

        return {
            "score": score,
            "raw_response": response,
            "parsed_from_text": True,
        }
