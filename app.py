from http.client import HTTPException
import os
from flask import Flask, render_template, request
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

from models import Base, Guest


# Load the environment variables
load_dotenv()

# Get the environment variable
db_user = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")
db_host = os.getenv("DB_HOST")
db_port = os.getenv("DB_PORT")
db_name = os.getenv("DB_NAME")
env = os.getenv("ENV")

if env == "production":
    db_url = os.getenv("HEROKU_POSTGRESQL_BRONZE_URL")
else:
    db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

# Create a new Flask app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = db_url
db = SQLAlchemy(app)


# Gérer les erreurs
@app.errorhandler(HTTPException)
def handle_error(err):
    return render_template("400.html", errorCode=err.code), err.code


@app.errorhandler(500)
@app.errorhandler(501)
def server_error(err):
    return render_template("500.html"), err.code


@app.route("/", methods=["GET", "POST"])
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

            # Add the data to the database
            # Create a connection to the database
            engine = create_engine(db_url)

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
                number_guests=int(number_guests),
                is_present=is_present,
                message=message,
            )
        except Exception as e:
            return f"An Error Occurred: {e}"
    else:
        return render_template("index.html")


@app.route("/guests")
def guests():
    # Create a connection to the database
    engine = create_engine(db_url)

    Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    guests = session.query(Guest).all()

    # Count the number of guests from the column number_guests
    total_guests = 0
    for guest in guests:
        if guest.is_present:
            total_guests += guest.number_guests

    session.close()

    return render_template("guests.html", guests=guests, total_guests=total_guests)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    app.run(host="0.0.0.0", port=port, debug=True)
