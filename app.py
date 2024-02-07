from flask import Flask, render_template, request

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
@app.route("/index", methods=["GET", "POST"])
def index():
    error_message = ""
    if request.method == "POST":
        try:
            name = request.form["name"]
            firstname = request.form["firstname"]
            number_guests = request.form["number_guests"]
            is_present = request.form["is_present"]
            message = request.form["message"]

            if name == "" or firstname == "":
                error_message = "Veillez remplir tous les champs obligatoires."
                return render_template("index.html", error_message=error_message)
            if number_guests == "":
                error_message = "Veillez remplir tous les champs obligatoires."
                return render_template("index.html", error_message=error_message)
            if is_present == "yes":
                is_present = True
            else:
                is_present = False
            if message == "":
                message = "No message"

            # Ajoutez les données du formulaire dans la base de données
            # sqlite
            import sqlite3

            conn = sqlite3.connect("guests.db")

            conn.row_factory = sqlite3.Row

            cursor = conn.cursor()

            cursor.execute("SELECT name, firstname FROM guests WHERE name = ? AND firstname = ?", (name, firstname))
            row = cursor.fetchone()

            if row:
                error_message = "Vous avez déjà soumis une réponse."
                return render_template("index.html", error_message=error_message)
            else:
                cursor.execute(
                    "INSERT INTO guests (name, firstname, number_guests, is_present, message) VALUES (?, ?, ?, ?, ?)",
                    (name, firstname, number_guests, is_present, message),
                )

            conn.commit()
            conn.close()

            return render_template(
                "confirmation.html",
                name=name,
                firstname=firstname,
                number_guests=number_guests,
                is_present=is_present,
                message=message,
            )
        except Exception as e:
            return f"An Error Occurred: {e}"
    else:
        return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True)
