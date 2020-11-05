"""
Global Configuration for Application
"""
import os
import json

# Get configuration from environment

# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

# Secret for session management
# SECRET_KEY = os.getenv("SECRET_KEY", "s3cr3t-key-shhhh")

# override if we are running in Cloud Foundry
if 'VCAP_SERVICES' in os.environ:
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    for item in vcap['user-provided']:
        if item['name'] == "ElephantSQL":
            DATABASE_URI = item['credentials']['url']

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False
