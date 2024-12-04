from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from Models.dataplotting import commits_by_author

router = APIRouter()

@router.get("/piechart", response_class=HTMLResponse)
def get_pie_chart():
    # Generate the Plotly HTML for the pie chart
    pie_chart_html = commits_by_author()  # Ensure this returns HTML content
    return HTMLResponse(content=pie_chart_html)

