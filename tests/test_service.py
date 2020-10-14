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


######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
