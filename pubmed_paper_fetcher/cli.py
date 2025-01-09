import argparse
import sys
import pandas as pd
from pubmed_module import PubMedAPI, identify_non_academic_authors, save_to_csv

def main():
    parser = argparse.ArgumentParser(description="Fetch research papers from PubMed based on a query.")
    parser.add_argument("query", type=str, help="Search query for PubMed.")
    parser.add_argument("-f", "--file", type=str, help="Output CSV file name.", default=None)
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug mode.")

    args = parser.parse_args()

    api = PubMedAPI()
    try:
        pubmed_ids = api.fetch_papers(args.query)
        if args.debug:
            print(f"Fetched PubMed IDs: {pubmed_ids}")

        details = api.fetch_details(pubmed_ids)
        results = []
        for paper in details:
            authors = paper.get("authors", [])
            non_academic_authors = identify_non_academic_authors(authors)
            results.append({
                "PubmedID": paper.get("uid"),
                "Title": paper.get("title"),
                "Publication Date": paper.get("pubdate"),
                "Non-academic Author(s)": ", ".join([a["name"] for a in non_academic_authors]),
                "Company Affiliation(s)": ", ".join([a["affiliation"] for a in non_academic_authors]),
                "Corresponding Author Email": paper.get("corresponding_email", "Unknown")
            })

        if args.file:
            save_to_csv(results, args.file)
            print(f"Results saved to {args.file}")
        else:
            print(pd.DataFrame(results))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()