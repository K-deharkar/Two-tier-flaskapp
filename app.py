from flask import Flask, render_template, request, redirect
import mysql.connector

app = Flask(__name__)


def get_db_connection():
    return mysql.connector.connect(
        host="mysql-service",
        user="root",
        password="root",
        database="twotierdb"
    )


@app.route("/")
def index():
    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, message FROM messages")
    messages = cursor.fetchall()

    cursor.close()
    connection.close()

    return render_template("index.html", messages=messages)


@app.route("/add", methods=["POST"])
def add_message():
    name = request.form["name"]
    message = request.form["message"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO messages (name, message) VALUES (%s, %s)",
        (name, message)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return redirect("/")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)