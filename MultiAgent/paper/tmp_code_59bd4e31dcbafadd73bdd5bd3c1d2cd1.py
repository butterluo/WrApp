import arxiv
import datetime
from collections import defaultdict

# Define the search query and date range
query = "LLM applications"
today = datetime.date.today()
last_week = today - datetime.timedelta(days=7)

# Search for papers
search = arxiv.Search(
    query=query,
    max_results=100,
    sort_by=arxiv.SortCriterion.SubmittedDate,
    sort_order=arxiv.SortOrder.Descending
)

# Filter papers from the last week
papers = [result for result in search.results() if result.published.date() >= last_week]

# Categorize papers by domain
domains = defaultdict(list)
for paper in papers:
    # Simple domain categorization based on title and abstract
    if "health" in paper.title.lower() or "health" in paper.summary.lower():
        domain = "Healthcare"
    elif "finance" in paper.title.lower() or "finance" in paper.summary.lower():
        domain = "Finance"
    else:
        domain = "Other"
    
    domains[domain].append(paper)

# Create markdown table
markdown_table = "| Title | Authors | Domain | Abstract | URL |\n"
markdown_table += "|-------|---------|--------|----------|-----|\n"

for domain, papers in domains.items():
    for paper in papers:
        title = paper.title.replace("\n", " ")
        authors = ", ".join(author.name for author in paper.authors)
        abstract = paper.summary.replace("\n", " ")[:150] + "..."
        url = paper.entry_id
        markdown_table += f"| {title} | {authors} | {domain} | {abstract} | [Link]({url}) |\n"

# Output the markdown table
print(markdown_table)