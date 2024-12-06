from fastapi import FastAPI
from Routes import routes as routes
from starlette.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()
#cors allow all just for testing may change later
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
# Include routes
app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Visualization API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)





