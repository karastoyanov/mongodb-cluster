### Cluster exercises

#### 1. Login as admin, create database utp-bank and create users with readWrite access
   
```bash
mongosh --host <hostname> --port 27017
use utp-bank
```


##### 1.1 Create users with `readWrite` access for database `utp-bank`

```js
db.createUser({user: "<user>", pwd: "<pass>", roles: [{ role: "readWrite", db: "utp-bank" }]})
```

##### 1.2 Login as regular user

```bash
mongosh --host <hostname> --port 27017 -u <username> -p <password> --authenticationDatabase utp-bank
```

#### 2. Create collection `customers` with validators //already created
   
```js
db.createCollection("customers", {
  validator: {
  "$jsonSchema": {
    "bsonType": "object",
    "required": ["first_name", "last_name", "gender", "date_of_birth", "email", "phone", "address", "occupation", "employer", "marital_status", "accounts"],
    "properties": {
      "first_name": { "bsonType": "string" },
      "last_name": { "bsonType": "string" },
      "gender": { "enum": ["Male", "Female", "Other"] },
      "date_of_birth": { "bsonType": "string"},
      "email": { "bsonType": "string"},
      "phone": { "bsonType": "string" },
      "address": {
        "bsonType": "object",
        "required": ["street", "number", "city", "state", "postal_code", "country"],
        "properties": {
          "street": { "bsonType": "string" },
          "number": { "bsonType": "string" },
          "city": { "bsonType": "string" },
          "state": { "bsonType": "string" },
          "postal_code": { "bsonType": "string" },
          "country": { "bsonType": "string" }
        }
      },
      "occupation": { "bsonType": "string" },
      "employer": { "bsonType": "string" },
      "marital_status": { "enum": ["Single", "Married", "Divorced", "Widowed"] },
      "accounts": {
        "bsonType": "array",
        "items": {
          "bsonType": "object",
          "required": ["account_number", "type", "balance"],
          "properties": {
            "account_number": { "bsonType": "string" },
            "type": { "enum": ["Savings", "Checking"] },
            "balance": { "bsonType": "double" }
          }
        }
      }
    }
  }
}
});
```

#### 3. Execute transactions in parallel

##### 3.1 Transaction 1

```js
var session = db.getMongo().startSession( { readPreference: { mode: "primary" } } );
session.startTransaction({
    readConcern: { level: "snapshot" }, // Use snapshot isolation level
    writeConcern: { w: "majority" },   // Use majority write concern
    maxTimeMS: 120000 // Set maximum transaction time to 120 seconds (adjust as needed)
});
var customers = session.getDatabase("utp-bank").getCollection("customers");
customers.insertOne({"first_name":"Pesho","last_name":"Peshev","gender":"Male","date_of_birth":"1985-10-15","email":"pesho.peshev@example.com",
                      "phone":"+1234567890","address":{"street":"Shipka","number":"6","city":"Sofia","state":"Sofia","postal_code":"1000","country":"Bulgaria"},"occupation":"Engineer",
                      "employer":"ABC Inc.","marital_status":"Married","accounts":[{"account_number":"123-456-789","type":"Savings","balance":5000.20},{"account_number":"987-654-321",
                      "type":"Checking","balance":2500.40}]});
```

##### 3.2 Transaction 2

```js
var session = db.getMongo().startSession( { readPreference: { mode: "primary" } } );
session.startTransaction({
    readConcern: { level: "snapshot" }, // Use snapshot isolation level
    writeConcern: { w: "majority" },   // Use majority write concern
    maxTimeMS: 120000 // Set maximum transaction time to 120 seconds (adjust as needed)
});
var customers = session.getDatabase("utp-bank").getCollection("customers");
customers.insertOne({"first_name":"Ivan","last_name":"Ivanov","gender":"Male","date_of_birth":"1988-09-03","email":"ivan.ivanov@example.com",
                    "phone":"+7354093771","address":{"street":"3ti Mart","number":"17","city":"Sofia","state":"Sofia","postal_code":"1000","country":"Bulgaria"},"occupation":"Doctor",
                    "employer":"XYZ Hospital","marital_status":"Married","accounts":[{"account_number":"309-531-029","type":"Savings","balance":3200.20},{"account_number":"092-310-713",
                    "type":"Checking","balance":1500.90}]});

session.commitTransaction();
```


#### 4. Create collection transactions with validators //already created

```js
db.createCollection("transactions", {
  validator: {
    "$jsonSchema": {
      "bsonType": "object",
      "required": ["transaction_date", "amount", "sender", "recipient"],
      "properties": {
        "transaction_date": { "bsonType": "date" },
        "amount": { "bsonType": "double" },
        "sender": {
          "bsonType": "object",
          "required": ["first_name", "last_name", "email", "account_number", "account_type"],
          "properties": {
            "first_name": { "bsonType": "string" },
            "last_name": { "bsonType": "string" },
            "email": { "bsonType": "string" },
            "account_number": { "bsonType": "string"},
            "account_type": { "enum": ["Savings", "Checking"]}
          }
        },
        "recipient": {
          "bsonType": "object",
          "required": ["first_name", "last_name", "email"],
          "properties": {
            "first_name": { "bsonType": "string" },
            "last_name": { "bsonType": "string" },
            "email": { "bsonType": "string" },
            "account_number": {"bsonType": "string"},
            "account_type": {"enum": ["Savings", "Checking"]}
          }
        }
      }
    }
  }
})
```

#### 5. Create a new record in collection `transactions`
   
```js
var transactions = session.getDatabase("utp-bank").getCollection("transactions");
```

```js
session.startTransaction();
```
```js
transactions.insertOne({
    "transaction_date": ISODate("2020-05-18T14:10:30Z"), // Sets the transaction date in ISO Date format
    "amount": 500.10, // Specifies the transaction amount
    "sender": { // Specifies the details of the sender
        "first_name": "Pesho",
        "last_name": "Peshev",
        "email": "pesho.peshev@example.com",
        "account_number": "123-456-789",
        "account_type": "Savings"
    },
    "recipient": { // Specifies the details of the recipient
        "first_name": "Ivan",
        "last_name": "Ivanov",
        "email": "ivan.ivanov@example.com",
        "account_number": "092-310-713",
        "account_type": "Checking"
    }
});
```

```js
db.customers.updateOne(
    { "accounts.account_number": "123-456-789" }, // Filter condition
    { $inc: { "accounts.$.balance": -500.10 } } // Decrease balance by the amount
);
```

```js
db.customers.updateOne(
    { "accounts.account_number": "092-310-713" }, // Filter condition
    { $inc: { "accounts.$.balance": 500.10 } } // Increase balance by 100
);
```

```js
session.commitTransaction();
```


#### 6. Create collection `services_providers` with validators // already created
   
```js
db.createCollection("services_providers", {
    validator: {
        $jsonSchema: {
            bsonType: "object",
            required: ["provider_name", "contact_info", "services", "account_number", "type", "balance"],
            properties: {
                provider_name: {
                    bsonType: "string",
                    description: "must be a string and is required"
                },
                contact_info: {
                    bsonType: "object",
                    required: ["email", "phone", "address"],
                    properties: {
                        email: {
                            bsonType: "string",
                            pattern: "^.+@.+$",
                            description: "must be a valid email address and is required"
                        },
                        phone: {
                            bsonType: "string",
                            description: "must be a string and is required"
                        },
                        address: {
                            bsonType: "object",
                            required: ["street", "city", "state", "postal_code", "country"],
                            properties: {
                                street: {
                                    bsonType: "string",
                                    description: "must be a string and is required"
                                },
                                city: {
                                    bsonType: "string",
                                    description: "must be a string and is required"
                                },
                                state: {
                                    bsonType: "string",
                                    description: "must be a string and is required"
                                },
                                postal_code: {
                                    bsonType: "string",
                                    description: "must be a string and is required"
                                },
                                country: {
                                    bsonType: "string",
                                    description: "must be a string and is required"
                                }
                            }
                        }
                    }
                },
                services: {
                    bsonType: "array",
                    minItems: 1,
                    items: {
                        bsonType: "object",
                        required: ["service_name", "service_type", "description"],
                        properties: {
                            service_name: {
                                bsonType: "string",
                                description: "must be a string and is required"
                            },
                            service_type: {
                                bsonType: "string",
                                description: "must be a string and is required"
                            },
                            description: {
                                bsonType: "string",
                                description: "must be a string and is required"
                            }
                        }
                    }
                },
                account_number: {
                    bsonType: "string",
                    pattern: "^[0-9]{3}-[0-9]{3}-[0-9]{3}$",
                    description: "must be a string in the format XXX-XXX-XXX and is required"
                },
                type: {
                    bsonType: "string",
                    enum: ["Bills"],
                    description: "must be 'Bills' and is required"
                },
                balance: {
                    bsonType: "double",
                    minimum: 0,
                    description: "must be a positive double and is required"
                }
            }
        }
    }
});
```

##### 6.1 Create a new record in `services_providers` collection

```js
var services_providers = session.getDatabase("utp-bank").getCollection("services_providers");
```

```js
session.startTransaction();

db.services_providers.insertOne({
    "provider_name": "Electric-Sofia",
    "contact_info": {
        "email": "contact@electric-sofia.com",
        "phone": "+8312797154",
        "address": {
            "street": "Ivan Vazov",
            "city": "Sofia",
            "state": "Sofia",
            "postal_code": "1000",
            "country": "Bulgaria"
        }
    },
    "services": [
        {
            "service_name": "Electricity",
            "service_type": "Utility",
            "description": "Electric power supply"
        }
    ],
    "account_number": "294-203-510",
    "type": "Bills",
    "balance": 1200.03
});
```

```js
session.commitTransaction();
```

#### 7. Create new record in `transactions` collection reflecting the payment of a services
