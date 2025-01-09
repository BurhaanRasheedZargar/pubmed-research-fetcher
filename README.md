# Research Paper Fetcher

## Overview
The Research Paper Fetcher is a Python-based command-line program that fetches research papers from PubMed using a user-specified query. It identifies papers with authors affiliated with pharmaceutical or biotech companies and exports the results to a CSV file.

## Features
1. **Fetch Research Papers:**
   - Queries PubMed using its full syntax.
   - Retrieves metadata for up to 100 papers per query.
2. **Filter Authors:**
   - Identifies authors affiliated with non-academic institutions such as pharmaceutical or biotech companies.
3. **Output Options:**
   - Saves results as a CSV file.
   - Displays results in the console if no file is specified.
4. **Debug Mode:**
   - Provides detailed information about execution for debugging.
5. **Robust Error Handling:**
   - Handles invalid queries, API failures, and missing data gracefully.

## Project Structure
```
.
├── pubmed_module.py   # Core module for PubMed API interaction and filtering
├── cli.py             # Command-line interface for the program
├── pyproject.toml     # Poetry configuration file
├── README.md          # Project documentation
```

## Installation
### Prerequisites
- Python 3.8+
- Poetry package manager

### Steps
1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install dependencies:
   ```bash
   poetry install
   ```

## Usage
### Basic Command
To fetch papers based on a query and save the results to a CSV file:
```bash
poetry run python cli.py "<query>" -f <output_file>.csv
```

### Example
```bash
poetry run python cli.py "cancer therapy" -f results.csv -d
```
- **`"cancer therapy"`**: Search query.
- **`-f results.csv`**: Specifies the output file.
- **`-d`**: Enables debug mode to print additional information.

### Help
To view available options:
```bash
poetry run python cli.py -h
```

## Output Format
The program generates a CSV file with the following columns:
- **PubmedID**: Unique identifier for the paper.
- **Title**: Title of the paper.
- **Publication Date**: Date of publication.
- **Non-academic Author(s)**: Names of authors affiliated with non-academic institutions.
- **Company Affiliation(s)**: Names of pharmaceutical/biotech companies.
- **Corresponding Author Email**: Email address of the corresponding author (if available).

## Development
### Adding Features
- The core functionalities are encapsulated in the `pubmed_module.py`.
- You can extend the filtering logic in `identify_non_academic_authors` to add more heuristics for identifying non-academic affiliations.

### Testing
- Use debug mode (`-d`) to verify outputs during development.
- Validate outputs by comparing them with PubMed's web interface results.

## Publishing the Module
To publish the core module to Test PyPI:
1. Build the package:
   ```bash
   poetry build
   ```
2. Publish to Test PyPI:
   ```bash
   poetry publish -r testpypi
   ```

## Tools Used
- **Python:** Core programming language.
- **Poetry:** Dependency management and packaging.
- **Requests:** For interacting with PubMed's API.
- **Pandas:** For CSV handling and data manipulation.

## License
This project is licensed under the MIT License.

## Contributors
- **Burhaan Rasheed Zargar**

