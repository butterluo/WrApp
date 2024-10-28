# filename: search_arxiv_gpt4.py

import feedparser

# Search for GPT-4 papers on arXiv
def search_arxiv(query="gpt-4"):
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results=1&sortBy=submittedDate&sortOrder=descending"
    feed = feedparser.parse(url)
    for entry in feed.entries:
        print(f"Title: {entry.title}")
        print(f"Published: {entry.published}")
        print(f"Summary: {entry.summary}")
        print(f"Link: {entry.link}\n")

if __name__ == "__main__":
    search_arxiv("gpt-4")