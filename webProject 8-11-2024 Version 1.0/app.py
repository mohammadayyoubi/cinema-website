from flask import Flask, jsonify, request, redirect, url_for, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "mysql+mysqlconnector://root:123@localhost/webProject"
)
app.config["SECRET_KEY"] = "your_secret_key"

db = SQLAlchemy(app)
login_manager = LoginManager(app)


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

    def __repr__(self):
        return "<User {}>".format(self.username)


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.Integer, primary_key=True)
    fileInput = db.Column(db.String(100))
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

############################## menu backend ####################################33
class Item(db.Model):
    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Double, nullable=False)
    description = db.Column(db.Text, nullable=True)
    categoryName= db.Column(db.String(100),db.ForeignKey("categories.name", ondelete='CASCADE'))  
    def __repr__(self):
        return f"<Item {self.name}>"
    
class Category(db.Model):
    __tablename__ = "categories"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    items = db.relationship('Item', backref='category', cascade="all, delete-orphan", passive_deletes=True)

    def __repr__(self):
        return f"<Category {self.name}>"
    
    

# Create the database tables
with app.app_context():
    db.create_all()



# User Loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


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


@app.route("/add_movie", methods=["POST"])
def add_movie():
    if request.method == "POST":
        file_name = request.form["fileInput"]
        movie_name = request.form["movie-name"]
        startDate = request.form["start-date"]
        endDate = request.form["end-date"]
        cinemaBranch = request.form["cinema-branch"]
        movieTime = request.form["movie-time"]
        room = request.form["room"]
        duration = request.form["duration"]
        description = request.form["description"]

        new_movie = Movie(
            fileInput=file_name,
            movieName=movie_name,
            startDate=startDate,
            endDate=endDate,
            cinemaBranch=cinemaBranch,
            movieTime=movieTime,
            room=room,
            duration=duration,
            description=description,
        )

        db.session.add(new_movie)
        db.session.commit()

        return redirect(url_for("movies"))


@app.route("/delete_movie/<int:movie_id>", methods=["POST"])
def delete_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    db.session.delete(movie)
    db.session.commit()
    # flash('Movie deleted successfully', 'success')
    return redirect(url_for("movies"))


@app.route("/api/edit_movie/<int:movie_id>", methods=["GET", "POST"])
@login_required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == "POST":
        movie.fileInput = request.form["custom-fileInput"]
        movie.movieName = request.form["custom-movie-name"]
        movie.startDate = request.form["custom-start-date"]
        movie.endDate = request.form["custom-end-date"]
        movie.cinemaBranch = request.form["custom-cinema-branch"]
        movie.movieTime = request.form["custom-movie-time"]
        movie.room = request.form["custom-room"]
        movie.duration = request.form["custom-duration"]
        movie.description = request.form["custom-description"]
        db.session.commit()
        # flash('Movie updated successfully', 'success')
        return redirect(url_for("movies"))
    return render_template("edit_movie.html", movie=movie)


@app.route("/results")
def search():

    query = request.args.get("query")
    if query:
        search_results = Movie.query.filter(Movie.movieName.ilike(f"%{query}%")).all()
    else:
        search_results = []
    return render_template("results.html", search_results=search_results, query=query)


@app.route("/movies")
@login_required
def movies():
    new_releases = Movie.query.all()
    return render_template("movies.html", new_releases=new_releases, user=current_user)


@app.route("/book/<int:movie_id>")
def book(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    seats = getSeats(
        movie.room
    )
    htmlClass=[]# Ensure movie.room matches the room_id in the seats table
    for seat in seats:
        htmlClass.append(seat.get('htmlClass'))
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
        "movieId": movie.id
    }

  
    print(htmlClass)
    return render_template("seat_booking.html", seat_layout=seat_layout, movie=movie_data,htmlClass=htmlClass)


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
    found=False
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
            found=True
            try:
                db.session.commit()
                print("comited")
            except Exception as e:
                db.session.rollback()
                print(f"Error: {e}")
                return("Error: Could not reserve seat", 500)
        else:
            found=False
    if found:

        return redirect(url_for("index"))
    else:
        return("Error: Could not reserve seat", 500)

@app.route("/menu")
def menu():
    user = User.query.filter_by(id=current_user.id).first()
    items = Item.query.all()
    categories = Category.query.all()
    return render_template("menu.html", user=current_user, categories=categories,items=items)


# Logout Route
@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))


# Index Route (Requires authentication)
@app.route("/")
def index():
    if current_user.is_authenticated:
        new_releases = Movie.query.all()  # Fetch new movie releases from the database
        return render_template(
            "index.html", user=current_user, new_releases=new_releases
        )
    else:
        return redirect(url_for("login"))


# Add a route for user profile
@app.route("/profile")
@login_required
def profile():
    user = User.query.filter_by(id=current_user.id).first()
    return render_template("profile.html", user=current_user)


# Example Route with RBAC
@app.route("/admin")
@login_required
def admin():
    if current_user.role == "admin":
        return "Admin Dashboard"
    else:
        return "Access Denied"


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
                email=email,
            )
            db.session.add(new_user)
            db.session.commit()
            flash("User created successfully", "success")
            return redirect(url_for("login"))
    return render_template("signup.html")


# ---- Profile
@app.route("/editProfile", methods=["POST", "GET"])
def editProfile():
    # @login_required

    user = User.query.filter_by(id=current_user.id).first()
    name = request.form["profile-name"]
    username = request.form["profile-username"]
    dob = request.form["profile-dob"]
    email = request.form["profile-email"]

    user.Uname = name
    user.username = username
    user.dob = dob
    user.email = email

    db.session.commit()
    return redirect(url_for("profile"))


####################################################################################  new  Secuirty Settings ###########################################


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


# settings for admins


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

@app.route("/AddCategory", methods=['POST','GET'])
def AddCategory():
    if request.method == 'POST':
        name = request.form['category-name']
        new_category = Category(
            name=name
        )
        db.session.add(new_category)
        db.session.commit()
        return redirect(url_for('menu'))

@app.route("/AddItem", methods=['POST','GET'])
def AddItem():
    if request.method == 'POST':
        name = request.form['item-name']
        price = request.form['item-price']
        description = request.form['item-description']
        category = request.form['item-category']
        new_item = Item(
            name=name,
            price=price,
            description=description,
            categoryName=category
        )
        db.session.add(new_item)
        db.session.commit()
        return redirect(url_for('menu'))
    
@app.route("/deleteItem/<int:item_id>",methods=["POST"])
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





if __name__ == "__main__":
    app.run(debug=True)


