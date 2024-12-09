from fastapi import APIRouter, Request
from Models.dataplotting import generate_histogrammm
from Models.database import getCommitsPerDay
from fastapi.responses import JSONResponse

router = APIRouter()



@router.post("/histogram")
async def get_histogram_chart(request: Request):

    body_data = await request.json()
    repoName = body_data.get("reponame")
    startdate = body_data.get("start_date")  # New parameter
    enddate = body_data.get("end_date") 

    # Generate the Plotly JSON for the pie chart
    data = getCommitsPerDay(repoName, startdate, enddate)
    print(data)
    date_array = []
    commitsCount_array = []

    for result in data:
       # print(data)
        date_array.append(result["commit_date"])
        commitsCount_array.append(result["commit_count"])
    
    data = {
        "Date":date_array,
        "Commits":commitsCount_array
    }
    
    
    fig = generate_histogrammm(data)
    return JSONResponse(fig)