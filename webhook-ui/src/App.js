import React, { useEffect, useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [events, setEvents] = useState([]);

  const fetchEvents = async () => {
    try {
      const response = await axios.get("http://127.0.0.1:5000/webhook/events");
      setEvents(response.data);
    } catch (error) {
      console.error("Error fetching events:", error);
    }
  };

  useEffect(() => {
    fetchEvents(); // fetch immediately
    const interval = setInterval(fetchEvents, 15000); // then every 15s
    return () => clearInterval(interval); // cleanup on unmount
  }, []);

  const renderEvent = (event) => {
    const { type, author, from_branch, to_branch, timestamp } = event;

    switch (type) {
      case "push":
        return `${author} pushed to ${to_branch} on ${timestamp}`;
      case "pull_request":
        return `${author} submitted a pull request from ${from_branch} to ${to_branch} on ${timestamp}`;
      case "merge":
        return `${author} merged branch ${from_branch} to ${to_branch} on ${timestamp}`;
      default:
        return "Unknown event";
    }
  };

  return (
    <div className="container">
      <h1>GitHub Activity Feed</h1>
      <ul className="event-list">
        {events.length === 0 ? (
          <li>No events found</li>
        ) : (
          events.map((event, index) => (
            <li key={index} className="event-item">
              {renderEvent(event)}
            </li>
          ))
        )}
      </ul>
    </div>
  );
}

export default App;

