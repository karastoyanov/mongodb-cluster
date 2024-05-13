#!./venv/bin/python3

from bson.objectid import ObjectId
from connect import mongo1_client, db

def add_customer(customer_data):
    """add_customer --> Add a new customer to the database.
    Args:
        customer_data (json): Customer's data to be added to the database.
    """
    # Start a transaction
    session = mongo1_client.start_session()
    try:
        with session.start_transaction():
            # Insert customer data
            customers_collection = db['customers']
            result = customers_collection.insert_one(customer_data, session=session)

            # Get the inserted customer's _id
            customer_id = result.inserted_id

            # Commit the transaction
            session.commit_transaction()
            print(f"Customer added with ID: {customer_id}")
    except Exception as e:
        print(f"Transaction aborted: {e}")
        session.abort_transaction()


def delete_customer(customer_id):
    """delete_customer --> Delete a customer from the database.
    Args:
        customer_id (str): Customer's _id to be deleted from the database.
    """
    # Start a transaction
    session = mongo1_client.start_session()
    try:
        with session.start_transaction():
            # Delete the customer
            customers_collection = db['customers']
            result = customers_collection.delete_one({"_id": ObjectId(customer_id)}, session=session)

            # Commit the transaction
            session.commit_transaction()
            print(f"Customer deleted: {result.deleted_count}")
    except Exception as e:
        print(f"Transaction aborted: {e}")
        session.abort_transaction()


# Example customer data
new_customer = {
    "_id": str(ObjectId()),
    "first_name": "",
    "last_name": "",
    "gender": "",
    "date_of_birth": "",
    "email": "",
    "phone": "",
    "address": {
        "street": "",
        "number": "",
        "city": "",
        "state": "",
        "postal_code": "",
        "country": ""
    },
    "occupation": "",
    "employer": "",
    "marital_status": "",
    "accounts": [
        {
            "account_number": "",
            "type": "",
            "balance": 0000
        },
        {
            "account_number": "",
            "type": "",
            "balance": 0000
        }
    ]
}

# Execute that line to add the customer
# add_customer(new_customer)


customer_id = "5f9b3b3b7b3b3b3b3b3b3b3b" # Not a real ID, for demonstration purposes only
# Execute that line to delete the customer
# delete_customer(customer_id)