import sqlite3
import os

# Database location
DATABASE_FOLDER = "database"
DATABASE_PATH = os.path.join(DATABASE_FOLDER, "campusconnect.db")


def get_connection():
    os.makedirs(DATABASE_FOLDER, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def create_database():

    connection = get_connection()
    cursor = connection.cursor()

    # Events table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            event_date TEXT,
            location TEXT
        )
    """)

    # Study materials table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS materials (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT,
            semester TEXT,
            file_path TEXT
        )
    """)

    # Lost and found table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lost_found (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            description TEXT,
            location TEXT,
            status TEXT DEFAULT 'Lost'
        )
    """)

    # Internships table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS internships (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            company TEXT NOT NULL,
            role TEXT,
            description TEXT,
            application_link TEXT
        )
    """)

    # Community posts table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS community_posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Contact messages table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL,
            message TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
        # Event registrations table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS registrations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_name TEXT NOT NULL,
            usn TEXT NOT NULL,
            email TEXT NOT NULL,
            department TEXT NOT NULL,
            event_name TEXT NOT NULL,
            registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()

    print("CampusConnect Database Created Successfully!")


if __name__ == "__main__":
    create_database()