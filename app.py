from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import dotenv_values

from models import Base, Guest


config = dotenv_values(".env")

db_user = config["DB_USER"]
db_password = config["DB_PASSWORD"]
db_host = config["DB_HOST"]
db_port = config["DB_PORT"]
db_name = config["DB_NAME"]

db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


# Create a connection to the database
engine = create_engine(db_url)


# Create a new Flask app
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

            Base.metadata.create_all(engine)

            Session = sessionmaker(bind=engine)
            session = Session()

            guest = Guest(
                name=name,
                firstname=firstname,
                number_guests=number_guests,
                is_present=is_present,
                message=message,
            )

            query = session.query(Guest).filter_by(name=name, firstname=firstname).first()

            if query:
                error_message = "Vous avez déjà soumis une réponse."
                return render_template("index.html", error_message=error_message)
            else:
                session.add(guest)
                session.commit()
                session.close()

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
    app.run(debug=True, port=8000, host='0.0.0.0')
