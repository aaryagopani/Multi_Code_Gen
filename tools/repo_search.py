from langchain.tools import tool
import requests

GITHUB_SEARCH_API = "https://api.github.com/search/repositories"

@tool("search_repos")
def search_repos(query: str):
    """
    Search GitHub repositories based on a keyword-based query for GitHub API.
    """
    headers = {
        "Accept": "application/vnd.github+json",
    }
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": 5,
    }

    response = requests.get(GITHUB_SEARCH_API, headers=headers, params=params)

    if response.status_code != 200:
        return f"Error: {response.status_code} - {response.text}"

    results = response.json()
    repos = results.get("items", [])
    if not repos:
        return "No repositories found."
    
    details = []
    for r in repos:
        details.append({
            'owner' : r['owner']['login'],
            'repo' : r['name'],
            'url' : r['url']
            })
    print(details)
    # repo_list = []
    # for r in repos:
    #     repo_list.append(f"{r['full_name']} - {r['html_url']}")
    # return "\n".join(repo_list)
    return details


# r = search_repos.invoke("(react OR vue) financial in:description language:JavaScript")
# print(r)
