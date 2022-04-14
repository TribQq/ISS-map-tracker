
import json
from urllib import request
from fastapi import APIRouter, Response, status
from config.db import conn
from schemas.users import userEntity, usersEntity
from models.users import User
from passlib.hash import sha256_crypt # crypt/uncrypt pass
from bson.objectid import ObjectId
from starlette.status import HTTP_204_NO_CONTENT


user = APIRouter()


@user.get('/users', response_model=list[User], tags=['users'])
def find_all_users():
    return usersEntity(conn.local.user.find())

# response model, tags -otional, for /docs
@user.post('/user', response_model=User, tags=['user']) 
def create_user(user: User):
    print(type(user))
    new_user = dict(user) # model => to dict
    new_user['password'] = sha256_crypt.encrypt(new_user['password']) # add salt to pass
    del new_user["id"]
    id = conn.local.user.insert_one(new_user).inserted_id
    user = conn.local.user.find_one({'_id': id})
    return userEntity(user)


@user.get('/user/{id}', tags=['user'])
def find_user(id: str):
    return userEntity(conn.local.user.find_one({'_id': ObjectId(id)}))



@user.put('/user/{id}', response_model=User, tags=['user'])
def update_user(id: str, user:User):
    dict_user = dict(user)
    dict_user['password'] = sha256_crypt.encrypt(dict_user['password'])
    conn.local.user.find_one_and_update({'_id': ObjectId(id)},
                                         {'$set': dict_user})
    return Response(f'User "{dict_user["name"]}" updated')
    # alt return info vars
    # dict_user['_id'] = ObjectId(id) 
    # return userEntity(dict_user)
    # return userEntity(conn.local.user.find_one({'_id': ObjectId(id)}))
    


@user.delete('/user/{id}', status_code=status.HTTP_204_NO_CONTENT, tags=['user'])
def delete_user(id: str):
    userEntity(conn.local.user.find_one_and_delete({'_id': ObjectId(id)}))
    return Response(status_code=HTTP_204_NO_CONTENT)
    # alt return info vars
    # return Response('User id:' + id + '. Deleted Successfully') 

