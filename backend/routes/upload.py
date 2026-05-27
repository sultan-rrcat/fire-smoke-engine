import uuid
import shutil
from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException, status
from config import UPLOAD_DIR
from core.logging import setup_logging

# Initialize logger
logger = setup_logging()

router = APIRouter()

@router.post("/upload-video", status_code=status.HTTP_201_CREATED)
async def upload_video(file: UploadFile = File(...)):
    logger.info(f"Received upload request for file: {file.filename}")
    
    # 1. Validate that the uploaded file is actually a video
    if not file.content_type.startswith("video/"):
        logger.warning(f"Upload rejected. Invalid content type: {file.content_type} for file '{file.filename}'")
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Invalid file type '{file.content_type}'. Please upload a valid video file."
        )
        
    try:
        video_id = str(uuid.uuid4())
        save_path = UPLOAD_DIR / f"{video_id}.mp4"
        
        # 2. Ensure the upload directory exists (safety net)
        UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
        
        logger.debug(f"Allocated ID {video_id}. Streaming upload to {save_path}")
        
        # 3. Use shutil.copyfileobj instead of await file.read()
        with open(save_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        logger.info(f"Successfully saved video '{file.filename}' with ID: {video_id}")
        return {
            "video_id": video_id,
            "status": "uploaded",
            "original_filename": file.filename
        }
        
    except IOError as e:
        # Catch specific file system errors (e.g., out of disk space, permission denied)
        logger.error(f"IOError while saving uploaded file '{file.filename}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save the video file due to a server storage error."
        )
    except Exception as e:
        # Catch all other unexpected errors
        logger.exception(f"Unexpected error during video upload for '{file.filename}': {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during the file upload process."
        )
    finally:
        # 4. Always close the uploaded file to free up system resources
        await file.close()