from fastapi import APIRouter
from fastapi.responses import HTMLResponse
import Models.database as database
from fastapi.responses import JSONResponse

router = APIRouter()

@router.get("/getreponames")
def getRepoNames():
    repoNames = database.getRepoNamesData()
    return JSONResponse(repoNames)