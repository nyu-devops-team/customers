"""
Test cases for Customer Model


Test cases can be run with:
    nosetests
    coverage report -m 
"""
import logging
import unittest
import os
from service.models import Customer, DataValidationError, db
from service import app

DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///../db/test.db")

######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestYourResourceModel(unittest.TestCase):
    """ Test Cases for <your resource name> Model """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.debug = False
        # Set up the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        Customer.init_db(app)
        db.drop_all()  # clean up the last tests
        db.create_all()  # make our sqlalchemy tables

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()


######################################################################
#  P L A C E   T E S T   C A S E S   H E R E 
######################################################################

    def test_create_a_customer(self):
        """ Create a customer and assert that it exists """
        customer = Customer(first_name="John", last_name="Smith", email="jsmith@gmail.com", 
                            address="123 Brooklyn Ave", active=True)
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.first_name, "John")
        self.assertEqual(customer.last_name, "Smith")
        self.assertEqual(customer.email = "jsmith@gmail.com")
        self.assertEqual(customer.address = "123 Brooklyn Ave")
        self.assertEqual(customer.active, True)

    def test_add_a_customer(self):
        """
        Create a customer and add to the database
        """

        # TODO
        pass

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
