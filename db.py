from pymongo import MongoClient
import settings

client = MongoClient(settings.MONGO_LINK)

db = client[settings.MONGO_DB]

def get_or_create_user(db, effective_user, chat_id):
    user = db.users.find_one({"user_id": effective_user.id})
    if not user:
        user = {
            "user_id": effective_user.id,
            "username": effective_user.username,
            "chat_id": chat_id
        }
        db.users.insert_one(user)
    return user

def subscribe_user(db, user_data):
    if not user_data.get('subscribed'):
        db.users.update_one(
            {'_id': user_data['_id']},
            {'$set': {'subscribed': True}}
        )

def unsubscribe_user(db, user_data):
    db.users.update_one(
        {'_id': user_data['_id']},
        {'$set': {'subscribed': False}}
    )

def get_subscription(db):
    return db.users.find({'subscribed': True})