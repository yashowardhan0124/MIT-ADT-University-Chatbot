import sqlite3

conn = sqlite3.connect("university.db")
c = conn.cursor()

tables = ["courses", "fees", "documents", "contact", "departments", "hostel", "placements", "clubs", "faculty","Students"]
for t in tables:
    c.execute(f"DROP TABLE IF EXISTS {t}")

# Courses Table
c.execute("""
CREATE TABLE courses (
    course_name TEXT PRIMARY KEY,
    duration TEXT,
    eligibility TEXT,
    specializations TEXT,
    subjects TEXT,
    labs TEXT,
    career_paths TEXT,
    projects TEXT,
    description TEXT,
    career_opportunities TEXT,
    alumni_success TEXT
)
""")

courses_data = [
    ('B.Tech',
     '4 Years (8 Semesters)',
     '10+2 with Physics, Chemistry, and Mathematics (min. 50%)',
     'Computer Science, Electronics, Mechanical, Civil, Biotechnology, Artificial Intelligence',
     'Data Structures, Algorithms, OS, DBMS, Computer Networks, Machine Learning, IoT, Cybersecurity',
     'AI Lab, Robotics Lab, IoT Lab, Embedded Systems Lab, Programming Labs',
     'Software Engineer, Data Scientist, IoT Developer, Cloud Engineer, R&D Specialist',
     'Capstone Project, Industrial Training, Hackathons, Research Paper Submission',
     'B.Tech program equips students with strong analytical and technical skills, preparing them for diverse engineering roles in the IT and tech industries.',
     'Career in Software, Data Science, Product Development, M.Tech/MBA/Research opportunities.',
     'Many alumni now work at Google, Amazon, Infosys, and pursue higher studies at IITs and abroad.'
     ),

    ('MBA',
     '2 Years (4 Semesters)',
     'Graduation with minimum 50% marks (any discipline)',
     'Marketing, Finance, HR, Operations, Business Analytics, Entrepreneurship',
     'Strategic Management, Marketing Research, Financial Accounting, HR Management, Data Analytics',
     'Business Simulation Lab, Analytics Lab, Bloomberg Terminal Access',
     'Business Analyst, Marketing Executive, Financial Consultant, Product Manager',
     'Corporate Internships, Case Study Competitions, Live Industry Projects',
     'MBA develops leadership, communication, and strategic management skills for corporate excellence.',
     'Career in Business Leadership, Consulting, Banking, or Startup Management.',
     'Our alumni hold senior positions at Deloitte, TCS, KPMG, and have launched successful startups.'
     ),

    ('BBA',
     '3 Years (6 Semesters)',
     '10+2 from recognized board (any stream)',
     'Marketing, Finance, HR, International Business',
     'Business Communication, Financial Accounting, Marketing Principles, Organizational Behavior',
     'Commerce Lab, Entrepreneurship Cell, Business Simulation Sessions',
     'Business Executive, HR Coordinator, Market Analyst, Sales Manager',
     'Mini Projects, Group Presentations, Industrial Visits',
     'BBA builds a strong foundation in management and prepares students for MBA or corporate careers.',
     'Entry-level jobs in Banking, Retail, and Business Development.',
     'Graduates placed in ICICI Bank, HDFC, and leading startups.'
     ),

    ('BCA',
     '3 Years (6 Semesters)',
     '10+2 with Mathematics or Computer Science',
     'Software Development, Data Analytics, Networking, Web Development',
     'C Programming, Java, Python, Web Technologies, Database Management Systems',
     'Computer Lab, Web Development Lab, Software Engineering Lab',
     'Software Developer, Web Designer, Database Administrator, System Analyst',
     'Internship in Tech Firms, App Development Projects, Web Portfolios',
     'BCA provides IT skills and computer application knowledge for software and web industries.',
     'Career in IT Support, Software Testing, and Full-Stack Development.',
     'Our alumni work at Wipro, Infosys, and Capgemini as software developers.'
     )
]
c.executemany("INSERT INTO courses VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", courses_data)

# Fees Table
c.execute("""
CREATE TABLE fees (
    program TEXT PRIMARY KEY,
    tuition INTEGER,
    labs INTEGER,
    hostel INTEGER,
    total INTEGER,
    scholarships TEXT
)
""")

fees_data = [
    ('B.Tech', 120000, 30000, 50000, 200000, 'Merit-based scholarships available for top 10% scorers'),
    ('MBA', 150000, 25000, 50000, 225000, 'Need-based and merit scholarships offered'),
    ('BBA', 100000, 15000, 45000, 160000, 'Early bird scholarships and sibling discounts'),
    ('BCA', 110000, 20000, 40000, 170000, 'Tech talent scholarships available')
]
c.executemany("INSERT INTO fees VALUES (?, ?, ?, ?, ?, ?)", fees_data)

# Documents Table
c.execute("""
CREATE TABLE documents (
    doc_type TEXT PRIMARY KEY,
    items TEXT
)
""")

documents_data = [
    ('Admission', '- 10th & 12th Marksheet\n- ID Proof\n- Passport-size Photos\n- Transfer Certificate\n- Entrance Exam Scorecard'),
    ('Hostel', '- Admission Letter\n- Parent Consent Form\n- Medical Certificate\n- Photos\n- ID Proof'),
    ('Office Work', '- Identity Proof\n- Address Proof\n- Filled Application Form')
]
c.executemany("INSERT INTO documents VALUES (?, ?)", documents_data)

#Contact Table
c.execute("""
CREATE TABLE contact (
    type TEXT PRIMARY KEY,
    info TEXT
)
""")

contact_data = [
    ('Email', 'admissions@mitadt.edu.in'),
    ('Phone', '+91-9876543210'),
    ('Address', 'MIT ADT University, Loni Kalbhor, Pune, Maharashtra'),
    ('Website', 'https://www.mituniversity.edu.in')
]
c.executemany("INSERT INTO contact VALUES (?, ?)", contact_data)

# Departments Table
c.execute("""
CREATE TABLE departments (
    name TEXT PRIMARY KEY,
    hod TEXT,
    contact TEXT,
    location TEXT,
    description TEXT
)
""")

departments_data = [
    ('Computer Engineering', 'Dr. A. Sharma', '+91-9001112233', 'Block A - 2nd Floor', 'Focuses on AI, ML, Data Science, IoT, and Software Development.'),
    ('Information Technology', 'Dr. S. Menon', '+91-9001112277', 'Block A - 3rd Floor', 'Emphasizes networking, cybersecurity, and web development.'),
    ('Mechanical Engineering', 'Dr. R. Kulkarni', '+91-9001112244', 'Block B - Ground Floor', 'Covers design, manufacturing, thermodynamics, and robotics.'),
    ('Civil Engineering', 'Dr. V. Patil', '+91-9001112255', 'Block C - 1st Floor', 'Specializes in sustainable infrastructure and structural design.'),
    ('Electronics and Telecommunication', 'Dr. P. Joshi', '+91-9001112288', 'Block D - 2nd Floor', 'Focuses on VLSI, signal processing, and communication systems.'),
    ('Electrical Engineering', 'Dr. R. Deshmukh', '+91-9001112299', 'Block B - 2nd Floor', 'Deals with power systems, renewable energy, and electrical machines.'),
    ('Management Studies', 'Prof. M. Singh', '+91-9001112266', 'Block D - 3rd Floor', 'Covers HR, Finance, Marketing, and Business Analytics.'),
    ('Biotechnology', 'Dr. K. Nair', '+91-9001112300', 'Block E - 1st Floor', 'Focuses on genetics, bioinformatics, and biomedical engineering.'),
    ('Architecture', 'Prof. R. Kamat', '+91-9001112311', 'Block F - Ground Floor', 'Specializes in sustainable architecture and urban design.'),
    ('Artificial Intelligence & Data Science', 'Dr. P. Iyer', '+91-9001112322', 'Block A - 4th Floor', 'Focuses on AI, Deep Learning, and Predictive Analytics.')
]


c.executemany("INSERT INTO departments VALUES (?, ?, ?, ?, ?)", departments_data)

# Hostel Table
c.execute("""
CREATE TABLE hostel (
    hostel_name TEXT PRIMARY KEY,
    gender TEXT,
    facilities TEXT,
    fees INTEGER,
    contact TEXT
)
""")

hostel_data = [
    ('MIT Boys Hostel', 'Male', 'Wi-Fi, Mess, Gym, 24x7 Security, Laundry', 60000, '+91-9001001001'),
    ('MIT Girls Hostel', 'Female', 'Wi-Fi, Mess, Library Access, Security, Study Room', 55000, '+91-9001001002')
]
c.executemany("INSERT INTO hostel VALUES (?, ?, ?, ?, ?)", hostel_data)

# Placements Table
c.execute("""
CREATE TABLE placements (
    company TEXT,
    avg_package TEXT,
    highest_package TEXT,
    roles TEXT,
    batch TEXT
)
""")

placement_data = [
    ('Infosys', '5 LPA', '12 LPA', 'Software Engineer, Analyst', '2024'),
    ('TCS', '4.5 LPA', '10 LPA', 'System Engineer, Developer', '2024'),
    ('Amazon', '12 LPA', '45 LPA', 'SDE, Cloud Engineer', '2024')
]
c.executemany("INSERT INTO placements VALUES (?, ?, ?, ?, ?)", placement_data)

# Clubs Table
c.execute("""
CREATE TABLE clubs (
    name TEXT,
    description TEXT,
    mentor TEXT,
    contact TEXT
)
""")

clubs_data = [
    ('Coding Club', 'Promotes coding, hackathons, and technical talks on emerging technologies.', 'Prof. D. Mehta', 'codingclub@mit.edu'),
    ('Cultural Club', 'Organizes cultural fests, dance, drama, and music events throughout the year.', 'Prof. P. Rao', 'cultural@mit.edu'),
    ('Entrepreneurship Cell', 'Encourages innovation and supports student startups through workshops and pitch events.', 'Prof. S. Verma', 'ecell@mit.edu'),
    ('Robotics Club', 'Focuses on building autonomous robots, participating in competitions, and hands-on mechanical projects.', 'Prof. R. Shah', 'robotics@mit.edu'),
    ('Sports Club', 'Promotes fitness, inter-college tournaments, and various indoor & outdoor sports.', 'Prof. M. Naik', 'sports@mit.edu'),
    ('Literary Club', 'Hosts debates, poetry recitations, and creative writing sessions to improve communication skills.', 'Prof. K. Sharma', 'literary@mit.edu'),
    ('Photography Club', 'Captures campus moments and organizes photo walks and exhibitions.', 'Prof. A. Gupta', 'photography@mit.edu'),
    ('Art and Design Club', 'Encourages creativity through sketching, painting, graphic design, and digital art workshops.', 'Prof. N. Deshmukh', 'artdesign@mit.edu'),
    ('Social Welfare Club', 'Engages in community service, blood donation drives, and social awareness campaigns.', 'Prof. R. Nair', 'social@mit.edu'),
    ('Environmental Club', 'Focuses on sustainability, tree plantation drives, and awareness programs on climate change.', 'Prof. T. Kulkarni', 'environment@mit.edu')
]


c.executemany("INSERT INTO clubs VALUES (?, ?, ?, ?)", clubs_data)

# Faculty Table
c.execute("""
CREATE TABLE faculty (
    name TEXT,
    designation TEXT,
    qualification TEXT,
    experience TEXT,
    email TEXT
)
""")

faculty_data = [
    ('Dr. A. Sharma', 'Professor & HOD (CSE)', 'Ph.D. in Artificial Intelligence', '15 years', 'asharma@mit.edu'),
    ('Prof. P. Rao', 'Assistant Professor', 'M.Tech in Data Science', '8 years', 'prao@mit.edu'),
    ('Dr. M. Iyer', 'Professor', 'Ph.D. in Management', '12 years', 'miyer@mit.edu')
]
c.executemany("INSERT INTO faculty VALUES (?, ?, ?, ?, ?)", faculty_data)

c.execute("""
CREATE TABLE students (
    enrollment_no TEXT PRIMARY KEY,
    roll_no INTEGER,
    name TEXT,
    year INTEGER,
    cgpa DECIMAL,
    GENDER TEXT
)
""")

# ======================================================
conn.commit()
conn.close()
print("✅ Database created and populated successfully with expanded data!")
