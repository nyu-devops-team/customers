"""
Global Configuration for Application
"""
import os
import json

# Get configuration from environment
print("-----Initial DATABASE_URL-----")
# DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///../db/test.db')
DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgres://postgres:postgres@localhost:5432/postgres"
)

# Secret for session management
# SECRET_KEY = os.getenv("SECRET_KEY", "s3cr3t-key-shhhh")

# override if we are running in Cloud Foundry
if 'VCAP_SERVICES' in os.environ:
    print("-----DATABASE_URL change to cloud version-----")
    vcap = json.loads(os.environ['VCAP_SERVICES'])
    DATABASE_URI = vcap['user-provided'][0]['credentials']['url'] 

# Configure SQLAlchemy
SQLALCHEMY_DATABASE_URI = DATABASE_URI
SQLALCHEMY_TRACK_MODIFICATIONS = False 
