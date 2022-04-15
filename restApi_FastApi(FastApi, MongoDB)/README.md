## FastApi & MongoDB RESTAPI

This application is a REST API CRUD using Python FastApi and MongoDB

### Full installation with mongo
Install local mongo , from  official <a href="https://www.mongodb.com/docs/manual/administration/install-community/"> site </a>. Ubuntu <a href="https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-ubuntu/#considerations ">example</a>

###### If you want, you can install a GUI MongoDB-Compass
```
virtualenv fatapi_mongo_env -p python3.10
source  fatapi_mongo_env/bin/activate
pip install -r requirements.txt
uvicorn app:app
```
##### now u can visit: http://localhost:8000

### Test
For example , u can test all operations with FastApi docs
http://localhost:8000/docs
