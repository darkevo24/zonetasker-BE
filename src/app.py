from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Configure the SQLite database
app.config[
    "SQLALCHEMY_DATABASE_URI"
] = "postgresql+psycopg2://default:Jpg7lu0eQLtR@ep-lingering-poetry-97048855.us-east-1.postgres.vercel-storage.com:5432/verceldb"
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    task = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255))
    applicants = db.Column(db.Integer, nullable=False)
    categories = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)


class SignUp(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email_address = db.Column(db.String(100), nullable=False, unique=True)
    mobile_phone = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    zip_code = db.Column(db.String(20), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    province = db.Column(db.String(50), nullable=False)


@app.route("/api/data", methods=["GET"])
def get_all_signups():
    signups = SignUp.query.all()

    signup_list = []
    for signup in signups:
        signup_dict = {
            "id": signup.id,
            "first_name": signup.first_name,
            "last_name": signup.last_name,
            "email_address": signup.email_address,
            "mobile_phone": signup.mobile_phone,
            "password": signup.password,
            "zip_code": signup.zip_code,
        }
        signup_list.append(signup_dict)

    return jsonify({"profile": signup_list})


@app.route("/api/data/<int:id>", methods=["GET"])
def get_signup_by_id(id):
    signup = SignUp.query.get(id)

    if signup:
        signup_dict = {
            "id": signup.id,
            "first_name": signup.first_name,
            "last_name": signup.last_name,
            "email_address": signup.email_address,
            "mobile_phone": signup.mobile_phone,
            "password": signup.password,
            "zip_code": signup.zip_code,
        }
        return jsonify({"profile": signup_dict})
    else:
        return jsonify({"message": "Signup not found"}), 404


@app.route("/api/tasks", methods=["GET"])
def get_tasks():
    email_param = request.args.get("email")

    if email_param:
        tasks = Task.query.filter_by(email=email_param).all()
    else:
        tasks = Task.query.all()

    task_list = [
        {
            "id": task.id,
            "task": task.task,
            "description": task.description,
            "applicants": task.applicants,
            "categories": task.categories,
            "email": task.email,
        }
        for task in tasks
    ]
    return jsonify(task_list)


@app.route("/api/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404
    return jsonify(
        {
            "id": task.id,
            "task": task.task,
            "description": task.description,
            "applicants": task.applicants,
            "categories": task.categories,
            "email": task.email,
        }
    )


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    new_task = Task(
        task=data["task"],
        description=data.get("description", ""),
        applicants=data["applicants"],
        categories=data["categories"],
        email=data["email"],
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Task created successfully"}), 201


@app.route("/api/tasks", methods=["DELETE"])
def delete_all_tasks():
    # Assuming you want to delete all tasks
    Task.query.delete()
    db.session.commit()
    return jsonify({"message": "All tasks deleted successfully"}), 200


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task is None:
        return jsonify({"error": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": f"Task with ID {task_id} deleted successfully"}), 200


@app.route("/api/signup/<string:email>", methods=["GET", "DELETE"])
def signup_by_email(email):
    if request.method == "GET":
        # Retrieve signup by email
        signup = SignUp.query.filter_by(email_address=email).first()
        if signup:
            signup_dict = {
                "id": signup.id,
                "first_name": signup.first_name,
                "last_name": signup.last_name,
                "email_address": signup.email_address,
                "mobile_phone": signup.mobile_phone,
                "password": signup.password,
                "zip_code": signup.zip_code,
                "city": signup.city,
                "province": signup.province,
            }
            return jsonify({"profile": signup_dict})
        else:
            return jsonify({"error": "Signup not found"}), 404

    elif request.method == "DELETE":
        # Delete signup by email
        signup = SignUp.query.filter_by(email_address=email).first()
        if signup:
            db.session.delete(signup)
            db.session.commit()
            return jsonify({"message": "Signup deleted successfully"})
        else:
            return jsonify({"error": "Signup not found"}), 404


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
        city=data["city"],
        province=data["province"],
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
        return jsonify({"message": "Invalid email address or password"})


# For Vercel compatibility, you need to change how the app is run
def create_app():
    return app


app = create_app()

if __name__ == "__main__":
    # Create the database tables before running the app
    with app.app_context():
        db.create_all()

    app.run(debug=False)
