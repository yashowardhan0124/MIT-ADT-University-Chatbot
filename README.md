# MIT-ADT University AI Assistant

A Flask-based university chatbot with a redesigned professional MIT-ADT themed interface.

## Run locally

1. Open PowerShell in the project folder.
2. Activate your virtual environment if you have one:
   `.\.venv\Scripts\Activate.ps1`
3. Install dependencies:
   `python -m pip install -r requirements.txt`
4. If the database needs to be recreated:
   `python setup_db.py`
5. Start the application:
   `cd flask_session`
   `python app.py`
6. Open `http://127.0.0.1:5000/login`

## UI changes

- MIT-ADT purple/gold visual identity
- Premium split-screen login and signup
- Branded welcome experience
- Modern AI assistant workspace
- Responsive sidebar and mobile layout
- Conversation search and active-chat styling
- Quick question cards
- AI-style typing indicator
- Improved dataset upload experience
- Light/dark theme control
- MIT-ADT logo used consistently

The existing Flask routes and chatbot/database logic are retained, with only small path-handling improvements in `app.py` so the app can find its database and uploads folder regardless of the terminal's working directory.
