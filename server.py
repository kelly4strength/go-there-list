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

    return render_template("choose_location.html")


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
    print session
    flash("you have logged out")
    print session

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


@app.route('/choose_location', methods=["POST"])
def choose_location():
    """choose location for new list as logged in user that saves to the db"""

# flash("User is logged in")
# user_id = session['current_user']

    location_name = request.form.get("location_name")

    new_location = Location(location_name=location_name)

    db.session.add(new_location)
    db.session.commit()

    return render_template("choose_list_name.html", location_name=location_name)


@app.route('/choose_list_name', methods=["POST"])
def choose_list_name():
    """choose list name for new list as logged in user that saves to the db"""

# flash("User is logged in")
# user_id = session['current_user']

    list_name = request.form.get("list_name")

    new_list = List(list_name=list_name)

    db.session.add(new_list)
    db.session.commit()

    return render_template("add_items.html")


@app.route('/add_items', methods=["POST"])
def add_items():
    """create list as logged in user that saves to the db"""

# flash("User is logged in")
# user_id = session['current_user']

    category_name = request.form.get("category_name")
    item_name = request.form.get("item_name")
    item_address = request.form.get("item_address")
    item_comments = request.form.get("item_comments")

    new_category = Category(category_name=category_name)

    db.session.add(new_category)
    db.session.commit()

    new_item = Item(item_name=item_name,
                    item_address=item_address,
                    item_comments=item_comments)

    db.session.add(new_item)
    db.session.commit()

    return render_template("homepage.html")
    # return render_template("list_detail.html",
                        # list_name=list_name,
                        # location_name=location_name,
                        # category_name=category_name,
                        # item_name=item_name,
                        # item_address=item_address,
                        # item_comments=item_comments)


if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()
