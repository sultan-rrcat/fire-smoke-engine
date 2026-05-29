import VideoPanel from "../components/Video/VideoPanel"
import DetectionChart from "../components/Charts/DetectionChart"
import EventList from "../components/Events/EventList"
import { useParams } from "react-router-dom"


export default function ResultPage() {
    const { id } = useParams();
    return (
        <div>
            <div>
                <VideoPanel videoId={id} />
                <EventList videoId={id} />
                <DetectionChart videoId={id} />
            </div>
        </div>
    )
}