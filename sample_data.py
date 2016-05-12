from model import connect_to_db, db, User, List, Location, Category, Item
from flask_sqlalchemy import SQLAlchemy
from server import app


def sample_data():
    """create sample data"""

 # In case this is run more than once, dump existing data
    # User.query.delete()
    # List.query.delete()
    # Location.query.delete()
    # Category.query.delete()
    # Item.query.delete()

    # Add sample Uers
    user1 = User(user_name='Kelly', password='1234', email='kelly4strength@gmail.com')
    user2 = User(user_name='Kate', password='1234', email='snothead@kellyhoffer.com')
    user3 = User(user_name='Jack', password='1234', email='jack@kellyhoffer.com')

    db.session.add_all([user1, 
                        user2,
                        user3])
	db.session.commit()

	kelly_id = User.query.filter_by(user_name='Kelly')
	kate_id = User.query.filter_by(user_name='Kate')
	jack_id = User.query.filter_by(user_name='Jack')

	    # Add sample locations
	location1 = Location(location_name='New York')
	location2 = Location(location_name='San Francisco')
	location3 = Location(location_name='Rome')
	
	db.session.add_all([location1,
	                    location2,
	                    location3])

	db.session.commit()  

	l1 = Location.query.filter_by(location_name='New York')
	l2 = Location.query.filter_by(location_name='San Francisco')
	l3 = Location.query.filter_by(location_name='Rome') 

	# Add sample lists
	list1 = List(list_name='My New York', user_id=kelly_id, location_id=l1)
	list2 = List(list_name='I love SF', user_id=kate_id, location_id=l2)
	list3 = List(list_name='Rome yay', user_id=jack_id, location_id=l3)

	db.session.add_all([list1,
	                    list2,
	                    list3])

	db.session.commit()

	lst1 = List.query.filter_by(list_name='My New York')
	lst2 = List.query.filter_by(list_name='I love SF')
	lst3 = List.query.filter_by(list_name='Rome yay')


	# Add sample categories
	category1 = Category(category_name='restaurant')
	category2 = Category(category_name='museum')
	category3 = Category(category_name='bar')

	db.session.add_all([category1,
	                    category2,
	                    category3])

	db.session.commit()

	r1 = Category.query.filter_by(category_name='restaurant')
	r2 = Category.query.filter_by(category_name='museum')
	r3 = Category.query.filter_by(category_name='bar')

	# Add sample items for lists
	item1 = Item(item_name='Pick Me Up', item_comments='our favorite cafe from college', item_address='address, ny', list_id=lst1, category_id=r1)
	item2 = Item(item_name='Foreign Cinema', item_comments='fried chicken', item_address='address, sf', list_id=lst2, category_id=r1 )
	item3 = Item(item_name='San Crispino', item_comments='eat all the gelato', item_address='address, rome', list_id=lst2, category_id=r1 )

	#Add all the data to the session
	db.session.add_all([ item1,
	                    item2,
	                    item3 ])

	#commit data to the database
	db.session.commit()

    
connect_to_db(app)
print "Connected to DB."

sample_data()
