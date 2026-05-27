const events = [
    {
        time: "00:12",
        confidence: 0.91,
    },{
        time: "00:17",
        confidence: 0.87,
    },
];


export default function EventList() {
  return (
    <div className="bg-slate-900 rounded-xl p-4">
      <h2 className="text-xl mb-4">
        Smoke Events
      </h2>

      <div className="space-y-3">
        {events.map((event, idx) => (
          <div
            key={idx}
            className="bg-slate-800 p-3 rounded-lg"
          >
            <p>Time: {event.time}</p>
            <p>
              Confidence: {event.confidence}
            </p>
          </div>
        ))}
      </div>
    </div>
  );
}