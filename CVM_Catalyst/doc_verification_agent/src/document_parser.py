"""Document parsing and extraction."""

import frontmatter
from typing import Dict, Any, List
from loguru import logger
from bs4 import BeautifulSoup


class DocumentParser:
    """Parses documents in various formats."""

    @staticmethod
    def parse_markdown(content: str) -> Dict[str, Any]:
        """
        Parse markdown content including front matter.

        Args:
            content: The markdown content

        Returns:
            A dictionary containing metadata and content
        """
        logger.info("Parsing markdown document")

        try:
            post = frontmatter.loads(content)
            return {
                "metadata": post.metadata,
                "content": post.content,
                "raw": content,
            }
        except Exception as e:
            logger.error(f"Failed to parse markdown: {e}")
            return {
                "metadata": {},
                "content": content,
                "raw": content,
            }

    @staticmethod
    def parse_html(content: str) -> Dict[str, Any]:
        """
        Parse HTML content.

        Args:
            content: The HTML content

        Returns:
            A dictionary containing extracted text and structure
        """
        logger.info("Parsing HTML document")

        try:
            soup = BeautifulSoup(content, "html.parser")
            text = soup.get_text(separator="\n", strip=True)

            return {
                "text": text,
                "title": soup.find("title").string if soup.find("title") else "",
                "headings": [h.get_text() for h in soup.find_all(["h1", "h2", "h3"])],
                "paragraphs": [p.get_text() for p in soup.find_all("p")],
                "raw": content,
            }
        except Exception as e:
            logger.error(f"Failed to parse HTML: {e}")
            return {
                "text": content,
                "raw": content,
            }

    @staticmethod
    def parse_confluence_content(confluence_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Parse Confluence API response.

        Args:
            confluence_data: The Confluence API response

        Returns:
            A dictionary containing extracted content
        """
        logger.info("Parsing Confluence content")

        try:
            body = confluence_data.get("body", {}).get("storage", {})
            content = body.get("value", "")

            return {
                "title": confluence_data.get("title", ""),
                "page_id": confluence_data.get("id", ""),
                "space": confluence_data.get("space", {}).get("key", ""),
                "content": content,
                "labels": [label.get("name") for label in confluence_data.get("metadata", {}).get("labels", {}).get("results", [])],
                "metadata": {
                    "created": confluence_data.get("version", {}).get("when", ""),
                    "created_by": confluence_data.get("version", {}).get("by", {}).get("username", ""),
                },
                "raw": confluence_data,
            }
        except Exception as e:
            logger.error(f"Failed to parse Confluence content: {e}")
            return confluence_data

    @staticmethod
    def extract_sections(content: str) -> List[Dict[str, str]]:
        """
        Extract sections from markdown or text content.

        Args:
            content: The document content

        Returns:
            A list of sections with their content
        """
        sections = []
        current_section = None
        current_content = []

        for line in content.split("\n"):
            if line.startswith("#"):
                if current_section:
                    sections.append({
                        "heading": current_section,
                        "content": "\n".join(current_content).strip(),
                    })
                current_section = line.lstrip("#").strip()
                current_content = []
            else:
                current_content.append(line)

        if current_section:
            sections.append({
                "heading": current_section,
                "content": "\n".join(current_content).strip(),
            })

        return sections
