"""Template matching and comparison logic."""

from typing import Dict, List, Any
from loguru import logger
from .document_parser import DocumentParser


class TemplateMatcher:
    """Matches and compares documents against templates."""

    def __init__(self):
        """Initialize the template matcher."""
        self.parser = DocumentParser()

    def load_template(self, template_path: str) -> Dict[str, Any]:
        """
        Load a markdown template file.

        Args:
            template_path: Path to the template markdown file

        Returns:
            Parsed template content
        """
        logger.info(f"Loading template from: {template_path}")

        try:
            with open(template_path, "r", encoding="utf-8") as f:
                content = f.read()
            return self.parser.parse_markdown(content)
        except Exception as e:
            logger.error(f"Failed to load template: {e}")
            raise

    def compare_structures(
        self,
        document: Dict[str, Any],
        template: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Compare document structure against template.

        Args:
            document: Parsed document
            template: Parsed template

        Returns:
            Comparison results
        """
        logger.info("Comparing document structure against template")

        doc_sections = self.parser.extract_sections(document.get("content", ""))
        template_sections = self.parser.extract_sections(template.get("content", ""))

        template_headings = {s["heading"].lower() for s in template_sections}
        doc_headings = {s["heading"].lower() for s in doc_sections}

        missing_sections = template_headings - doc_headings
        extra_sections = doc_headings - template_headings
        matching_sections = template_headings & doc_headings

        return {
            "matching_sections": list(matching_sections),
            "missing_sections": list(missing_sections),
            "extra_sections": list(extra_sections),
            "template_section_count": len(template_sections),
            "document_section_count": len(doc_sections),
            "completeness_ratio": len(matching_sections) / len(template_sections)
            if template_sections else 0,
        }

    def check_metadata(
        self,
        document: Dict[str, Any],
        template: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Check if document metadata matches template requirements.

        Args:
            document: Parsed document
            template: Parsed template

        Returns:
            Metadata check results
        """
        logger.info("Checking document metadata")

        template_metadata = template.get("metadata", {})
        doc_metadata = document.get("metadata", {})

        required_fields = set(template_metadata.keys())
        present_fields = set(k for k in doc_metadata.keys() if doc_metadata[k])

        missing_metadata = required_fields - present_fields

        return {
            "required_fields": list(required_fields),
            "present_fields": list(present_fields),
            "missing_fields": list(missing_metadata),
            "metadata_completeness": len(present_fields) / len(required_fields)
            if required_fields else 1.0,
        }

    def get_matching_score(
        self,
        document: Dict[str, Any],
        template: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate a matching score between document and template.

        Args:
            document: Parsed document
            template: Parsed template

        Returns:
            Matching score and analysis
        """
        structure_comparison = self.compare_structures(document, template)
        metadata_check = self.check_metadata(document, template)

        structure_score = structure_comparison.get("completeness_ratio", 0) * 100
        metadata_score = metadata_check.get("metadata_completeness", 0) * 100

        overall_score = (structure_score + metadata_score) / 2

        return {
            "overall_score": overall_score,
            "structure_score": structure_score,
            "metadata_score": metadata_score,
            "structure_comparison": structure_comparison,
            "metadata_check": metadata_check,
        }
