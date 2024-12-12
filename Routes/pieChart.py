from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from Models.database import getAuthorCommitsByRepoName
from Models.dataplotting import generate_plots_pie_chart

# Create a FastAPI router for managing routes related to pie charts.
router = APIRouter()

@router.post("/piechart")
async def get_pie_chart(request: Request):
    # Endpoint to generate a pie chart of commits by author for a specific repository.
    try:
        # Parse the incoming JSON request body.
        body_data = await request.json()

        # Extract the repository name from the request body.
        repoName = body_data.get("reponame")

        # Validate that the repository name is provided.
        if not repoName:
            return JSONResponse({"error": "Repository name is required"}, status_code=400)

        # Retrieve commit data grouped by authors for the specified repository.
        data = getAuthorCommitsByRepoName(repoName)

        # If no data is found, return a 404 response.
        if not data:
            return JSONResponse({"error": "No commit data found for the specified repository"}, status_code=404)

        # Initialize arrays to hold author names and their corresponding commit counts.
        author_array = []  # List for storing author names.
        commit_array = []  # List for storing commit counts.

        # Process the query results and populate the arrays.
        for result in data:
            author_array.append(result["author"])  # Add the author's name to the list.
            commit_array.append(result["commit_count"])  # Add the author's commit count to the list.

        # Structure the processed data into a dictionary for generating the pie chart.
        pie_chart_data = {
            "author": author_array,         # List of author names.
            "commit_count": commit_array    # Corresponding commit counts.
        }

        # Generate the pie chart using the structured data.
        fig = generate_plots_pie_chart(pie_chart_data)

        # Return the generated pie chart as a JSON response.
        return JSONResponse(fig)

    except Exception as e:
        # Handle exceptions and return an error response with the exception details.
        print(f"Error generating pie chart: {str(e)}")  # Log the error for debugging.
        return JSONResponse({"error": str(e)}, status_code=500)
