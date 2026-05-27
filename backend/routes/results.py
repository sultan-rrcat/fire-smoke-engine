import json
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import FileResponse
from config import (
    OUTPUT_DIR,
    DETECTION_DIR
)
from core.logging import setup_logging

# Initialize logger
logger = setup_logging()

router = APIRouter()

@router.get("/results/{video_id}")
def get_results(video_id: str):
    logger.info(f"Requested detection results for video: {video_id}")
    
    try:
        detection_file = DETECTION_DIR / f"{video_id}.json"
        
        # 1. Check if the JSON results actually exist
        if not detection_file.exists():
            logger.warning(f"Detection file not found for video: {video_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Detection results for video '{video_id}' not found. It may still be processing."
            )
            
        # 2. Safely open and parse the JSON file
        with open(detection_file, "r", encoding="utf-8") as f:
            detections = json.load(f)
            
        logger.debug(f"Successfully loaded detection results for {video_id}")
        return {
            "video_id": video_id,
            "detections": detections
        }
        
    except json.JSONDecodeError as e:
        # Handle cases where the JSON file was written improperly or corrupted
        logger.error(f"Corrupted JSON file for video '{video_id}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error parsing detection results. The file might be corrupted."
        )
    except HTTPException:
        raise # Re-raise FastAPI HTTP exceptions
    except Exception as e:
        logger.exception(f"Unexpected error retrieving results for '{video_id}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while retrieving detection results."
        )

@router.get("/download/{video_id}")
def download_video(video_id: str):
    logger.info(f"Download requested for processed video: {video_id}")
    
    try:
        output_file = OUTPUT_DIR / f"{video_id}.mp4"
        
        # 1. Check if the final video file actually exists
        if not output_file.exists():
            logger.warning(f"Processed video not found for download: {video_id}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Processed video '{video_id}.mp4' not found. It may still be processing."
            )
            
        logger.info(f"Initiating file transfer for: {output_file.name}")
        return FileResponse(
            path=output_file,
            media_type="video/mp4",
            filename=f"{video_id}.mp4"
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.exception(f"Unexpected error during file download for '{video_id}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while preparing the video for download."
        )