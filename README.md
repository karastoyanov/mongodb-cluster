
### Part 1
* Install [Docker Engine](https://docs.docker.com/engine/install/) on your host machine 
* Deploy MongoDB replica set cluster with three nodes
	* Primary Node: `mongo1`
	* Secondary Node: `mongo2`
	* Secondary Node: `mongo3`
##### 1. Deploy Docker cluster with MongoDB replica set or use `docker-compose` file
```bash
docker network create mongoCluster

docker run -d -p 27017:27017 --name mongo1 --network mongoCluster mongo:5 mongod --replSet rs0 --bind_ip localhost,mongo1`

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

