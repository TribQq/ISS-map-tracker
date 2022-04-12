## Flask & MongoDB RESTAPI

This application is a REST API CRUD using Python Flask and mongodb module Flask-Pymongo

### Full installation with mongo
Install local mongo , from  official <a href="https://www.mongodb.com/docs/manual/administration/install-community/"> site </a>, ubuntu <a href="https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/#considerations ">example</a>

##### If you want, you can install a GUI MongoDB-Compass
```
virtualenv flask_mongo_env -p python3.10
source  flask_mongo_env/bin/activate
pip install -r requirements.txt
python src/app.py
```
##### now you can visit: http://localhost:3000


### Installation with docker-compose 

if before that you installed "MongoDB":

#### (linux command), u can check how stop mongo serv in <a href="https://www.mongodb.com/docs/manual/">doc</a>, or change port in docker

```
sudo systemctl stop mongod
```


```
docker-compose up
```

##### now u can visit: http://localhost:3000


### Test

For example , u can test all operations with <a href="https://www.postman.com/downloads/"> Postman </a>
##### Headers
###### Content-Type : application/json
##### Body
```
{
    "username": "username0",
    "password": "password0",
    "email": "email0@gmail.com"
}
```
###### POST http://localhost:3000/users => create user
###### GET: http://localhost:3000/users => users array
###### GET : http://localhost:3000/users/ + _id => one user by id
###### DELETE : http://localhost:3000/users/ + _id => del one user by id
