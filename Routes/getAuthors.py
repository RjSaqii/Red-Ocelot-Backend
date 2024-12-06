from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
import Models.database as database
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/authorsbyreponame")
async def getAuthors(request: Request):
    
    body_data = await request.json()

    repoName = body_data.get("reponame")

    authors = database.getAuthors(repoName)

    return JSONResponse(authors)
