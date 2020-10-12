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

    def create(self):
        """
        Creates a Customer to the database
        """
        logger.info("Creating %s %s", self.first_name, self.last_name)
        db.session.add(self)
        db.session.commit()

    def update(self):
        """
        Updates a Customer to the database
        """
        logger.info("Saving %s %s", self.first_name, self.last_name)
        if not self.id:
            raise DataValidationError("Update called with empty ID field")
        db.session.commit()

    def delete(self):
        """ Removes a Customer from the data store """
        logger.info("Deleting %s %s", self.first_name, self.last_name)
        db.session.delete(self)
        db.session.commit()

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
        """ Returns all of the Customers in the database """
        logger.info("Processing all Customers")
        return cls.query.all()

    @classmethod
    def find(cls, customer_id):
        """Finds a Customer by it's ID

        :param customer_id: the id of the Customer to find
        :type customer_id: int

        :return: an instance with the customer_id, or None if not found
        :type: Pet
        """
        logger.info("Processing lookup for id %s ...", customer_id)
        return cls.query.get(customer_id)

    @classmethod
    def find_or_404(cls, customer_id):
        """Find a Customer by it's id

        :param customer_id: the id of the Customer to find
        :type customer_id: int

        :return: an instance with the customer_id, or 404_NOT_FOUND if not found
        :rtype: Pet

        """
        logger.info("Processing lookup or 404 for id %s ...", customer_id)
        return cls.query.get_or_404(customer_id)

    @classmethod
    def find_by_first_name(cls, first_name):
        """Returns all Customers with the given first name

        :param first_name: the first name of the Customers you want to match
        :type first_name: str

        :return: a collction of Customers with the given first name
        :rtype: list
        """
        logger.info("Processing first name query for %s ...", first_name)
        return cls.query.filter(cls.first_name == first_name)

    @classmethod
    def find_by_last_name(cls, last_name):
        """Returns all Customers with the given last name

        :param last_name: the last name of the Customers you want to match
        :type last_name: str

        :return: a collction of Customers with the given last name
        :rtype: list
        """
        logger.info("Processing last name query for %s ...", last_name)
        return cls.query.filter(cls.last_name == last_name)

    @classmethod
    def find_by_active(cls, active):
        """Return all Customers that are active

        :param active: True for customers that are active (not suspended)
        :type active: boolean

        :return: a collction of Customers that are active
        :rtype: list
        """

        # TODO
        pass
