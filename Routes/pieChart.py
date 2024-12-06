from fastapi import APIRouter, Request
# from Models.dataplotting import fetch_commit_counts_by_author
from fastapi.responses import JSONResponse
from Models.database import getAuthorCommitsByRepoName
from Models.dataplotting import generate_pie_chart

router = APIRouter()

@router.post("/piechart")
async def get_pie_chart(request: Request):

    body_data = await request.json()
    repoName = body_data.get("reponame")

    # Generate the Plotly JSON for the pie chart
    data = getAuthorCommitsByRepoName(repoName)
    fig = generate_pie_chart(data)
    return JSONResponse(fig)


