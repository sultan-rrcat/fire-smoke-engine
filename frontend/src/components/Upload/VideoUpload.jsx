import { useDropzone } from "react-dropzone";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { useState } from "react";
import { BACKEND_API } from "../../config";

export default function VideoUpload() {
    const navigate = useNavigate();
    const [isUploading, setIsUploading] = useState(false);
    const [error, setError] = useState(null);

    const onDrop = async (acceptedFiles) => {
        const file = acceptedFiles;
        if (!file) return;

        const formData = new FormData();
        formData.append("file", file);
        setIsUploading(true);
        setError(null);

        try {
            // 1. Upload the video
            // 1. Upload the video (Updated with Headers)
            const uploadRes = await axios.post(
                `${BACKEND_API}/upload-video`, 
                formData,
                {
                    headers: {
                        "Content-Type": "multipart/form-data",
                    }
                }
            );
            const videoId = uploadRes.data.video_id;

            // 2. Trigger the processing thread
            await axios.post(`${BACKEND_API}/process-video/${videoId}`);

            // 3. Navigate to processing page
            navigate(`/processing/${videoId}`);
            
        } catch (err) {
            console.error("Upload/Processing Error:", err);
            
            // --- NEW ERROR HANDLING LOGIC ---
            const detail = err.response?.data?.detail;
            let errorMessage = "An error occurred during upload.";

            if (Array.isArray(detail)) {
                // Handle FastAPI's 422 validation array of objects
                errorMessage = detail.map(e => `${e.loc[e.loc.length - 1]}: ${e.msg}`).join(", ");
            } else if (typeof detail === "string") {
                // Handle our custom FastAPI HTTPException strings
                errorMessage = detail;
            } else if (err.message) {
                // Handle generic network errors (e.g., server offline)
                errorMessage = err.message;
            }

            setError(errorMessage);
        } finally {
            setIsUploading(false);
        }
    };

    const { getRootProps, getInputProps } = useDropzone({
        accept: {
            "video/*": [],
        },
        multiple: false,
        disabled: isUploading,
        onDrop
    });

    return (
        <div 
            {...getRootProps()}
            className={`border-2 border-dashed p-20 rounded-xl transition text-center
                ${isUploading ? 'border-slate-500 cursor-not-allowed opacity-50' : 'border-slate-600 cursor-pointer hover:border-blue-500'}`
            }
        >
            <input {...getInputProps()} />
            <div>
                {isUploading ? (
                    <p className="text-2xl text-blue-400 animate-pulse">
                        Uploading & Initializing...
                    </p>
                ) : (
                    <>
                        <p className="text-2xl">Drag & Drop Video Here</p>
                        <p className="text-slate-400 mt-2">mp4 / avi / mov</p>
                    </>
                )}
                
                {/* Display backend errors to the user if things fail */}
                {error && (
                    <p className="text-red-500 mt-4 font-semibold">{error}</p>
                )}
            </div>
        </div>
    );
}