from fastapi import APIRouter
from Routes.getRepoNames import router as repo_names_router
from .barChart import router as bar_chart_router
from .pieChart import router as pie_chart_router
from .histogram import router as histogram_router
from .getRepoNames import router as getRepoNames_router
from .getAuthors import router as getAuthors_router
from .bubblechart import router as bubble_chart_router
from .getreponamebyauthor import router as github_intergration_router
from .githubauthorpiechart import router as github_author_piechart
from .authorrepolinecount import router as line_count_router
from .authorbubblechart import router as author_bubble_chart
from .authorcommithistogram import router as author_commit_histogram
from .filterhisto import router as filter_git_histo

# Create the main router instance to group all related endpoints.
router = APIRouter()

# Include routers from individual modules, grouping their endpoints under the main router.
router.include_router(github_intergration_router) 
router.include_router(bar_chart_router)           
router.include_router(pie_chart_router)        
router.include_router(histogram_router)         
router.include_router(getRepoNames_router)      
router.include_router(getAuthors_router)         
router.include_router(bubble_chart_router)       
router.include_router(github_author_piechart)     
router.include_router(line_count_router)         
router.include_router(author_bubble_chart)       
router.include_router(author_commit_histogram) 
router.include_router(filter_git_histo)
