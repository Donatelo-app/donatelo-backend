import os
from base64 import encodebytes, decodebytes

from utils import validate_cover

from pymongo import MongoClient

mongo_client = MongoClient(os.get_enviroment("MONGO_URL", "mongodb://localhost:27017"))
mongo = mongo_client[os.get_enviroment("MONGO_URL", "/donatelo").split("/")[-1]]


def get_cover(group_id):
	pass

def get_enviroment(group_id):
	enviroment = mongo.enviroment.find_one({"group_id":group_id})
	return enviroment

def get_varible(group_id, varible_name):
	enviroment = mongo.enviroment.find_one({"group_id":group_id})
	return enviroment.get(varible_name)

def get_access_token(group_id):
	group = mongo.groups.find_one({"group_id":group_id})	
	if not group: return None

	return group["access_token"]


def create_group(group_id, access_token):
	group = mongo.groups.find_one({"group_id":group_id})
	if group: return False

	mongo.group.insert({"group_id":group_id, "access_token": access_token})
	return True

def set_cover(group_id, cover, resources):
	message, code = validate_cover(cover)
	if not code:
		return message, code

	for key, image in resources.items():
		resources[key] = encodebytes(image)

	

	return "ok", True

def set_varible(group_id, varible_name, value):
	enviroment = mongo.enviroment.find_one({"group_id":group_id})
	if not enviroment.get(varible_name): reutrn False
	if not type(enviroment.get(varible_name)) is type(value): reutrn False

	enviroment[varible_name] = value
	mongo.enviroment.update_one({"group_id":group_id}, {"$set":enviroment})

	return True