from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from Models.github_integration import GitHubClient
from Models.dataplotting import generate_bubble_chart_plots

# Initialize the FastAPI router for managing endpoints
router = APIRouter()

@router.post("/authorbubblechartdata")
async def get_bubble_chart(request: Request):
    # Endpoint to generate bubble chart data for a GitHub user's repositories
    try:
        # Parse the JSON request body
        body_data = await request.json()
        username = body_data.get("username")

        # Check if the username is provided in the request
        if not username:
            return JSONResponse({"error": "Username is required"}, status_code=400)

        # Initialize the GitHub API client
        client = GitHubClient()

        # Fetch all repositories for the specified username
        repos = await client.get_repositories(username)

        # If no repositories are found, return a 404 response
        if not repos:
            return JSONResponse({"error": "No repositories found for the user"}, status_code=404)

        # Initialize arrays to store data for the bubble chart
        watcher_count_array = []  # Array to store watcher counts
        fork_count_array = []     # Array to store fork counts
        commit_count_array = []   # Array to store commit counts
        repos_array = []          # Array to store repository names

        # Iterate over each repository to extract data
        for repo in repos:
            repo_name = repo["name"]  # Get the repository name

            # Append watcher and fork counts to their respective arrays
            watcher_count_array.append(repo["watchers_count"])
            fork_count_array.append(repo["forks_count"])

            # Fetch the commit count for the repository
            commits = await client.get_commits(username, repo_name)
            commit_count_array.append(len(commits))  # Add the number of commits to the array

            # Add the repository name to the repos array
            repos_array.append(repo_name)

        # Prepare the data dictionary for the bubble chart
        data = {
            "repository_name": repos_array,
            "watcher_count": watcher_count_array,
            "fork_count": fork_count_array,
            "commit_count": commit_count_array,
        }

        # Generate the bubble chart using the data
        fig = generate_bubble_chart_plots(data)

        # Return the generated chart as a JSON response
        return JSONResponse(fig)

    except Exception as e:
        # Handle any exceptions and return an error response
        return JSONResponse({"error": str(e)}, status_code=500)

