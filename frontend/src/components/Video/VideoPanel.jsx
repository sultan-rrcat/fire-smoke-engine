import { BACKEND_API } from "../../config";

export default function VideoPanel({ videoId }) {
    return (
        <div>
            <h2>Annotated Output</h2>

            <video controls className="w-full rounded-lg">
                <source
                    src={`${BACKEND_API}/outputs/${videoId}.mp4`}
                    type="video/mp4"
                />
            </video>
        </div>
    );
}