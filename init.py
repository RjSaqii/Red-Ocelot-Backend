from fastapi import FastAPI
from Routes import routes as routes
from starlette.middleware.cors import CORSMiddleware
import uvicorn

# Create a FastAPI instance.
app = FastAPI()

# Add CORS middleware to allow cross-origin requests.
# Note: This configuration allows all origins, methods, and headers (for testing purposes).
# It may need to be restricted in production for security.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from all origins.
    allow_credentials=True,  # Allow credentials in cross-origin requests.
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.).
    allow_headers=["*"],  # Allow all headers.
)

# Include the router with all the application routes from the `Routes` module.
app.include_router(routes.router)

@app.get("/")
def root():
    # Define the root endpoint that responds to GET requests.
    # This provides a welcome message when visiting the root URL.
    return {"message": "Welcome to the Visualization API"}

# Entry point for running the application.
if __name__ == "__main__":
    import uvicorn  # Import Uvicorn (again, if running as a standalone script).
    # Run the FastAPI application using Uvicorn on localhost and port 8000.
    uvicorn.run(app, host="127.0.0.1", port=8000)
