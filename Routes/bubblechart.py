from fastapi import APIRouter, Request
from Models.dataplotting import generate_bubble_chart_plots
from Models.database import getBubbleChartData
from fastapi.responses import JSONResponse

# Create a new FastAPI router instance for handling routes related to bubble charts.
router = APIRouter()

@router.get("/bubblechart")
async def get_bubble_chart(request: Request):
    # Endpoint to generate a bubble chart.
    try:
        # Fetch data for all repositories from the database.
        data = getBubbleChartData()

        # Check if data is available. If not, return a 404 response with an error message.
        if not data:
            return JSONResponse({"error": "No data available for bubble chart"}, status_code=404)

        # Initialize arrays to store chart data for watchers, commits, forks, and repository names.
        watcher_count_array = []  # List to store watcher counts for repositories.
        commits_count_array = []  # List to store commit counts for repositories.
        fork_count_array = []     # List to store fork counts for repositories.
        repos_array = []          # List to store names of repositories.

        # Process the query results to extract relevant data for the bubble chart.
        for result in data:
            watcher_count_array.append(result["watcher_count"])  # Add watcher count to array.
            commits_count_array.append(result["commit_count"])  # Add commit count to array.
            fork_count_array.append(result["fork_count"])        # Add fork count to array.
            repos_array.append(result["repository_name"])        # Add repository name to array.

        # Structure the processed data into a dictionary for generating the bubble chart.
        data = {
            "watcher_count": watcher_count_array,   # Watcher counts for repositories.
            "commit_count": commits_count_array,   # Commit counts for repositories.
            "fork_count": fork_count_array,        # Fork counts for repositories.
            "repository_name": repos_array         # Names of repositories.
        }

        # Generate the bubble chart using the structured data.
        fig = generate_bubble_chart_plots(data)

        # Return the bubble chart as a JSON response to the client.
        return JSONResponse(fig)

    except Exception as e:
        # Handle exceptions and return an error response with the exception message.
        print(f"Error in bubble chart generation: {str(e)}")  # Log the error for debugging.
        return JSONResponse({"error": str(e)}, status_code=500)
