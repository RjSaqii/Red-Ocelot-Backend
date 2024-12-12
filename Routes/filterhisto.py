from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from Models.github_integration import GitHubClient
from Models.dataplotting import generate_author_histogram_plots  # Assumes this function generates the histogram

# Initialize the FastAPI router for managing histogram-related routes.
router = APIRouter()

@router.post("/commithistogram")
async def get_histogram_chart(request: Request):
    # Endpoint to generate a histogram chart of commit data for a GitHub repository.
    try:
        # Parse the incoming JSON request body.
        body_data = await request.json()
        username = body_data.get("username")  # GitHub username.
        reponame = body_data.get("reponame")  # Repository name.
        start_date = body_data.get("start_date")  # Start date for filtering commits.
        end_date = body_data.get("end_date")  # End date for filtering commits.
        time_filter = body_data.get("time_filter", "day")  # Time filter for grouping commits (default is 'day').

        # Validate that all required fields are provided.
        if not username or not reponame or not start_date or not end_date:
            return JSONResponse(
                {"error": "Username, repository name, start_date, and end_date are required"},
                status_code=400,
            )

        # Initialize the GitHub client for fetching commit data.
        client = GitHubClient()

        # Fetch commit data for the specified repository and date range.
        commits_data = await client.get_commits_within_date_range(username, reponame, start_date, end_date)

        # If no commits are found, return a 404 response with an error message.
        if not commits_data:
            return JSONResponse({"error": "No commit data found for the repository within the given date range"}, status_code=404)

        # Group the commit data using the specified time filter.
        grouped_data = await client.group_commits_by_time_filter(commits_data, time_filter)

        # Prepare the data for the histogram chart.
        data = {
            "Commit Dates": [entry["date_range"] for entry in grouped_data],  # Date ranges for commits.
            "Commit Counts": [entry["count"] for entry in grouped_data],  # Commit counts for each date range.
        }

        # Generate the histogram chart using the prepared data.
        fig = generate_author_histogram_plots(data)

        # Return the generated histogram chart as a JSON response.
        return JSONResponse(fig)

    except Exception as e:
        # Handle exceptions and log the error for debugging.
        print(f"Error in commitshistogram: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)
