from fastapi import FastAPI
from Routes import routes as routes
import uvicorn

app = FastAPI()

# Include routes
app.include_router(routes.router)

@app.get("/")
def root():
    return {"message": "Welcome to the Visualization API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)





