from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from Models.dataplotting import generate_histogram

router = APIRouter()

@router.get("/histogram", response_class=HTMLResponse)
def get_histogram():
    # Generate the Plotly histogram as HTML
    histogram_html = generate_histogram()
    return HTMLResponse(content=histogram_html)
