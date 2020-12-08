"""
Customer Service

PATHS:
------
GET /customers - returns a list of all the Customers
GET /customers/{id} - returns the Customer with a given id number
POST /customers - creates a new Customer record in the database
PUT /customers/{id} - updates a Customer record in the database
DELETE /customers/{id} - deletes a Customer record in the databse

PUT /customers/{id}/suspend - suspend the Customer with the given id number

"""
import sys
import uuid
from functools import wraps
from flask import Flask, jsonify, request, url_for, make_response, abort, render_template
from flask_api import status  # HTTP Status Codes
from flask_restx import Api, Resource, fields, reqparse, inputs
from werkzeug.exceptions import NotFound, PreconditionFailed

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Customer, DataValidationError

# Import Flask application
from . import app

# Document the type of autorization required
authorizations = {
    'apikey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-Api-Key'
    }
}

######################################################################
# Error Handlers
######################################################################
@app.errorhandler(DataValidationError)
def request_validation_error(error):  # pragma: no cover
    """ Handles Value Errors from bad data """
    return bad_request(error)


@app.errorhandler(status.HTTP_400_BAD_REQUEST)
def bad_request(error):  # pragma: no cover
    """ Handles bad reuests with 400_BAD_REQUEST """
    app.logger.warning(str(error))
    return (
        jsonify(
            status=status.HTTP_400_BAD_REQUEST, error="Bad Request", message=str(error)
        ),
        status.HTTP_400_BAD_REQUEST,
    )


@app.errorhandler(status.HTTP_404_NOT_FOUND)
def not_found(error):
    """ Handles resources not found with 404_NOT_FOUND """
    app.logger.warning(str(error))
    return (
        jsonify(
            status=status.HTTP_404_NOT_FOUND, error="Not Found", message=str(error)
        ),
        status.HTTP_404_NOT_FOUND,
    )


@app.errorhandler(status.HTTP_405_METHOD_NOT_ALLOWED)
def method_not_supported(error):  # pragma: no cover
    """ Handles unsuppoted HTTP methods with 405_METHOD_NOT_SUPPORTED """
    app.logger.warning(str(error))
    return (
        jsonify(
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
            error="Method not Allowed",
            message=str(error),
        ),
        status.HTTP_405_METHOD_NOT_ALLOWED,
    )


@app.errorhandler(status.HTTP_415_UNSUPPORTED_MEDIA_TYPE)
def mediatype_not_supported(error):  # pragma: no cover
    """ Handles unsuppoted media requests with 415_UNSUPPORTED_MEDIA_TYPE """
    app.logger.warning(str(error))
    return (
        jsonify(
            status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            error="Unsupported media type",
            message=str(error),
        ),
        status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
    )


@app.errorhandler(status.HTTP_500_INTERNAL_SERVER_ERROR)
def internal_server_error(error):  # pragma: no cover
    """ Handles unexpected server error with 500_SERVER_ERROR """
    app.logger.error(str(error))
    return (
        jsonify(
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="Internal Server Error",
            message=str(error),
        ),
        status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return app.send_static_file('index.html')

######################################################################
# Configure Swagger before initializing it
######################################################################
api = Api(app,
          version='1.0.0',
          title='Customer Demo REST API Service',
          description='This is a sample server Customer server.',
          default='customers',
          default_label='Customer operations',
          doc='/apidocs', # default also could use doc='/apidocs/'
<<<<<<< HEAD
<<<<<<< HEAD
          authorizations=authorizations
=======
         #   authorizations=authorizations
>>>>>>> master-restplus
          )
=======
          authorizations=authorizations
        )
>>>>>>> c5282739ba496aa00bf2046e840ed06ab8b5eca0

# Define the model so that the docs reflect what can be sent
create_model = api.model('Customer', {
    'first_name': fields.String(required=True,
                          description='The first name of the Customer'),
    'last_name': fields.String(required=True,
                              description='The last name of the Customer'),
    'email': fields.String(required=True,
                              description='The email of the Customer'),
    'address': fields.String(required=True,
                              description='The address of the Customer'),
    'active': fields.Boolean(required=True,
                                description='Is the Customer avaialble for purchase?')
})

customer_model = api.inherit(
    'CustomerModel', 
    create_model,
    {
        'id': fields.String(readOnly=True,
                            description='The unique id assigned internally by service'),
    }
)

# query string arguments
customer_args = reqparse.RequestParser()
customer_args.add_argument('last_name', type=str, required=False, help='List Customers by last name')
customer_args.add_argument('first_name', type=str, required=False, help='List Customers by first name')
customer_args.add_argument('email', type=str, required=False, help='List Customers email')
customer_args.add_argument('address', type=str, required=False, help='List Customers by address')
customer_args.add_argument('active', type=inputs.boolean, required=False, help='List Customers by availability')

######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
    """ Helper function used when testing API keys """
    return uuid.uuid4().hex

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################
def init_db():
    """ Initialies the SQLAlchemy app """
    global app
    Customer.init_db(app)


def check_content_type(content_type):  # pragma: no cover
    """ Checks that the media type is correct """
    if request.headers["Content-Type"] == content_type:
        return
    app.logger.error("Invalid Content-Type: %s", request.headers["Content-Type"])
    abort(415, "Content-Type must be {}".format(content_type))

@api.route('/customers/<customer_id>')
@api.param('customer_id', 'The Customer identifier')
class CustomerResource(Resource):
    """
    CustomerResource class
    Allows the manipulation of a single Customer
    GET /customer{id} - Returns a Customer with the id
    PUT /customer{id} - Update a Customer with the id
    DELETE /customer{id} -  Deletes a Customer with the id
    """

    #------------------------------------------------------------------
    # RETRIEVE A CUSTOMER
    #------------------------------------------------------------------
    @api.doc('get_customers')
    @api.response(404, 'Customer not found')
    @api.marshal_with(customer_model)
    def get(self, customer_id):
        """
        Retrieve a single Customer
        This endpoint will return a Customer based on it's id
        """
        app.logger.info("Request to Retrieve a customer with id [%s]", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            api.abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        return customer.serialize(), status.HTTP_200_OK

    #------------------------------------------------------------------
    # UPDATE AN EXISTING PET
    #------------------------------------------------------------------
    @api.doc('update_customers', security='apikey')
    @api.response(404, 'Customer not found')
    @api.response(400, 'The posted Customer data was not valid')
    @api.expect(customer_model)
    @api.marshal_with(customer_model)
    def put(self, customer_id):
        """
        Update a Customer
        This endpoint will update a Customer based the body that is posted
        """
        app.logger.info('Request to Update a customer with id [%s]', customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            api.abort(status.HTTP_404_NOT_FOUND, "Customer with id '{}' was not found.".format(customer_id))
        app.logger.debug('Payload = %s', api.payload)
        data = api.payload
        customer.deserialize(data)
        customer.id = customer_id
        customer.save()
        return customer.serialize(), status.HTTP_200_OK

######################################################################
#  PATH: /customers
######################################################################
@api.route('/customers', strict_slashes=False)
class CustomerCollection(Resource):
    """ Handles all interactions with collections of Customers """
    #------------------------------------------------------------------
    # ADD A NEW CUSTOMER
    #------------------------------------------------------------------
    @api.doc('create_customers', security='apikey')
    @api.expect(create_model)
    @api.response(400, 'The posted data was not valid')
    @api.response(201, 'Customer created successfully')
    @api.marshal_with(customer_model, code=201)
    def post(self):
        """
        Creates a Customer
        This endpoint will create a Customer based the data in the body that is posted
        """
        app.logger.info('Request to Create a Customer')
        customer = Customer()
        app.logger.debug('Payload = %s', api.payload)
        customer.deserialize(api.payload)
        customer.create()
        app.logger.info('Customer with new id [%s] saved!', customer.id)
        location_url = api.url_for(CustomerResource, customer_id=customer.id, _external=True)
        return customer.serialize(), status.HTTP_201_CREATED, {'Location': location_url}

######################################################################
#  PATH: /customers/{customer_id}/suspend
######################################################################
@api.route('/customers/<customer_id>/suspend')
@api.param('customer_id', 'Customer Identifier')
class SuspendResource(Resource):
    """ Suspend Action on a Customer"""
    @api.doc('suspend_customers')
    @api.response(404, 'Customer not found')
    @api.response(200, 'Success - action completed')
    def put(self, customer_id):
        """
        Suspend a Customer
        This endpoint will suspend a customer based on its ID
        """
        app.logger.info("Request to suspend customer with id: %s", customer_id)
        customer = Customer.find(customer_id)
        if not customer:
            raise NotFound("Cus...tomer with id '{}' was not found.".format(customer_id))
        customer.active = False
        customer.update()
        app.logger.info("Customer with ID [%s] suspended.", customer.id)
<<<<<<< HEAD
        return customer.serialize(), status.HTTP_200_OK 
=======
<<<<<<< HEAD
        return customer.serialize(), status.HTTP_200_OK 
=======
        return customer.serialize(), status.HTTP_200_OK
>>>>>>> 154b1b1b0de444d446e60786d3ec6d571c592bd3
>>>>>>> c5282739ba496aa00bf2046e840ed06ab8b5eca0
