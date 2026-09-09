import mysql.connector
from mysql.connector import Error


# ============================================================
# MYSQL CONFIGURATION
# ============================================================

HOST = "localhost"
USER = "root"
PASSWORD = "study"


# ============================================================
# CREATE DATABASE
# ============================================================

def create_database():

    try:

        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD
        )

        cursor = connection.cursor()

        cursor.execute(
            "CREATE DATABASE IF NOT EXISTS recruitment"
        )

        print("Database 'recruitment' is ready.")

        cursor.close()
        connection.close()

    except Error as e:

        print("Error creating database:")
        print(e)

        return False

    return True


# ============================================================
# CREATE TABLES
# ============================================================

def create_tables() -> bool:

    try:

        connection = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database="recruitment"
        )

        cursor = connection.cursor()


        # ----------------------------------------------------
        # USERS TABLE
        # ----------------------------------------------------

        users_table = """
        CREATE TABLE IF NOT EXISTS users (

            id INT AUTO_INCREMENT PRIMARY KEY,

            username VARCHAR(100) NOT NULL UNIQUE,

            password VARCHAR(255) NOT NULL,

            role VARCHAR(50) DEFAULT 'HR',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """

        cursor.execute(users_table)


        # ----------------------------------------------------
        # JOBS TABLE
        # ----------------------------------------------------

        jobs_table = """
        CREATE TABLE IF NOT EXISTS jobs (

            job_id INT AUTO_INCREMENT PRIMARY KEY,

            job_title VARCHAR(150) NOT NULL,

            required_skills TEXT NOT NULL,

            experience INT DEFAULT 0,

            qualification VARCHAR(200),

            job_description TEXT,

            status VARCHAR(50) DEFAULT 'Open',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """

        cursor.execute(jobs_table)


        # ----------------------------------------------------
        # CANDIDATES TABLE
        # ----------------------------------------------------

        candidates_table = """
        CREATE TABLE IF NOT EXISTS candidates (

            candidate_id INT AUTO_INCREMENT PRIMARY KEY,

            name VARCHAR(150) NOT NULL,

            email VARCHAR(150),

            phone VARCHAR(30),

            qualification VARCHAR(200),

            skills TEXT,

            experience INT DEFAULT 0,

            resume_path VARCHAR(500),

            ai_score FLOAT DEFAULT 0,

            status VARCHAR(50) DEFAULT 'Under Review',

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

        )
        """

        cursor.execute(candidates_table)


        # ----------------------------------------------------
        # INTERVIEWS TABLE
        # ----------------------------------------------------

        interviews_table = """
        CREATE TABLE IF NOT EXISTS interviews (

            interview_id INT AUTO_INCREMENT PRIMARY KEY,

            candidate_id INT NOT NULL,

            interview_date DATE,

            interview_time TIME,

            interviewer VARCHAR(150),

            status VARCHAR(50) DEFAULT 'Scheduled',

            notes TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            FOREIGN KEY (candidate_id)

            REFERENCES candidates(candidate_id)

            ON DELETE CASCADE

        )
        """

        cursor.execute(interviews_table)


        connection.commit()

        print("All tables created successfully.")


        # ----------------------------------------------------
        # CREATE DEFAULT HR ACCOUNT
        # ----------------------------------------------------

        cursor.execute(
            "SELECT id FROM users WHERE username = %s",
            ("admin",)
        )

        existing_user = cursor.fetchone()


        if existing_user is None:

            insert_user = """
            INSERT INTO users
            (username, password, role)

            VALUES
            (%s, %s, %s)
            """

            cursor.execute(
                insert_user,
                ("admin", "admin123", "HR")
            )

            connection.commit()

            print("Default HR account created.")

        else:

            print("Default HR account already exists.")


        cursor.close()
        connection.close()

        return True


    except Error as e:

        print("Error creating tables:")
        print(e)

        return False


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    print()
    print("=" * 60)
    print("AI RECRUITMENT SYSTEM - DATABASE SETUP")
    print("=" * 60)
    print()

    database_created = create_database()

    if database_created:

        tables_created = create_tables()

        if tables_created:

            print()
            print("=" * 60)
            print("DATABASE SETUP COMPLETED SUCCESSFULLY")
            print("=" * 60)
            print()
            print("Default Login:")
            print("Username : admin")
            print("Password : admin123")
            print()

        else:

            print("Table creation failed.")

    else:

        print("Database creation failed.")