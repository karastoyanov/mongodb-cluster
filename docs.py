#!./venv/bin/python3
from new_customer import add_customer, delete_customer

print("*" * 50 + "\n")

# Get the documentation data for the functions
print(add_customer.__doc__)
print("*" * 50)

print(delete_customer.__doc__)
print("*" * 50)