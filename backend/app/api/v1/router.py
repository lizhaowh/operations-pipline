from fastapi import APIRouter

from app.api.v1.endpoints import brand_profiles, contents, dashboard, media, projects, publish, review, topics

api_router = APIRouter()
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(brand_profiles.router, prefix="/brand-profiles", tags=["brand-profiles"])
api_router.include_router(topics.router, prefix="/topics", tags=["topics"])
api_router.include_router(contents.router, prefix="/contents", tags=["contents"])
api_router.include_router(media.router, prefix="/media", tags=["media"])
api_router.include_router(review.router, prefix="/review", tags=["review"])
api_router.include_router(publish.router, prefix="/publish", tags=["publish"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
