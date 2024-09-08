# from MySQLdb import IntegrityError
from datetime import datetime, timedelta
import random
import os
from flask import (
    Flask,
    Response,
    jsonify,
    request,
    redirect,
    url_for,
    render_template,
    flash,
)
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
import requests
import sqlalchemy
from werkzeug.security import generate_password_hash, check_password_hash
import json
import base64
from sqlalchemy import LargeBinary, text

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root:123@127.0.0.1/webProject"
)
app.config["SECRET_KEY"] = "your_secret_key"

db = SQLAlchemy(app)
login_manager = LoginManager(app)

# -------------------------- Database Tables---------------------------------------------------


# Define User Model
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(100), default="user")
    gender = db.Column(db.String(10))
    dob = db.Column(db.Date)
    Uname = db.Column(db.String(100))
    email = db.Column(db.String(100))
    profilePic = db.Column(db.LargeBinary)

    def __repr__(self):
        return "<User {}>".format(self.username)


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    fileInput = db.Column(db.LargeBinary)  # Store image as BLOB
    movieName = db.Column(db.String(100), nullable=False)
    startDate = db.Column(db.Date, nullable=False)
    endDate = db.Column(db.Date, nullable=False)
    cinemaBranch = db.Column(db.String(50), nullable=False)
    movieTime = db.Column(db.String(5), nullable=False)
    room = db.Column(db.String(20), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"<Movie {self.movieName}>"


class room(db.Model):
    __tablename__ = "rooms"
    roomId = db.Column(db.Integer, primary_key=True)
    NbSeats = db.Column(db.Integer, nullable=False)
    available = db.Column(db.Boolean)

    def __repr__(self):
        return "<room {}>".format(self.roomId)


class Seat(db.Model):
    __tablename__ = "seats"

    room_id = db.Column(db.Integer, primary_key=True)
    seatId = db.Column(db.Integer, primary_key=True)
    available = db.Column(
        db.Boolean, default=True
    )  # This should match the `tinyint(1)` in the database
    reservedBy = db.Column(db.Integer, nullable=True)
    htmlClass = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        return f"<Seat {self.seatId} in Room {self.room_id}>"


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.Integer, primary_key=True)
    movieId = db.Column(db.Integer, db.ForeignKey("movies.id"))
    userId = db.Column(db.Integer, db.ForeignKey("users.id"))
    seatId = db.Column(db.Integer, db.ForeignKey("seats.seatId"))
    price = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.String(5), nullable=False)

    def __repr__(self):
        return f"<Ticket {self.id}>"


class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Double, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image = db.Column(db.LargeBinary)  # Store image as BLOB
    categoryId = db.Column(
        db.Integer, db.ForeignKey("categories.id", ondelete="CASCADE")
    )

    def __repr__(self):
        return f"<Item {self.name}>"


class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Category {self.name}>"


class forgotPass(db.Model):
    __tablename__ = "forgotPass"
    id = db.Column(db.Integer, primary_key=True)
    userId = db.Column(db.Integer, nullable=False)
    token = db.Column(db.String(100), nullable=False, unique=True)
    tokenExpiry = db.Column(db.DateTime, nullable=False)

    def __repr__(self):
        return f"<forgotPass {self.email}>"


# Create the database tables
with app.app_context():
    db.create_all()
    with db.engine.connect() as connection:
        # Use the `text` function to create an executable object
        sql = text("ALTER TABLE movies MODIFY fileInput LONGBLOB;")
        sql2 = text("ALTER TABLE items MODIFY image LONGBLOB;")
        sql3 = text("ALTER TABLE users MODIFY profilePic LONGBLOB")
        # Execute the SQL command
        connection.execute(sql)
        connection.execute(sql2)
        connection.execute(sql3)

# ------------------------------------------- Login/Logout/signup ------------------------------------------------------


# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Signup Route
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        gender = request.form[
            "gender"
        ]  # assuming gender is selected from a dropdown or radio buttons
        dob = request.form["dob"]  # assuming dob is input in a date field
        Uname = request.form["name"]
        email = request.form["email"]
        profilePic = None
        if User.query.filter_by(username=username).first():
            flash("Username already exists", "error")
        else:
            new_user = User(
                username=username,
                password=generate_password_hash(
                    password, method="scrypt", salt_length=16
                ),
                role="user",
                gender=gender,
                dob=dob,
                Uname=Uname,
                profilePic=profilePic,
                email=email,
            )
            db.session.add(new_user)
            db.session.commit()
            flash("User created successfully", "success")
            return redirect(url_for("login"))
    return render_template("signup.html")


# Login Route
@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password", "error")
    return render_template("login.html")


# Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Example Route with RBAC  // This found written but we didnt use / to be used later in control panel
@app.route("/admin")
@login_required
def admin():
    if current_user.role == "admin":
        return "Admin Dashboard"
    else:
        return "Access Denied"


#  ---------------------------------------------- Movies Actions --------------------------------------------------------


# add movie
@app.route("/add_movie", methods=["POST"])
def add_movie():
    if request.method == "POST":
        file_input = request.files[
            "fileInput"
        ].read()  # Read the binary data from the uploaded file

        movie_name = request.form["movie-name"]
        startDate = request.form["start-date"]
        endDate = request.form["end-date"]
        cinemaBranch = request.form["cinema-branch"]
        movieTime = request.form["movie-time"]
        room = request.form["room"]
        duration = request.form["duration"]
        description = request.form["description"]
        checkSaved = True
        newMovie = Movie(
            fileInput=file_input,
            movieName=movie_name,
            startDate=startDate,
            endDate=endDate,
            cinemaBranch=cinemaBranch,
            movieTime=movieTime,
            room=room,
            duration=duration,
            description=description,
        )
        try:
            db.session.add(newMovie)
            db.session.commit()
            return redirect(url_for("movies"))
        except sqlalchemy.exc.IntegrityError as e:
            db.session.rollback()
            checkSaved = False
            print("Error:", e)

        new_releases = Movie.query.all()
        return render_template(
            "movies.html",
            new_releases=new_releases,
            user=current_user,
            checkSaved=checkSaved,
            movie=newMovie,
        )


# delete movie
@app.route("/delete_movie/<int:movie_id>", methods=["POST"])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    # flash('Movie deleted successfully', 'success')
    return redirect(url_for("movies"))


# edit movie
@app.route("/edit_movie/<int:movie_id>", methods=["GET", "POST"])
@login_required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        # movie.fileInput = request.files.get("custom-fileInput")
        movie.movieName = request.form["custom-movie-name"]
        movie.startDate = request.form["custom-start-date"]
        movie.endDate = request.form["custom-end-date"]
        movie.cinemaBranch = request.form["custom-cinema-branch"]
        movie.movieTime = request.form["custom-movie-time"]
        movie.room = request.form["custom-room"]
        movie.duration = request.form["custom-duration"]
        movie.description = request.form["custom-description"]
        movie.fileInput = request.files[
            "custom-fileInput"
        ].read()  # Read the binary data from the uploaded file
        db.session.commit()
        return redirect(url_for("movies"))

    return render_template("edit_movie.html", movie=movie)


# ---------------------------------------------- pages routes --------------------------------------------------------


# result search page
@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    if query:
        # Query to filter movies
        search_results = Movie.query.filter(
            (Movie.movieName.ilike(f'%{query}%')) |
            (Movie.description.ilike(f'%{query}%'))
        ).all()
        
        # If it's an AJAX request, return JSON response
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            result_list = [{
                'id': movie.id,
                'movieName': movie.movieName,
                'description': movie.description,
                'img_url': url_for('serve_image', movie_id=movie.id),
                'book_url': url_for('book', movie_id=movie.id)
            } for movie in search_results]
            return jsonify(result_list)
    else:
        search_results = []

    return render_template('results.html', search_results=search_results, query=query)

    return jsonify(result_list)
    query = request.args.get("query")
    if query:
        search_results = Movie.query.filter(Movie.movieName.ilike(f"%{query}%")).all()
    else:
        search_results = []
    return render_template("results.html", search_results=search_results, query=query)


# all movies page
@app.route("/movies")
@login_required
def movies():
    new_releases = Movie.query.all()
    return render_template(
        "movies.html", new_releases=new_releases, user=current_user, checkSaved=True
    )


# Index Route (Requires authentication)
@app.route("/")
def index():
    if current_user.is_authenticated:
        current_date = datetime.now().date()  # Get the current date
        new_releases = Movie.query.all()  # Fetch new movie releases from the database
        return render_template(
            "index.html", user=current_user, new_releases=new_releases, current_date = current_date
        )
    else:
        return redirect(url_for("login"))


# profile page
@app.route("/profile")
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template("profile.html", user=current_user)


# menu page
@app.route("/menu")
def menu():
    user = User.query.filter_by(id=current_user.id).first()
    items = Item.query.all()
    categories = Category.query.all()
    return render_template(
        "menu.html", user=current_user, categories=categories, items=items
    )


# ---------------------------------------------- Tickets Booking Actions --------------------------------------------------------
@app.route("/book/<int:movie_id>")
def book(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    seats = getSeats(movie.room)
    htmlClass = []  # Ensure movie.room matches the room_id in the seats table
    for seat in seats:
        htmlClass.append(seat.get("htmlClass"))
    # Example seat layout with multiple rows
    seat_layout = [
        seats[0:6],  # Row 1
        seats[6:12],  # Row 2
        seats[12:18],  # Row 3
        seats[18:24],  # Row 4
        seats[24:30],  # Row 5
        seats[30:36],  # Row 6
        seats[36:42],  # Row 7
    ]
    print(seat_layout)
    movie_data = {
        "movieName": movie.movieName,
        "movieTime": movie.movieTime,
        "movieId": movie.id,
    }

    print(htmlClass)
    return render_template(
        "seat_booking.html",
        seat_layout=seat_layout,
        movie=movie_data,
        htmlClass=htmlClass,
    )


def getSeats(room_id):
    # Query the Seat model to get all seats for the specified room_id
    seats = Seat.query.filter_by(room_id=room_id).all()

    # Serialize the seats into a list of dictionaries
    seats_list = [
        {
            "room_id": seat.room_id,
            "seatId": seat.seatId,
            "available": seat.available,
            "reservedBy": seat.reservedBy,
            "htmlClass": seat.htmlClass,
        }
        for seat in seats
    ]

    return seats_list


@app.route("/save_seating/<int:movie_id>", methods=["POST"])
@login_required
def save_seating(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    selected_seats = request.form.get("seats", "").split(",")
    user_id = current_user.id  # Ensure this gives the correct user ID
    print(selected_seats)
    found = False
    for seat_id in selected_seats:
        seat = Seat.query.filter_by(
            seatId=seat_id, room_id=movie.room
        ).first()  # Include room_id in the filter
        print(seat)

        if seat and seat.available:
            seat.available = False
            seat.reservedBy = user_id
            seat.htmlClass = "seat sold"
            print("success sold")
            found = True
            try:
                db.session.commit()
                print("comited")
            except Exception as e:
                db.session.rollback()
                print(f"Error: {e}")
                return ("Error: Could not reserve seat", 500)
        else:
            found = False
    if found:

        return redirect(url_for("index"))
    else:
        return ("Error: Could not reserve seat", 500)


# ---------------------------------------------- Profile page actions --------------------------------------------------------
# Edit Profile
@app.route("/editProfile", methods=["POST", "GET"])
def editProfile():
    # @login_required

    user = User.query.filter_by(id=current_user.id).first()
    name = request.form["profile-name"]
    username = request.form["profile-username"]
    dob = request.form["profile-dob"]
    email = request.form["profile-email"]
    if "profile-picture" in request.files:
        file = request.files["profile-picture"]
        if file.filename != "":
            user.profilePic = file.read()

    user.Uname = name
    user.username = username
    user.dob = dob
    user.email = email

    db.session.commit()
    return redirect(url_for("profile"))


# ------- Secuirty Settings --------


@app.route("/changePassforUser", methods=["GET", "POST"])
def changePass():
    if request.method == "POST":
        curr_pass = request.form["current-password"]
        new_pass1 = request.form["new-password"]
        new_pass2 = request.form["confirm-password"]

        user = User.query.filter_by(id=current_user.id).first()

        if user:
            # Check if the current password matches the one in the database
            if check_password_hash(user.password, curr_pass):
                # Check if the new password and confirmation match
                if new_pass1 == new_pass2:
                    # Update the password in the database with the new hashed password
                    user.password = generate_password_hash(new_pass1)
                    db.session.commit()
                    flash("Password updated successfully", "success")
                    return redirect(
                        url_for("profile")
                    )  # Redirect to the profile page after success
                else:
                    flash("Passwords do not match", "error")
            else:
                flash("Incorrect current password", "error")
        else:
            flash("User not found", "error")
    return render_template("profile.html", user=current_user)


# ------ settings for admins (Security control settings) ------


@app.route("/changePassforAdmin", methods=["POST", "GET"])
def changeAdminPass():
    usernameP = request.form["other-username"]
    new_pass1 = request.form["new-password"]
    new_pass2 = request.form["confirm-password"]

    user = User.query.filter_by(
        username=usernameP
    ).first()  # query la njib user yle 3ndo hl username

    if user != None:

        if new_pass1 == new_pass2:
            user.password = generate_password_hash(new_pass1)
            db.session.commit()
            flash("Password updated successfully", "success")
            return redirect(url_for("profile"))
        else:
            flash("Passwords are not matched", "error")
    else:
        flash("User not found!", "error")
    return render_template("profile.html", user=current_user)


@app.route("/changeRole", methods=["POST", "GET"])
def changeRole():
    usernameR = request.form["other-username"]
    role = request.form["role"]

    user = User.query.filter_by(username=usernameR).first()

    if user != None:
        user.role = role
        db.session.commit()
        flash("Role updated successfully", "success")
        return redirect(url_for("profile"))
    else:
        flash("User not found!", "error")
    return render_template("profile.html", user=current_user)


@app.route("/deleteUser", methods=["POST", "GET"])
def deleteUser():
    usernameD = request.form["other-username"]

    user = User.query.filter_by(username=usernameD).first()

    if user != None:
        db.session.delete(user)
        db.session.commit()
        flash("User deleted successfully", "success")
        return redirect(url_for("profile"))
    else:
        flash("User not found!", "error")
    return render_template("profile.html", user=current_user)


# ---------------------------------------------- Menu Actions --------------------------------------------------------


@app.route("/AddCategory", methods=["POST", "GET"])
def AddCategory():
    if request.method == "POST":
        name = request.form["category-name"]
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for("menu"))


@app.route("/AddItem", methods=["POST", "GET"])
def AddItem():
    if request.method == "POST":
        name = request.form["item-name"]
        price = request.form["item-price"]
        description = request.form["item-description"]
        category = request.form["item-category"]
        image = request.files["fileInput"].read()
        new_item = Item(
            name=name,
            price=price,
            description=description,
            categoryId=category,
            image=image,
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for("menu"))


@app.route("/deleteItem/<int:item_id>", methods=["POST"])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for("menu"))


@app.route("/delete_category/<int:category_id>", methods=["POST"])
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return redirect(url_for("menu"))


@app.route("/edit_category", methods=["POST"])
def edit_category():
    category_id = request.form["Ecategory-id"]
    new_name = request.form.get("Ecategory-name")

    try:
        # Fetch the category to update
        category = Category.query.filter_by(id=category_id).first()
        if category:
            category.name = new_name
            db.session.commit()
            return redirect(url_for("menu"))
        else:
            return "Category not found", 404
    except Exception as e:
        db.session.rollback()
        return str(e), 500


@app.route("/edit_item", methods=["POST"])
def edit_item():
    item_id = request.form["Eitem-id"]
    new_name = request.form.get("Eitem-name")
    new_price = request.form.get("Eitem-price")
    new_description = request.form.get("Eitem-description")
    new_category = request.form.get("Eitem-category")
    new_image = request.files["fileInput"].read()

    try:
        # Fetch the item to update
        item = Item.query.filter_by(id=item_id).first()
        if item:
            item.name = new_name
            item.price = new_price
            item.description = new_description
            item.categoryId = new_category
            item.image = new_image
            db.session.commit()
            return redirect(url_for("menu"))
        else:
            return "Item not found", 404
    except Exception as e:
        db.session.rollback()
        return str(e), 500


# ---------------------------- Serve Image (display from bd) -------------------------------------


@app.route(
    "/image/<int:movie_id>"
)  # krml t3rod image w t2raha image mesh binary file  --  movie image
def serve_image(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return Response(movie.fileInput, mimetype="image/jpeg")


@app.route(
    "/imageItem/<int:item_id>"
)  # krml t3rod image w t2raha image mesh binary file  -- menu item image
def serve_imageItem(item_id):
    item = Item.query.get_or_404(item_id)
    return Response(item.image, mimetype="image/jpeg")


@app.route(
    "/imageUser/<int:user_id>"
)  # krml t3rod image w t2raha image mesh binary file   -- user profile pic
def serve_imageUser(user_id):
    user = User.query.get_or_404(user_id)
    return Response(user.profilePic, mimetype="image/jpeg")


# ---------------------------- Forgot Password -------------------------------------


@app.route("/forgotpass", methods=["GET", "POST"])
def forgotpass():
    return render_template("forgotpass.html")


@app.route("/sendemailpin", methods=["GET", "POST"])
def sendemailpin():
    email = request.form["email"]
    print(email)
    user = User.query.filter_by(email=email).first()
    if user:
        pin = generate_pin()
        send_simple_message(pin, email)
        current_time = datetime.now()

        two_hours_from_now = current_time + timedelta(hours=2)

        forgotpassword = forgotPass(
            userId=user.id,  # Make sure this value is provided
            token=pin,
            tokenExpiry=datetime.now() + timedelta(hours=2),  # Expiry in 2 hours
        )
        db.session.add(forgotpassword)
        db.session.commit()
        print("user pin is set:", forgotpassword.token)
        userFound = True
        login_user(user)
        return render_template("forgotpass.html", userFound=userFound, email=email)

    else:
        userNotFound = True
        return render_template("forgotpass.html", userNotFound=userNotFound)


@app.route("/verifyPin", methods=["POST"])
def verifyPin():
    # Safely retrieve 'pin' from the form
    pin = request.form.get("pin")

    # Debugging: print the form data
    print(f"Form data: {request.form}")

    # Look up the forgot password record
    forgotPassword = forgotPass.query.filter_by(token=pin).first()

    if forgotPassword:
        return render_template("resetpass.html", userId=forgotPassword.userId)
    else:
        wrongPin = True
        return render_template("forgotpass.html", wrongPin=wrongPin)


@app.route("/resetPassword", methods=["GET", "POST"])
def resetPassword():
    if request.method == "POST":
        newPassword = request.form["newpass"]

        # Debugging: Print the new password and current user
        print(f"New password: {newPassword}")
        print(f"Current user: {current_user.username}")

        user = current_user
        if user:
            user.password = generate_password_hash(newPassword)
            db.session.commit()
            print(
                f"Password changed successfully for user {user.username} with new password {newPassword}"
            )
            return render_template("index.html", passwordChanged=True, user=user)
        else:
            return "User not found", 404
    else:
        return render_template(
            "resetpass.html"
        )  # Render reset password form for GET requests


# --------------------- Email Verification -------------------------
def send_simple_message(pin, email):

    response = requests.post(
        "https://api.mailgun.net/v3/sandbox3ceaa358036244608f598cba5865bf95.mailgun.org/messages",
        auth=("api", "f6e3c37753e8e6edbe1e8361cb6e4338-777a617d-59c24f7e"),
        data={
            "from": "verification@gmail.com",
            "to": [email],
            "subject": "Your Verification Code",
            "text": f"Here is your verification code: {pin} you have 2 hours to enter it...",
        },  # Include the PIN in the email body
    )

    status_code = response.status_code
    response_text = response.text

    if status_code == 200:
        print(f"Email sent successfully! with pin: {pin}")
    elif status_code == 401:
        print("401 Unauthorized: Check if your API key is correct and not expired.")
    elif status_code == 403:
        print(
            "403 Forbidden: Verify that the recipient email addresses are authorized for your sandbox domain."
        )
    else:
        print(f"Error {status_code}: {response_text}")


def generate_pin():
    pin = str(random.randint(1000, 9999))  # Generate a 4-digit PIN

    while forgotPass.query.filter_by(
        token=pin
    ).first():  # Check if the generated PIN exists
        pin = str(random.randint(1000, 9999))  # Generate a new PIN if it already exists

    print(f"Generated unique PIN: {pin}")
    return pin


if __name__ == "__main__":
    app.run(debug=True)
