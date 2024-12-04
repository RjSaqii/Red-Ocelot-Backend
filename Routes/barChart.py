from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from Models.dataplotting import commits_per_repo

router = APIRouter()

@router.get("/barchart", response_class=HTMLResponse)
def get_bar_chart():
    # Generate the Plotly bar chart as HTML
    bar_chart_html = commits_per_repo()
    return HTMLResponse(content=bar_chart_html)

