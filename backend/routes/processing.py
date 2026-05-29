from pathlib import Path
from threading import Thread
from fastapi import APIRouter, HTTPException, status
from config import UPLOAD_DIR
from services.video_service import (
    process_video,
    processing_status
)
from core.logging import setup_logging

# Initialize logger at the module level
logger = setup_logging()

router = APIRouter()

@router.post("/process-video/{video_id}", status_code=status.HTTP_202_ACCEPTED)
def start_processing(video_id: str):
    logger.info(f"Received request to process video: {video_id}")
    
    try:
        video_path = UPLOAD_DIR / f"{video_id}.mp4"
        
        # 1. Validate that the uploaded file actually exists
        if not video_path.exists():
            logger.error(f"Processing failed: Video file not found for ID '{video_id}' at {video_path}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Video file {video_id}.mp4 not found in uploads directory."
            )

        # 2. Spawn the processing thread
        logger.debug(f"Spawning background thread for video: {video_id}")

        processing_status[video_id] = "processing"

        thread = Thread(
            target=process_video,
            args=(video_id, video_path),
            daemon=True  # Ensures the thread doesn't block app shutdown
        )
        thread.start()
        
        logger.info(f"Successfully started processing thread for video: {video_id}")
        return {"status": "processing_started", "video_id": video_id}
        
    except HTTPException:
        # Re-raise HTTP exceptions so FastAPI handles them and returns the correct status code
        raise
    except Exception as e:
        # Catch unexpected errors (e.g., threading issues, permission errors)
        logger.exception(f"Unexpected error while starting video processing for '{video_id}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while starting the video processing task."
        )

@router.get("/status/{video_id}")
def get_status(video_id: str):
    logger.debug(f"Status check requested for video: {video_id}")
    
    try:
        current_status = processing_status.get(video_id, "not_found")
        
        if current_status == "not_found":
            logger.warning(f"Status requested for unknown or unprocessed video ID: {video_id}")
        else:
            logger.debug(f"Status for {video_id} returned as: {current_status}")
            
        return {"status": current_status, "video_id": video_id}
        
    except Exception as e:
        logger.exception(f"Error retrieving status for video '{video_id}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the processing status."
        )