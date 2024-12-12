from fastapi import APIRouter, Request
from Models.dataplotting import generate_histogram_plots
from Models.database import getCommitsPerDay
from fastapi.responses import JSONResponse

# Create a new FastAPI router instance for handling routes related to histograms.
router = APIRouter()

@router.post("/histogram")
async def get_histogram_chart(request: Request):
    # Endpoint to generate a histogram chart for commit data.
    try:
        # Parse the request body to extract input parameters.
        body_data = await request.json()
        repoName = body_data.get("reponame")  # Repository name.
        startdate = body_data.get("start_date")  # Start date for filtering commits.
        enddate = body_data.get("end_date")  # End date for filtering commits.
        max_no_of_commits = body_data.get("max_no_of_commits")  # Maximum commits per day.
        filter_by = body_data.get("filter_by", "day")  # Filter by time unit (default: "day").

        # Validate that required fields are provided.
        if not repoName or not startdate or not enddate or not max_no_of_commits:
            return JSONResponse(
                {"error": "reponame, start_date, end_date, and max_no_of_commits are required"},
                status_code=400
            )

        # Retrieve filtered commit data from the database based on the input parameters.
        data = getCommitsPerDay(repoName, startdate, enddate, max_no_of_commits)

        # Check if any data is retrieved; if not, return a 404 error response.
        if not data:
            return JSONResponse({"error": "No data available for the given parameters"}, status_code=404)

        # Prepare the data for generating the histogram.
        date_array = []  # Array to store dates.
        commitsCount_array = []  # Array to store commit counts.

        # Process the query results to extract commit dates and counts.
        for result in data:
            date_array.append(result["commit_date"])  # Append commit date.
            commitsCount_array.append(result["commit_count"])  # Append commit count.

        # Structure the data in a dictionary format for the histogram.
        data_dict = {
            "Date": date_array,  # List of dates.
            "Commits": commitsCount_array  # List of commit counts for corresponding dates.
        }

        # Generate the histogram plot using the prepared data.
        fig = generate_histogram_plots(data_dict)

        # Return the generated histogram as a JSON response.
        return JSONResponse(content=fig)

    except Exception as e:
        # Handle exceptions and log the error for debugging.
        print(f"Error in histogram generation: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)
