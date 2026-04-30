🧠 Notion Clone App

A full-stack Notion-like productivity application that allows users to manage tasks, notes, and notifications with a Kanban-style board.

---

🚀 Features

- 📝 Create and manage notes
- ✅ Task management (Todo / In Progress / Completed)
- 🔔 Real-time notifications
- 📊 Analytics (task stats)
- 🔍 Search functionality
- ⚡ Fast API with optimized backend
- 📄 Pagination support

---

🛠️ Tech Stack

🔹 Frontend

- React.js
- Axios
- CSS

🔹 Backend

- FastAPI
- SQLAlchemy
- SQLite

---

📁 Project Structure

notion-clone/
│
├── backend/
│   ├── app/
│   ├── routes/
│   ├── models/
│   └── main.py
│
├── frontend/
│   ├── src/
│   ├── public/
│   └── package.json
│
└── README.md

---

⚙️ Installation & Setup

1️⃣ Clone Repository

git clone https://github.com/YOUR_USERNAME/notion-clone.git
cd notion-clone

---

2️⃣ Backend Setup

cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

---

3️⃣ Frontend Setup

cd frontend
npm install
npm start

---

🌐 API Docs

After running backend:

http://127.0.0.1:8000/docs

---

💡 Future Improvements

- User authentication (JWT)
- Drag & drop Kanban
- Dark mode UI
- Deployment (Render / Vercel)

---

🙌 Author

Akshaya Gudla

---

⭐ If you like this project, give it a star!
