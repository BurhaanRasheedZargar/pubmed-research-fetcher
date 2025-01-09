# Required Libraries
import requests
import pandas as pd
import typer
import re
from typing import List, Optional

# Constants
BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
SUMMARY_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"


def fetch_paper_ids(query: str) -> List[str]:
    """
    Fetch paper IDs matching the given query from PubMed.
    """
    params = {
        'db': 'pubmed',
        'term': query,
        'retmax': 100,  # Number of papers to fetch at once
        'retmode': 'json'
    }
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json().get('esearchresult', {}).get('idlist', [])


def fetch_paper_details(paper_ids: List[str]) -> dict:
    """
    Fetch paper details for a list of paper IDs from PubMed.
    """
    if not paper_ids:
        return {}

    params = {
        'db': 'pubmed',
        'id': ','.join(paper_ids),
        'retmode': 'json'
    }
    response = requests.get(SUMMARY_URL, params=params)
    response.raise_for_status()
    return response.json().get('result', {})


def identify_non_academic_authors(authors: List[dict]) -> List[str]:
    """
    Identify non-academic authors based on affiliations.
    """
    non_academic_authors = []
    for author in authors:
        affiliation = author.get('affiliation', '').lower()
        if any(keyword in affiliation for keyword in ['pharma', 'biotech', 'company']):
            non_academic_authors.append(author.get('name', ''))
    return non_academic_authors


def extract_company_affiliations(authors: List[dict]) -> List[str]:
    """
    Extract company affiliations from author affiliations.
    """
    company_affiliations = []
    for author in authors:
        affiliation = author.get('affiliation', '').lower()
        if any(keyword in affiliation for keyword in ['pharma', 'biotech', 'company']):
            company_affiliations.append(affiliation)
    return company_affiliations


def save_to_csv(data: List[dict], filename: str):
    """
    Save the paper details to a CSV file.
    """
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


def main(query: str, filename: Optional[str] = None, debug: bool = False):
    """
    Main function to fetch and process PubMed research papers.
    """
    if debug:
        print(f"Fetching papers for query: {query}")

    paper_ids = fetch_paper_ids(query)
    if debug:
        print(f"Fetched {len(paper_ids)} paper IDs")

    details = fetch_paper_details(paper_ids)
    result_data = []

    for paper_id in paper_ids:
        paper = details.get(paper_id, {})
        if not paper:
            continue

        authors = paper.get('authors', [])

        non_academic_authors = identify_non_academic_authors(authors)
        company_affiliations = extract_company_affiliations(authors)

        result_data.append({
            'PubmedID': paper_id,
            'Title': paper.get('title', ''),
            'Publication Date': paper.get('pubdate', ''),
            'Non-academic Author(s)': ", ".join(non_academic_authors),
            'Company Affiliation(s)': ", ".join(company_affiliations),
            'Corresponding Author Email': ''  # Mock email
        })

    if filename:
        save_to_csv(result_data, filename)
        print(f"Results saved to {filename}")
    else:
        print(pd.DataFrame(result_data))


if __name__ == "__main__":
    typer.run(main)