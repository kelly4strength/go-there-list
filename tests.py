"""Flask unit tests"""

import unittest
# Unit Test: does this individual component work?

from unittest import TestCase
#not sure...

from server import app
# from flask.ext.sqlalchemy import SQLAlchemy
import server


from model import *
from sample_data import *

class FlaskTestsBasic(unittest.TestCase):
    """Flask tests."""

    def setUp(self):
        """Do before every test"""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test homepage page"""

        result = self.client.get("/")
        self.assertIn("Create a List", result.data)
        print "completed homepage test"


    def test_login(self):
        """test login page"""

        result = self.client.get("/login")
        self.assertIn("Login to Go", result.data)
        print "completed login page test"


    def test_register(self):
        """test the registration page"""

        result = self.client.get("/register")
        self.assertIn("Register for Go", result.data)
        print "completed register page test"


    def test_users(self):
        """Test users page."""

        result = self.client.get("/users")
        self.assertIn("Click on a User to see their lists", result.data)
        print "completed users page test"


    def test_lists(self):
        """Test lists page."""

        result = self.client.get("/lists")
        self.assertIn("Click on a goList", result.data)
        print "completed lists page test"


    def test_logout(self):
        """Test lists page."""

        result = self.client.get("/logout")
        self.assertIn("logged out. See", result.data)
        print "completed logout page test"


class FlaskTestsDatabase(TestCase):
    """Flask tests that use the database."""

    def setUp(self):
        """Stuff to do before every test."""

       
        app.config['TESTING'] = True
        app.config['SECRET_KEY'] = 'key'
        self.client = app.test_client()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["current_user"] = 1
                sess["current_list"] = 1
                sess["current_item"] = 1
                sess["current_category"] = 1

        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        sample_data()
        
        print "completed sample data setup"

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()


    def test_list_details(self):
        """Test list detail page."""

        result = self.client.get("/lists/1")
        self.assertIn("New York", result.data)
        print "completed list details page test"


    def test_user_page(self):
        """Test list detail page."""

        result = self.client.get("/users/1")
        self.assertIn("Kelly's Lists", result.data)
        print "completed user details page test"

    def test_create_list(self):
        """Test create list route."""

        result = self.client.get("/create_list")
        self.assertIn("Choose a location", result.data)
        print "completed create list route test"

    def test_my_lists(self):
        """Test mylists page."""

        result = self.client.get("/my_lists")
        self.assertIn("My New York", result.data)
        print "completed my_lists page test"

    def test_user_validation(self):
        """Test user validation route."""

        result = self.client.post('/user_validation', 
                                  data={"email": "kelly4strength@gmail.com", "password": "1234"})
        self.assertIn("you are now logged in!", result.data)
        print "completed user validation page test"

    def test_item_detail(self):
        """Test item detail page."""

        result = self.client.get("/item_detail/1")
        self.assertIn("My New York", result.data)
        print "completed my_lists page test"



# Post and form data
# def test_favorite_color_form(self):
#     test_client = server.app.test_client()

#     result = test_client.post('/fav_color', data={'color': 'blue'})
#     self.assertIn('I like blue, too', result.data)




    # def test_user_add(self):

    

    # def test_edit_item_detail(self):

    # def test_delete_item(self):

    # def test_copy_items(self):

    # def test_copy_items_to_list(self):

    # def test_create_list_form(self):

    # def test_add_item_to_existing_list(self):

    # def test_add_another_item(self):

# class FlaskTestsLoggedIn(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         app.config['SECRET_KEY'] = 'key'
#         self.client = app.test_client()

#         with self.client as c:
#             with c.session_transaction() as sess:
#                 sess['user_id'] = 1

#     def test_important_page(self):
#         """Test important page."""

#         result = self.client.get("/important")
#         self.assertIn("You are a valued user", result.data)


# class FlaskTestsLoggedOut(TestCase):
#     """Flask tests with user logged in to session."""

#     def setUp(self):
#         """Stuff to do before every test."""

#         app.config['TESTING'] = True
#         self.client = app.test_client()

#     def test_important_page(self):
#         """Test that user can't see important page when logged out."""

#         result = self.client.get("/important", follow_redirects=True)
#         self.assertNotIn("You are a valued user", result.data)
#         self.assertIn("You must be logged in", result.data)



if __name__ == "__main__":
    import unittest

    unittest.main()