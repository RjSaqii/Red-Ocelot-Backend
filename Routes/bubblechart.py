from fastapi import APIRouter, Request
from Models.dataplotting import generate_bubble_chart
from Models.database import getBubbleChartData
from fastapi.responses import JSONResponse

router = APIRouter()




@router.get("/bubblechart")
async def get_bubble_chart(request: Request):
    # Fetch data for all repositories
    data = getBubbleChartData()
    watcher_count_array = []
    commits_count_array = []
    fork_count_array = []
    repos_array = []

    if not data:
        return JSONResponse({"error": "No data available for bubble chart"}, status_code=404)

    
    for result in data:
       # print(data)
        watcher_count_array.append(result["watcher_count"])
        commits_count_array.append(result["commit_count"])
        fork_count_array.append(result["fork_count"])
        repos_array.append(result["repository_name"])
    
    data = {
        "watcher_count":watcher_count_array,
        "commit_count":commits_count_array,
        "fork_count":fork_count_array,
        "repository_name":repos_array 
    }
    
    
    fig = generate_bubble_chart(data)
    return JSONResponse(fig)

