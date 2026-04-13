"""
seed_demo.py – Seed the knowledge base with demo sources.

Usage:
    python scripts/seed_demo.py --api-url http://localhost:8000
"""
import argparse
import sys

import httpx

DEMO_URLS = [
    {
        "url": "https://en.wikipedia.org/wiki/Retrieval-augmented_generation",
        "label": "RAG – Wikipedia",
    },
    {
        "url": "https://python.langchain.com/docs/introduction/",
        "label": "LangChain – Introduction",
    },
]


def seed_urls(api_url: str) -> None:
    base = api_url.rstrip("/")
    with httpx.Client(timeout=60) as client:
        for item in DEMO_URLS:
            print(f"Ingesting: {item['label']} …", end=" ", flush=True)
            resp = client.post(
                f"{base}/api/v1/ingest/url",
                json={"url": item["url"], "source_label": item["label"]},
            )
            if resp.status_code == 201:
                data = resp.json()
                print(f"✓  ({data['chunk_count']} chunks, id={data['source_id'][:8]}…)")
            else:
                print(f"✗  HTTP {resp.status_code}: {resp.text[:200]}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed Knowledge Hub with demo data.")
    parser.add_argument(
        "--api-url",
        default="http://localhost:8000",
        help="Base URL of the running API server",
    )
    args = parser.parse_args()

    print(f"Seeding knowledge base at {args.api_url}\n")
    try:
        seed_urls(args.api_url)
    except httpx.ConnectError:
        print(f"\nError: Could not connect to {args.api_url}. Is the server running?")
        sys.exit(1)
    print("\nDone.")


if __name__ == "__main__":
    main()
