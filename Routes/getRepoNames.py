from fastapi import APIRouter
from fastapi.responses import JSONResponse
import Models.database as database

# Create a new FastAPI router instance for handling routes related to repository names.
router = APIRouter()

@router.get("/getreponames")
def getRepoNames():
    # Endpoint to retrieve all repository names.
    # The endpoint accepts GET requests at the "/getreponames" route.

    try:
        # Call the `getRepoNamesData` function from the `database` module to fetch repository names.
        repoNames = database.getRepoNamesData()

        # Return the list of repository names as a JSON response to the client.
        return JSONResponse(repoNames)
    except Exception as e:
        # Handle exceptions and return an error response with the exception message.
        return JSONResponse({"error": str(e)}, status_code=500)
