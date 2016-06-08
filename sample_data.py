from model import connect_to_db, db, User, List, Location, Category, Item
from flask_sqlalchemy import SQLAlchemy
from server import app


def sample_data():
	"""create sample data"""

	# In case this is run more than once, dump existing data
	db.drop_all()
	db.create_all()

	# Add sample Uers
	user1 = User(user_name='Kelly', password='1234', email='kelly4strength@gmail.com')
	user2 = User(user_name='Kate', password='1234', email='kate@kellyhoffer.com')
	user3 = User(user_name='Jack', password='1234', email='jack@kellyhoffer.com')

	db.session.add_all([user1, 
	                    user2,
	                    user3])
	db.session.commit()

	kelly_id = User.query.filter_by(user_name='Kelly').first().user_id
	kate_id = User.query.filter_by(user_name='Kate').first().user_id
	jack_id = User.query.filter_by(user_name='Jack').first().user_id

	    # Add sample locations
	location1 = Location(location_name='New York')
	location2 = Location(location_name='San Francisco')
	location3 = Location(location_name='Rome')
	location4 = Location(location_name='Tokyo')

	db.session.add_all([location1,
	                    location2,
	                    location3,
	                    location4])

	db.session.commit()  

	NY = Location.query.filter_by(location_name='New York').first().location_id
	SF = Location.query.filter_by(location_name='San Francisco').first().location_id
	RM = Location.query.filter_by(location_name='Rome').first().location_id
	TK = Location.query.filter_by(location_name='Tokyo').first().location_id

	# Add sample lists
	list1 = List(list_name='My New York', user_id=kelly_id, location_id=NY)
	list2 = List(list_name='I love SF', user_id=kate_id, location_id=SF)
	list3 = List(list_name='Rome yay', user_id=jack_id, location_id=RM)
	list4 = List(list_name='Kate NYC', user_id=kate_id, location_id=NY)
	list5 = List(list_name='Kelly SF', user_id=kelly_id, location_id=SF)
	list6 = List(list_name='Rome in Summer', user_id=kelly_id, location_id=RM)
	list7 = List(list_name='Tokyo with Noel', user_id=kelly_id, location_id=TK)



	db.session.add_all([list1,
	                    list2,
	                    list3,
	                    list4,
	                    list5,
	                    list6,
	                    list7])

	db.session.commit()

	lst1 = List.query.filter_by(list_name='My New York').first().list_id
	lst2 = List.query.filter_by(list_name='I love SF').first().list_id
	lst3 = List.query.filter_by(list_name='Rome yay').first().list_id
	lst4 = List.query.filter_by(list_name='Kate NYC').first().list_id
	lst5 = List.query.filter_by(list_name='Kelly SF').first().list_id
	lst6 = List.query.filter_by(list_name='Rome in Summer').first().list_id
	lst7 = List.query.filter_by(list_name='Tokyo with Noel').first().list_id


	# Add sample categories
	category1 = Category(category_name='restaurant')
	category2 = Category(category_name='museum')
	category3 = Category(category_name='bar')

	db.session.add_all([category1,
	         	        category2,
	                    category3])

	db.session.commit()

	r1 = Category.query.filter_by(category_name='restaurant').first().category_id
	r2 = Category.query.filter_by(category_name='museum').first().category_id
	r3 = Category.query.filter_by(category_name='bar').first().category_id

	# Add sample items for lists
	item1 = Item(item_name='PickMeUp', item_comments='our favorite cafe from college', item_address='address, ny', list_id=lst1, category_id=r1)
	item2 = Item(item_name='Foreign Cinema', item_comments='fried chicken', item_address='address, sf', list_id=lst2, category_id=r1)
	item3 = Item(item_name='San Crispino', item_comments='eat all the gelato', item_address='address, rome', list_id=lst3, category_id=r1)
	item4 = Item(item_name='The Vatican', item_comments='Amazing assortment of tourists, all the people watching', item_address='Vatican City', list_id=lst6, category_id=r2)
	item5 = Item(item_name="Rocco's", item_comments='cannoli and cheesecake', item_address='400 Bleeker St, NY, NY', list_id=lst4, category_id=r1)
	item6 = Item(item_name='Brothers Korean BBQ', item_comments='Bi Bim Bop!', item_address='Geary at 6th St, SF, CA', list_id=lst5, category_id=r3)
	item7 = Item(item_name='Robot Cafe', item_comments='Robot waiters', item_address='Tokyo', list_id=lst7, category_id=r3)



	#Add all the data to the session
	db.session.add_all([ item1,
	                    item2,
	                    item3, 
	                    item4,
	                    item5,
	                    item6,
	                    item7 ])

	#commit data to the database
	db.session.commit()

connect_to_db(app)
print "Connected to DB."

sample_data()

print "Sample Data created"
