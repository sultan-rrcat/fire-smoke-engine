import VideoUpload from "../components/Upload/VideoUpload"

export default function UploadPage() {
    return (
        <div className="min-h-screen bg-slate-950 text-white p-8">
            <h1 className="text-4xl font-bold mb-8">Fire & Smoke Detection Surveillance</h1>
            <VideoUpload />
        </div>
    )
}