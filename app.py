from flask import Flask, render_template, request, redirect, url_for, flash
from database import get_connection, create_database

app = Flask(__name__)
app.secret_key = "campusconnect_secret_key"

# Create database
create_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")


@app.route("/events")
def events():
    return render_template("events.html")


@app.route("/materials")
def materials():
    return render_template("materials.html")


# LOST AND FOUND
@app.route("/lost-found", methods=["GET", "POST"])
def lost_found():

    if request.method == "POST":

        item_name = request.form.get("item_name", "").strip()
        description = request.form.get("description", "").strip()
        location = request.form.get("location", "").strip()
        status = request.form.get("report_type", "Lost").strip()

        if not item_name or not description or not location:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("lost_found"))

        if status not in ["Lost", "Found"]:
            flash("Invalid report type.", "error")
            return redirect(url_for("lost_found"))

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO lost_found
                (item_name, description, location, status)
                VALUES (?, ?, ?, ?)
            """, (item_name, description, location, status))

            connection.commit()

            flash("Lost and Found report submitted successfully!", "success")

        except Exception as error:
            connection.rollback()
            flash("Error saving report: " + str(error), "error")

        finally:
            connection.close()

        return redirect(url_for("lost_found"))

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, item_name, description, location, status
            FROM lost_found
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()
        columns = [column[0] for column in cursor.description]

        items = [dict(zip(columns, row)) for row in rows]

    finally:
        connection.close()

    return render_template("lost_found.html", items=items)


# INTERNSHIPS
@app.route("/internships")
def internships():
    return render_template("internships.html")


# COMMUNITY
@app.route("/community", methods=["GET", "POST"])
def community():

    if request.method == "POST":

        student_name = request.form.get("student_name", "").strip()
        usn = request.form.get("usn", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        community_name = request.form.get("community_name", "").strip()

        allowed_communities = [
            "Programming Club",
            "AI & ML Community",
            "Web Development Club",
            "Academic Discussion",
            "Project Collaboration",
            "Creative Community"
        ]

        if not all([
            student_name, usn, email, department, community_name
        ]):
            flash("Please fill in all fields.", "error")
            return redirect(url_for("community") + "#joinForm")

        if community_name not in allowed_communities:
            flash("Please select a valid community.", "error")
            return redirect(url_for("community") + "#joinForm")

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS community_members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_name TEXT NOT NULL,
                    usn TEXT NOT NULL,
                    email TEXT NOT NULL,
                    department TEXT NOT NULL,
                    community_name TEXT NOT NULL,
                    joined_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            cursor.execute("""
                INSERT INTO community_members
                (student_name, usn, email, department, community_name)
                VALUES (?, ?, ?, ?, ?)
            """, (
                student_name,
                usn,
                email,
                department,
                community_name
            ))

            connection.commit()

            flash(
                "Congratulations! You joined the community successfully!",
                "success"
            )

        except Exception as error:
            connection.rollback()
            flash("Registration failed: " + str(error), "error")

        finally:
            connection.close()

        return redirect(url_for("community") + "#joinForm")

    return render_template("community.html")


# CONTACT
@app.route("/contact", methods=["GET", "POST"])
def contact():

    if request.method == "POST":

        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        subject = request.form.get("subject", "").strip()
        message = request.form.get("message", "").strip()

        if not name or not email or not subject or not message:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("contact"))

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO contact_messages
                (name, email, message)
                VALUES (?, ?, ?)
            """, (
                name,
                email,
                "Subject: " + subject + "\n\n" + message
            ))

            connection.commit()

            flash("Your message has been sent successfully!", "success")

        except Exception as error:
            connection.rollback()
            flash("Error sending message: " + str(error), "error")

        finally:
            connection.close()

        return redirect(url_for("contact"))

    return render_template("contact.html")


# EVENT REGISTRATION
@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        student_name = request.form.get("student_name", "").strip()
        usn = request.form.get("usn", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        event_name = request.form.get("event_name", "").strip()

        if not all([
            student_name,
            usn,
            email,
            department,
            event_name
        ]):
            return render_template(
                "registration.html",
                error="Please fill in all fields.",
                selected_event=event_name
            )

        connection = get_connection()

        try:
            cursor = connection.cursor()

            cursor.execute("""
                INSERT INTO registrations
                (student_name, usn, email, department, event_name)
                VALUES (?, ?, ?, ?, ?)
            """, (
                student_name,
                usn,
                email,
                department,
                event_name
            ))

            connection.commit()

        except Exception as error:
            connection.rollback()

            return render_template(
                "registration.html",
                error="Registration failed: " + str(error),
                selected_event=event_name
            )

        finally:
            connection.close()

        return render_template(
            "registration.html",
            success="Registration completed successfully!",
            selected_event=event_name
        )

    selected_event = request.args.get("event", "")

    return render_template(
        "registration.html",
        selected_event=selected_event
    )


# VIEW ALL EVENT REGISTRATIONS
@app.route("/event-registrations")
def event_registrations():

    connection = get_connection()

    try:
        cursor = connection.cursor()

        cursor.execute("""
            SELECT student_name, usn, email, department,
                   event_name, registered_at
            FROM registrations
            ORDER BY id DESC
        """)

        rows = cursor.fetchall()

        columns = [
            column[0] for column in cursor.description
        ]

        registrations = [
            dict(zip(columns, row)) for row in rows
        ]

    finally:
        connection.close()

    return render_template(
        "event_registrations.html",
        registrations=registrations
    )


if __name__ == "__main__":
    app.run(debug=True)