#!./venv/bin/python3

from bson.objectid import ObjectId
from connect import mongo1_client, db
from datetime import datetime


def create_transaction(transaction_data, sender, recipient):
    """create_transaction --> Create a new transaction between two customers.
    Args:
        transaction_data (json): Transaction data to be added to the database / collection `transactions`.
        sender (str): Sender's account number.
        recipient (str): Recipient's account number.
    """

    # Start a transaction
    session = mongo1_client.start_session()
    try:
        with session.start_transaction():
            # Insert transaction data
            transactions_collection = db['transactions']
            result = transactions_collection.insert_one(transaction_data, session=session)
            # Get the inserted transaction's _id
            transaction_id = result.inserted_id
            
            # Update sender's account balance
            accounts_collection = db['customers']
            sender_account = accounts_collection.find_one({"account_number": sender})
            sender_balance = sender_account['balance']
            sender_balance -= transaction_data['amount']
            accounts_collection.update_one({"account_number": sender}, {"$set": {"balance": sender_balance}}, session=session)
            
            # Update recipient's account balance
            recipient_account = accounts_collection.find_one({"account_number": recipient})
            recipient_balance = recipient_account['balance']
            recipient_balance += transaction_data['amount']
            accounts_collection.update_one({"account_number": recipient}, {"$set": {"balance": recipient_balance}}, session=session)
            
            # Commit the transaction
            session.commit_transaction()
            print(f"Transaction added with ID: {transaction_id}")
    except Exception as e:
        print(f"Transaction aborted: {e}")
        session.abort_transaction()


# Example transaction data. Update the data as needed.
sender_account = "987-654-321" # Update the sender's account number
recipient_account = "347-658-347" # Update the recipient's account number
amount = 1000.00 # Update the amount
data = {
    "_id": str(ObjectId()),
    "transaction_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "amount": amount,
    "sender": {
        "first_name": "",
        "last_name": "",
        "email": "",
        "account_number": sender_account,
    },
    "recipient": {
        "first_name": "",
        "last_name": "",
        "email": "",
        "account_number": recipient_account,
    },
}


# create_transaction(data, sender_account, recipient_account)