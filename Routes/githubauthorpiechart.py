from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from Models.github_integration import GitHubClient
from Models.dataplotting import generate_author_plots

# Initialize the FastAPI router for handling routes related to author commit pie charts.
router = APIRouter()

@router.post("/githubauthorpiechart")
async def get_repo_commit_piechart(request: Request):
    # Endpoint to generate a pie chart showing commit distribution by author for a specific repository.
    try:
        # Parse the request body to extract username and repository name.
        body_data = await request.json()
        username = body_data.get("username")  # GitHub username.
        reponame = body_data.get("reponame")  # Repository name.

        # Validate that both username and repository name are provided.
        if not username or not reponame:
            return JSONResponse({"error": "Both username and reponame are required"}, status_code=400)

        # Initialize the GitHub client for fetching commit data.
        client = GitHubClient()

        # Fetch commit counts grouped by author for the specified repository.
        author_commit_data = await client.get_commit_count_by_author(username, reponame)

        # If no commit data is found, return a 404 response with an error message.
        if not author_commit_data:
            return JSONResponse({"error": "No commit data found for the repository"}, status_code=404)

        # Prepare the data for generating the pie chart.
        authors = list(author_commit_data.keys())  # Extract author names.
        commit_counts = list(author_commit_data.values())  # Extract commit counts.

        data = {
            "Author": authors,  # Author names.
            "Commit Count": commit_counts,  # Commit counts per author.
        }

        # Generate the pie chart using the prepared data.
        fig = generate_author_plots(data)

        # Return the generated pie chart as a JSON response.
        return JSONResponse(fig)

    except Exception as e:
        # Handle exceptions and log the error for debugging.
        print("Error:", str(e))
        return JSONResponse({"error": str(e)}, status_code=500)
