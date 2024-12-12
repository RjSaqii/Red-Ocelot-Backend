from fastapi import APIRouter, Request
from Models.dataplotting import generate_bar_plots
from Models.database import getFilesDetailsBYRepoName
from fastapi.responses import JSONResponse

# Create a new FastAPI router instance to handle routes for this module.
router = APIRouter()

@router.post("/barchart")
async def get_bar_chart(request: Request):
    # Endpoint to generate a bar chart based on input data provided in the request.
    try:
        # Parse the JSON body from the incoming request asynchronously.
        body_data = await request.json()

        # Extract repository name and the maximum number of lines from the parsed request body.
        repoName = body_data.get("reponame")  # Name of the repository to analyze.
        no_of_lines = body_data.get("no_of_lines")  # Maximum line count for filtering files.

        # Validate that both required fields are provided.
        if not repoName or not no_of_lines:
            return JSONResponse({"error": "Both reponame and no_of_lines are required"}, status_code=400)

        # Retrieve data from the database for files in the repository within the specified line count limit.
        data = getFilesDetailsBYRepoName(repoName, no_of_lines)

        # If no data is retrieved, return a 404 response.
        if not data:
            return JSONResponse({"error": "No data found for the specified repository and line count limit"}, status_code=404)

        # Initialize arrays to hold file names and their corresponding line counts.
        file_array = []  # List to store file names.
        lineCount_array = []  # List to store line counts.

        # Process the query results to extract file names and line counts.
        for result in data:
            file_array.append(result["name"])  # Append the file name to the `file_array`.
            lineCount_array.append(result["functional_line_count"])  # Append the line count to the `lineCount_array`.

        # Structure the data into a dictionary format suitable for generating the bar chart.
        data = {
            "Name": file_array,  # File names.
            "LineCount": lineCount_array,  # Corresponding line counts.
        }

        # Generate the bar chart using the structured data.
        fig = generate_bar_plots(data)

        # Return the generated bar chart as a JSON response to the client.
        return JSONResponse(fig)

    except Exception as e:
        # Handle any unexpected exceptions and return an error response.
        print(f"Error in generating bar chart: {str(e)}")  # Log the error for debugging.
        return JSONResponse({"error": str(e)}, status_code=500)
