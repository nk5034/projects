"""Main document verification agent."""

from typing import Dict, Any, Optional
from dataclasses import dataclass
from loguru import logger

from .document_fetcher import DocumentFetcher
from .document_parser import DocumentParser
from .template_matcher import TemplateMatcher
from .llm_scorer import LLMScorer


@dataclass
class VerificationResult:
    """Result of document verification."""
    url: str
    score: int
    template_match: Dict[str, Any]
    llm_feedback: Dict[str, Any]
    raw_content: str
    parsed_content: Dict[str, Any]


class DocumentVerificationAgent:
    """Main agent that orchestrates document verification."""

    def __init__(
        self,
        fetcher: Optional[DocumentFetcher] = None,
        parser: Optional[DocumentParser] = None,
        matcher: Optional[TemplateMatcher] = None,
        scorer: Optional[LLMScorer] = None,
    ):
        """
        Initialize the verification agent.

        Args:
            fetcher: Document fetcher instance
            parser: Document parser instance
            matcher: Template matcher instance
            scorer: LLM scorer instance
        """
        self.fetcher = fetcher or DocumentFetcher()
        self.parser = parser or DocumentParser()
        self.matcher = matcher or TemplateMatcher()
        self.scorer = scorer or LLMScorer()

    def verify_document(
        self,
        url: str,
        template_path: str,
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> VerificationResult:
        """
        Verify a document against a template.

        Args:
            url: URL of the document to verify
            template_path: Path to the template markdown file
            additional_context: Additional context for scoring

        Returns:
            VerificationResult with score and feedback
        """
        logger.info(f"Starting verification for {url}")

        # Step 1: Fetch the document
        logger.info("Step 1: Fetching document")
        raw_content = self.fetcher.fetch_from_url(url)

        # Step 2: Parse the document
        logger.info("Step 2: Parsing document")
        parsed_document = self.parser.parse_markdown(raw_content)

        # Step 3: Load and parse template
        logger.info("Step 3: Loading template")
        template = self.matcher.load_template(template_path)

        # Step 4: Compare against template
        logger.info("Step 4: Comparing against template")
        template_match = self.matcher.get_matching_score(parsed_document, template)

        # Step 5: Score with LLM
        logger.info("Step 5: Scoring with LLM")
        llm_feedback = self.scorer.score_document(
            raw_content,
            template.get("content", ""),
            additional_context,
        )

        score = llm_feedback.get("score", 5)

        result = VerificationResult(
            url=url,
            score=score,
            template_match=template_match,
            llm_feedback=llm_feedback,
            raw_content=raw_content,
            parsed_content=parsed_document,
        )

        logger.info(f"Verification complete. Score: {score}/10")
        return result

    def verify_confluence_document(
        self,
        page_id: str,
        template_path: str,
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> VerificationResult:
        """
        Verify a Confluence document against a template.

        Args:
            page_id: Confluence page ID
            template_path: Path to the template markdown file
            additional_context: Additional context for scoring

        Returns:
            VerificationResult with score and feedback
        """
        logger.info(f"Starting Confluence verification for page {page_id}")

        # Step 1: Fetch from Confluence
        logger.info("Step 1: Fetching from Confluence")
        confluence_data = self.fetcher.fetch_from_confluence(page_id)

        # Step 2: Parse Confluence content
        logger.info("Step 2: Parsing Confluence content")
        parsed_document = self.parser.parse_confluence_content(confluence_data)

        # Step 3: Load and parse template
        logger.info("Step 3: Loading template")
        template = self.matcher.load_template(template_path)

        # Step 4: Compare against template
        logger.info("Step 4: Comparing against template")
        template_match = self.matcher.get_matching_score(parsed_document, template)

        # Step 5: Score with LLM
        logger.info("Step 5: Scoring with LLM")
        llm_feedback = self.scorer.score_document(
            parsed_document.get("content", ""),
            template.get("content", ""),
            additional_context,
        )

        score = llm_feedback.get("score", 5)

        result = VerificationResult(
            url=f"confluence://{page_id}",
            score=score,
            template_match=template_match,
            llm_feedback=llm_feedback,
            raw_content=confluence_data,
            parsed_content=parsed_document,
        )

        logger.info(f"Confluence verification complete. Score: {score}/10")
        return result

    def batch_verify(
        self,
        urls: list,
        template_path: str,
        additional_context: Optional[Dict[str, Any]] = None,
    ) -> list:
        """
        Verify multiple documents.

        Args:
            urls: List of URLs to verify
            template_path: Path to the template markdown file
            additional_context: Additional context for scoring

        Returns:
            List of VerificationResult objects
        """
        logger.info(f"Starting batch verification for {len(urls)} documents")

        results = []
        for url in urls:
            try:
                result = self.verify_document(url, template_path, additional_context)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to verify {url}: {e}")

        logger.info(f"Batch verification complete. Processed {len(results)} documents")
        return results
