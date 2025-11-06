import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="", 
    database="resume_db"
)


def add_resume():
    print("\n=== ADD NEW RESUME ===")

    full_name = input("Full Name: ")
    age = input("Age: ")
    address = input("Address: ")
    phone = input("Phone: ")
    email = input("Email: ")
    job_title = input("Job Title: ")
    summary = input("Professional Summary : ")
    #experience
    experiences = []
    while True:
        add_exp = input("Add experience? (y/n): ")
        if add_exp.lower() == "n":
            break
        job = input(" Job Title: ")
        company = input(" Company: ")
        years = input(" Years (e.g. 2020–2022): ")
        experiences.append((job, company, years))

    #education
    educations = []
    while True:
        add_edu = input("Add education? (y/n): ")
        if add_edu.lower() == "n":
            break
        degree = input(" Degree: ")
        school = input(" School/Institution: ")
        year = input(" Year: ")
        educations.append((degree, school, year))

    #skills
    skills_input = input("Skills (separate with commas): ")
    skills = [s.strip() for s in skills_input.split(",") if s.strip()]

    cursor = db.cursor()

    sql_resume = """
        INSERT INTO resumes (full_name, age, address, phone, email, job_title, summary)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    data_resume = (full_name, age, address, phone, email, job_title, summary)
    cursor.execute(sql_resume, data_resume)
    resume_id = cursor.lastrowid

    for exp in experiences:
        sql_exp = "INSERT INTO experience (resume_id, job_title, company, years) VALUES (%s, %s, %s, %s)"
        data_exp = (resume_id, exp[0], exp[1], exp[2])
        cursor.execute(sql_exp, data_exp)

    for edu in educations:
        sql_edu = "INSERT INTO education (resume_id, degree, institution, year) VALUES (%s, %s, %s, %s)"
        data_edu = (resume_id, edu[0], edu[1], edu[2])
        cursor.execute(sql_edu, data_edu)


    for skill in skills:
        sql_skill = "INSERT INTO skills (resume_id, skill) VALUES (%s, %s)"
        data_skill = (resume_id, skill)
        cursor.execute(sql_skill, data_skill)

    db.commit()
    print("\n✅ Resume saved successfully!\n")


def view_resumes():
    print("\n=== VIEW ALL RESUMES ===")

    cursor = db.cursor(dictionary=True)
    cursor.execute("SELECT * FROM resumes")
    resumes = cursor.fetchall()

    if not resumes:
        print("No resumes found yet.\n")
        return

    for r in resumes:
        print("\n========================================")
        print("Name:", r["full_name"])
        print("Age:", r["age"])
        print("Job Title:", r["job_title"])
        print("Phone:", r["phone"])
        print("Email:", r["email"])
        print("Address:", r["address"])
        if r["summary"]:
            print("Summary:", r["summary"])
        print("----------------------------------------")

        resume_id = r["id"]

        # --- Show Experiences ---
        cursor.execute("SELECT job_title, company, years FROM experience WHERE resume_id = %s", (resume_id,))
        exps = cursor.fetchall()
        if exps:
            print("Experience:")
            for e in exps:
                print(" -", e["job_title"], "|", e["company"], "|", e["years"])

        # --- Show Education ---
        cursor.execute("SELECT degree, institution, year FROM education WHERE resume_id = %s", (resume_id,))
        edus = cursor.fetchall()
        if edus:
            print("Education:")
            for e in edus:
                print(" -", e["degree"], "|", e["institution"], "|", e["year"])

        cursor.execute("SELECT skill FROM skills WHERE resume_id = %s", (resume_id,))
        skills = cursor.fetchall()
        if skills:
            print("Skills:")
            print(" ", ", ".join(s["skill"] for s in skills))
        print("========================================\n")



def main_menu():
    while True:
        print("=== INTERACTIVE RESUME BUILDER ===")
        print("1. Add New Resume")
        print("2. View All Resumes")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add_resume()
        elif choice == "2":
            view_resumes()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")



main_menu()
