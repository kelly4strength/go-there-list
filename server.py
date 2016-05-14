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
    """Send user to login page""" 

    return render_template("login.html")

@app.route('/create_list')
def create_list():
    """Send user to list creation page""" 

    return render_template("create_list.html")


@app.route('/register')
def register():
    """Send user to registration page"""

    return render_template("register.html")


@app.route('/user_add', methods=["POST"])
def user_add():
    """add new users to dbase"""
    # ADD a Flask flash message 

    email = request.form.get("email")
    password = request.form.get("password")
    user_name = request.form.get("user_name")

    if User.query.filter_by(email=email).first() == None:
        new_user = User(email=email,
                        password=password, 
                        user_name=user_name)
        db.session.add(new_user)
        db.session.commit()

        flash("User " + email + " is now registered")

        session['current_user'] = new_user.user_id

    return render_template("homepage.html")
    # want this to reroute you to your user detail page?
    #maybe need to add a query in here... like /lists
    # return render_template("user_detail.html")
    # return render_template("user_detail.html", user=user, lists=lists)

@app.route('/user_validation', methods=["POST"])
def user_validation():
    """Validate user login"""

    email = request.form.get("email")
    password = request.form.get("password")
    
    user = User.query.filter_by(email=email).first()
    
    if user == None:
        flash("Looks like you need to register")
        return render_template("register.html")
    elif user.password == password:
        session['current_user'] = user.user_id
        print session
        flash("User " + email + " signed in")
        #should this also rereout to the user detail page?
        return render_template("homepage.html")
    else:
        flash("Password doesn't match. Try 1234")
        return render_template("login.html")
        
@app.route('/logout')
def log_user_out_of_session():
    """remove user from session"""
    
    session.clear()
    # print session
    flash("you have logged out")
    # print session

    return render_template("homepage.html")


@app.route('/users/<int:user_id>')
def user_page(user_id):
    """Take user to a page that displays user info"""

    user = User.query.filter_by(user_id=user_id).first()
    lists = List.query.filter_by(user_id=user_id).all()

    # raise Exception("let's play")

    return render_template("user_detail.html", user=user, lists=lists)

@app.route('/lists/<int:list_id>')
def list_details(list_id):
    """Take user to a page that displays a list"""

#queries here are to give the jinja the info it needs to render on the page?
    list = List.query.filter_by(list_id=list_id).first()
    # session['current_list'] = list.list_id

    items = Item.query.filter_by(list_id=list_id).all()

    # raise Exception("let's play")
    return render_template("list_detail.html", list=list, items=items)

# MAKE THIS for adding lists
@app.route('/create_a_list', methods=["GET"])
def create_list():
    """create list as logged in user that saves to the db"""

    list_name = request.args.get ("list_name")
    location_name = request.args.get("location_name")
    category_name = request.args.get("category_name")
    item_name = request.args.get ("item_name")
    item_address = request.args.get ("item_address")
    item_comments = request.args.get ("item_comments")


    # new_list = List(list_name=list_name)
    # new_item = Location(location_name=location_name)
    # new_category = Category(category_name=category_name)
    # new_item = Item(item_name=item_name,
    #                     item_address=item_address,
    #                     item_comments=item_comments)

    # db.session.add(new_list)
    # db.session.commit()

    return render_template("create_list.html")
    # render_template("list_detail.html",
    #                     list_name=list_name,
    #                     location_name=location_name,
    #                     category_name=category_name,
    #                     item_name=item_name,
    #                     item_address=item_address,
    #                     item_comments=item_comments)

# Button - create_list
# user clicks Button
# taken to new page at (create_list.html)
# user fills in info
# clicks submit
# data from form is saved to db

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


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
