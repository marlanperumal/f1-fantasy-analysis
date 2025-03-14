"""Main FastAPI application for F1 Fantasy Analysis."""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from backend.api.routes import router as api_router

app = FastAPI(
    title="F1 Fantasy Analysis API",
    description="API for analyzing F1 Fantasy data",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router)


@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "F1 Fantasy Analysis API",
        "version": "0.1.0",
        "status": "online",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"} 