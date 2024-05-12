#!./venv/bin/python3

from bson.objectid import ObjectId
from connect import mongo1_client, db

def add_customer(customer_data):
    """Add a new customer to the database.
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
    """Delete a customer from the database.
    Args:
        customer_id (str): Customer's _id to be deleted from the database.
    """
    # Start a transaction
    session = primary_client.start_session()
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
    "first_name": "Pesho",
    "last_name": "Peshov",
    "gender": "Male",
    "date_of_birth": "1985-10-15",
    "email": "pesho.peshov@example.com",
    "phone": "+1234567890",
    "address": {
        "street": "Shipka",
        "number": "6",
        "city": "Sofia",
        "state": "Sofia",
        "postal_code": "1000",
        "country": "Bulgaria"
    },
    "occupation": "Engineer",
    "employer": "ABC Inc.",
    "marital_status": "Married",
    "accounts": [
        {
            "account_number": "123456789",
            "type": "Savings",
            "balance": 5000.0
        },
        {
            "account_number": "987654321",
            "type": "Checking",
            "balance": 2500.0
        }
    ]
}

# Execute that line to add the customer
# add_customer(new_customer)


customer_id = "5f9b3b3b7b3b3b3b3b3b3b3b" # Not a real ID, for demonstration purposes only
# Execute that line to delete the customer
# delete_customer(customer_id)
