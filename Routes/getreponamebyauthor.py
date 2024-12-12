from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
import Models.database as database
from Models.github_integration import GitHubClient
from decouple import config

# Initialize the FastAPI router for managing routes related to repositories.
router = APIRouter()

def get_github_client() -> GitHubClient:
    # Dependency injection to provide an instance of the GitHubClient.
    return GitHubClient()

@router.get("/getreponamesbyuser/{username}")
async def get_repo_names(username: str, client: GitHubClient = Depends(get_github_client)):
    # Fetch all repository names for a specified GitHub username.
    # Args:
    # - username (str): The GitHub username to fetch repositories for.
    # - client (GitHubClient): An instance of GitHubClient provided via dependency injection.
    # Returns:
    # - JSONResponse: A list of repository names as a JSON response.
    # Raises:
    # - HTTPException: If an error occurs during the API request or processing.
    try:
        # Fetch the list of repositories for the specified username using the GitHub client.
        repos = await client.get_repositories(username)

        # Extract repository names from the list of repositories.
        repo_names = [repo["name"] for repo in repos]

        # Return the repository names as a JSON response.
        return JSONResponse(repo_names)
    except Exception as e:
        # Handle exceptions and raise an HTTP 400 error with the exception details.
        raise HTTPException(status_code=400, detail=str(e))
