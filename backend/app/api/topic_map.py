from fastapi import APIRouter
from app.models.schemas import TopicMapResponse
from app.services.topic_mapper import topic_mapper_service

router = APIRouter(prefix="/topic-map", tags=["Topic Map"])

@router.get("", response_model=TopicMapResponse)
def get_topic_map():
    return topic_mapper_service.get_topic_map()

