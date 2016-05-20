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
    """Show all users."""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route("/lists")
def all_lists():
    """Show all user lists."""

    lists = List.query.order_by('list_name').all()
    return render_template("alL_lists.html", lists=lists)


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

        #This session message is assigning the value 6 to the user_id in the session
        session['user_id'] = new_user.user_id
        print session
        
        if session.get('user_id') == new_user.user_id:
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

    print session

    return render_template("user_detail.html", 
                            user=user, 
                            lists=lists)


@app.route('/lists/<int:list_id>')
def list_details(list_id):
    """Take user to a page that displays a list"""

    lists = List.query.filter_by(list_id=list_id).first()
    items = Item.query.filter_by(list_id=list_id).all()

    session['current_list'] = list_id
    print session

    return render_template("list_detail.html", 
                            lists=lists, 
                            items=items)


@app.route('/item_detail/<int:item_id>')
def item_details(item_id):
    """Take user to a page that displays a list"""

    # item = Item.query.filter_by(list_id=list_id).first()
    session['current_list'] = list_id

    session['current_item'] = item_id
    list_id = List.query.filter_by(list_id=list_id).first()
    # session['current_user'] = user_id
    print session

    return render_template("list_detail.html", 
                            lists=lists, 
                            items=items)



@app.route('/my_lists')
def my_lists():
    """Show all lists created by user""" 

    if session.get('current_user') == None:
        flash ("please login first")
        return render_template("login.html") 

    flash("User is logged in")
    user_id = session['current_user']
    print session

    user = User.query.filter_by(user_id=user_id).first()
    lists = List.query.filter_by(user_id=user_id).all()

    # items = Items.query.filter_by(list_id=list_id).all()
    #decided I don't need list items here as it has links to list pages
    return render_template("my_lists.html", 
                            user=user, 
                            lists=lists)


@app.route('/create_list')
def create_list():
    """Form to create a new list, choose location and list name""" 

    if session.get('current_user') == None:
        flash ("please login before creating a list")
        return render_template("login.html") 

    flash("User is logged in")
    user_id = session['current_user']
    print session

    return render_template("create_list_form.html")


@app.route('/create_list_form', methods=["POST"])
def start_new_list():
    """Add first item to newly created list"""

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

    lists = List.query.filter_by(list_name=list_name).first()
    
    #telling the session to please remember this now
    session['current_list'] = lists.list_id
    
    user_id = session['current_user']
    location_id = session['current_location']
    list_id = session['current_list']
    print session

    category_name = request.form.get("category_name")
    # query categories to get the id 
    category = Category.query.filter_by(category_name=category_name).first()
    
    session['current_category'] = category.category_id
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
    """Form to ask user if they want to add another item"""
    
    user_id = session['current_user']
    # location_id = session['current_location'] (needed this for previous route, may reinstate)
    list_id = session['current_list']

    print session
    user = User.query.filter_by(user_id=user_id).first()
    lists = List.query.filter_by(user_id=user_id).all()

    YN = request.form.get("YN")

# browser says: http://localhost:5000/new_item for either option 
    if YN == "yes":
         return render_template("add_new_items.html", 
                                list_id=list_id)
    
    return render_template("my_lists.html",
                                user=user, 
                                lists=lists)


@app.route('/add_another_item', methods=["POST"])
def add_another_item():
    """add item to list"""

    user_id = session['current_user']
    # location_id = session['current_location']
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
                            list_id=list_id)


@app.route('/add_item_to_existing_list')
def add_item_to_existing_list():
    """Add item to existing list"""

    user_id = session['current_user']
    list_id = session['current_list']

    lists = List.query.filter_by(user_id=user_id).all()

    return render_template("add_new_items.html",
                                list_id=list_id)



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()





