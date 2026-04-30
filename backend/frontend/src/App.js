import React, { useEffect, useState } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

function App() {
  const [notifications, setNotifications] = useState([]);
  const [message, setMessage] = useState("");

  // Fetch notifications
  const fetchNotifications = async () => {
    try {
      const res = await axios.get(`${API}/notifications/`);
      setNotifications(res.data);
    } catch (err) {
      console.error("Error fetching notifications:", err);
    }
  };

  // Create notification
  const createNotification = async () => {
    if (!message) return;

    try {
      await axios.post(`${API}/notifications/?message=${message}`);
      setMessage("");
      fetchNotifications();
    } catch (err) {
      console.error("Error creating notification:", err);
    }
  };

  // Mark as read
  const markAsRead = async (id) => {
    try {
      await axios.put(`${API}/notifications/${id}`);
      fetchNotifications();
    } catch (err) {
      console.error("Error updating notification:", err);
    }
  };

  useEffect(() => {
    fetchNotifications();
  }, []);

  return (
    <div style={{ padding: "20px" }}>
      <h1>Kanban Board</h1>

      {/* Notifications Section */}
      <h3>Notifications</h3>

      <input
        type="text"
        placeholder="Enter message"
        value={message}
        onChange={(e) => setMessage(e.target.value)}
      />
      <button onClick={createNotification}>Add</button>

      <p>Total: {notifications.length}</p>

      <ul>
        {notifications.map((n) => (
          <li key={n.id}>
            {n.message} - <b>{n.status}</b>
            {n.status === "unread" && (
              <button onClick={() => markAsRead(n.id)}>
                Mark Read
              </button>
            )}
          </li>
        ))}
      </ul>

      {/* Simple Kanban UI (static for now) */}
      <div style={{ display: "flex", gap: "20px", marginTop: "40px" }}>
        <div style={{ background: "orange", padding: "20px", width: "200px" }}>
          <h3>Todo</h3>
          <p>No tasks</p>
        </div>

        <div style={{ background: "lightblue", padding: "20px", width: "200px" }}>
          <h3>In Progress</h3>
          <p>No tasks</p>
        </div>
      </div>
    </div>
  );
}

export default App;