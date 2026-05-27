export default function VideoPanel() {
    return (
        <div>
            <h2>Annotated Output</h2>
            <video controls className="w-full rounded-lg">
                <source src="http://localhost:8000/output/sample.mp4" type="video/mp4"/>
            </video>
        </div>
    )
}