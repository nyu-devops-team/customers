"""
<your resource name> API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import mock
import logging
import unittest
import json
from flask_api import status  # HTTP Status Codes

from service.models import db, Customer
from service.service import app, init_db

from .customer_factory import CustomerFactory


# Disable all but ciritcal erros suirng unittest
logging.disable(logging.CRITICAL)

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    for item in vcap['user-provided']:
        if item['name'] == "ElephantSQL-Test":
            DATABASE_URI = item['credentials']['url']

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
        init_db()

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        db.drop_all()  # clean the last tests
        db.create_all()  # create new tables
        self.app = app.test_client()
        self.headers = {'X-Api-Key': app.config['API_KEY']}

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
                active=True,
            )
            db.session.add(temp)
            customers.append(temp)
        return customers

    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ Test index call """
        resp = self.app.get('/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertIn(b'Customer Demo REST API Service', resp.data)

    def test_get_customer_list(self):
        """Get a list of Customers"""
        self._create_customers(3)
        resp = self.app.get("/customers")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(len(data), 3)

    def test_get_customer(self):
        """ Get a single Customer """
        # get the id of a customer
        test_customer = self._create_customers(1)[0]
        resp = self.app.get(
            "/customers/{}".format(test_customer.id),
            content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertEqual(data["last_name"], test_customer.last_name)

    # def test_get_customer_not_found(self):
    #     """ Get a Customer thats not found """
    #     resp = self.app.get("/customers/0")
    #     self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def _create_customers(self, count):
        """ Factory method to create customers in bulk """
        customers = []
        for _ in range(count):
            test_customer = CustomerFactory()
            resp = self.app.post(
                "/customers",
                json=test_customer.serialize(),
                content_type="application/json",
                headers = self.headers
            )
            self.assertEqual(
                resp.status_code,
                status.HTTP_201_CREATED,
                "Could not create test customer",
            )
            new_customer = resp.get_json()
            test_customer.id = new_customer["id"]
            customers.append(test_customer)
        return customers

    def test_create_customer(self):
        """ Create a new Customer """
        test_customer = CustomerFactory()
        resp = self.app.post(
            "/customers",
            json=test_customer.serialize(),
            content_type="application/json",
            headers = self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # Make sure location header is set
        location = resp.headers.get("Location", None)
        self.assertTrue(location is not None)
        # Check the data is correct
        new_customer = resp.get_json()
        # self.assertEqual(new_customer["name"], test_customer.name, "Names do not match")
        self.assertEqual(
            new_customer["first_name"],
            test_customer.first_name,
            "first_name does not match",
        )
        self.assertEqual(
            new_customer["last_name"],
            test_customer.last_name,
            "last_name does not match",
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
            new_customer["first_name"],
            test_customer.first_name,
            "first_name does not match",
        )
        self.assertEqual(
            new_customer["last_name"],
            test_customer.last_name,
            "last_name does not match",
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
            "/customers",
            json=test_customer.serialize(),
            content_type="application/json",
            headers = self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

        # update the customer
        new_customer = resp.get_json()
        new_customer["address"] = "2014 Forest Hills Drive"
        resp = self.app.put(
            "/customers/{}".format(new_customer["id"]),
            json=new_customer,
            content_type="application/json",
            headers = self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        updated_customer = resp.get_json()
        self.assertEqual(updated_customer["address"], "2014 Forest Hills Drive")

    def test_delete_a_customer(self):
        """ Delete a Customer """
        test_customer = self._create_customers(1)[0]
        resp = self.app.delete(
            "/customers/{}".format(test_customer.id), 
            content_type="application/json",
            headers = self.headers
        )
        self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(len(resp.data), 0)

        resp = self.app.get(
            "/customers/{}".format(test_customer.id), content_type="application/json"
        )
        self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    # def test_customers_reset(self):
    #     """ Delete all customers """
    #     self._create_customers(3)
    #     delete_resp = self.app.delete("/customers/reset", content_type="application/json")
    #     self.assertEqual(delete_resp.status_code, status.HTTP_204_NO_CONTENT)
        
    #     resp = self.app.get("/customers")
    #     data = resp.get_json()
    #     self.assertEqual(len(data), 0)

    # def test_suspend_customer(self):
    #     """ Suspend an existing Customer """
    #     # create a customer to suspend
    #     test_customer = CustomerFactory()
    #     test_customer.active = 1
    #     resp = self.app.post(
    #         "/customers",
    #         json=test_customer.serialize(),
    #         content_type="application/json",
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    #     # suspend the customer
    #     new_customer = resp.get_json()
    #     resp = self.app.put(
    #         "/customers/{}/suspend".format(new_customer["id"]),
    #         content_type="application/json",
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_200_OK)

    #     # attempt to resuspend the customer
    #     suspended_customer = resp.get_json()
    #     self.assertEqual(suspended_customer["active"], False)
    #     resp2 = self.app.put(
    #         "/customers/{}/suspend".format(suspended_customer["id"]),
    #         content_type="application/json",
    #     )
    #     self.assertEqual(resp2.status_code, status.HTTP_200_OK)

    # def test_suspend_not_available(self):
    #     """ Suspend a customer that is not available """
    #     resp = self.app.put(
    #         "/customers/{}/suspend".format(0),
    #         content_type="application/json",
    #     )
    #     self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)

    def test_query_customer_list_by_first_name(self):
        """ Query Customers by first name """
        customers = self._create_customers(10)
        test_first_name = customers[0].first_name
        resp = self.app.get(
            "/customers", query_string="first_name={}".format(test_first_name)
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        first_name_customers = [
            customer for customer in data if customer["first_name"] == test_first_name
        ]
        # check the data just to be sure
        for customer in first_name_customers:
            self.assertEqual(customer["first_name"], test_first_name)

    def test_query_customer_list_by_last_name(self):
        """ Query Customers by last name """
        customers = self._create_customers(10)
        test_last_name = customers[0].last_name
        resp = self.app.get(
            "/customers", query_string="last_name={}".format(test_last_name)
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        last_name_customers = [
            customer for customer in data if customer["last_name"] == test_last_name
        ]
        # check the data just to be sure
        for customer in last_name_customers:
            self.assertEqual(customer["last_name"], test_last_name)

    def test_query_customer_list_by_address(self):
        """ Query Customers by address """
        customers = self._create_customers(10)
        test_address = customers[0].address
        resp = self.app.get(
            "/customers", query_string="address={}".format(test_address)
        )
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        address_customers = [
            customer for customer in data if customer["address"] == test_address
        ]
        # check the data just to be sure
        for customer in address_customers:
            self.assertEqual(customer["address"], test_address)

    def test_query_customer_list_by_email(self):
        """ Query Customers by email """
        customers = self._create_customers(10)
        test_email = customers[0].email
        resp = self.app.get("/customers", query_string="email={}".format(test_email))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        email_customers = [
            customer for customer in data if customer["email"] == test_email
        ]
        # check the data just to be sure
        for customer in email_customers:
            self.assertEqual(customer["email"], test_email)

    def test_query_customer_list_by_active(self):
        """ Query Customers by active """
        customers = self._create_customers(10)
        test_active = customers[0].active
        resp = self.app.get("/customers", query_string="active={}".format(test_active))
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        active_customers = [
            customer for customer in data if customer["active"] == test_active
        ]
        # check the data just to be sure
        for customer in active_customers:
            self.assertEqual(customer["active"], test_active)

    def test_method_not_supported(self):
        resp = self.app.put('/customers')
        self.assertEqual(resp.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    # @mock.patch('service.service.Customer.all')
    # def test_search_bad_data(self, customer_find_mock):
    #     customer_find_mock.side_effect = Exception()
    #     resp = self.app.get('/customers', query_string='id=20')

    #     self.assertEqual(resp.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

######################################################################
#   M A I N
######################################################################
if __name__ == "__main__":
    unittest.main()
