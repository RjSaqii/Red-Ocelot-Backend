from fastapi import APIRouter, Request
from Models.dataplotting import generate_barPlots
from Models.database import getFilesDetailsBYRepoName
from fastapi.responses import JSONResponse


router = APIRouter()

@router.post("/barchart")
async def get_bar_chart(request: Request):

    body_data = await request.json()
    print(body_data)
    repoName = body_data.get("reponame")
    no_of_lines = body_data.get("no_of_lines")

    # Generate the Plotly JSON for the pie chart
    data = getFilesDetailsBYRepoName(repoName, no_of_lines)
    file_array = []
    lineCount_array = []

    for result in data:
       # print(data)
        file_array.append(result["name"])
        lineCount_array.append(result["functional_line_count"])
    
    data = {
        "Name":file_array,
        "LineCount":lineCount_array
    }
    
    
    fig = generate_barPlots(data)
    return JSONResponse(fig)