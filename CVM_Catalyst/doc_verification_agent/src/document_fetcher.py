"""Document fetching from various sources (URLs, Confluence, etc.)."""

import requests
from typing import Optional, Dict, Any
from loguru import logger
from .config import settings


class DocumentFetcher:
    """Fetches documents from URLs and other sources."""

    def __init__(self):
        """Initialize the document fetcher."""
        self.timeout = settings.request_timeout
        self.max_retries = settings.max_retries
        self.headers = {
            "User-Agent": settings.user_agent,
        }

    def fetch_from_url(self, url: str) -> str:
        """
        Fetch document content from a URL.

        Args:
            url: The URL to fetch from

        Returns:
            The document content as a string

        Raises:
            requests.RequestException: If the request fails
        """
        logger.info(f"Fetching document from: {url}")

        try:
            response = requests.get(
                url,
                headers=self.headers,
                timeout=self.timeout,
            )
            response.raise_for_status()
            logger.info(f"Successfully fetched document from {url}")
            return response.text
        except requests.RequestException as e:
            logger.error(f"Failed to fetch document from {url}: {e}")
            raise

    def fetch_from_confluence(
        self,
        page_id: str,
        expand: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Fetch a document from Confluence.

        Args:
            page_id: The Confluence page ID
            expand: Additional fields to expand (e.g., 'body.storage')

        Returns:
            The Confluence page data as a dictionary

        Raises:
            requests.RequestException: If the request fails
        """
        if not settings.confluence_base_url:
            raise ValueError("CONFLUENCE_BASE_URL not configured")

        url = f"{settings.confluence_base_url}/rest/api/content/{page_id}"
        params = {"expand": expand or "body.storage,metadata.labels"}

        headers = {
            **self.headers,
            "Authorization": f"Bearer {settings.confluence_api_token}",
        }

        logger.info(f"Fetching Confluence page: {page_id}")

        try:
            response = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            response.raise_for_status()
            logger.info(f"Successfully fetched Confluence page: {page_id}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch Confluence page {page_id}: {e}")
            raise

    def fetch_with_retry(self, url: str, method: str = "GET") -> str:
        """
        Fetch a document with retry logic.

        Args:
            url: The URL to fetch from
            method: HTTP method to use

        Returns:
            The document content as a string

        Raises:
            requests.RequestException: If all retries fail
        """
        last_exception = None

        for attempt in range(self.max_retries):
            try:
                logger.info(f"Fetch attempt {attempt + 1}/{self.max_retries} for {url}")
                return self.fetch_from_url(url)
            except requests.RequestException as e:
                last_exception = e
                logger.warning(f"Attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    continue

        raise last_exception or RuntimeError("Failed to fetch document after retries")
