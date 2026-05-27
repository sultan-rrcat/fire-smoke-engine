import VideoPanel from "../components/Video/VideoPanel"
import DetectionChart from "../components/Charts/DetectionChart"
import EventList from "../components/Events/EventList"

export default function ResultPage(){
    return(
        <div>
            <div>
                <div><VideoPanel/></div>
                <div><EventList/></div>
                <div><DetectionChart/></div>
            </div>
        </div>
    )
}