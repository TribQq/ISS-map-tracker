

def userEntity(item) -> dict:
    # получение юзера
   return {
       'id': str(item['_id']),
       'name': item['name'],
       'email': item['email'],
       'password': item['password'],
   }


def usersEntity(entity) -> list:
    # получение списка юзеров и передача их по одномк в userEntity для генерации по одному
    return [userEntity(item) for item in entity]