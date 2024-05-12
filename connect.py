#!./venv/bin/python

from pymongo import MongoClient
from dotenv import load_dotenv
import os

# Load variables from .env file
load_dotenv()

# Access variables
username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")
hostname = os.getenv("HOSTNAME")
primary_port = int(os.getenv("PRIMARY_PORT")) # Ports must be integers
secondary_port = int(os.getenv("SECONDARY_PORT")) # Ports must be integers
secondary_port_2 = int(os.getenv("SECONDARY_PORT_2")) # Ports must be integers
replica_set = os.getenv("REPLICA_SET")
auth_source = os.getenv("AUTH_SOURCE")
database = os.getenv("DATABASE")


# Connect to the primary node mongo1
mongo1_client = MongoClient(
    host=f'mongodb://{username}:{password}@{hostname}:{primary_port}/?'
         f'authSource={database}&replicaSet={replica_set}&directConnection=true')

# Connect to the secondary node mongo2
mongo2_client = MongoClient(    
    host=f'mongodb://{username}:{password}@{hostname}:{secondary_port}/?'
         f'authSource={database}&replicaSet={replica_set}&directConnection=true')

# Connect to the secondary node mongo3
mongo3_client = MongoClient(    
    host=f'mongodb://{username}:{password}@{hostname}:{secondary_port_2}/?'
         f'authSource={database}&replicaSet={replica_set}&directConnection=true')

db = mongo1_client[database]
db2 = mongo2_client[database]
db3 = mongo3_client[database]
print(mongo1_client.list_database_names())
