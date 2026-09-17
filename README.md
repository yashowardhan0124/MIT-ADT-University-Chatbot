# 🎓 MIT-ADT University Chatbot

An AI-powered university chatbot designed to provide students with quick and interactive access to university-related information through a modern, responsive web interface.

The project combines a Flask-based backend with a professional chatbot UI, database integration, and dataset-based functionality to create a centralized student assistance platform.

---

## ✨ Features

- 🤖 **AI-Powered Chatbot Interface**
  - Interactive conversational interface for student queries.
  - Provides university-related information through a centralized platform.

- 🔐 **User Authentication**
  - Student-friendly Login and Signup functionality.
  - Secure session-based user interaction.

- 💬 **Modern Chat Interface**
  - Clean and responsive chatbot dashboard.
  - User and chatbot messages are displayed in an easy-to-follow format.

- 📊 **Dataset Upload**
  - Supports uploading student datasets through the web application.
  - Designed to work with CSV-based student data.

- 🗄️ **Database Integration**
  - SQLite database for storing and managing application data.
  - Database can be created and populated using the provided setup script.

- 🎨 **Professional MIT-ADT UI**
  - Modern university-themed interface.
  - Responsive design for different screen sizes.
  - MIT-ADT branding and custom styling.

---

## 🛠️ Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Database management |
| HTML5 | Web page structure |
| CSS3 | UI design and styling |
| JavaScript | Frontend interaction |
| Pandas | Dataset processing |
| Jinja2 | Dynamic HTML templates |
| Git & GitHub | Version control |

---

## 📁 Project Structure

```text
MIT-ADT-University-Chatbot/
│
├── flask_session/
│   └── app.py
│
├── templates/
│   ├── index.html
│   ├── login.html
│   ├── signup.html
│   ├── upload_dataset.html
│   └── static/
│       ├── MIT logo.png
│       ├── logo.png
│       └── style.css
│
├── setup_db.py
├── setupdp.py
├── requirements.txt
├── README.md
└── .gitignore
