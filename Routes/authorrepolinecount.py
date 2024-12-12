from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from Models.github_integration import GitHubClient
from Models.dataplotting import generate_author_barchart_plots

# Initialize the FastAPI router for managing API routes
router = APIRouter()

@router.post("/filelinecountbyrepo")
async def get_bar_chart(request: Request):
    # Endpoint to generate a bar chart showing the line count of files in a repository
    try:
        # Parse the JSON request body
        body_data = await request.json()
        username = body_data.get("username")  # GitHub username
        reponame = body_data.get("reponame")  # Repository name

        # Validate that both username and repository name are provided
        if not username or not reponame:
            return JSONResponse({"error": "Both username and reponame are required"}, status_code=400)

        # Initialize the GitHub client for API interactions
        client = GitHubClient()

        # Fetch file details for the specified repository
        files_data = await client.get_file_details(username, reponame)

        # If no file data is found, return a 404 response
        if not files_data:
            return JSONResponse({"error": "No file data found for the repository"}, status_code=404)

        # Initialize lists to store file names and line counts
        file_names = []  # List to store file names
        line_counts = []  # List to store line counts

        # Process the fetched file data
        for file in files_data:
            file_names.append(file["filename"])  # Add file name to the list
            line_counts.append(file.get("line_count", 0))  # Add line count (default to 0 if missing)

        # Prepare data for generating the bar chart
        data = {
            "File Name": file_names,  # File names
            "Line Count": line_counts,  # Corresponding line counts
        }

        # Generate the bar chart using the prepared data
        fig = generate_author_barchart_plots(data)

        # Return the generated chart as a JSON response
        return JSONResponse(fig)

    except Exception as e:
        # Handle exceptions and log the error
        print(f"Error in filelinecountbyrepo: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)
