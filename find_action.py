import os
import requests
import csv
import logging
from typing import List
import base64

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


class Contributor:
    def __init__(self, name: str):
        self.name = name

    def __repr__(self):
        return self.name


class Repository:
    def __init__(self, name: str):
        self.name = name
        self.workflows: List[str] = []
        self.vulnerable_workflows: List[str] = []
        self.contributors: List[Contributor] = []

    def mark_vulnerable(self, workflow_file: str):
        self.vulnerable_workflows.append(workflow_file)


class GitHubScanner:
    def __init__(self, org: str, token: str):
        self.org = org
        self.base_url = "https://api.github.com"
        self.headers = {"Authorization": f"token {token}"}

    def list_repos(self) -> List[str]:
        url = f"{self.base_url}/users/{self.org}/repos?per_page=100&type=all"
        repos = []
        while url:
            r = requests.get(url, headers=self.headers)
            r.raise_for_status()
            data = r.json()
            repos.extend([repo["full_name"] for repo in data])
            url = r.links.get("next", {}).get("url")
        return repos

    def get_workflow_files(self, repo: str) -> List[str]:
        url = f"{self.base_url}/repos/{repo}/contents/.github/workflows"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 404:
            return []
        
        r.raise_for_status()
        return [wf["name"] for wf in r.json() if wf["type"] == "file"]

    def parse_support_file(self, repo: str) -> List[Contributor]:
        url = f"{self.base_url}/repos/{repo}/contents/SUPPORT.md"
        r = requests.get(url, headers=self.headers)
        if r.status_code == 404:
            print("not found")
            return []
        r.raise_for_status()
        content = base64.b64decode(r.json()["content"]).decode("utf-8")
        contributors = []
        for line in content.splitlines():
            if line.strip().startswith("-"):
                contributors.append(Contributor(line.strip("- ").strip()))
        return contributors

    def scan_repo(self, repo: str, action_file="buggy-actions_expose-passwords.yml") -> Repository:
        repository = Repository(repo)
        workflows = self.get_workflow_files(repo)
        repository.workflows = workflows

        for wf in workflows:
            if action_file in wf:
                logging.warning(f"Vulnerable workflow file found in {repo}: {wf}")
                repository.mark_vulnerable(wf)

        repository.contributors = self.parse_support_file(repo)
        return repository

    def export_to_csv(self, repositories: List[Repository], filename="compliance-report.csv"):
        with open(filename, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Repository", "Vulnerable Workflows", "Contributors"])
            for repo in repositories:
                writer.writerow([
                    repo.name,
                    ";".join(repo.vulnerable_workflows) if repo.vulnerable_workflows else "None",
                    ";".join([c.name for c in repo.contributors]) if repo.contributors else "Unknown"
                ])
        logging.info(f"Report saved to {filename}")


if __name__ == "__main__":
    org = os.getenv("ORG_NAME", "metin-prog")
    token = os.getenv("GITHUB_TOKEN")
    
    if not token:
        raise RuntimeError("Missing GITHUB_TOKEN")

    scanner = GitHubScanner(org, token)

    logging.info(f"Scanning repositories in org: {org}")
    repos = scanner.list_repos()

    results = []
    for repo in repos:
        logging.info(f"Scanning {repo}...")
        results.append(scanner.scan_repo(repo))

    scanner.export_to_csv(results)
