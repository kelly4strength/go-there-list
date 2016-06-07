"""Models and database functions for GoList project"""

from flask_sqlalchemy import SQLAlchemy

# from werkzeug.security import generate_password_hash, \
#      check_password_hash


# This is the connection to the PostgreSQL database through
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
    # password = db.Column(db.BigInteger, nullable=True)

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
    
    # Define relationships
    user = db.relationship('User')
    location = db.relationship('Location')
    item = db.relationship('Item')  

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<List list_id=%s list_name=%s user_id=%s location_id=%s>" % (
            self.list_id, self.list_name, self.user_id, self.location_id)


class Location(db.Model):
    """Location of list. One location can have many lists."""

    __tablename__ = "locations"

    location_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    location_name = db.Column(db.String(100))

    list = db.relationship('List')

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
    item_name = db.Column(db.String(100))
    item_comments = db.Column(db.String(1000))
    item_address = db.Column(db.String(1000))
    
    list_id = db.Column(db.Integer, db.ForeignKey('lists.list_id'))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    
    # Setting up table relationships
    list = db.relationship('List')
    category = db.relationship('Category')

    def __repr__(self):
        """Provide helpful representation when printed."""

        return "<Item item_id=%s item_name=%s item address_id=%s item_comments=%s list_id=%s, category_id=%s>" % (
            self.item_id, self.item_name, self.item_address, self.item_comments, self.list_id, self.category_id)


def copy_items_to_db(categories, list_id, item_name, item_address, item_comments):

    for num in range(len(categories)):

        final_item = Item(list_id=list_id,
                    category_id=categories[num],
                    item_name=item_name[num],
                    item_address=item_address[num],
                    item_comments=item_comments[num])

        db.session.add(final_item)
        db.session.commit()







##############################################################################

def connect_to_db(app, db_uri="postgresql:///golists"):
    """Connect the database to our Flask app."""

    # Configure to use our PostgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    from server import app
    
    connect_to_db(app)
    print "Connected to DB."

    db.create_all()
