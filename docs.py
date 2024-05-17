#!./venv/bin/python3
from manage_customers import add_customer, delete_customer
from create_new_transaction import create_transaction

print("*" * 50 + "\n")

# Get the documentation data for the functions
print(add_customer.__doc__)
print("*" * 50)

print(delete_customer.__doc__)
print("*" * 50)

print(create_transaction.__doc__)
print("*" * 50)