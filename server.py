"""Go Lists"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, List, Location, Category, Item


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")


@app.route("/users")
def user_list():
    """Show list of users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/lists")
def all_lists():
    """Show list of lists."""

    lists = List.query.order_by('list_name').all()
    return render_template("all_lists.html", lists=lists)


@app.route('/login')
def login():
    """Take users to page where they have the option to login or register""" 

    return render_template("login.html")


@app.route('/register')
def register():
    """Send user to registration page"""

    return render_template("register.html")


@app.route('/users/<int:user_id>')
def user_page(user_id):
    """Take user to a page that displays user info"""

    user = User.query.filter_by(user_id=user_id).first()
    lists = List.query.filter_by(user_id=user_id).all()

    # raise Exception("let's play")

    return render_template("user_detail.html", user=user, lists=lists)


# @app.route('/movies/<int:movie_id>')
# def movie_page(movie_id):
#     """Take user to a page that displays movie info"""

#     movie = Movie.query.filter_by(movie_id=movie_id).first()
#     session['current_movie'] = movie.movie_id
    
#     ratings = Rating.query.filter_by(movie_id=movie_id).all()

#     # raise Exception("let's play")

#     return render_template("movie_detail.html", movie=movie, ratings=ratings)


# @app.route('/rate', methods=["POST"])
# def rate_movie():
#     """rate movie in db"""

#     movie_id = session['current_movie']

#     flash("User is logged in")
#     user_id = session['current_user']
   
#     score = request.form.get("rating")
    
#     # raise Exception("let's play")

#     if Rating.query.filter_by(movie_id=movie_id, user_id=user_id).first() == None:
#         # raise Exception("let's play")
#         new_rating = Rating(movie_id=movie_id,
#                             user_id=user_id,
#                             score=score)
#         db.session.add(new_rating)
#         db.session.commit()
#         flash("database updated")
#     # else:
#     #     use db.session to update dbase

#     print "got here!"
    

#     movie = Movie.query.filter_by(movie_id=movie_id).first()
#     ratings = Rating.query.filter_by(movie_id=movie_id).all()

#     return render_template("movie_detail.html", movie=movie, ratings=ratings)


# @app.route('/user_add', methods=["POST"])
# def user_add():
#     """add new users to dbase"""
#     # ADD a Flask flash message 

#     email = request.form.get("email")
#     password = request.form.get("password")
#     age = request.form.get("age")
#     zipcode = request.form.get("zipcode")

#     if User.query.filter_by(email=email).first() == None:
#         new_user = User(email=email,
#                         password=password, 
#                         age=age, 
#                         zipcode=zipcode)
#         db.session.add(new_user)
#         db.session.commit()

#         flash("User " + email + " is now registered")
#         session['current_user'] = new_user.user_id

#     return render_template("homepage.html")

# @app.route('/user_validation', methods=["POST"])
# def user_validation():
#     """Validate user login"""

#     email = request.form.get("email")
#     password = request.form.get("password")
    
#     user = User.query.filter_by(email=email).first()
    
#     if user == None:
#         flash("No cheesecake for you! Looks like you need to register")
#         return render_template("register.html")
#     elif user.password == password:
#         session['current_user'] = user.user_id
#         print session
#         flash("User " + email + " signed in")
#         return render_template("homepage.html")
#     else:
#         flash("Password doesn't match. No cheesecake for you!")
#         return render_template("sign_in.html")
        
# @app.route('/logout')
# def log_user_out_of_session():
#     """remove user from session"""
    
#     session.clear()
#     # print session
#     flash("you have logged out")
#     # print session

#     return render_template("homepage.html")


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
