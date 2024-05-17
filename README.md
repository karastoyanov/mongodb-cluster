
### Part 1 ACID Transactions in mongo shell
* Install [Docker Engine](https://docs.docker.com/engine/install/) on your host machine 
* Deploy MongoDB replica set cluster with three nodes
	* Primary Node: `mongo1`
	* Secondary Node: `mongo2`
	* Secondary Node: `mongo3`
##### 1. Deploy Docker cluster with MongoDB replica set or use `docker-compose` file
```bash
docker network create mongoCluster

docker run -d -p 27017:27017 --name mongo1 --network mongoCluster mongo:5 mongod --replSet rs0 --bind_ip localhost,mongo1

docker run -d -p 27018:27017 --name mongo2 --network mongoCluster mongo:5 mongod --replSet rs0 --bind_ip localhost,mongo2

docker run -d -p 27019:27017 --name mongo3 --network mongoCluster mongo:5 mongod --replSet rs0 --bind_ip localhost,mongo3
```

##### 2. Init the replica set. One primary node `mongo1` and two secondary nodes `mongo2` & `mongo3`
```bash
docker exec -it mongo1 mongosh --eval "rs.initiate({ _id: 'rs0', members: [ {_id: 0, host: 'mongo1'}, {_id: 1, host: 'mongo2'}, {_id: 2, host: 'mongo3'} ] })" 
```

##### 3. Use `mongosh` to create a session to the MongoDB cluster at `mongo1` node. Replace `hostname` with the actual hostname. In case you are running the cluster locally, use `localhost` or `127.0.0.1`
```bash
mongosh --host hostname --port 27017
```

##### 4. Create new users(Before create new users as admin, run use `demodb` OR any other database). Replace the credentials with actual data
```javascript
db.createUser({user: "regularUser", pwd: "regularPassword", roles: [{ role: "readWrite", db: "admin" }]})
db.createUser({user: "regularUser2", pwd: "regluarPassword2", roles: [{ role: "readWrite", db: "admin" }]})
```

##### 5. Connect with the users using `mongosh`. Replace the hostname with your deployment hostname, check step 3 for details.
```bash
mongosh --host hostname --port 27017 -u regularUser -p regularPassword --authenticationDatabase admin
mongosh --host hostname --port 27017 -u regularUser2 -p regularPassword2 --authenticationDatabase admin
```

##### 6. Create sessions for both users, each on the separate `mongosh` session
```javascript
var session = db.getMongo().startSession() // for regularUser
var session2 = db.getMongo().startSession() // for regularUser2
```

##### 7. Start Transaction
```javascript
session.startTransaction({ "readConcern": { "level": "snapshot" }, "writeConcern": { "w": "majority" }}) 
session2.startTransaction({ "readConcern": { "level": "snapshot" }, "writeConcern": { "w": "majority" }}) //for regularUser2
```

##### 8. Create `cities` variables associated with `cities` collection
```javascript
var cities = session.getDatabase("demodb").getCollection("cities") // for regularUser
var cities = session2.getDatabase("demodb").getCollection("cities") // for regularUser2
```

##### 9. Insert new records in `cities` collection. Refer to `demodb/cities.json` 
```javascript
cities.insertOne({"_id": 1, "name":"New York","country":"United States","continent":"North America","population":18.819 }) // for regularUser
cities.insertOne({"_id": 2, "name":"Delhi","country":"India","continent":"Asia","population":28.514}) // for regularUser2
```


### Part 2 ACID Transactions in parallel with mongo shell

* Database name `utp-bank`
* Collections `customers`
##### 1. Login as admin, create database `utp-bank` and create users with `readWrite` access
```bash
mongosh --host hostname --port 27017
```

```javascript
use utp-bank
```

##### 2. Create collection `customers` and define schema
```javascript
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
})
```

##### 3. Create users with `readWrite` access for database `utp-bank`
```javascript
db.createUser({user: "pesho", pwd: "pesho", roles: [{ role: "readWrite", db: "utp-bank" }]});

db.createUser({user: "gosho", pwd: "gosho", roles: [{ role: "readWrite", db: "utp-bank" }]});
```

##### 4. Login with the users on `mongo1` node
```bash
mongosh --host localhost --port 27017 -u pesho -p pesho --authenticationDatabase utp-bank

mongosh --host localhost --port 27017 -u gosho -p gosho --authenticationDatabase utp-bank
```

##### 5. Start session for each of the users and commit one transaction: create new customer record
* User `pesho`
```javascript
var session = db.getMongo().startSession({readPreference:{mode:"primary"}});

session.startTransaction({
    readConcern: { level: "snapshot" }, // Use snapshot isolation level
    writeConcern: { w: "majority" },   // Use majority write concern
    maxTimeMS: 120000 // Set maximum transaction time to 120 seconds (adjust as needed)
});

var customers = session.getDatabase("utp-bank").getCollection("customers");

customers.insertOne({data}); // Replace data with actual record
```
* User `gosho`
```javascript
var session = db.getMongo().startSession({readPreference:{mode:"primary"}});

session.startTransaction({
    readConcern: { level: "snapshot" }, // Use snapshot isolation level
    writeConcern: { w: "majority" },   // Use majority write concern
    maxTimeMS: 120000 // Set maximum transaction time to 120 seconds (adjust as needed)
});

var customers = session.getDatabase("utp-bank").getCollection("customers");

customers.insertOne({data}); // Replace data with actual record
```
### Part 3 ACID Transactions with `pymongo` driver

* Create Python virtual environment 
```bash
python3 -m venv venv
```
* Start the Python venv 
```bash
source venv/bin/activate # Linux/macOS

.\venv\Scripts\activate.bat # Windows with PowerShell
```
* Install Python dependencies
```bash
pip3 install -m requirements.txt
```

##### 1. Create `.env` file on your local machine. 
**!!!! Keep the contents of that file hidden and do not share it with anyone if you are running your MongoDB cluster on a publicly available host**

```txt
USERNAME=your_username

PASSWORD=your_password

HOSTNAME=mongodb_cluster_hostanme // localhost or public IP address

PRIMARY_PORT="27017" // Primary node (mongo1) port

SECONDARY_PORT="27018" // Secondary node (mongo2) port

SECONDARY_PORT_2="27019" // Secondary node (mongo3) port

REPLICA_SET=your_replica_set_name // Your replica set name

AUTH_SOURCE=admin

DATABASE=your_database_bame // Database name
```

##### 2. Run `connect.py` in order to check the connection. 
**Example of the expected output with the MongoDB cluster from Part 1**
```
['admin', 'config', 'demodb', 'local']
```