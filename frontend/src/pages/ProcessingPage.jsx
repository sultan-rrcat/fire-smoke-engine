import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { BACKEND_API } from "../config";

export default function ProcessingPage() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [status, setStatus] = useState("initializing...");

    useEffect(() => {
        const interval = setInterval(async () => {
            try {
                const response = await axios.get(
                    `${BACKEND_API}/status/${id}`
                );
                
                const currentStatus = response.data.status;
                setStatus(currentStatus);

                if (currentStatus === "completed") {
                    clearInterval(interval); // Stop polling immediately
                    navigate(`/results/${id}`); // Use React Router for smooth navigation
                }
                
                // Optional: Handle failure states if your backend supports it
                if (currentStatus === "failed") {
                    clearInterval(interval);
                    setStatus("Processing failed. Please try again.");
                }
                
            } catch (error) {
                console.error("Error checking status:", error);
                // Don't clear interval on a single network blip, 
                // but you might want to handle persistent errors here
            }
        }, 2000);

        // Cleanup function when component unmounts
        return () => clearInterval(interval);
    }, [id, navigate]);

    return (
        <div className="min-h-screen bg-slate-950 text-white flex flex-col items-center justify-center p-8">
            <div className="bg-slate-900 p-12 rounded-xl border border-slate-800 text-center shadow-lg">
                <div className="mb-6">
                    <svg className="animate-spin h-10 w-10 text-blue-500 mx-auto" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                </div>
                <h2 className="text-3xl font-semibold mb-2">Processing Video...</h2>
                <p className="text-slate-400 text-lg uppercase tracking-wider mt-4">
                    Status: <span className="text-blue-400 font-bold">{status}</span>
                </p>
                <p className="text-slate-600 text-sm mt-6">
                    This may take a few minutes depending on the video length.
                </p>
            </div>
        </div>
    );
}