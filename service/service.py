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

from flask import Flask, jsonify, request, url_for, make_response, abort
from flask_api import status  # HTTP Status Codes
from werkzeug.exceptions import NotFound, PreconditionFailed

# For this example we'll use SQLAlchemy, a popular ORM that supports a
# variety of backends including SQLite, MySQL, and PostgreSQL
from flask_sqlalchemy import SQLAlchemy
from service.models import Customer, DataValidationError

# Import Flask application
from . import app

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
    # app.logger.info("Request for Root URL")
    # return (
    #     jsonify(
    #         name="Customer REST API Service",
    #         version="1.0",
    #         paths=url_for(
    #             "list_customers", _external=True
    #         ),  # url_for() generates the url for a function
    #     ),
    #     status.HTTP_200_OK,
    # )
    return app.send_static_file('index.html')


# ######################################################################
# # LIST ALL CUSTOMERS
# ######################################################################
@app.route("/customers", methods=["GET"])
def list_customers():
    """ Returns all of the Customers """
    app.logger.info("Request to list all customers")
    customers = []
    
    first_name = request.args.get('first_name')
    last_name = request.args.get('last_name')
    address = request.args.get('address')
    email = request.args.get('email')
    active = request.args.get('active')
    
    if first_name:
        customers = Customer.find_by_first_name(first_name)
    elif last_name:
        customers = Customer.find_by_last_name(last_name)
    elif address:
        customers = Customer.find_by_address(address)
    elif email:
        customers = Customer.find_by_email(email)
    elif active:
        customers = Customer.find_by_active(active)
    else:
        try:
            customers = Customer.all()
        except:
            abort(500)

    results = [customer.serialize() for customer in customers]
    app.logger.info("Returning %d customerss", len(results))
    return make_response(jsonify(results), status.HTTP_200_OK)
    
######################################################################
# RETRIEVE A CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["GET"])
def get_customers(customer_id):
    """
    Retrieve a single Customer
    This endpoint will return a Customer based on it's id
    """
    app.logger.info("Request for customer with id: %s", customer_id)
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with the id was not found.")

    app.logger.info(
        "Returning customer: %s", customer.first_name + " " + customer.last_name
    )
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# ADD A NEW CUSTOMERS
######################################################################
@app.route("/customers", methods=["POST"])
def create_customers():
    """
    Creates a Customer
    This endpoint will create a Customer based the data in the body that is posted
    """
    app.logger.info("Request to create a customer")
    check_content_type("application/json")
    customer = Customer()
    customer.deserialize(request.get_json())
    customer.create()
    message = customer.serialize()
    location_url = url_for("get_customers", customer_id=customer.id, _external=True)

    app.logger.info("Customer with ID [%s] created.", customer.id)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )


######################################################################
# UPDATE AN EXISTING CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["PUT"])
def update_customers(customer_id):
    """
    Update a Customer
    This endpoint will update a Customer based the body that is posted
    """
    app.logger.info("Request to update customer with id: %s", customer_id)
    check_content_type("application/json")
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    customer.deserialize(request.get_json())
    customer.id = customer_id
    customer.update()

    app.logger.info("Customer with ID [%s] updated.", customer.id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# SUSPEND AN EXISTING CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>/suspend", methods=["PUT"])
def suspend_customers(customer_id):
    """
    Suspend a Customer
    This endpoint will Suspend a Customer
    """
    app.logger.info("Request to suspend customer with id: %s", customer_id)
    check_content_type("application/json")
    customer = Customer.find(customer_id)
    if not customer:
        raise NotFound("Customer with id '{}' was not found.".format(customer_id))
    customer.active = False
    customer.update()

    app.logger.info("Customer with ID [%s] suspended.", customer.id)
    return make_response(jsonify(customer.serialize()), status.HTTP_200_OK)


######################################################################
# DELETE AN EXISTING CUSTOMER
######################################################################
@app.route("/customers/<int:customer_id>", methods=["DELETE"])
def delete_customers(customer_id):
    """
    Delete a Customer
    This endpoint will delete a customer based on the ID specified in the path
    """
    app.logger.info("Request to delete a customer with ID: %s", customer_id)
    customer = Customer.find(customer_id)
    if customer:
        customer.delete()

    app.logger.info("Customer with ID [%s] has been deleted.", customer_id)
    return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
# DELETE ALL CUSTOMER DATA (for testing only)
######################################################################
@app.route('/customers/reset', methods=['DELETE'])
def customers_reset():
    """ Removes all pets from the database """
    Customer.remove_all()
    return make_response('', status.HTTP_204_NO_CONTENT)


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
