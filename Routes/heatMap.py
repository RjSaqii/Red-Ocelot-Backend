from fastapi import APIRouter
from fastapi.responses import HTMLResponse
from Models.dataplotting import commits_heatmap

router = APIRouter()

@router.get("/heatmap", response_class=HTMLResponse)
def get_heat_map():
    # Generate the Plotly heatmap as HTML
    heatmap_html = commits_heatmap()
    return HTMLResponse(content=heatmap_html)
