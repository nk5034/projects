"""Tests for the main verification agent."""

import pytest
from unittest.mock import Mock, patch
from doc_verification_agent import DocumentVerificationAgent


@pytest.fixture
def agent():
    """Create a test agent with mocked components."""
    fetcher = Mock()
    parser = Mock()
    matcher = Mock()
    scorer = Mock()

    return DocumentVerificationAgent(
        fetcher=fetcher,
        parser=parser,
        matcher=matcher,
        scorer=scorer,
    )


def test_agent_initialization(agent):
    """Test that agent initializes correctly."""
    assert agent is not None
    assert agent.fetcher is not None
    assert agent.parser is not None
    assert agent.matcher is not None
    assert agent.scorer is not None


def test_verify_document_flow(agent):
    """Test the document verification flow."""
    # Setup mocks
    agent.fetcher.fetch_from_url.return_value = "test content"
    agent.parser.parse_markdown.return_value = {"content": "test"}
    agent.matcher.load_template.return_value = {"content": "template"}
    agent.matcher.get_matching_score.return_value = {"score": 75}
    agent.scorer.score_document.return_value = {"score": 8}

    # Test verification
    result = agent.verify_document(
        url="https://example.com/doc",
        template_path="templates/example.md",
    )

    assert result.score == 8
    assert result.url == "https://example.com/doc"
    agent.fetcher.fetch_from_url.assert_called_once()
    agent.scorer.score_document.assert_called_once()


@pytest.mark.parametrize("urls,expected_count", [
    (["url1", "url2"], 2),
    (["url1"], 1),
    ([], 0),
])
def test_batch_verify(agent, urls, expected_count):
    """Test batch verification with different URL counts."""
    agent.fetcher.fetch_from_url.return_value = "test content"
    agent.parser.parse_markdown.return_value = {"content": "test"}
    agent.matcher.load_template.return_value = {"content": "template"}
    agent.matcher.get_matching_score.return_value = {"score": 75}
    agent.scorer.score_document.return_value = {"score": 8}

    results = agent.batch_verify(urls, "templates/example.md")

    assert len(results) == expected_count


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
