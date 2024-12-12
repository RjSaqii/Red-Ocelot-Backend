from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
import Models.database as database

# Create a new FastAPI router instance for handling routes related to authors.
router = APIRouter()

@router.post("/authorsbyreponame")
async def getAuthors(request: Request):
    # Endpoint to retrieve authors associated with a specific repository name.
    try:
        # Parse the JSON body from the incoming request asynchronously.
        body_data = await request.json()

        # Extract the repository name from the parsed request body.
        repoName = body_data.get("reponame")

        # Validate that the repository name is provided.
        if not repoName:
            return JSONResponse({"error": "Repository name is required"}, status_code=400)

        # Call the `getAuthors` function from the `database` module to fetch authors for the specified repository.
        authors = database.getAuthors(repoName)

        # If no authors are found, return a 404 response with an error message.
        if not authors:
            return JSONResponse({"error": "No authors found for the specified repository"}, status_code=404)

        # Return the list of authors as a JSON response to the client.
        return JSONResponse(authors)

    except Exception as e:
        # Handle exceptions and log the error.
        print(f"Error in authorsbyreponame: {str(e)}")
        return JSONResponse({"error": str(e)}, status_code=500)
