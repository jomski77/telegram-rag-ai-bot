import argparse
import asyncio
from query_data import query_rag

async def main():
    # Create CLI.
    parser = argparse.ArgumentParser()
    parser.add_argument("query_text", type=str, help="The query text.")
    args = parser.parse_args()
    query_text = args.query_text
    print("\n")
    print(await query_rag(query_text))


if __name__ == "__main__":
    asyncio.run(main())
