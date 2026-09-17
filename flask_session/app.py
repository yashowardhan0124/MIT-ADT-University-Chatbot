from flask import Flask, flash, redirect, render_template, request, jsonify, session, url_for
import sqlite3
import traceback
import os
import pandas as pd

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "university.db")

app = Flask(__name__, template_folder="../templates", static_folder="../templates/static")
app.secret_key = 'your_secret_key_here'


def fetch_from_db(query, params=()):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute(query, params)
    data = c.fetchall()
    conn.close()
    return data


user_context = {}

@app.route('/')
def home():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = user[1]
            return redirect(url_for('index'))  
        else:
            return "<script>alert('Invalid credentials'); window.location.href='/login';</script>"

    return render_template('login.html')


@app.route('/index')
def index():
    if 'user' in session:
        return render_template('index.html')
    else:
        return redirect(url_for('login'))



@app.route('/welcome')
def welcome():
    if 'user' in session:
        return redirect(url_for('index'))
    return redirect(url_for('login'))


@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, email TEXT UNIQUE, password TEXT)")
        try:
            c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)", (name, email, password))
            conn.commit()
            conn.close()
            return "<script>alert('Account created! Please login.'); window.location.href='/login';</script>"
        except:
            conn.close()
            return "<script>alert('Email already exists!'); window.location.href='/signup';</script>"
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/upload_dataset", methods=["POST"])
def upload_dataset():
    try:
        file = request.files.get("file")
        if not file:
            return jsonify({"status": "error", "message": "⚠️ No file selected."}), 400

        if not file.filename.endswith(".csv"):
            return jsonify({"status": "error", "message": "❌ Please upload a CSV file."}), 400

        # Save file to uploads/
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(filepath)

        # Read CSV and store in DB
        import pandas as pd
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_csv(filepath)
        df.to_sql("students", conn, if_exists="replace", index=False)
        conn.close()

        return jsonify({"status": "success", "message": "✅ Dataset uploaded and stored successfully!"})

    except Exception as e:
        print("Error uploading dataset:", e)
        return jsonify({"status": "error", "message": f"⚠️ Error: {e}"})


@app.route("/get", methods=["POST"])
def chatbot_response():
    try:
        # read user message 
        user_msg = ""
        if request.is_json:
            user_msg = request.get_json().get("message", "").strip().lower()
        else:
            user_msg = request.form.get("msg", "").strip().lower()

        # --- Student / CGPA Queries ---
        if "student" in user_msg or "cgpa" in user_msg or "list" in user_msg:
            import sqlite3
            conn = sqlite3.connect(DB_PATH)
            c = conn.cursor()

            if "cgpa" in user_msg:
                c.execute("SELECT name, cgpa FROM students WHERE cgpa > 8.0")
                data = c.fetchall()
                response = "🎓 Students with CGPA above 8:\n"
                for row in data:
                    response += f"- {row[0]} ({row[1]})\n"
            else:
                c.execute("SELECT name, department FROM students LIMIT 10")
                data = c.fetchall()
                response = "📋 Top 10 Students:\n"
                for row in data:
                    response += f"- {row[0]} — {row[1]}\n"

            conn.close()  # ✅ Close the connection safely
            return jsonify({"response": response})

        # --- Course List Fetch ---
        courses = fetch_from_db("SELECT course_name FROM courses")
        course_list = [c[0] for c in courses]

        # --- Keyword Mapping ---
        keyword_map = {
            "btech": "B.Tech",
            "b.tech": "B.Tech",
            "bachelor of technology": "B.Tech",
            "mba": "MBA",
            "bba": "BBA",
            "bca": "BCA",
            "mca": "MCA"
        }

        matched_course = None
        for key, value in keyword_map.items():
            if key in user_msg:
                matched_course = value
                break

        if not matched_course:
            for course_name in course_list:
                if course_name.lower() in user_msg:
                    matched_course = course_name
                    break

        # --- Matched Course Details ---
        if matched_course:
            data = fetch_from_db("SELECT * FROM courses WHERE course_name = ?", (matched_course,))
            if data:
                row = data[0]
                if len(row) == 4:
                    course_name, duration, eligibility, details = row
                    response = (
                        f"🎓 *{course_name}* Details:\n\n"
                        f"📘 Duration: {duration}\n"
                        f"🧾 Eligibility: {eligibility}\n"
                        f"📚 Details: {details}"
                    )
                else:
                    padded = list(row) + [""] * (11 - len(row))
                    (course_name, duration, eligibility, specializations, subjects, labs,
                     career_paths, projects, description, career_opportunities, alumni_success) = padded[:11]

                    response = (
                        f"Here’s a comprehensive overview of *{course_name}*:\n\n"
                        f"📘 Duration: {duration}\n"
                        f"🎓 Eligibility: {eligibility}\n"
                        f"🧩 Specializations: {specializations}\n"
                        f"📚 Key Subjects: {subjects}\n"
                        f"🧪 Labs: {labs}\n"
                        f"💼 Career Paths: {career_paths}\n"
                        f"🛠️ Projects & Internships: {projects}\n\n"
                        f"🧭 About the Course: {description}\n"
                        f"🚀 Career Opportunities: {career_opportunities}\n"
                        f"🌟 Notable Alumni: {alumni_success}"
                    )

                return jsonify({"response": response})

        # --- B.Tech ---
        if "btech" in user_msg or "b.tech" in user_msg:
            course_data = fetch_from_db("SELECT * FROM courses WHERE course_name = 'B.Tech'")
            response = "B.Tech Course Details:\n"
            if course_data:
                for row in course_data:
                    if len(row) >= 4:
                        response += f"- Course Name: {row[0]}\n"
                        response += f"- Duration: {row[1]}\n"
                        response += f"- Eligibility: {row[2]}\n"
                        response += f"- Details: {row[3]}\n"
            else:
                response = "Sorry, B.Tech data not found in database."
            return jsonify({"response": response})

        # --- MBA ---
        if "mba" in user_msg:
            course_data = fetch_from_db("SELECT * FROM courses WHERE course_name = 'MBA'")
            response = "MBA Course Details:\n"
            if course_data:
                for row in course_data:
                    if len(row) >= 4:
                        response += f"- Course Name: {row[0]}\n"
                        response += f"- Duration: {row[1]}\n"
                        response += f"- Eligibility: {row[2]}\n"
                        response += f"- Details: {row[3]}\n"
            else:
                response = "Sorry, MBA data not found in database."
            return jsonify({"response": response})

        # --- Course Selection Flow ---
        if user_context.get("expecting_course_detail"):
            course = user_msg.lower()
            data = fetch_from_db("SELECT * FROM courses WHERE LOWER(course_name) LIKE ?", (f"%{course}%",))

            if data:
                (course_name, duration, eligibility, specializations, subjects, labs,
                 career_paths, projects, description, career_opportunities, alumni_success) = data[0]
                user_context["expecting_course_detail"] = False

                return jsonify({
                    "response": (
                        f"Here are the complete details for *{course_name}*:\n\n"
                        f"📘 Duration: {duration}\n"
                        f"🎓 Eligibility: {eligibility}\n"
                        f"🧩 Specializations: {specializations}\n"
                        f"📚 Subjects: {subjects}\n"
                        f"🧪 Labs: {labs}\n"
                        f"💼 Career Paths: {career_paths}\n"
                        f"🛠️ Projects & Internships: {projects}\n\n"
                        f"🧭 About the Course: {description}\n"
                        f"🚀 Career Opportunities: {career_opportunities}\n"
                        f"🌟 Notable Alumni: {alumni_success}"
                    )
                })
            else:
                return jsonify({
                    "response": "Sorry, I couldn’t find that course. Please choose from B.Tech, MBA, BBA, or BCA."
                })

        # --- List Courses ---
        if "course" in user_msg or "courses" in user_msg or "program" in user_msg:
            user_context["expecting_course_detail"] = True
            return jsonify({
                "response": (
                    "🎓 We offer a wide range of dynamic and industry-relevant programs aimed at developing both theoretical foundation "
                    "and practical expertise. Whether you're interested in technology, business, or computer applications, "
                    "we have a course designed to help you succeed.\n\n"
                    "💡 Our main programs include:\n" +
                    ", ".join(course_list) +
                    "\n\nWhich course would you like to explore in detail?"
                )
            })

        # --- Fees ---
        elif "fee" in user_msg or "fees" in user_msg:
            data = fetch_from_db("SELECT * FROM fees")
            response = "Here’s a summary of fees:\n"
            for row in data:
                response += f"\n💼 {row[0]}: ₹{row[1]} tuition + ₹{row[2]} labs + ₹{row[3]} hostel = ₹{row[4]} total\n🎓 Scholarships: {row[5]}\n"
            return jsonify({"response": response})

        # --- Documents ---
        elif "document" in user_msg or "documents" in user_msg:
            data = fetch_from_db("SELECT * FROM documents")
            response = "📂 Required Documents:\n"
            for doc in data:
                response += f"\n🗂️ {doc[0]}:\n{doc[1]}\n"
            return jsonify({"response": response})

        # --- Contact Info ---
        elif "contact" in user_msg or "contacts" in user_msg:
            data = fetch_from_db("SELECT * FROM contact")
            response = "📞 University Contact Info:\n"
            for row in data:
                response += f"{row[0]}: {row[1]}\n"
            return jsonify({"response": response})

        # --- Departments ---
        elif "department" in user_msg or "departments" in user_msg:
            data = fetch_from_db("SELECT * FROM departments")
            response = "🏛️ Departments at MIT ADT:\n"
            for row in data:
                response += f"\n{row[0]} (HOD: {row[1]})\n📍 {row[3]}\n📞 {row[2]}\n📘 {row[4]}\n"
            return jsonify({"response": response})

        # --- Hostel ---
        elif "hostel" in user_msg:
            data = fetch_from_db("SELECT * FROM hostel")
            response = "🏠 Hostel Information:\n"
            for row in data:
                response += f"\n{row[0]} ({row[1]} Hostel): ₹{row[3]} per year\nFacilities: {row[2]}\n📞 Contact: {row[4]}\n"
            return jsonify({"response": response})

        # --- Events ---
        elif "event" in user_msg or "events" in user_msg:
            data = fetch_from_db("SELECT * FROM events")
            response = "🎉 Upcoming Events:\n"
            for row in data:
                response += f"\n{row[0]} ({row[1]}): {row[2]}\n🔗 {row[3]}\n"
            return jsonify({"response": response})

        # --- Placements ---
        elif "placement" in user_msg or "placements" in user_msg:
            data = fetch_from_db("SELECT * FROM placements")
            response = "💼 Placement Highlights:\n"
            for row in data:
                response += f"\n🏢 {row[0]} ({row[4]} Batch)\nAvg Package: {row[1]} | Highest: {row[2]}\nRoles: {row[3]}\n"
            return jsonify({"response": response})

        # --- Faculty ---
        elif "faculty" in user_msg:
            data = fetch_from_db("SELECT * FROM faculty")
            response = "👩‍🏫 Faculty Members:\n"
            for row in data:
                response += f"\n{row[0]} ({row[1]})\n{row[2]}, Experience: {row[3]}\n📧 {row[4]}\n"
            return jsonify({"response": response})

        # --- Clubs ---
        elif "club" in user_msg or "clubs" in user_msg:
            data = fetch_from_db("SELECT * FROM clubs")
            response = "🎯 Student Clubs:\n"
            for row in data:
                response += f"\n{row[0]} — {row[1]}\nMentor: {row[2]}\n📩 {row[3]}\n"
            return jsonify({"response": response})

        # --- Default ---
        else:
            return jsonify({"response": "I'm sorry, I didn’t understand that. You can ask about courses, fees, departments, hostels, clubs, placements, or events."})

    except Exception as e:
        print("Error:", e)
        traceback.print_exc()
        return jsonify({"response": "⚠️ Sorry, something went wrong on the server. Please try again."})

if __name__ == "__main__":
    app.run(debug=True)
