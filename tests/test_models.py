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

# DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///../db/test.db")
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  C U S T O M E R   M O D E L   T E S T   C A S E S
######################################################################
class TestCustomerModel(unittest.TestCase):
    """ Test Cases for Customer Model """

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
        customer = Customer(
            first_name="John",
            last_name="Smith",
            email="jsmith@gmail.com",
            address="123 Brooklyn Ave",
            active=True,
        )
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.first_name, "John")
        self.assertEqual(customer.last_name, "Smith")
        self.assertEqual(customer.email, "jsmith@gmail.com")
        self.assertEqual(customer.address, "123 Brooklyn Ave")
        self.assertEqual(customer.active, True)

    def test_serialize_a_customer(self):
        """ Test serialization of a a Customer """
        customer = Customer(
            first_name="John",
            last_name="Smith",
            email="jsmith@gmail.com",
            address="123 Brooklyn Ave",
            active=True,
        )
        data= customer.serialize()

        self.assertNotEqual(data, None)
        self.assertIn("id", data)
        self.assertEqual(data["id"], None)
        self.assertIn("first_name", data)
        self.assertEqual(data["first_name"], "John")
        self.assertIn("last_name", data)
        self.assertEqual(data["last_name"], "Smith")
        self.assertIn("email", data)
        self.assertEqual(data["email"], "jsmith@gmail.com")
        self.assertIn("address", data)
        self.assertEqual(data["address"], "123 Brooklyn Ave")
        self.assertIn("active", data)
        self.assertEqual(data["active"], True)

    def test_deserialize_a_customer(self):
        """ Test deserialization of a Customer """
        data = {"id": 1, 
                "first_name": "John", 
                "last_name": "Smith",
                "email": "jsmith@gmail.com",
                "address": "123 Brooklyn Ave",
                "active": True}
        
        customer = Customer()
        customer.deserialize(data)

        self.assertNotEqual(customer, None)
        self.assertEqual(customer.id, None)
        self.assertEqual(customer.first_name, "John")
        self.assertEqual(customer.last_name, "Smith")
        self.assertEqual(customer.email, "jsmith@gmail.com")
        self.assertEqual(customer.address, "123 Brooklyn Ave")
        self.assertEqual(customer.active, True)

    def test_deserialize_bad_data(self):
        """ Test deserialization of bad data """
        data = "this is not a dictionary"
        customer = Customer()
        self.assertRaises(DataValidationError, customer.deserialize, data)


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
