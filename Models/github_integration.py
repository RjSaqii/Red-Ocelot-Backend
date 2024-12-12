from decouple import config
from datetime import datetime, timedelta
from collections import defaultdict
import httpx
import calendar

class GitHubClient:
    # Base URL for GitHub's API
    BASE_URL = "https://api.github.com"

    def __init__(self):
        # Initialize the GitHub API token from the environment configuration file
        self.GITHUB_TOKEN = config("GITHUB_ACCESS_TOKEN")
        # Set up headers for authenticated API requests
        self.headers = {
            "Authorization": f"Bearer {self.GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json",
        }

    async def get_repositories(self, username: str):
        # Fetches a list of repositories for a given GitHub username.
        # Args: username (str): GitHub username to retrieve repositories for.
        # Returns: list: A list of repository objects.
        url = f"{self.BASE_URL}/users/{username}/repos"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()  # Raise exception for HTTP errors
            return response.json()

    async def get_repository_details(self, username: str, reponame: str):
        # Fetches details of a specific repository.
        # Args: 
        # - username (str): GitHub username.
        # - reponame (str): Repository name.
        # Returns: dict: Repository details as a dictionary.
        url = f"{self.BASE_URL}/repos/{username}/{reponame}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def get_commits(self, username: str, reponame: str):
        # Fetches commits for a specific repository.
        # Args: 
        # - username (str): GitHub username.
        # - reponame (str): Repository name.
        # Returns: list: A list of commit objects.
        url = f"{self.BASE_URL}/repos/{username}/{reponame}/commits"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            return response.json()

    async def get_file_details(self, username: str, reponame: str, path: str = ""):
        # Fetches file details within a repository, including line counts.
        # Args:
        # - username (str): GitHub username.
        # - reponame (str): Repository name.
        # - path (str): Directory path to fetch files from.
        # Returns: list: A list of file details including name, path, and line count.
        url = f"{self.BASE_URL}/repos/{username}/{reponame}/contents/{path}"
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers)
            response.raise_for_status()
            items = response.json()

        file_details = []

        for item in items:
            if item["type"] == "file":
                # Fetch the file content and calculate the number of lines
                file_url = item["download_url"]
                async with httpx.AsyncClient() as client:
                    file_response = await client.get(file_url)
                    file_response.raise_for_status()
                    content = file_response.text
                    line_count = content.count('\n') + 1 if content else 0

                file_details.append({
                    "filename": item["name"],
                    "path": item["path"],
                    "line_count": line_count,
                })

            elif item["type"] == "dir":
                # Recursive call for subdirectories
                subdir_details = await self.get_file_details(username, reponame, item["path"])
                file_details.extend(subdir_details)

        return file_details

    async def get_commits_within_date_range(self, username: str, reponame: str, start_date: str, end_date: str):
        # Fetches commits within a specified date range and groups them by date.
        # Args:
        # - username (str): GitHub username.
        # - reponame (str): Repository name.
        # - start_date (str): Start date in ISO format (YYYY-MM-DD).
        # - end_date (str): End date in ISO format (YYYY-MM-DD).
        # Returns: list: A list of dictionaries with dates and commit counts.
        url = f"{self.BASE_URL}/repos/{username}/{reponame}/commits"
        params = {"since": start_date, "until": end_date}

        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=self.headers, params=params)
            response.raise_for_status()
            commits = response.json()

        # Group commits by date
        date_commit_count = {}
        for commit in commits:
            commit_date = commit["commit"]["author"]["date"][:10]  # Extract the date in YYYY-MM-DD format
            date_commit_count[commit_date] = date_commit_count.get(commit_date, 0) + 1

        # Convert to a list of dictionaries
        return [{"date": date, "count": count} for date, count in date_commit_count.items()]

    async def get_commit_count_by_author(self, username: str, reponame: str):
        # Fetches the number of commits made by each author for a repository.
        # Args:
        # - username (str): GitHub username.
        # - reponame (str): Repository name.
        # Returns: dict: A dictionary of authors and their commit counts.
        commits_url = f"{self.BASE_URL}/repos/{username}/{reponame}/commits"
        async with httpx.AsyncClient() as client:
            response = await client.get(commits_url, headers=self.headers)
            response.raise_for_status()
            commits = response.json()

        author_commit_count = {}
        for commit in commits:
            author = commit.get("commit", {}).get("author", {}).get("name", "Unknown")
            if author:
                author_commit_count[author] = author_commit_count.get(author, 0) + 1

        return author_commit_count

    async def group_commits_by_time_filter(self, commits_data: list, time_filter: str):
        # Groups commits by a specified time filter (day, week, month, year).
        # Args:
        # - commits_data (list): List of commit data containing 'date' and 'count'.
        # - time_filter (str): Filter by 'day', 'week', 'month', or 'year'.
        # Returns: list: A list of dictionaries with date ranges and commit counts.
        grouped_data = defaultdict(int)

        for commit in commits_data:
            commit_date = datetime.strptime(commit["date"], "%Y-%m-%d")

            # Grouping logic based on the time filter
            if time_filter == "day":
                key = (commit_date, commit_date)
            elif time_filter == "week":
                start_of_week = commit_date - timedelta(days=commit_date.weekday())
                end_of_week = start_of_week + timedelta(days=6)
                key = (start_of_week, end_of_week)
            elif time_filter == "month":
                start_of_month = commit_date.replace(day=1)
                _, last_day = calendar.monthrange(commit_date.year, commit_date.month)
                end_of_month = commit_date.replace(day=last_day)
                key = (start_of_month, end_of_month)
            elif time_filter == "year":
                start_of_year = commit_date.replace(month=1, day=1)
                end_of_year = commit_date.replace(month=12, day=31)
                key = (start_of_year, end_of_year)
            else:
                raise ValueError(f"Invalid time filter: {time_filter}")

            grouped_data[key] += commit.get("count", 1)

        # Convert grouped data into a readable format
        return [
            {
                "date_range": f"{start.strftime('%Y-%m-%d')} to {end.strftime('%Y-%m-%d')}",
                "count": count
            }
            for (start, end), count in grouped_data.items()
        ]
