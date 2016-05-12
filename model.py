"""Models and database functions for Ratings project - altered to suit my GoList project"""

from flask_sqlalchemy import SQLAlchemy

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of lists project. User can have many Lists."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(80), nullable=True)
    password = db.Column(db.String(64), nullable=True)

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<User user_id=%s user_name=%s email=%s>" % (self.user_id, self.user_name, self.email)


class List(db.Model):
    """List on the lists website."""

    __tablename__ = "lists"

    list_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    list_name = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    location_id = db.Column(db.Integer, db.ForeignKey('locations.location_id'))

#     # Define relationship to user
#     user = db.relationship("User",
#                            backref=db.backref("lists", order_by=list_id))

# #    Define relationship to movie
#     location = db.relationship("Location",
#                             backref=db.backref("lists", order_by=list_id))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<List list_id=%s list_name=%s user_id=%s location_id=%s>" % (
            self.list_id, self.list_name, self.user_id, self.location_id)


class Location(db.Model):
    """Location of list. One location can have many lists."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    location_name = db.Column(db.String(100))


    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Location location_id=%s location_name=%s>" % (self.location_id, self.location_name)

class Category(db.Model):
    """Category of list item. This is to differentiate the types of Items in a list."""

    __tablename__ = "categories"

    category_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    category_name = db.Column(db.String(80))
    

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Category category_id=%s category_name=%s>" % (
            self.category_id, self.category_name)


class Item(db.Model):
    """restaurant item in a list."""

    __tablename__ = "items"

    item_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    item_name = db.Column(db.Integer)
    item_comments = db.Column(db.String(100))
    item_address = db.Column(db.String(100))
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    
    # Define relationship to list_id
    my_list = db.relationship('List')

    # Define relationship to category_id
    # category = db.relationship('Category')



    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Item item_id=%s item_name=%s item address_id=%s list_id=%s, category_id=%s>" % (
            self.item_id, self.item_name, self.item_address, self.list_id, self.category_id)



def sample_data():
    """create sample data"""

 # In case this is run more than once, dump existing data
    User.query.delete()
    List.query.delete()
    Location.query.delete()
    Category.query.delete()
    Item.query.delete()

    # Add sample Uers
    User1 = User(user_name='Kelly', password='1234', email='kelly4strength@gmail.com')
    User2 = User(user_name='Kate', password='1234', email='snothead@kellyhoffer.com')
    User3 = User(user_name='Jack', password='1234', email='jack@kellyhoffer.com')

    # Add sample lists
    List1 = List(list_name='My New York', user_id='1', location_id='1')
    List2 = List(list_name='I love SF', user_id='1', location_id='2')
    List3 = List(list_name='Rome yay', user_id='2', location_id='3')

    # Add sample locations
    Location1 = Location(location_name='New York')
    Location2 = Location(location_name='San Francisco')
    Location3 = Location(location_name='Rome')

    # Add sample categories
    Category1 = Category(category_name='restaurant')
    Category2 = Category(category_name='museum')
    Category3 = Category(category_name='bar')

    # Add sample items for lists
    Item1 = Item(item_name='Pick Me Up', item_comments='our favorite cafe from college', item_address='address, ny', list_id='1', category_id=1)
    Item2 = Item(item_name='Foreign Cinema', item_comments='fried chicken', item_address='address, sf', list_id='2', category_id=1 )
    Item3 = Item(item_name='San Crispino', item_comments='eat all the gelato', item_address='address, rome', list_id='2', category_id=1 )

    #Add all the data to the session
    db.session.add_all([ User1, 
                        User2,
                        User3,
                        List1,
                        List2,
                        List3,
                        Location1,
                        Location2,
                        Location3,
                        Category1,
                        Category2,
                        Category3,
                        Item1,
                        Item2,
                        Item3])

    #commit data to the database
    db.session.commit()



##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///golists'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."


    # uncomment as needed after dropdb/createdb to regenerate sample data.
    db.create_all()
    # sample_data()
    print "Sample Data created"
