from fastapi import APIRouter
from .barChart import router as bar_chart_router
from .pieChart import router as pie_chart_router
from .heatMap import router as heat_map_router
from .histogram import router as histogram_router

router = APIRouter()

router.include_router(bar_chart_router)
router.include_router(pie_chart_router)
router.include_router(heat_map_router)
router.include_router(histogram_router)

print("test2")