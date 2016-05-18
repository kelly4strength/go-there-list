"""Go Lists"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, List, Location, Category, Item


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Defining variable for Jinja2 to avoid it failing silently
# This way it will raise an error.
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


@app.route('/register')
def register():
    """Send user to registration page"""

    return render_template("register.html")


@app.route('/user_add', methods=["POST"])
def user_add():
    """add new users to dbase"""

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

        session['user_id'] = new_user.user_id
        print session

    return render_template("homepage.html")
   
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
        # at some point make this render a "logged in User homepage"
        return render_template("homepage.html")
    else:
        flash("Password doesn't match. Try 1234")
        return render_template("login.html")

        
@app.route('/logout')
def log_user_out_of_session():
    """remove user from session"""
    
    session.clear()
    print "session cleared"
    
    flash("you have logged out")
    
    return render_template("homepage.html")


@app.route('/users/<int:user_id>')
def user_page(user_id):
    """Take user to a page that displays user info"""

    user = User.query.filter_by(user_id=user_id).first()
    lists = List.query.filter_by(user_id=user_id).all()
#NEED TO WORK ON THIS
    # list_id = List.query.filter_by(user_id=user_id).first()
    # items = Item.query.filter_by(list_id=list_id).all()


    return render_template("user_detail.html", 
                            user=user, 
                            lists=lists)
                            # items=items)


@app.route('/lists/<int:list_id>')
def list_details(list_id):
    """Take user to a page that displays a list"""

    lists = List.query.filter_by(list_id=list_id).first()
    items = Item.query.filter_by(list_id=list_id).all()

    return render_template("list_detail.html", list=list, items=items)


@app.route('/create_list')
def create_list():
    """Send user to first list creation page""" 

    if session.get('current_user') == None:
        flash ("please login before creating a list")
        return render_template("login.html") 

    flash("User is logged in")
    user_id = session['current_user']
    print session

    return render_template("initiate_list.html")


@app.route('/my_lists')
def my_lists():
    """Send user to their personal lists page""" 

    if session.get('current_user') == None:
        flash ("please login first")
        return render_template("login.html") 

    flash("User is logged in")
    user_id = session['current_user']
    print session

    return render_template("my_lists.html")


@app.route('/initiate_list', methods=["POST"])
def initiate_list():
    """choose location and new list name to add to the db"""

    flash("User is logged in")
    #session carried over - remember that thing I asked you to remember? Here it is.
    user_id = session['current_user']

    location_name = request.form.get("location_name")

    location = Location.query.filter_by(location_name=location_name).first()

    if location == None:
        new_location = Location(location_name=location_name)
        db.session.add(new_location)
        db.session.commit()

        location = Location.query.filter_by(location_name=location_name).first()

        #telling the session to please remember this now
        session['current_location'] = location.location_id
        print session

    #session carried over - remember that thing I asked you to remember? Here it is.
    location_id = session['current_location']

    #query to set the variable list_name in order to pass it into the new_list object
    list_name = request.form.get("list_name")

    new_list = List(user_id=user_id,
                    location_id=location_id,
                    list_name=list_name)

    db.session.add(new_list)
    db.session.commit()

    list = List.query.filter_by(list_name=list_name).first()
    
    #telling the session to please remember this now
    session['current_list'] = list.list_id
    print session

    # return render_template("homepage.html")
    return render_template("add_items.html", 
                            location_name=location_name, 
                            list_name=list_name)


@app.route('/add_items', methods=["POST"])
def add_items():
    """create list as logged in user that saves to the db"""

    user_id = session['current_user']
    location_id = session['current_location']
    list_id = session['current_list']
    print session

    category_name = request.form.get("category_name")
    # query categories to get the id 
    category = Category.query.filter_by(category_name=category_name).first()
    
    session['current_category'] = category.category_id
    # print session
    category_id = session['current_category']
    print session
    
    item_name = request.form.get("item_name")
    item_address = request.form.get("item_address")
    item_comments = request.form.get("item_comments")

    new_item = Item(list_id=list_id,
                    category_id=category_id,
                    item_name=item_name,
                    item_address=item_address,
                    item_comments=item_comments)

    db.session.add(new_item)
    db.session.commit()

    flash ("Your item has been added")

    return render_template("new_item.html",
                            list_id=list_id,
                            location_id=location_id)


@app.route('/new_item', methods=["POST"])
def new_item():
    """ask user if they want to add another item"""
    
    user_id = session['current_user']
    location_id = session['current_location']
    list_id = session['current_list']

    print session

    YN = request.form.get("YN")
 
    if YN == "yes":
         return render_template("add_new_items.html", 
                                list_id=list_id,
                                location_id=location_id)

    else:
        return render_template("homepage.html")


@app.route('/add_new_items', methods=["POST"])
def add_new_items():
    """add item to list"""

    # user_id = session['current_user']
    location_id = session['current_location']
    list_id = session['current_list']
    print session

    category_name = request.form.get("category_name")
    # query categories to get the id 
    category = Category.query.filter_by(category_name=category_name).first()
    
    session['current_category'] = category.category_id
    # print session
    category_id = session['current_category']
    print session
    
    item_name = request.form.get("item_name")
    item_address = request.form.get("item_address")
    item_comments = request.form.get("item_comments")

    new_item = Item(list_id=list_id,
                    category_id=category_id,
                    item_name=item_name,
                    item_address=item_address,
                    item_comments=item_comments)

    db.session.add(new_item)
    db.session.commit()

    flash ("Your item has been added")

    return render_template("new_item.html",
                            list_id=list_id,
                            location_id=location_id)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()





