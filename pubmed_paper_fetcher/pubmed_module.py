import requests
import pandas as pd
from typing import List, Dict, Any

class PubMedAPI:
    BASE_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    DETAILS_URL = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"

    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def fetch_papers(self, query: str, max_results: int = 100) -> List[str]:
        params = {
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "api_key": self.api_key
        }
        response = requests.get(self.BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("esearchresult", {}).get("idlist", [])

    def fetch_details(self, pubmed_ids: List[str]) -> List[Dict[str, Any]]:
        if not pubmed_ids:
            return []
        params = {
            "db": "pubmed",
            "id": ",".join(pubmed_ids),
            "retmode": "json",
            "api_key": self.api_key
        }
        response = requests.get(self.DETAILS_URL, params=params)
        response.raise_for_status()
        return response.json().get("result", {}).values()


def identify_non_academic_authors(authors: List[Dict[str, str]]) -> List[Dict[str, str]]:
    non_academic = []
    for author in authors:
        affiliation = author.get("affiliation", "").lower()
        if any(keyword in affiliation for keyword in ["pharma", "biotech", "inc", "ltd", "corporation"]):
            non_academic.append({
                "name": author.get("name", "Unknown"),
                "affiliation": affiliation
            })
    return non_academic


def save_to_csv(data: List[Dict[str, Any]], filename: str):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)


