from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from Models.github_integration import GitHubClient
from Models.dataplotting import generate_author_histogram_plots

# Initialize the FastAPI router for endpoint management
router = APIRouter()

@router.post("/commithistogramm")
async def get_histogram_chart(request: Request):
    # Endpoint to generate a histogram chart of commit data for a specific GitHub repository
    try:
        # Parse the incoming JSON request body
        body_data = await request.json()
        username = body_data.get("username")  # GitHub username
        reponame = body_data.get("reponame")  # Repository name
        start_date = body_data.get("start_date")  # Start date for commits
        end_date = body_data.get("end_date")  # End date for commits

        # Validate that all required fields are provided
        if not username or not reponame or not start_date or not end_date:
            return JSONResponse(
                {"error": "Username, repository name, start_date, and end_date are required"},
                status_code=400,
            )

        # Initialize the GitHub client for API interactions
        client = GitHubClient()

        # Fetch commit data for the specified repository and date range
        commits_data = await client.get_commits_within_date_range(username, reponame, start_date, end_date)

        # If no commits are found, return a 404 response
        if not commits_data:
            return JSONResponse({"error": "No commit data found for the repository within the given date range"}, status_code=404)

        # Extract commit dates and counts from the fetched data
        commit_dates = []  # List to store commit dates
        commit_counts = []  # List to store commit counts

        for commit in commits_data:
            commit_dates.append(commit["date"])  # Add the commit date
            commit_counts.append(commit["count"])  # Add the commit count

        # Prepare data for generating the histogram
        data = {
            "Commit Dates": commit_dates,  # Dates of commits
            "Commit Counts": commit_counts,  # Counts of commits per date
        }

        # Generate the histogram chart using the prepared data
        fig = generate_author_histogram_plots(data)

        # Return the generated chart as a JSON response
        return JSONResponse(fig)

    except Exception as e:
        # Handle any exceptions and log the error
        print(f"Error in commitshistogram: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)
