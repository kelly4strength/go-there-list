"""Go Lists"""

from jinja2 import StrictUndefined

from flask import Flask, render_template, request, flash, redirect, session
from flask_debugtoolbar import DebugToolbarExtension

from model import connect_to_db, db, User, List, Location, Category, Item

from helper import *

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

    return render_template("user_list.html", users=User.query.all())


@app.route("/lists")
def all_lists():
    """Show all user lists."""

    return render_template("alL_lists.html", lists=List.query.order_by('list_name').all())


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
    #add code to make sure email/username chosen are unique

    email = request.form.get("email")
    password = request.form.get("password")
    user_name = request.form.get("user_name")

    if User.query.filter_by(email=email).first() == None:
        new_user = User(email=email,
                        password=password, 
                        user_name=user_name)
        db.session.add(new_user)
        db.session.commit()

        flash("Hi %s, You are now registered! Please log in." % user_name)

        return render_template("homepage.html")
   
@app.route('/user_validation', methods=["POST"])
def user_validation():
    """Validate user login"""

    email = request.form.get("email")
    password = request.form.get("password")
    
    user = User.query.filter_by(email=email).one()
    #add try and except for cases where the emails are duplicates

    if user == None:
        flash("Looks like you need to register")
        return render_template("register.html")
    
    elif user.password == password:
        session['current_user'] = user.user_id
        flash("Hi  %s, you are now logged in!" % user.user_name)
        return render_template("homepage.html")

    else:
        flash("Sorry, your password doesn't match. Try 1234")
        return render_template("login.html")

        
@app.route('/logout')
def log_user_out_of_session():
    """remove user from session"""

    session.clear()
    flash("You have logged out. See you next time.")
    
    return render_template("homepage.html")


@app.route('/users/<int:user_id>')
def user_page(user_id):
    """Take user to a page that displays user info"""

    return render_template("user_detail.html", 
                            user=User.query.filter_by(user_id=user_id).one(), 
                            lists=List.query.filter_by(user_id=user_id).all())


@app.route('/lists/<int:list_id>')
def list_details(list_id):
    """Take user to a page that displays a list"""
    
    session['current_list'] = list_id

    return render_template("list_detail.html", 
                            lists=List.query.filter_by(list_id=list_id).one(), 
                            items=Item.query.filter_by(list_id=list_id).all())


@app.route('/my_lists')
def my_lists():
    """Show all lists created by user""" 

    if session.get('current_user') == None:
        flash ("please login first")
        return render_template("login.html") 
        
    user_id = session['current_user']

    return render_template("my_lists.html", 
                            user=User.query.filter_by(user_id=user_id).one(), 
                            lists=List.query.filter_by(user_id=user_id).all())


@app.route('/item_detail/<int:item_id>')
def item_details(item_id):
    """Take user to a page that displays the item in their list"""
    
    # if session.get('current_user') == None:
    #     flash ("please login first")
    #     return render_template("login.html") 

    # user_id = session['current_user']
    # list_id = session['current_list']

    # session['current_item'] = item_id

    # Which is better? 
    try:
        user_id = session['current_user']
        list_id = session['current_list']

        session['current_item'] = item_id
    
    except:
        session['current_user'] = None
        flash('Please log in to see item details. Thanks :)')
        return render_template("login.html")
 
    return render_template("item_detail.html", 
                        lists=List.query.filter_by(list_id=list_id).first(), 
                        item=Item.query.filter_by(item_id=item_id).first())


@app.route('/edit_item_detail', methods=["POST"])
def edit_item():
    """user can edit item in their list"""

    user_id = session['current_user']
    list_id = session['current_list']
    item_id = session['current_item']

    update = Item.query.filter_by(item_id=item_id).first()
                                                        
    category_name = request.form.get("category_name")
    category = Category.query.filter_by(category_name=category_name).first()
    
    update.category_id = category_id = category.category_id
    update.item_name = request.form.get("item_name")
    update.item_address = request.form.get("item_address")
    update.item_comments = request.form.get("item_comments")
    
    db.session.commit()

    flash ("Your item has been updated")

    return render_template("list_detail.html", 
                            lists=List.query.filter_by(list_id=list_id).first(), 
                            items=Item.query.filter_by(list_id=list_id).all())


@app.route('/delete_item', methods=["POST"])
def delete_item():
    """delete an item from your item_detail page"""

    list_id = session.get('current_list')
    item_id = session.get('current_item')
    user_id = session.get('current_user')
        # set up way to deal with None
        # use .get - safer, so you avoid errors 
        # If there is nothing in the session, just returns None 
        # from user_id= session['current_user']

    to_delete = Item.query.filter_by(item_id=item_id).one()
                            
    db.session.delete(to_delete)
    db.session.commit()

    flash ("%s has been deleted" % to_delete.item_name)

    return render_template("list_detail.html", 
                            lists=List.query.filter_by(list_id=list_id).first(), 
                            items=Item.query.filter_by(list_id=list_id).all())


@app.route('/copy_items', methods=["POST"])
def copy_items():
    """copy item(s) from list_detail page"""

    try:
        user_id = session.get('current_user')

        #query to get the checked item ids to copy - they come in a list format
        copy_ids = request.form.getlist("copy_item_ids")
        
        ids = []
        # unpack the list of item ids to copy
        
        for i in copy_ids: 
            i = int(i)
            ids.append(i)
        
        new_items = []

        for i in ids:
            
            #query to get the item that goes with item id
            old_item = Item.query.filter_by(item_id=i).one() 

            #passing the old_item data into the new_item for editing
            new_item = Item(item_name=old_item.item_name, 
                        item_address=old_item.item_address,
                        item_comments=old_item.item_comments,
                        category_id=old_item.category_id)
            
            #sets the variable category to represent the old category id being shown on the copy_items html page
            category = Category.query.filter_by(category_id=old_item.category_id).first()

            new_items.append(new_item)

        #query to get current users lists(to populate dropdown to be made on form)
        user_lists = List.query.filter_by(user_id = user_id).all()
        
        list_names = []
        
        #for loop to fetch each list_name and put it in the list_names []
        for l in user_lists:
            list_names.append(l.list_name)
            print list_names
            
        
    except session['current_user'] == None:
        flash('Please log in to copy an item. Thanks :)')
        return render_template("login.html")

    return render_template("copy_items.html",
                                new_items=new_items,
                                list_names=list_names,
                                category=category,
                                item_name=new_item.item_name,
                                item_address=new_item.item_address,
                                item_comments=new_item.item_comments)


@app.route('/copy_items_to_list', methods=["POST"])
def copy_items_to_list():
    """save copied item(s) to list"""

    user_id = session['current_user']
    
    existing_list_name = request.form.get("existing_list_name")
    existing_list = List.query.filter_by(list_name=existing_list_name).first()

    list_id = existing_list.list_id

    categories, item_name, item_address, item_comments = get_item_choices(request)

    for num in range(len(categories)):

        final_item = Item(list_id=list_id,
                    category_id=categories[num],
                    item_name=item_name[num],
                    item_address=item_address[num],
                    item_comments=item_comments[num])

        db.session.add(final_item)
        db.session.commit()

    flash ("%s has been copied to your list" % item_name )

    return render_template("list_detail.html", 
                            lists=List.query.filter_by(list_id=list_id).first(), 
                            items=Item.query.filter_by(list_id=list_id).all())


@app.route('/create_list')
def create_list():
    """Form to create a new list, choose location and list name""" 

    if session.get('current_user') == None:
        flash ("please login before creating a list")
        return render_template("login.html") 

    user_id = session['current_user']

    return render_template("create_list_form.html")


@app.route('/create_list_form', methods=["POST"])
def start_new_list():
    """Add first item to newly created list"""

    user_id = session['current_user']

    list_name = request.form.get("list_name") 

    location_name = request.form.get("location_name")
    location = Location.query.filter_by(location_name=location_name).first()

    if location == None:
        new_location = Location(location_name=location_name)
        db.session.add(new_location)
        db.session.commit()

        location = Location.query.filter_by(location_name=location_name).one()

        session['current_location'] = location.location_id

    location_id = session['current_location']

    new_list = List(user_id=user_id,
                    location_id=location_id,
                    list_name=list_name)

    db.session.add(new_list)
    db.session.commit()
    
    lists = List.query.filter_by(list_name=list_name).one()
    
    user_id = session['current_user']
    location_id = session['current_location']
    list_id = session['current_list'] = lists.list_id

    category_name = request.form.get("category_name")
    category = Category.query.filter_by(category_name=category_name).one()
    
    category_id = session['current_category'] = category.category_id

    new_item = Item(list_id=list_id,
                    category_id=category_id,
                    item_name=request.form.get("item_name"),
                    item_address=request.form.get("item_address"),
                    item_comments=request.form.get("item_comments"))

    db.session.add(new_item)
    db.session.commit()

    return render_template("list_detail.html", 
                            lists=List.query.filter_by(list_id=list_id).one(), 
                            items=Item.query.filter_by(list_id=list_id).all())


@app.route('/add_item_to_existing_list')
def add_item_to_existing_list():
    """Sends user to add another item page"""

    user_id = session['current_user']
    list_id = session['current_list']

    #list query need to be here or things get save to last list viewed
    lists = List.query.filter_by(user_id=user_id).all()

    return render_template("add_new_items.html",
                                list_id=list_id)


@app.route('/add_another_item', methods=["POST"])
def add_another_item():
    """add item(s) to a list"""

    # TODO: fix DOM so that we can get rid of workaround for empty submission

    user_id = session['current_user']
    list_id = session['current_list']

    categories, item_name, item_address, item_comments = get_item_choices(request)

    for num in range(len(categories)):
        final_item = Item(list_id=list_id,
                category_id=categories[num],
                item_name=item_name[num],
                item_address=item_address[num],
                item_comments=item_comments[num])

        db.session.add(final_item)
        db.session.commit()

    flash ("Your item has been added")

    return render_template("list_detail.html", 
                            lists=List.query.filter_by(list_id=list_id).one(), 
                            items=Item.query.filter_by(list_id=list_id).all())



if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension

    # Do not debug for demo
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()





