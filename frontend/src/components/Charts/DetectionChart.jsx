import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

const data = [
    { time: 1, confidence: 0.2},
    { time: 2, confidence: 0.4},
    { time: 3, confidence: 0.8},
    { time: 4, confidence: 0.9},
]

export default function DetectionChart(){
    return(
        <div>
            <h2>Smoke Confidence Timeline</h2>
            <ResponsiveContainer>
                <LineChart>
                    <XAxis datakey="time"/>
                    <YAxis/>
                    <Tooltip/>

                    <Line
                        type="monotone"
                        datakey="confidence"
                    />
                </LineChart>
            </ResponsiveContainer>
        </div>
    )
}