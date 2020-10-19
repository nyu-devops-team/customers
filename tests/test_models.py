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

    def test_add_a_customer(self):
        """Create a customer and add it to the database"""
        customers = Customer.all()
        self.assertEqual(customers,[])
        customer = Customer(
            first_name="John",
            last_name="Doe",
            email="jdoe@gmail.com",
            address="456 Bronx Ave",
            active=True)
        self.assertTrue(customer != None)
        self.assertEqual(customer.id, None)
        customer.create()
        # Assert that it was assigned an id and shows up in the database
        self.assertEqual(customer.id,1)
        customers = Customer.all()
        self.assertEqual(len(customers),1)
        
    def test_update_a_customer(self):
        """ Update a Customer """
        customer = Customer(
            first_name="John", 
            last_name="Smith",
            email="jsmith@gmail.com",
            address="123 Brooklyn Ave",
            active=True,
            )
        customer.create()
        self.assertEqual(customer.id, 1)
        # Change it an update it
        customer.address = "Times Sq 42nd St"
        customer.update()
        self.assertEqual(customer.id, 1)
        # Fetch it back and make sure the id hasn't changed
        # but the data did change
        customers = Customer.all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0].address, "Times Sq 42nd St")

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

    def test_find_customer(self):
        """ Find a Customer by ID """
        customer = Customer(
            id=1,
            first_name="bye",
            last_name="yoyoyo",
            email="yoyoyobye@gmail.com",
            address="456 7th street, New York, NY, 10001",
            active=True
        )
        db.session.add(customer)
        result = Customer.find(customer.id)
        self.assertIsNot(result, None)
        self.assertEqual(result.id, customer.id)
        self.assertEqual(result.first_name, "bye")
        self.assertEqual(result.last_name, "yoyoyo")
        self.assertEqual(result.email, "yoyoyobye@gmail.com")
        self.assertEqual(result.address, "456 7th street, New York, NY, 10001")
        self.assertEqual(result.active, True)


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
