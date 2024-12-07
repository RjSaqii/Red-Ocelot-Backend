from fastapi import APIRouter, Request
# from Models.dataplotting import fetch_commit_counts_by_author
from fastapi.responses import JSONResponse
from Models.database import getAuthorCommitsByRepoName
from Models.dataplotting import generate_plots

router = APIRouter()

@router.post("/piechart")
async def get_pie_chart(request: Request):

    body_data = await request.json()
    repoName = body_data.get("reponame")

    # Generate the Plotly JSON for the pie chart
    data = getAuthorCommitsByRepoName(repoName)
    author_array = []
    commit_array = []

    for result in data:
        print(data)
        author_array.append(result["author"])
        commit_array.append(result["commit_count"])
    
    data = {
        "author":author_array,
        "commit_count":commit_array
    }
    
    
    fig = generate_plots(data)
    return JSONResponse(fig)


