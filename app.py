from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure the SQLite database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///zonetasker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)


# Create a model for the signup table
class SignUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(100), nullable=False, unique=True)
    mobile_phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)


@app.route("/api/signup", methods=["POST"])
def signup():
    # Assuming you want to receive JSON data
    data = request.get_json()

    existing_email_user = SignUp.query.filter_by(
        email_address=data["emailAddress"]
    ).first()
    if existing_email_user:
        return jsonify({"message": "Email address already exists"})

    # Check if the mobile phone already exists
    existing_mobile_user = SignUp.query.filter_by(
        mobile_phone=data["mobilePhoneCountryCode"]
    ).first()
    if existing_mobile_user:
        return jsonify({"message": "Mobile phone number already exists"})

    # Save the signup data to the database
    new_signup = SignUp(
        first_name=data["firstName"],
        last_name=data["lastName"],
        email_address=data["emailAddress"],
        mobile_phone=data["mobilePhoneCountryCode"],
        password=data["password"],
        zip_code=data["zipCode"],
    )

    db.session.add(new_signup)
    db.session.commit()

    # Return a response if needed
    return jsonify({"message": "Signup successful"}), 200


# Route for login
@app.route("/api/login", methods=["POST"])
def login():
    # Assuming you want to receive JSON data
    data = request.get_json()

    # Find the user with the given email address
    user = SignUp.query.filter_by(email_address=data["emailAddress"]).first()

    # Check if the user exists and the provided password matches
    if user and user.password == data["password"]:
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid email address or password"})


if __name__ == "__main__":
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()

    app.run(debug=True)
