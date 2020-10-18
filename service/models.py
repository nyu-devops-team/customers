"""
Models for Customers service

All of the models are stored in this module

Models
------
Customer - A Customer is a resource that represents a customer account of an eCommerce website

Attributes:
----------
first name (string) - the first name of the customer
last name (string) - the last name of the customer
email (string) - email of the the customer
address (string) - shipping address of the customer
active (boolean) - whether the customer account is active or disabled

"""
import logging
from flask_sqlalchemy import SQLAlchemy

logger = logging.getLogger("flask.app")

# Create the SQLAlchemy object to be initialized later in init_db()
db = SQLAlchemy()


class DataValidationError(Exception):
    """ Used for an data validation errors when deserializing """

    pass


class Customer(db.Model):
    """
    Class that represents a Customer

    This version uses a relational database for persistence which is hidden
    from us by SQLAlchemy's object relational mappings (ORM)
    """

    logger = logging.getLogger(__name__)
    app = None

    ##################################################
    # Table Schema
    ##################################################
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(63))
    last_name = db.Column(db.String(63))
    email = db.Column(db.String(127))
    address = db.Column(db.String(255))
    active = db.Column(db.Boolean())

    ##################################################
    # INSTANCE METHODS
    ##################################################

    def __repr__(self):
        return "<Customer> %r %r id = [%s]>" % (
            self.first_name,
            self.last_name,
            self.id,
        )

    def serialize(self):
        """ Serializes a Customer into a dictionary """
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "address": self.address,
            "active": self.active,
        }

    def deserialize(self, data):
        """
        Deserializes a Customer from a dictionary

        Args:
            data (dict): A dictionary containing the resource data
        """
        try:
            self.first_name = data["first_name"]
            self.last_name = data["last_name"]
            self.email = data["email"]
            self.address = data["address"]
            self.active = data["active"]
        except KeyError as error:
            raise DataValidationError("Invalid customer: missing " + error.args[0])
        except TypeError as error:
            raise DataValidationError(
                "Invalid customer: body of request contained" "bad or no data"
            )
        return self


    def create(self):
        """
        Creates a Customer to the data store
        """
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Customer to the data store
        """
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def suspend(self):
        """
        Suspends a Customer to the data store
        """
        if not self.id:
            raise DataValidationError("Suspend called with empty ID field")
        db.session.commit()

    ##################################################
    # CLASS METHODS
    ##################################################

    @classmethod
    def init_db(cls, app):
        """Initializes the database session

        :param app: the Flast app
        :type data: Flask

        """
        logger.info("Initializing database")
        cls.app = app
        # This is where we initialize SQLAlchemy from the Flask app
        db.init_app(app)
        app.app_context().push()
        db.create_all()  # make our sqlalchemy tables

    @classmethod
    def all(cls):
        """ Returns all of the Pets in the database """
        cls.logger.info("Processing all Pets")
        return cls.query.all()

    @classmethod
    def find(cls, customer_id: int):
        """Finds a Customer by it's ID
        :param customer_id: the id of the Customer to find
        :type customer_id: int
        :return: an instance with the customer_id, or None if not found
        :rtype: Customer
        """
        cls.logger.info("Processing lookup for id %s ...", customer_id)
        return cls.query.get(customer_id)
