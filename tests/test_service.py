"""
<your resource name> API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
import unittest
from unittest.mock import MagicMock, patch
from flask_api import status  # HTTP Status Codes
from .customer_factory import CustomerFactory

from service.models import db, Customer
from service.service import app, init_db

# Disable all but ciritcal erros suirng unittest
logging.disable(logging.CRITICAL)

# DATABASE_URI = os.getenv("DATABASE_URI", "sqlite:///../db/test.db")
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

######################################################################
#  T E S T   C A S E S
######################################################################
class TestCustomers(unittest.TestCase):
    """ REST API Server Tests """

    @classmethod
    def setUpClass(cls):
        """ This runs once before the entire test suite """
        app.debug = False
        app.testing = True

        # setup the test database
        app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        pass

    def setUp(self):
        """ This runs before each test """
        init_db()
        db.drop_all()  # clean the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()
        db.drop_all()

    def _create_customers(self, count):
        """ Create customers in bulk """
        customers = []
        for i in range(count):
            temp = Customer(
                id=i,
                first_name="bye",
                last_name="world",
                email="helloworld2@gmail.com",
                address="456 7th street, New York, NY, 10001",
                active=True
            )
            db.session.add(temp)
            customers.append(temp)
        return customers

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get("/")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["name"], "Customer REST API Service")

    def test_get_customer_list(self):
        """Get a list of Customers"""
        self._create_customers(3)
        resp = self.app.get("/customers")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data),3)
        
    def test_get_customer(self):
        """ Get a single Customer """
        # get the id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get(
            "/customers/{}".format(test_customer.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["last_name"], test_customer.last_name)

    def test_get_customer_not_found(self):
        """ Get a Customer thats not found """
        resp = self.app.get("/customers/0")
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)


    def _create_customers(self, count):
        """ Factory method to create customers in bulk """
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            resp = self.app.post(
                "/customers", json=test_customer.serialize(), content_type="application/json"
            )
            self.assertEqual(
                resp.status_code, status.HTTP_201_CREATED, "Could not create test customer"
            )
            new_customer = resp.get_json()
            test_customer.id = new_customer["id"]
            customers.append(test_customer)
        return customers

    def test_create_customer(self):
        """ Create a new Customer """
        test_customer = CustomerFactory()
        resp = self.app.post(
            "/customers", json=test_customer.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue(location != None)
        # Check the data is correct
        new_customer = resp.get_json()
        # self.assertEqual(new_customer["name"], test_customer.name, "Names do not match")
        self.assertEqual(
            new_customer["first_name"], test_customer.first_name, "first_name does not match"
        )
        self.assertEqual(
            new_customer["last_name"], test_customer.last_name, "last_name does not match"
        )
        self.assertEqual(
            new_customer["email"], test_customer.email, "email does not match"
        )
        self.assertEqual(
            new_customer["address"], test_customer.address, "address does not match"
        )
        self.assertEqual(
            new_customer["active"], test_customer.active, "active does not match"
        )
        # Check that the location header was correct
        resp = self.app.get(location, content_type="application/json")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        new_customer = resp.get_json()
        # self.assertEqual(new_customer["name"], test_customer.name, "Names do not match")
        # self.assertEqual(
        #     new_customer["category"], test_customer.category, "Categories do not match"
        # )
        # self.assertEqual(
        #     new_customer["available"], test_customer.available, "Availability does not match"
        # )
        self.assertEqual(
            new_customer["first_name"], test_customer.first_name, "first_name does not match"
        )
        self.assertEqual(
            new_customer["last_name"], test_customer.last_name, "last_name does not match"
        )
        self.assertEqual(
            new_customer["email"], test_customer.email, "email does not match"
        )
        self.assertEqual(
            new_customer["address"], test_customer.address, "address does not match"
        )
        self.assertEqual(
            new_customer["active"], test_customer.active, "active does not match"
        )


    def test_update_customer(self):
        """ Update an existing Customer """
        # create a customer to update
        test_customer = CustomerFactory()
        resp = self.app.post(
            "/customers", json=test_customer.serialize(), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        new_customer["address"] = "2014 Forest Hills Drive"
        resp = self.app.put(
            "/customers/{}".format(new_customer["id"]),
            json=new_customer,
            content_type="application/json",
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer["address"], "2014 Forest Hills Drive")

    def test_delete_a_customer(self):
        """ Delete a Customer """
        test_customer = self._create_customers(1)[0]
        resp = self.app.delete(
            "/customers/{}".format(test_customer.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data),0)

        resp = self.app.get(
            "/customers/{}".format(test_customer.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
