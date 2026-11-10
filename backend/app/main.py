import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.core.config import settings

# Import API routers
from app.api.auth import router as auth_router
from app.api.materials import router as materials_router
from app.api.topic_map import router as topic_map_router
from app.api.quiz import router as quiz_router
from app.api.gap_report import router as gap_report_router
from app.api.revision_plan import router as revision_plan_router
from app.api.explain import router as explain_router
from app.api.analytics import router as analytics_router

app = FastAPI(
    title="GapFinder AI - API Engine",
    description="Intelligent diagnostic testing, RAG-grounded topic gap analysis, and personalized adaptive revision planning.",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register route prefixes under /api
app.include_router(auth_router, prefix="/api")
app.include_router(materials_router, prefix="/api")
app.include_router(topic_map_router, prefix="/api")
app.include_router(quiz_router, prefix="/api")
app.include_router(gap_report_router, prefix="/api")
app.include_router(revision_plan_router, prefix="/api")
app.include_router(explain_router, prefix="/api")
app.include_router(analytics_router, prefix="/api")

# Static files & Web UI
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/")
def serve_index_ui():
    index_file = os.path.join(static_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "app": settings.APP_NAME,
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

