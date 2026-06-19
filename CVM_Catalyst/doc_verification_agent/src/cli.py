"""CLI for document verification agent."""

import sys
import argparse
from pathlib import Path
from doc_verification_agent import DocumentVerificationAgent
from loguru import logger


def setup_logging(debug: bool = False):
    """Configure logging."""
    level = "DEBUG" if debug else "INFO"
    logger.remove()
    logger.add(
        sys.stderr,
        format="<level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>",
        level=level,
    )


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Document verification agent for checking document readiness"
    )

    parser.add_argument(
        "--url",
        type=str,
        help="URL of the document to verify",
    )
    parser.add_argument(
        "--page-id",
        type=str,
        help="Confluence page ID to verify",
    )
    parser.add_argument(
        "--template",
        type=str,
        required=True,
        help="Path to template markdown file",
    )
    parser.add_argument(
        "--file",
        type=str,
        help="File containing list of URLs (one per line)",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Enable debug logging",
    )

    args = parser.parse_args()

    setup_logging(args.debug)

    if not any([args.url, args.page_id, args.file]):
        parser.error("Must provide --url, --page-id, or --file")

    if not Path(args.template).exists():
        parser.error(f"Template file not found: {args.template}")

    agent = DocumentVerificationAgent()

    try:
        if args.url:
            logger.info(f"Verifying document: {args.url}")
            result = agent.verify_document(args.url, args.template)
            print_result(result)

        elif args.page_id:
            logger.info(f"Verifying Confluence page: {args.page_id}")
            result = agent.verify_confluence_document(args.page_id, args.template)
            print_result(result)

        elif args.file:
            with open(args.file, "r") as f:
                urls = [line.strip() for line in f if line.strip()]
            logger.info(f"Batch verifying {len(urls)} documents")
            results = agent.batch_verify(urls, args.template)
            print_batch_results(results)

    except Exception as e:
        logger.error(f"Verification failed: {e}")
        sys.exit(1)


def print_result(result):
    """Print verification result."""
    print("\n" + "=" * 60)
    print(f"Document: {result.url}")
    print(f"Score: {result.score}/10")
    print("=" * 60)

    if "strengths" in result.llm_feedback:
        print("\nStrengths:")
        for strength in result.llm_feedback["strengths"]:
            print(f"  ✓ {strength}")

    if "improvements" in result.llm_feedback:
        print("\nAreas for Improvement:")
        for improvement in result.llm_feedback["improvements"]:
            print(f"  ✗ {improvement}")

    if "action_items" in result.llm_feedback:
        print("\nAction Items:")
        for item in result.llm_feedback["action_items"]:
            print(f"  → {item}")

    print("\n" + "=" * 60)


def print_batch_results(results):
    """Print batch verification results."""
    print("\n" + "=" * 60)
    print(f"Batch Verification Results ({len(results)} documents)")
    print("=" * 60)

    scores = [r.score for r in results]
    avg_score = sum(scores) / len(scores) if scores else 0

    for result in results:
        status = "✓" if result.score >= 7 else "✗"
        print(f"{status} {result.url}: {result.score}/10")

    print("\n" + "-" * 60)
    print(f"Average Score: {avg_score:.1f}/10")
    print(f"Pass Rate: {sum(1 for s in scores if s >= 7)}/{len(results)}")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
