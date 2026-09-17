import sqlite3

conn = sqlite3.connect("university.db")
c = conn.cursor()

c.execute("""ALTER TABLE courses ADD COLUMN duration1 TEXT;
ALTER TABLE courses ADD COLUMN eligibility TEXT;
ALTER TABLE courses ADD COLUMN specializations TEXT;
ALTER TABLE courses ADD COLUMN subjects TEXT;
ALTER TABLE courses ADD COLUMN labs TEXT;
ALTER TABLE courses ADD COLUMN career_paths TEXT;
ALTER TABLE courses ADD COLUMN projects TEXT;
ALTER TABLE courses ADD COLUMN description TEXT;
ALTER TABLE courses ADD COLUMN career_opportunities TEXT;
ALTER TABLE courses ADD COLUMN alumni_success TEXT;
""")

c.execute("""UPDATE courses
SET 
  duration = '4 Years (8 Semesters)',
  eligibility = '10+2 (Science) with Physics, Chemistry, and Mathematics with minimum 50% marks',
  specializations = 'Computer Science, Electronics & Communication, Mechanical, Civil, Information Technology, Artificial Intelligence, Data Science',
  subjects = 'Data Structures, Operating Systems, Algorithms, Computer Networks, Database Management Systems, Machine Learning, Cloud Computing, Software Engineering',
  labs = 'Programming Lab, Networking Lab, AI Lab, IoT Lab, Data Science Lab, Robotics Lab',
  career_paths = 'Software Developer, Data Analyst, Network Engineer, AI Engineer, Cloud Architect, Cybersecurity Expert',
  projects = 'Mini Project (3rd Year), Major Project (Final Year), Internship during 6th Semester',
  description = 'The Bachelor of Technology (B.Tech) program provides a comprehensive foundation in engineering principles, technical skills, and real-world problem-solving. Students gain exposure to industry tools and technologies through hands-on labs and projects.',
  career_opportunities = 'Graduates are hired by top tech firms like Google, Infosys, TCS, and Wipro, or pursue higher studies (M.Tech, MBA, or abroad).',
  alumni_success = 'Our alumni are working at Microsoft, Amazon, and leading research labs worldwide.'
WHERE course_name = 'B.Tech';
""")

c.execute("""SELECT * FROM courses WHERE course_name = 'B.Tech'""")