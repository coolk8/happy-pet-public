from dataclasses import dataclass
from typing import Optional

@dataclass
class User:
    _id: int
    user_id: int
    username: Optional[str] = None
    user_first_name: Optional[str] = None
    user_lastname: Optional[str] = None
    user_lang: Optional[str] = None
    user_sd_images: Optional[list] = None
    user_pet_type: Optional[str] = None
    user_pet_image: Optional[list] = None
    user_pet_name: Optional[str] = None
    user_pet_character: Optional[str] = None
    #TODO добавить всякие таймстампы (рега, последняя активность и тп)

async def get_users(users_collection):
    users = await users_collection.find({})
    return [User(**u) for u in users]


async def get_user(users_collection, _id: int):
    user = await users_collection.find_one({'_id': _id})
    return User(**user) if user else None


async def create_user(users_collection, _id: int, **kwargs):
    user = await users_collection.insert_one({'_id': _id, **kwargs})
    return await get_user(users_collection, user.inserted_id)


async def update_user(users_collection, _id: int, **kwargs):
    user = await users_collection.find_one_and_update({'_id': _id}, 
                                                      {'$set': kwargs}, 
                                                      return_document=True)
    return User(**user)


async def get_or_create_user(users_collection, _id: int, **kwargs):
    user = await get_user(users_collection, _id)
    if user: 
        kwargs['user_lang'] = user.user_lang
    user = await update_user(users_collection, _id, **kwargs) if user else await create_user(users_collection, _id, **kwargs)
    return user